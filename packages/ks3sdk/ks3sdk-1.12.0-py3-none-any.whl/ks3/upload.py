import logging
import os
import math
from concurrent import futures

from ks3.exception import KS3ClientError
from ks3.multipart import MultiPartUpload, PartInfo
from ks3.utils import ChunkIO, ResumeRecordManager

KB = 1024
MB = KB * KB
GB = KB * MB

MAX_PARTS = 10_000
MAX_SIZE = 5 * GB
MIN_SIZE = 100 * KB

logger = logging.getLogger(__name__)


class UploadTask:
    def __init__(
            self, key, bucket, filename,
            executor,
            part_size=100 * KB,
            resumable=False,
            resumable_filename=None,
    ):
        """
        key: 需要上传的Key对象（ks3.key.Key）
        bucket: 需要上传到的Bucket对象（ks3.bucket.Bucket）
        filename: 待上传的本地文件路径
        executor: 线程池
        part_size: 分块大小，默认100KB。小于分块大小的文件，使用简单上传；大于分块大小的文件，使用分块上传
        resumable: 是否开启断点续传，默认False。开启断点续传时，如果本地存在有效的断点续传记录，则尝试恢复上传，否则初始化分块上传
        resumable_filename: 断点续传记录文件路径。如果不指定，则使用默认路径（self.filename + '.ks3resume'）
        """
        self.key = key
        self.bucket = bucket
        self.filename = filename
        self.executor = executor
        self.part_size = part_size
        self.resumable = resumable
        if self.resumable:
            if resumable_filename is None:
                resumable_filename = self.filename + '.ks3resume'
            self.record_manager = ResumeRecordManager(resumable_filename)
        else:
            self.record_manager = None
        # 本地文件的修改时间
        self.__mtime = os.path.getmtime(filename)
        # 本地文件的大小
        self.__file_size = os.path.getsize(filename)

    def upload(self, headers=None):
        if self.__file_size <= self.part_size:
            logger.debug('key_name={0}, file_size({1}) less than part_size({2}), use simple upload'
                         .format(self.key.name, self.__file_size, self.part_size))
            self.key.set_contents_from_filename(self.filename, headers=headers)
        else:
            logger.debug('key_name={0}, file_size({1}) greater than part_size({2}), use multipart upload'
                         .format(self.key.name, self.__file_size, self.part_size))
            self.multipart_upload(headers)

    def multipart_upload(self, headers=None):
        # 初始化分块上传
        mp = self._get_or_init_record_as_mp(headers)

        if not self.resumable:
            part_uploaded = set()
        elif self.bucket.connection.enable_crc:
            # 开启了crc校验，已上传分块以本地记录为准，防止本地与远端记录分块数据不一致。
            part_uploaded = set(self.record_manager.record.part_crc_infos.keys())
        else:
            # 未开启crc校验，已上传分块以远端记录为准（通过断点续传文件内记录的upload_id等信息获取远端分块记录）。
            part_uploaded = set()
            # for循环将调用 List Parts 接口
            for p in mp:
                part_uploaded.add(p.part_number)

        part_size = self._adjust_part_size()
        num_parts = int(math.ceil(self.__file_size / float(part_size)))
        remain_size = self.__file_size
        # 分块上传
        # part_futures<future, part_num>
        part_futures = {}
        for part_num in range(1, num_parts + 1):
            # 跳过已上传的part
            if part_num in part_uploaded:
                logger.debug('key_name={0}, part {1} already uploaded, skip'.format(self.key.name, part_num))
                remain_size -= part_size
                continue
            part_futures[self.executor.submit(
                self._upload_part,
                mp=mp,
                part_num=part_num,
                part_size=min(part_size, remain_size),
                headers=headers,
            )] = part_num
            remain_size -= part_size
        # 不能及时处理中断信号
        self.executor.shutdown(wait=True)
        for future in futures.as_completed(part_futures):
            try:
                future.result()
            except Exception as e:
                logger.error('key_name={0}, part {1} upload failed: {2}'.format(self.key.name, part_futures[future], e))
                raise e
        try:
            resp = mp.complete_upload()
        except KS3ClientError as e:
            # crc校验失败，删除本地断点续传记录，以便于下次重新上传
            if 'Inconsistent CRC checksum' in e.reason:
                if self.resumable:
                    self.record_manager.delete()
            raise e
        # 正常上传完成，未抛出异常，则删除本地断点续传记录
        if self.resumable:
            self.record_manager.delete()
        return resp

    def _get_or_init_record_as_mp(self, headers):
        """
        获取或初始化分块上传:
        1. 如果没有开启断点续传，则初始化分块上传
        2. 如果开启断点续传，则尝试加载本地记录，如果记录存在且有效，则恢复分块上传，否则初始化分块上传
        return: 返回分块上传对象MultiPartUpload类型
        """
        if not self.resumable:
            mp = self.bucket.initiate_multipart_upload(self.key.name, headers=headers)
            return mp

        self.record_manager.load()

        if self.record_manager.record is not None and not self._check_record_valid():
            logger.debug('key_name={0}, found invalid record, delete it'.format(self.key.name))
            self.record_manager.delete()
        if self.record_manager.record is None:
            logger.debug('key_name={0}, not found record, initiate multipart upload'.format(self.key.name))
            mp = self.bucket.initiate_multipart_upload(self.key.name, headers=headers)
            self.record_manager.record = UploadRecord(mp.id, self.__file_size, self.__mtime,
                                                      self.bucket.name, self.key.name, self.part_size, {})
            self.record_manager.save()
        else:
            logger.debug('key_name={0}, found record, resume multipart upload: {1}'
                         .format(self.key.name, self.record_manager.record.upload_id))
            mp = MultiPartUpload(self.bucket)
            mp.id = self.record_manager.record.upload_id
            mp.key_name = self.record_manager.record.key_name
            mp.part_crc_infos = self.record_manager.record.part_crc_infos
            self.part_size = self.record_manager.record.part_size
        return mp

    def _check_record_valid(self):
        record = self.record_manager.record
        if not isinstance(record, UploadRecord):
            return False
        for attr in [record.upload_id, record.bucket_name, record.key_name]:
            if not isinstance(attr, str):
                return False
        for attr in [record.file_size, record.part_size]:
            if not isinstance(attr, int):
                return False
        if not isinstance(record.mtime, float) and not isinstance(record.mtime, int):
            return False
        if not isinstance(record.part_crc_infos, dict):
            return False
        if record.mtime != self.__mtime or record.file_size != self.__file_size:
            return False
        return True

    def _adjust_part_size(self):
        part_size = self.part_size
        num_parts = int(math.ceil(self.__file_size / float(part_size)))
        # 以分块数的标准，调整分块大小
        while num_parts > MAX_PARTS:
            part_size *= 2
            num_parts = int(math.ceil(self.__file_size / float(part_size)))
        # 以单次上传大小的标准，调整分块大小
        if part_size > MAX_SIZE:
            part_size = MAX_SIZE
        elif part_size < MIN_SIZE:
            part_size = MIN_SIZE
        return part_size

    def _upload_part(self, mp, part_num, part_size, headers=None):
        with ChunkIO(self.filename, (part_num - 1) * self.part_size, part_size) as fp:
            resp = mp.upload_part_from_file(fp, part_num, headers=headers)
            if self.resumable and self.bucket.connection.enable_crc:
                self.record_manager.record.part_crc_infos[part_num] = PartInfo(
                    part_size, resp.getheader(self.bucket.connection.provider.checksum_crc64ecma_header))
                # 保存crc信息
                self.record_manager.save()


class UploadRecord(object):
    def __init__(self, upload_id, file_size, mtime, bucket_name, key_name, part_size, part_crc_infos):
        self.upload_id = upload_id
        self.file_size = file_size
        self.mtime = mtime
        self.bucket_name = bucket_name
        self.key_name = key_name
        self.part_size = part_size
        self.part_crc_infos = part_crc_infos
