import re


class Regex:
    @staticmethod
    def regex(value: str, pattern: str) -> bool:
        """
        基于正则表达式验证值的内容
        :param value: 被验证值
        :param pattern: 正则表达式
        :return:
        """
        return bool(re.match(pattern, value))


class RegexAsync(Regex):
    @staticmethod
    async def regex(value: str, pattern: str) -> bool:
        return Regex.regex(value, pattern)
