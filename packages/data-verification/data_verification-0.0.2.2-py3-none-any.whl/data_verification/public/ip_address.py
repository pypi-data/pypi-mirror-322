import re


class IPAddress:
    @staticmethod
    def verify_mac_address(mac_address: str) -> bool:
        """
        对Mac地址进行验证
        :param mac_address: 被验证的Mac地址
        :return:
        """
        # 定义匹配 MAC 地址的正则表达式
        mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$|^([0-9A-Fa-f]{12})$'
        return bool(re.match(mac_pattern, mac_address))

    @staticmethod
    def verify_ipv4(ip_address: str) -> bool:
        """
        对IPv4地址进行验证
        :param ip_address: 被验证的IPv4地址
        :return:
        """
        # 正则表达式匹配规则
        ipv4_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

        # 使用正则表达式进行匹配
        if re.match(ipv4_pattern, ip_address):
            return True
        else:
            return False

    @staticmethod
    def verify_ipv6(ip_address: str) -> bool:
        """
        对IPv6地址进行验证
        :param ip_address: 被验证的IPv6地址
        :return:
        """
        # 去除可能存在的双冒号表示法中的多余零段
        parts = ip_address.split(':')
        # 处理双冒号的情况
        if '::' in ip_address:
            if ip_address.count('::') > 1 or (ip_address.startswith(':::') or ip_address.endswith(':::')):
                return False
            # 计算缺失的部分数量并填充为 '0'
            missing_parts = 8 - len(parts) + 1
            parts = ip_address.replace('::', ':' + ('0:' * missing_parts), 1).split(':')
        # 确保有8个段
        if len(parts) != 8:
            return False
        # 验证每个段是否为有效的十六进制数
        for part in parts:
            if not part or len(part) > 4 or not all(c in '0123456789abcdefABCDEF' for c in part):
                return False
        return True

    @staticmethod
    def verify_ip_address(ip_address: str) -> bool:
        """
        对IPv4或IPv6地址进行验证
        :param ip_address: 被验证的IPv4或IPv6地址
        :return:
        """
        if IPAddress.verify_ipv4(ip_address):
            return True
        elif IPAddress.verify_ipv6(ip_address):
            return True
        else:
            return False


class IPAddressAsync(IPAddress):
    @staticmethod
    async def verify_ip_address(ip_address: str) -> bool:
        return IPAddress.verify_ip_address(ip_address)

    @staticmethod
    async def verify_mac_address(mac_address: str) -> bool:
        return IPAddress.verify_mac_address(mac_address)

    @staticmethod
    async def verify_ipv4(ip_address: str) -> bool:
        return IPAddress.verify_ipv4(ip_address)

    @staticmethod
    async def verify_ipv6(ip_address: str) -> bool:
        return IPAddress.verify_ipv6(ip_address)
