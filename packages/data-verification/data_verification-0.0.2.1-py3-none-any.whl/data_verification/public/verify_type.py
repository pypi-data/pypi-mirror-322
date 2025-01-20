class VerifyType:
    @staticmethod
    def is_bytes(value: bytes) -> bool:
        """
        验证是否是二进制数据
        :param value: 被验证数据
        :return:
        """
        return isinstance(value, bytes)

    @staticmethod
    def is_bool(value: bool) -> bool:
        """
        验证是否是布尔值
        :param value: 被验证数据
        :return:
        """
        return isinstance(value, bool)

    @staticmethod
    def is_str(value: str) -> bool:
        """
        验证是否是字符串
        :param value: 被验证数据
        :return:
        """
        return isinstance(value, str)

    @staticmethod
    def is_float(value: float) -> bool:
        """
        验证是否是浮点数
        :param value: 被验证数据
        :return:
        """
        return isinstance(value, float)

    @staticmethod
    def is_int(value: int) -> bool:
        """
        验证是否是整数
        :param value: 被验证数据
        :return:
        """
        return isinstance(value, int)


class VerifyTypeAsync(VerifyType):
    @staticmethod
    async def is_bytes(value: bytes) -> bool:
        return VerifyType.is_bytes(value)

    @staticmethod
    async def is_bool(value: bool) -> bool:
        return VerifyType.is_bool(value)

    @staticmethod
    async def is_str(value: str) -> str:
        return VerifyType.is_str(value)

    @staticmethod
    async def is_float(value: float) -> bool:
        return VerifyType.is_float(value)

    @staticmethod
    async def is_int(value: int) -> bool:
        return VerifyType.is_int(value)
