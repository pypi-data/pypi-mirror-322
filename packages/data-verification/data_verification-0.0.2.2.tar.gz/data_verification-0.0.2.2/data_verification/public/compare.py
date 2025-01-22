import hashlib


class Compare:
    @staticmethod
    def verify_compare(value1, value2, pattern: int = 0):
        """
        对两个数据进行比较验证
        :param value1: 数据1
        :param value2: 数据2
        :param pattern: 验证模式，0：是否小于，1：是否大于，2：是否等于，3：是否小于等于，4：是否大于等于，5：是否不等于
        :return:
        """
        if pattern not in [0, 1, 2, 3, 4, 5, 6]:
            return ValueError("pattern must in [0, 1, 2, 3, 4, 5, 6]")
        elif pattern == 0:
            return value1 < value2
        elif pattern == 1:
            return value1 > value2
        elif pattern == 2:
            return value1 == value2
        elif pattern == 3:
            return value1 <= value2
        elif pattern == 4:
            return value1 >= value2
        elif pattern == 5:
            return value1 != value2

    @staticmethod
    def verify_length(value, length: int, pattern: int = 0) -> bool:
        """
        验证数据长度
        :param value: 被验证数据
        :param length: 数据长度
        :param pattern: 验证模式，0：是否小于，1：是否大于，2：是否等于，3：是否小于等于，4：是否大于等于，5：是否不等于
        :return:
        """
        if pattern not in [0, 1, 2, 3, 4, 5, 6]:
            return ValueError("pattern must in [0, 1, 2, 3, 4, 5, 6]")
        elif pattern == 0:
            return len(value) < length
        elif pattern == 1:
            return len(value) > length
        elif pattern == 2:
            return len(value) == length
        elif pattern == 3:
            return len(value) <= length
        elif pattern == 4:
            return len(value) >= length
        elif pattern == 5:
            return len(value) != length

    @staticmethod
    def _get_hash(data, algorithm='sha256'):
        """
        根据给定的算法计算数据的哈希值。
        :param data: 要计算哈希值的数据（支持bytes或str类型）。
        :param algorithm: 使用的哈希算法名称，默认为sha256。
        :return:
        """
        # 确保输入是bytes类型
        if isinstance(data, str):
            data = data.encode('utf-8')

        try:
            hash_function = getattr(hashlib, algorithm)()
            hash_function.update(data)
            return hash_function.hexdigest()
        except AttributeError:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    @staticmethod
    def compare_hashes(data, hash_value, algorithm='sha256'):
        """
        比较数据对象与对应哈希值是否相同。
        :param data: 被验证数据对象。
        :param hash_value: 比对哈希值。
        :param algorithm: 使用的哈希算法名称，默认为sha256，支持；sha1，sha224，sha256，sha384，sha512，sha3_224，sha3_256，
            sha3_384，sha3_512，shake_128，shake_256，blake2b，blake2s，md5
        :return:
        """
        hash1 = Compare._get_hash(data, algorithm)
        return hash1 == hash_value


class CompareAsync(Compare):
    @staticmethod
    async def verify_compare(value1, value2, pattern: int = 0):
        return Compare.verify_compare(value1, value2, pattern)

    @staticmethod
    async def verify_length(value, length: int, pattern: int = 0) -> bool:
        return Compare.verify_compare(value, pattern, length)

    @staticmethod
    async def compare_hashes(data, hash_value, algorithm='sha256'):
        return Compare.compare_hashes(data, hash_value, algorithm)
