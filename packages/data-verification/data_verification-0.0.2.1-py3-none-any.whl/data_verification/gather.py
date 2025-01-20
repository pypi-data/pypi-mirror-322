import asyncio
from data_verification.public import *
from data_verification.geo import *


class PublicDataVerification(Regex, SCC, Number, Email, IDNumber, Organization, Compare, VerifyType, Coordinates, Time,
                             IPAddress, PhoneNumber, AdminDivision, Decode, Postal, Empty, Unique):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PublicDataVerificationAsync(RegexAsync, SCCAsync, NumberAsync, EmailAsync, IDNumberAsync, OrganizationAsync,
                                  TimeAsync, CompareAsync, VerifyTypeAsync, CoordinatesAsync, IPAddressAsync,
                                  EmptyAsync, PhoneNumberAsync, AdminDivisionAsync, DecodeAsync, PostalAsync,
                                  UniqueAsync):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GeoDataValidator:
    VALIDATOR_TYPES = {
        'point_data': PointDataValidator,
        'line_data': LineDataValidator,
        'polygon_data': PolygonDataValidator,
        'point_topology': PointTopologyValidator,
        'line_topology': LineTopologyValidator,
        'polygon_topology': PolygonTopologyValidator,
    }

    def __init__(self, file_path: str, validator_type: str, boundary_file_path: str = None):
        """
        综合地理数据位置合理性验证
        :param file_path: 地理数据shp文件路径
        :param validator_type: 验证器类型，如 'point_data':矢量点数据位置合理性, 'line_data':矢量线数据位置合理性,
            'polygon_data':矢量面数据位置合理性, 'point_topology':点拓扑规则合理性, 'line_topology':线拓扑规则合理性,
            'polygon_topology':面拓扑规则合理性
        :param boundary_file_path: 边界多边形shp文件地址（可选）
        """
        if validator_type not in self.VALIDATOR_TYPES:
            raise ValueError(
                f"Invalid validator type '{validator_type}'. Available types are {list(self.VALIDATOR_TYPES.keys())}")

        ValidatorClass = self.VALIDATOR_TYPES[validator_type]
        if validator_type.endswith('_topology'):
            # Topology validators may need line_file_path for point topology checks
            self.validator = ValidatorClass(file_path, boundary_file_path=boundary_file_path)
        else:
            self.validator = ValidatorClass(file_path, boundary_file_path)

    def check_validity(self, **kwargs):
        """
        检查地理数据位置合理性和拓扑规则。
        :param kwargs: 传递给具体检查方法的关键字参数。
        :return:
        """
        if isinstance(self.validator, (PointDataValidator, LineDataValidator, PolygonDataValidator)):
            return self._check_data_validity(**kwargs)
        elif isinstance(self.validator, (PointTopologyValidator, LineTopologyValidator, PolygonTopologyValidator)):
            return self._check_topology_validity(**kwargs)
        else:
            raise ValueError("Unknown validator type")

    def _check_data_validity(self, **kwargs):
        """
        检查地理数据位置合理性。
        """
        if isinstance(self.validator, PointDataValidator):
            return self.validator.check_point_data_validity(**kwargs)
        elif isinstance(self.validator, LineDataValidator):
            return self.validator.check_line_data_validity()
        elif isinstance(self.validator, PolygonDataValidator):
            return self.validator.check_polygon_data_validity(**kwargs)

    def _check_topology_validity(self, **kwargs):
        """
        检查地理数据拓扑规则。
        """
        if isinstance(self.validator, PointTopologyValidator):
            return self.validator.check_point_topology_validity(**kwargs)
        elif isinstance(self.validator, LineTopologyValidator):
            return self.validator.check_line_topology_validity(**kwargs)
        elif isinstance(self.validator, PolygonTopologyValidator):
            return self.validator.check_polygon_topology_validity(**kwargs)

    def check_specific_validity(self, index: int, **kwargs):
        """
        检查特定地理要素的位置合理性和拓扑规则。
        :param index: 要检查的要素索引。
        :param kwargs: 传递给具体检查方法的关键字参数。
        :return:
        """
        if isinstance(self.validator, (PointDataValidator, LineDataValidator, PolygonDataValidator)):
            method_name = f'check_specific_{self.validator.__class__.__name__.lower().replace("validator", "")}'
            method = getattr(self.validator, method_name, None)
            if method:
                return method(index, **kwargs)
            else:
                raise AttributeError(f"Method {method_name} not found in {self.validator.__class__.__name__}")
        elif isinstance(self.validator, (PointTopologyValidator, LineTopologyValidator, PolygonTopologyValidator)):
            method_name = f'check_specific_{self.validator.__class__.__name__.lower().replace("validator", "")}'
            method = getattr(self.validator, method_name, None)
            if method:
                return method(index, **kwargs)
            else:
                raise AttributeError(f"Method {method_name} not found in {self.validator.__class__.__name__}")
        else:
            raise ValueError("Unknown validator type")


class GeoDataValidatorAsync(GeoDataValidator):
    def __init__(self, file_path: str, validator_type: str, boundary_file_path: str = None):
        super().__init__(file_path, validator_type, boundary_file_path)

    async def check_validity(self, **kwargs):
        loop = asyncio.get_event_loop()
        if isinstance(self.validator, (PointDataValidator, LineDataValidator, PolygonDataValidator)):
            return await loop.run_in_executor(None, self._check_data_validity, kwargs)
        elif isinstance(self.validator, (PointTopologyValidator, LineTopologyValidator, PolygonTopologyValidator)):
            return await loop.run_in_executor(None, self._check_topology_validity, kwargs)
        else:
            raise ValueError("Unknown validator type")

    async def check_specific_validity(self, index: int, **kwargs):
        loop = asyncio.get_event_loop()
        if isinstance(self.validator, (PointDataValidator, LineDataValidator, PolygonDataValidator)):
            method_name = f'check_specific_{self.validator.__class__.__name__.lower().replace("validator", "")}'
            method = getattr(self.validator, method_name, None)
            if method:
                return await loop.run_in_executor(None, lambda: method(index, **kwargs))
            else:
                raise AttributeError(f"Method {method_name} not found in {self.validator.__class__.__name__}")
        elif isinstance(self.validator, (PointTopologyValidator, LineTopologyValidator, PolygonTopologyValidator)):
            method_name = f'check_specific_{self.validator.__class__.__name__.lower().replace("validator", "")}'
            method = getattr(self.validator, method_name, None)
            if method:
                return await loop.run_in_executor(None, lambda: method(index, **kwargs))
            else:
                raise AttributeError(f"Method {method_name} not found in {self.validator.__class__.__name__}")
        else:
            raise ValueError("Unknown validator type")
