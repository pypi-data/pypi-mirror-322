import types


class Domain:
    @staticmethod
    def enum_domain_check(value: str, valid_values: list) -> bool:
        """
        检查给定值是否在预定义的有效值列表中。
        :param value: 要检查的值。
        :param valid_values: 有效值的列表。
        :return:
        """
        return value in valid_values

    @staticmethod
    def encoded_domain_check(value: str, encoding_rule) -> bool:
        """
        检查给定值是否符合指定的编码规则。
        :param value: 要检查的值。
        :param encoding_rule: 编码规则函数，返回布尔值。
        :return:
        """
        if isinstance(encoding_rule, (types.FunctionType, types.LambdaType)):
            return encoding_rule(value)
        return ValueError("encoding_rule must be callable")

    @staticmethod
    def dictionary_domain_check(value: str, dictionary: dict, condition=None) -> bool:
        """
        检查给定值是否存在于字典中，并且其对应的值满足指定条件。
        :param value: 要检查的值（通常是键）。
        :param dictionary: 键值对集合。
        :param condition: 条件函数，接收字典中的值作为参数，返回布尔值。(可选)
        :return:
        """
        if condition is None:
            return value in dictionary
        return value in dictionary and condition(dictionary[value])

    @staticmethod
    def dictionary_enum_domain_check(value, enum_dict):
        """
        检查给定值是否在字典表中，并且其对应的值属于预定义的有效值列表。
        :param value: 要检查的值（通常是键）。
        :param enum_dict: 键值对集合，其中值是一个包含有效枚举值的列表。
        :return:
        """
        # 检查值是否存在于字典中
        if value in enum_dict:
            # 获取对应的有效枚举值列表
            valid_values = enum_dict[value]
            # 如果有效枚举值列表不为空，则进一步检查值是否在其内
            if isinstance(valid_values, list) and len(valid_values) > 0:
                return True
            else:
                raise ValueError(f"Invalid enum list for key '{value}'")
        else:
            return False


class DomainAsync(Domain):
    @staticmethod
    async def enum_domain_check(value, valid_values):
        return Domain.enum_domain_check(value, valid_values)

    @staticmethod
    async def encoded_domain_check(value, encoding_rule):
        return Domain.encoded_domain_check(value, encoding_rule)

    @staticmethod
    async def dictionary_domain_check(value, dictionary, condition=None):
        return Domain.dictionary_domain_check(value, dictionary, condition)

    @staticmethod
    async def dictionary_enum_domain_check(value, dictionary, condition=None):
        return Domain.dictionary_domain_check(value, dictionary, condition)
