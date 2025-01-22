class Unique:
    @staticmethod
    def is_unique(lst):
        """
        检查列表中的元素是否全部唯一。
        :param lst: 要检查的列表。
        :return:
        """
        return len(lst) == len(set(lst))


class UniqueAsync(Unique):
    @staticmethod
    async def is_unique(lst):
        return Unique.is_unique(lst)
