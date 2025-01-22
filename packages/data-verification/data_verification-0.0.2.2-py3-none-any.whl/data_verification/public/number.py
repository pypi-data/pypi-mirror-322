from decimal import Decimal, InvalidOperation


class Number:
    @staticmethod
    def number_range(value: int or float, min_value: int or float, max_value: int or float, pattern: int = 0) -> bool:
        """
        验证数是否在某个区间，前后闭区间
        :param value: 被验证数
        :param min_value: 区间小值
        :param max_value: 区间大值
        :param pattern: 区间判断类型，0：前闭后闭，1：前闭后开，2：前开后闭，3：前开后开
        :return:
        """
        if pattern not in [0, 1, 2, 3]:
            return ValueError("pattern must be 0 or 1, 2 or 3")
        if pattern == 0:
            return min_value <= value <= max_value
        elif pattern == 1:
            return min_value <= value < max_value
        elif pattern == 2:
            return min_value < value <= max_value
        elif pattern == 3:
            return min_value < value < max_value

    @staticmethod
    def check_precision(value, min_value=None, max_value=None, decimal_places=2):
        """
        检查数值是否符合指定的精度要求。
        :param min_value: 允许的最小值，默认为None表示无下限。
        :param max_value: 允许的最大值，默认为None表示无上限。
        :param decimal_places: 小数点后允许的最大位数，默认为2。
        :param value: 要检查的数值字符串或数字。
        :return:
        """
        try:
            # 将输入转换为Decimal类型，以便更精确地处理浮点数
            dec_value = Decimal(str(value))
        except (InvalidOperation, TypeError):
            return False
        # 检查边界
        if min_value is not None and dec_value < min_value:
            return False
        if max_value is not None and dec_value > max_value:
            return False
        # 检查小数位数
        tuple_form = dec_value.as_tuple()
        if abs(tuple_form.exponent) > decimal_places:
            return False
        return True


class NumberAsync(Number):
    @staticmethod
    async def number_range(value: int or float, min_value: int or float, max_value: int or float,
                           pattern: int = 0) -> bool:
        return Number.number_range(value, min_value, max_value, pattern)

    @staticmethod
    async def check_precision(value, min_value=None, max_value=None, decimal_places=2):
        return Number.check_precision(value, min_value, max_value, decimal_places)
