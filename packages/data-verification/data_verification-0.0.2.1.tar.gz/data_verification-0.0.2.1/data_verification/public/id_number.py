class IDNumber:
    @staticmethod
    def verify_id_number(id_number: str, factors: list = None, check_codes: list = None) -> bool:
        """
        对身份证号进行验证
        :param id_number: 身份证号
        :param factors: 权重因子
        :param check_codes: 校验码映射表
        :return:
        """
        if type(id_number) is not str:
            raise TypeError('id_number must be a string')
        if type(factors) is not list and factors is not None:
            raise TypeError('factors must be a list')
        if type(check_codes) is not list and check_codes is not None:
            raise TypeError('check_codes must be a list')
        # 初始化权重因子
        if check_codes is None:
            check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        # 初始化校验码映射表
        if factors is None:
            factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        # 确保输入长度为18，并且只有最后一位可能是 'X'
        if len(id_number) != 18 or not (id_number[:-1].isdigit() and id_number[-1] in "0123456789Xx"):
            return False
        # 计算前17位数字的加权和
        total = sum(int(id_number[i]) * factors[i] for i in range(17))
        # 得到校验码
        calculated_check_code = check_codes[total % 11]
        # 比较计算出的校验码和实际提供的校验码
        return calculated_check_code.upper() == id_number[-1].upper()


class IDNumberAsync(IDNumber):
    @staticmethod
    async def verify_id_number(id_number: str, factors: list = None, check_codes: list = None) -> bool:
        return IDNumber.verify_id_number(id_number, factors, check_codes)
