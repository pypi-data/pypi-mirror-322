import re


class Email:
    @staticmethod
    def verify_email_format(email: str) -> bool:
        """
        验证邮箱是否符合规则
        :param email: 被验证邮箱
        :return:
        """
        # 定义匹配邮箱地址的正则表达式
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        return bool(re.match(email_regex, email))


class EmailAsync(Email):
    @staticmethod
    async def verify_email_format(email: str) -> bool:
        return Email.verify_email_format(email)
