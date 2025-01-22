import re


class Postal:
    @staticmethod
    def postal_code(postal_code: str, country_code='CN') -> bool:
        """
        验证邮政编码是否正确
        :param postal_code: 被验证编码
        :param country_code: 地区，目前支持CN-中国，US-美国，GB-英国，DE-德国，FR-法国，AU-澳大利亚，JP-日报，IN-印度，RU-俄罗斯，
            IT-意大利，ES-西班牙，NL-荷兰，CH-瑞士，BR-巴西，CA-加拿大，AR-阿根廷，AT-奥地利，BE-比利时，CL-智利，CO-哥伦比亚，DK-丹麦，
            FI-荷兰，GR-希腊，HU-匈牙利，ID-印度尼西亚，IE-爱尔兰，IL-以色列，KR-韩国，LU-卢森堡，MY-马来西亚，MX-墨西哥，NZ-新西兰，NO-挪威，
            PL-波兰，PT-葡萄牙，RO-罗马尼亚，SG-新加坡，ZA-南非，SE-瑞典，TH-泰国，TR-土耳其，UA-乌克兰，VN-越南
        :return:
        """
        country_code = country_code.upper()
        regex_patterns = {
            'CN': r'^\d{6}$',
            'US': r'^\d{5}(-\d{4})?$',
            'GB': r'^(GIR 0AA|[A-PR-UWYZ][A-HK-Y]?[0-9][0-9]??[A-HJKPSTUW][ABD-HJLN-UW][A-IK-Y])$',
            'DE': r'^\d{5}$',
            'FR': r'^\d{5}$',
            'AU': r'^\d{4}$',
            'JP': r'^\d{3}-\d{4}$',
            'IN': r'^\d{6}$',
            'RU': r'^\d{6}$',
            'IT': r'^\d{5}$',
            'ES': r'^\d{5}$',
            'NL': r'^\d{4}\s?[A-Z]{2}$',
            'CH': r'^\d{4}$',
            'BR': r'^\d{5}-\d{3}$',
            'CA': r'^[ABCEGHJKLMNPRSTVXY]\d[ABCEGHJ-NPRSTV-Z] ?\d[ABCEGHJ-NPRSTV-Z]\d$',
            'AR': r'^\d{4}|\d{4}-\d{3}$',
            'AT': r'^\d{4}$',
            'BE': r'^\d{4}$',
            'CL': r'^\d{3}-\d{4}$',
            'CO': r'^\d{6}$',
            'DK': r'^\d{4}$',
            'FI': r'^\d{5}$',
            'GR': r'^\d{5}$',
            'HU': r'^\d{4}$',
            'ID': r'^\d{5}$',
            'IE': r'^[AC-FHKNPRTVWXYZ]{3}\d{4}$',
            'IL': r'^\d{5}$',
            'KR': r'^\d{5}|\d{6}$',
            'LU': r'^\d{4}$',
            'MY': r'^\d{5}$',
            'MX': r'^\d{5}$',
            'NZ': r'^\d{4}$',
            'NO': r'^\d{4}$',
            'PL': r'^\d{2}-\d{3}$',
            'PT': r'^\d{4}-\d{3}$',
            'RO': r'^\d{6}$',
            'SG': r'^\d{6}$',
            'ZA': r'^\d{4}$',
            'SE': r'^\d{3}\s?\d{2}$',
            'TH': r'^\d{5}$',
            'TR': r'^\d{5}$',
            'UA': r'^\d{5}$',
            'VN': r'^\d{6}$',
        }
        pattern = regex_patterns.get(country_code)
        if not pattern:
            raise ValueError(f"Unsupported country code '{country_code}'")

        return bool(re.match(pattern, postal_code))


class PostalAsync(Postal):
    @staticmethod
    async def postal_code(postal_code, country_code='CN'):
        return Postal.postal_code(postal_code, country_code)
