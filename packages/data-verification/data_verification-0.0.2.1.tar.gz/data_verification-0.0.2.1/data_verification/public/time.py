from datetime import datetime, timedelta


class Time:
    @staticmethod
    def time_range(time: str, start_time: str, end_time: str, time_format: str = None, pattern: int = 0) -> bool:
        """
        验证时间戳或带格式时间是否在某个区间
        :param time: 被验证时间
        :param start_time: 起始时间
        :param end_time: 结束时间
        :param time_format: 时间格式
        :param pattern: 区间判断类型，0：前闭后闭，1：前闭后开，2：前开后闭，3：前开后开
        :return:
        """
        if pattern not in [0, 1, 2, 3]:
            return ValueError("pattern must be 0 or 1, 2 or 3")
        if isinstance(time, (int, float)):  # 如果是时间戳
            return Time.timestamp_range(time, start_time, end_time, pattern)
        elif isinstance(time, str) and time_format:  # 如果是字符串且指定了格式
            return Time.datetime_range(time, start_time, end_time, time_format, pattern)
        else:
            return False

    @staticmethod
    def datetime_range(time: str, start_time: str, end_time: str, time_format: str = "%Y-%m-%d %H:%M",
                       pattern: int = 0) -> bool:
        """
        验证带有格式的时间是否在某个区间
        :param time: 被验证时间
        :param start_time: 起始时间
        :param end_time: 结束时间
        :param time_format: 时间格式
        :param pattern: 区间判断类型，0：前闭后闭，1：前闭后开，2：前开后闭，3：前开后开
        :return:
        """
        if pattern not in [0, 1, 2, 3]:
            return ValueError("pattern must be 0 or 1, 2 or 3")
        try:
            # 解析输入的日期时间字符串为 datetime 对象
            dt = datetime.strptime(time, time_format)
            start_dt = datetime.strptime(start_time, time_format)
            end_dt = datetime.strptime(end_time, time_format)
            if pattern == 0:
                return start_dt <= dt <= end_dt
            elif pattern == 1:
                return start_dt <= dt < end_dt
            elif pattern == 2:
                return start_dt < dt <= end_dt
            elif pattern == 3:
                return start_dt < dt < end_dt
        except ValueError:
            print("Invalid date format")
            return False

    @staticmethod
    def timestamp_range(timestamp: int, start_timestamp: int, end_timestamp: int, pattern: int = 0) -> bool:
        """
        验证时间戳是否在某个区间
        :param timestamp: 被验证的时间戳
        :param start_timestamp: 起始时间戳
        :param end_timestamp: 结束时间戳
        :param pattern: 区间判断类型，0：前闭后闭，1：前闭后开，2：前开后闭，3：前开后开
        :return:
        """
        if pattern not in [0, 1, 2, 3]:
            return ValueError("pattern must be 0 or 1, 2 or 3")
        if pattern == 0:
            return start_timestamp <= timestamp <= end_timestamp
        elif pattern == 1:
            return start_timestamp <= timestamp < end_timestamp
        elif pattern == 2:
            return start_timestamp < timestamp <= end_timestamp
        elif pattern == 3:
            return start_timestamp < timestamp < end_timestamp

    @staticmethod
    def verify_date(date_string: str, date_format: str = "%Y-%m-%d") -> bool:
        """
        对日期进行验证
        :param date_string: 被验证的日期
        :param date_format: 日期格式化规则
        :return:
        """
        try:
            # 尝试根据指定格式解析日期字符串
            parsed_date = datetime.strptime(date_string, date_format)
            # 验证解析后的日期是否合理（例如月份不能超过12，天数不能超过该月的最大天数）
            parsed_date.strftime(date_format)  # 这一步会抛出异常如果日期不合理
            return True
        except ValueError:
            return False

    @staticmethod
    def verify_timestamp(timestamp: str) -> bool:
        """
        对时间戳进行验证
        :param timestamp: 被验证的时间戳
        :return:
        """
        try:
            # 尝试将时间戳转换为 datetime 对象
            if isinstance(timestamp, int) or (isinstance(timestamp, str) and timestamp.isdigit()):
                timestamp = int(timestamp)
                datetime.fromtimestamp(timestamp)
                return True
            else:
                return False
        except (ValueError, OverflowError, OSError):  # OSError 可能出现在非常大的时间戳上
            return False

    @staticmethod
    def check_timeliness(timestamp_str, date_format="%Y-%m-%d %H:%M:%S", timeliness_threshold_minutes=60):
        """
        检查给定的时间戳是否符合及时性要求。
        :param timestamp_str: 时间戳字符串。
        :param date_format: 时间戳的格式，默认为"%Y-%m-%d %H:%M:%S"。
        :param timeliness_threshold_minutes: 数据被认为是及时的最大分钟数，默认为60分钟。
        :return:
        """
        threshold = timedelta(minutes=timeliness_threshold_minutes)
        try:
            # 将时间戳字符串转换为datetime对象
            data_timestamp = datetime.strptime(timestamp_str, date_format)
        except ValueError:
            return False
        # 获取当前时间
        now = datetime.now()
        # 计算时间差
        time_diff = now - data_timestamp
        # 判断是否超过阈值
        return time_diff <= threshold


class TimeAsync(Time):
    @staticmethod
    async def time_range(time: str, start_time: str, end_time: str, time_format: str = None, pattern: int = 0) -> bool:
        return Time.time_range(time, start_time, end_time, time_format, pattern)

    @staticmethod
    async def verify_date(date_string: str, date_format: str = "%Y-%m-%d") -> bool:
        return Time.verify_date(date_string, date_format)

    @staticmethod
    async def verify_timestamp(timestamp: str) -> bool:
        return Time.verify_timestamp(timestamp)

    @staticmethod
    async def datetime_range(time: str, start_time: str, end_time: str, time_format: str = "%Y-%m-%d %H:%M",
                             pattern: int = 0) -> bool:
        return Time.datetime_range(time, start_time, end_time, time_format, pattern)

    @staticmethod
    async def timestamp_range(timestamp: int, start_timestamp: int, end_timestamp: int, pattern: int = 0) -> bool:
        return Time.timestamp_range(timestamp, start_timestamp, end_timestamp, pattern)

    @staticmethod
    async def check_timeliness(timestamp_str, date_format="%Y-%m-%d %H:%M:%S", timeliness_threshold_minutes=60):
        return Time.check_timeliness(timestamp_str, date_format, timeliness_threshold_minutes)
