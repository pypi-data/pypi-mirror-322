import re


class PhoneNumber:
    @staticmethod
    def verify_mobile_number(phone_number: str) -> bool:
        """
        对移动手机号进行验证
        :param phone_number: 被验证手机号
        :return:
        """
        if len(phone_number) != 11:
            return False
        # 正则表达式匹配规则
        mobile_pattern = r'^1[3-9]\d{9}$'
        # 使用正则表达式进行匹配
        if re.match(mobile_pattern, phone_number):
            return True
        else:
            return False

    @staticmethod
    def verify_fixed_line_number(phone_number: str) -> bool:
        """
        对固定电话号进行验证
        :param phone_number: 被验证电话号
        :return:
        """
        # 去除所有非数字字符（如空格、破折号、括号）
        cleaned_phone = ''.join(filter(str.isdigit, phone_number))
        # 检查总长度是否合理
        if not (7 <= len(cleaned_phone) <= 12):
            return False
        # 如果有区号，区号应该是3或4位，并且以0开头
        if len(cleaned_phone) > 7 and cleaned_phone.startswith('0'):
            area_code_length = 3 if len(cleaned_phone) == 10 else 4
            if not (len(cleaned_phone) == 10 or len(cleaned_phone) == 11):
                return False
            # 分离区号和本地号码
            area_code, local_number = cleaned_phone[:area_code_length], cleaned_phone[area_code_length:]
            # 检查本地号码长度是否合理
            if not (7 <= len(local_number) <= 8):
                return False
        else:
            # 没有区号时直接检查本地号码长度
            if not (7 <= len(cleaned_phone) <= 8):
                return False
        return True

    @staticmethod
    def verify_phone_number(phone_number: str) -> bool:
        """
        对移动手机号或固定电话号进行验证
        :param phone_number: 被验证移动手机号或固定电话号
        :return:
        """
        # 尝试作为手机号码验证
        if PhoneNumber.verify_mobile_number(phone_number):
            return True
        # 尝试作为固定电话号码验证
        elif PhoneNumber.verify_fixed_line_number(phone_number):
            return True
        else:
            return False


class PhoneNumberAsync(PhoneNumber):
    @staticmethod
    async def verify_mobile_number(phone_number: str) -> bool:
        return PhoneNumber.verify_mobile_number(phone_number)

    @staticmethod
    async def verify_fixed_line_number(phone_number: str) -> bool:
        return PhoneNumber.verify_fixed_line_number(phone_number)

    @staticmethod
    async def verify_phone_number(phone_number: str) -> bool:
        return PhoneNumber.verify_phone_number(phone_number)
