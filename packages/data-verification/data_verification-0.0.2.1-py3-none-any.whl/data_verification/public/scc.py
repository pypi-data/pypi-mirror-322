class SCC:
    @staticmethod
    def verify_uscc(code: str, weights: list = None, check_code_map: str = None) -> bool:
        """
        统一社会信用代码校验
        :param code: 统一社会信用代码
        :param weights: 权重数组
        :param check_code_map: 校验码映射表
        :return:
        """
        if weights is None:
            weights = [31, 29, 23, 19, 17, 13, 11, 7, 5, 3, 31, 29, 23, 19, 17, 13, 11]
        if check_code_map is None:
            check_code_map = "0ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if len(code) != 18:
            return False
        # 计算加权和
        weighted_sum = sum(
            (ord(c) - 55 if 'A' <= c <= 'Z' else int(c)) * weight for c, weight in zip(code[:-1], weights))
        # 计算模数并获取校验码
        mod_result = weighted_sum % 31
        expected_check_code = check_code_map[mod_result]
        # 比较实际校验码
        return expected_check_code == code[-1]

    @staticmethod
    def verify_cscc(code: str, weights: list = None, check_code_map: str = None) -> bool:
        """
        企业社会信用代码校验
        :param code: 企业社会信用代码
        :param weights: 权重数组
        :param check_code_map: 校验码映射表
        :return:
        """
        return SCC.verify_uscc(code, weights, check_code_map)


class SCCAsync(SCC):
    @staticmethod
    async def verify_uscc(code: str, weights: list = None, check_code_map: str = None) -> bool:
        return SCC.verify_uscc(code, weights, check_code_map)

    @staticmethod
    async def verify_cscc(code: str, weights: list = None, check_code_map: str = None) -> bool:
        return SCC.verify_uscc(code, weights, check_code_map)
