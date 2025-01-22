class Decode:
    @staticmethod
    def decode(data: str, encoding: str) -> bool:
        """
        验证字符编码格式
        :param data: 被验证的数据
        :param encoding: 编码类型
        :return:
        """
        try:
            data.decode(encoding)
            return True
        except UnicodeDecodeError as e:
            return False


class DecodeAsync(Decode):
    @staticmethod
    async def decode(data: str, encoding: str) -> bool:
        return Decode.decode(data, encoding)
