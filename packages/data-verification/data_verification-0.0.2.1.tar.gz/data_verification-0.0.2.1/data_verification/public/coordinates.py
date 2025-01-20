class Coordinates:
    @staticmethod
    def verify_latitude(latitude: int or float, start_latitude_scope: int or float,
                        end_latitude_scope: int or float) -> bool:
        """
        纬度范围验证
        :param latitude: 被验证纬度
        :param start_latitude_scope: 起始纬度，大于-90
        :param end_latitude_scope: 结束纬度，小于90
        :return:
        """
        if start_latitude_scope < -90:
            return ValueError("start_latitude_scope must be greater than -90.")
        if end_latitude_scope > 90:
            return ValueError("end_latitude_scope must be greater than 90.")
        if not (start_latitude_scope <= latitude <= end_latitude_scope):
            return False
        return True

    @staticmethod
    def verify_longitude(longitude: int or float, start_longitude_scope: int or float,
                         end_longitude_scope: int or float) -> bool:
        """
        经度范围验证
        :param longitude: 被验证经度
        :param start_longitude_scope: 起始经度，大于-180
        :param end_longitude_scope: 结束经度，小于180
        :return:
        """
        if start_longitude_scope < -180:
            return ValueError("start_longitude_scope must be greater than -180.")
        if end_longitude_scope > 180:
            return ValueError("end_longitude_scope must be greater than 180.")
        if not (start_longitude_scope <= longitude <= end_longitude_scope):
            return False
        return True

    @staticmethod
    def verify_coordinates(latitude: int or float, start_latitude_scope: int or float, end_latitude_scope: int or float,
                           longitude: int or float, start_longitude_scope: int or float,
                           end_longitude_scope: int or float) -> bool:
        """
        经纬度范围验证
        :param latitude: 被验证纬度
        :param start_latitude_scope: 起始纬度，大于-90
        :param end_latitude_scope: 结束纬度，小于90
        :param longitude: 被验证经度
        :param start_longitude_scope: 起始经度，大于-180
        :param end_longitude_scope: 结束经度，小于180
        :return:
        """
        if start_latitude_scope < -90:
            return ValueError("start_latitude_scope must be greater than -90.")
        if end_latitude_scope > 90:
            return ValueError("end_latitude_scope must be greater than 90.")
        if start_longitude_scope < -180:
            return ValueError("start_longitude_scope must be greater than -180.")
        if end_longitude_scope > 180:
            return ValueError("end_longitude_scope must be greater than 180.")
        latitude_ = Coordinates.verify_latitude(latitude, start_latitude_scope, end_latitude_scope)
        longitude_ = Coordinates.verify_longitude(longitude, start_longitude_scope, end_longitude_scope)
        if latitude_ and longitude_:
            return True
        return False

    @staticmethod
    def verify_china_latitude(latitude: int or float) -> bool:
        """
        中国纬度验证
        :param latitude: 纬度
        :return:
        """
        if not (4 <= latitude <= 53):
            return False
        return True

    @staticmethod
    def verify_china_longitude(longitude: int or float) -> bool:
        """
        中国经度验证
        :param longitude: 经度
        :return:
        """
        if not (73 <= longitude <= 135):
            return False
        return True

    @staticmethod
    def verify_china_coordinates(latitude: int or float, longitude: int or float) -> bool:
        """
        中国经纬度验证
        :param latitude: 纬度
        :param longitude: 经度
        :return:
        """
        if not (4 <= latitude <= 53):
            return False
        if not (73 <= longitude <= 135):
            return False
        return True

    @staticmethod
    def verify_global_latitude(latitude: int or float) -> bool:
        """
        全球纬度验证
        :param latitude: 纬度
        :return:
        """
        if not (-90 <= latitude <= 90):
            return False
        return True

    @staticmethod
    def verify_global_longitude(longitude: int or float) -> bool:
        """
        全球经度验证
        :param longitude: 经度
        :return:
        """
        if not (-180 <= longitude <= 180):
            return False
        return True

    @staticmethod
    def verify_global_coordinates(latitude: int or float, longitude: int or float) -> bool:
        """
        全球经纬度验证
        :param latitude: 纬度
        :param longitude: 经度
        :return:
        """
        if not (-90 <= latitude <= 90):
            return False
        if not (-180 <= longitude <= 180):
            return False
        return True


class CoordinatesAsync(Coordinates):
    @staticmethod
    async def verify_latitude(latitude: int or float, start_latitude_scope: int or float,
                              end_latitude_scope: int or float) -> bool:
        return Coordinates.verify_latitude(latitude, start_latitude_scope, end_latitude_scope)

    @staticmethod
    async def verify_longitude(longitude: int or float, start_longitude_scope: int or float,
                               end_longitude_scope: int or float) -> bool:
        return Coordinates.verify_longitude(longitude, start_longitude_scope, end_longitude_scope)

    @staticmethod
    async def verify_coordinates(latitude: int or float, start_latitude_scope: int or float,
                                 end_latitude_scope: int or float, longitude: int or float,
                                 start_longitude_scope: int or float, end_longitude_scope: int or float) -> bool:
        return Coordinates.verify_coordinates(latitude, start_latitude_scope, end_latitude_scope, longitude,
                                              start_longitude_scope, end_longitude_scope)

    @staticmethod
    async def verify_china_latitude(latitude: int or float) -> bool:
        return Coordinates.verify_china_latitude(latitude)

    @staticmethod
    async def verify_china_longitude(longitude: int or float) -> bool:
        return Coordinates.verify_china_longitude(longitude)

    @staticmethod
    async def verify_china_coordinates(latitude: int or float, longitude: int or float) -> bool:
        return Coordinates.verify_china_coordinates(latitude, longitude)

    @staticmethod
    async def verify_global_latitude(latitude: int or float) -> bool:
        return Coordinates.verify_global_latitude(latitude)

    @staticmethod
    async def verify_global_longitude(longitude: int or float) -> bool:
        return Coordinates.verify_global_longitude(longitude)

    @staticmethod
    async def verify_global_coordinates(latitude: int or float, longitude: int or float) -> bool:
        return Coordinates.verify_global_coordinates(latitude, longitude)
