class Organization:
    @staticmethod
    def verify_organization_code(code: str, weights=None) -> bool:
        """
        验证组织机构代码
        :param code: 组织机构代码
        :param weights: 权重数组
        :return:
        """
        if weights is None:
            weights = [3, 7, 9, 10, 5, 8, 4, 2]
        if len(code) != 9 or not code[:8].isdigit() or (code[8] not in '0123456789X'):
            return False
        # 计算加权和
        weighted_sum = sum(int(c) * weight for c, weight in zip(code[:8], weights))
        # 计算模数并获取校验码
        mod_result = weighted_sum % 11
        expected_check_code = 'X' if mod_result == 10 else str(mod_result)
        # 比较实际校验码
        return expected_check_code.upper() == code[-1].upper()


class OrganizationAsync(Organization):
    @staticmethod
    async def verify_organization_code(code: str, weights=None) -> bool:
        return Organization.verify_organization_code(code, weights)
