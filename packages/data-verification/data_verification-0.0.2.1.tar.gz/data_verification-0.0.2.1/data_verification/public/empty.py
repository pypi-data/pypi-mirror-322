class Empty:
    @staticmethod
    def is_empty(value) -> bool:
        """
        检查给定值是否为空。
        :param value: 要检查的值。
        :return:
        """
        if bool(value):
            return False
        else:
            return True

    @staticmethod
    def is_not_empty(value) -> bool:
        """
        检查给定值是否非空。
        :param value: 要检查的值。
        :return:
        """
        return bool(value)

    @staticmethod
    def empty_in(lst: list) -> bool:
        """
        判断数组中是否包含None或者空字符串
        :param lst: 被验证数组
        :return:
        """
        if "" in lst or None in lst:
            return True
        return False

    @staticmethod
    def empty_not_in(lst: list) -> bool:
        """
        判断数组中是否不包含None或者空字符串
        :param lst: 被验证数组
        :return:
        """
        if "" not in lst and None not in lst:
            return True
        return False


class EmptyAsync(Empty):
    @staticmethod
    async def is_empty(value):
        return Empty.is_empty(value)

    @staticmethod
    async def is_not_empty(value):
        return Empty.is_not_empty(value)

    @staticmethod
    async def empty_in(lst: list) -> bool:
        return Empty.is_empty(lst)

    @staticmethod
    async def empty_not_in(lst: list) -> bool:
        return Empty.is_empty(lst)
