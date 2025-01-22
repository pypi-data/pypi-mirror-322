import geopandas as gpd
from shapely.ops import unary_union
from shapely.geometry import MultiPoint, Point, LineString


class LineDataValidator:
    def __init__(self, line_file_path: str, boundary_file_path: str = None):
        """
        矢量线数据位置合理性验证
        :param line_file_path: 线数据shp文件地址
        :param boundary_file_path: 边界多边形shp文件地址（可选）
        """
        # 加载线数据
        self.lines = gpd.read_file(line_file_path)
        # 如果提供了边界文件，则加载边界多边形数据
        if boundary_file_path:
            self.boundary_polygons = gpd.read_file(boundary_file_path)
        else:
            self.boundary_polygons = None

    def _check_geometry_validity(self):
        """检查几何有效性"""
        return self.lines.is_valid.all()

    def _find_dangling_nodes(self):
        """查找悬挂节点"""
        endpoints = [geom.boundary for geom in self.lines.geometry if not geom.is_empty]
        if endpoints:
            all_points = MultiPoint([pt for line in endpoints for pt in line])
            points_counts = {pt: sum(pt.equals(other) for other in all_points) for pt in all_points}
            dangling_nodes = [pt for pt, count in points_counts.items() if count == 1]
            return len(dangling_nodes) > 0
        else:
            return False

    def _check_line_intersections(self):
        """检查不必要的线间相交"""
        intersections = []
        for i, line_a in self.lines.iterrows():
            for j, line_b in self.lines.iterrows():
                if i < j:  # 避免重复比较
                    intersection = line_a.geometry.intersection(line_b.geometry)
                    if not intersection.is_empty and not isinstance(intersection, (Point)):
                        intersections.append(intersection)
        return len(intersections) > 0

    def _check_lines_within_boundaries(self):
        """检查所有线是否都在给定的边界内"""
        if self.boundary_polygons is None:
            print("No boundary provided for checking.")
            return True  # 没有提供边界，默认认为合理
        # 使用unary_union合并所有边界多边形
        boundary_union = unary_union(self.boundary_polygons.geometry)
        lines_within = self.lines.within(boundary_union)
        return lines_within.all()

    def check_line_data_validity(self) -> bool:
        """
        检查矢量线数据的位置合理性。
        :return:
        """
        geometry_valid = self._check_geometry_validity()
        has_dangling_nodes = self._find_dangling_nodes()
        has_unnecessary_intersections = self._check_line_intersections()
        within_boundaries = self._check_lines_within_boundaries()
        # 如果几何有效、没有悬挂节点、没有不必要的交叉且在边界内，则认为数据合理
        is_valid = geometry_valid and not has_dangling_nodes and not has_unnecessary_intersections and within_boundaries

        return is_valid


class PolygonDataValidator:
    def __init__(self, polygon_file_path, boundary_file_path=None):
        """
        矢量面数据位置合理性验证
        :param polygon_file_path: 面数据shp文件地址
        :param boundary_file_path: 边界多边形shp文件地址（可选）
        """
        # 加载面数据
        self.polygons = gpd.read_file(polygon_file_path)
        # 如果提供了边界文件，则加载边界多边形数据
        if boundary_file_path:
            self.boundary_polygons = gpd.read_file(boundary_file_path)
        else:
            self.boundary_polygons = None

    def _check_geometry_validity(self):
        """检查几何有效性"""
        return self.polygons.is_valid.all()

    def _check_overlap(self):
        """检查多边形之间的重叠情况"""
        overlaps = []
        for i, poly_a in self.polygons.iterrows():
            for j, poly_b in self.polygons.iterrows():
                if i < j:  # 避免重复比较
                    intersection = poly_a.geometry.intersection(poly_b.geometry)
                    if not intersection.is_empty and not isinstance(intersection, (Point, LineString)):
                        overlaps.append(intersection)
        return len(overlaps) > 0

    def _check_gaps(self):
        """检查多边形之间的空隙情况（适用于需要连续覆盖的情况）"""
        unioned_polygon = unary_union(self.polygons.geometry)
        boundary = unioned_polygon.boundary
        # 如果边界为空，则说明没有空隙（所有多边形连成一片）
        return not boundary.is_empty

    def _check_holes(self):
        """检查多边形内部是否存在孔洞（取决于应用需求）"""
        holes_exist = any(not poly.is_empty and poly.interiors for poly in self.polygons.geometry)
        return holes_exist

    def _check_within_boundaries(self):
        """检查所有多边形是否都在给定的边界内"""
        if self.boundary_polygons is None:
            print("No boundary provided for checking.")
            return True  # 没有提供边界，默认认为合理
        # 使用unary_union合并所有边界多边形
        boundary_union = unary_union(self.boundary_polygons.geometry)
        polygons_within = self.polygons.within(boundary_union)
        return polygons_within.all()

    def check_polygon_data_validity(self, allow_holes=False) -> bool:
        """
        检查矢量面数据的位置合理性。
        :param allow_holes: 是否允许多边形内存在孔洞，默认为 False。
        :return:
        """
        geometry_valid = self._check_geometry_validity()
        has_overlaps = self._check_overlap()
        has_gaps = self._check_gaps()
        has_unwanted_holes = self._check_holes() and not allow_holes
        within_boundaries = self._check_within_boundaries()
        # 如果几何有效、没有重叠、没有空隙、没有不希望出现的孔洞且在边界内，则认为数据合理
        is_valid = geometry_valid and not has_overlaps and not has_gaps and not has_unwanted_holes and within_boundaries
        return is_valid


class PointDataValidator:
    def __init__(self, point_file_path: str, boundary_file_path: str = None):
        """
        矢量点数据位置合理性验证
        :param point_file_path: 点数据shp文件地址
        :param boundary_file_path: 边界多边形shp文件地址（可选）
        """
        # 加载点数据
        self.points = gpd.read_file(point_file_path)
        # 如果提供了边界文件，则加载边界多边形数据
        if boundary_file_path:
            self.boundary_polygons = gpd.read_file(boundary_file_path)
        else:
            self.boundary_polygons = None

    def _check_geometry_validity(self):
        """检查几何有效性"""
        return self.points.is_valid.all()

    def _check_duplicates(self):
        """检查是否存在重复点"""
        unique_points = self.points.drop_duplicates(subset=['geometry'])
        return len(unique_points) != len(self.points)

    def _check_within_boundaries(self):
        """检查所有点是否都在给定的边界内"""
        if self.boundary_polygons is None:
            print("No boundary provided for checking.")
            return True  # 没有提供边界，默认认为合理
        # 使用unary_union合并所有边界多边形
        boundary_union = unary_union(self.boundary_polygons.geometry)
        points_within = self.points.within(boundary_union)
        return points_within.all()

    def _check_proximity_to_lines(self, line_file_path, max_distance=0.0):
        """检查点与线的距离是否在允许范围内（可选）"""
        lines = gpd.read_file(line_file_path)
        distances = self.points.geometry.apply(lambda point: min(lines.distance(point)))
        return (distances <= max_distance).all()

    def check_point_data_validity(self, check_within_boundaries=True, line_file_path=None, max_distance=0.0) -> bool:
        """
        检查矢量点数据的位置合理性。
        :param check_within_boundaries: 是否检查点是否位于边界内，默认为 True。
        :param line_file_path: 用于检查点到线距离的线数据文件路径（可选）。
        :param max_distance: 允许的最大距离，单位与坐标系一致，默认为 0.0 表示必须重合。
        :return:
        """
        geometry_valid = self._check_geometry_validity()
        has_duplicates = self._check_duplicates()
        within_boundaries = self._check_within_boundaries() if check_within_boundaries else True
        proximity_to_lines = True
        if line_file_path:
            proximity_to_lines = self._check_proximity_to_lines(line_file_path, max_distance)
        # 如果几何有效、没有重复点、都在边界内且与线的距离合理，则认为数据合理
        is_valid = geometry_valid and not has_duplicates and within_boundaries and proximity_to_lines
        return is_valid


class LineTopologyValidator:
    def __init__(self, line_file_path, boundary_file_path=None):
        """
        线拓扑规则合理性验证
        :param line_file_path: 线数据shp文件地址
        :param boundary_file_path: 边界多边形shp文件地址（可选）
        """
        # 加载线数据
        self.lines = gpd.read_file(line_file_path)
        # 如果提供了边界文件，则加载边界多边形数据
        if boundary_file_path:
            self.boundary_polygons = gpd.read_file(boundary_file_path)
        else:
            self.boundary_polygons = None

    def _check_geometry_validity(self):
        """检查几何有效性"""
        return self.lines.is_valid.all()

    def _find_dangling_nodes(self):
        """查找悬挂节点"""
        endpoints = [geom.boundary for geom in self.lines.geometry if not geom.is_empty]
        if endpoints:
            all_points = MultiPoint([pt for line in endpoints for pt in line])
            points_counts = {pt: sum(pt.equals(other) for other in all_points) for pt in all_points}
            dangling_nodes = [pt for pt, count in points_counts.items() if count == 1]
            return len(dangling_nodes) > 0
        else:
            return False

    def _check_line_intersections(self):
        """检查不必要的线间相交"""
        intersections = []
        for i, line_a in self.lines.iterrows():
            for j, line_b in self.lines.iterrows():
                if i < j:  # 避免重复比较
                    intersection = line_a.geometry.intersection(line_b.geometry)
                    if not intersection.is_empty and not isinstance(intersection, Point):
                        intersections.append(intersection)
        return len(intersections) > 0

    def _check_lines_within_boundaries(self):
        """检查所有线是否都在给定的边界内"""
        if self.boundary_polygons is None:
            print("No boundary provided for checking.")
            return True  # 没有提供边界，默认认为合理
        # 使用unary_union合并所有边界多边形
        boundary_union = unary_union(self.boundary_polygons.geometry)
        lines_within = self.lines.within(boundary_union)
        return lines_within.all()

    def check_line_topology_validity(self, check_within_boundaries=True) -> bool:
        """
        检查矢量线数据的拓扑规则合理性。
        :param check_within_boundaries: 是否检查线是否位于边界内，默认为 True。
        :return:
        """
        geometry_valid = self._check_geometry_validity()
        has_dangling_nodes = self._find_dangling_nodes()
        has_unnecessary_intersections = self._check_line_intersections()
        within_boundaries = self._check_lines_within_boundaries() if check_within_boundaries else True
        # 如果几何有效、没有悬挂节点、没有不必要的交叉且（如果适用）在边界内，则认为数据合理
        is_valid = geometry_valid and not has_dangling_nodes and not has_unnecessary_intersections and within_boundaries

        return is_valid

    def check_specific_line(self, index: int) -> bool:
        """
        检查某条特定线的拓扑规则合理性。
        :param index: 要检查的线的索引。
        :return:
        """
        specific_line = self.lines.iloc[[index]]
        geometry_valid = specific_line.is_valid.all()
        has_dangling_nodes = self._find_dangling_nodes_for_specific_line(specific_line)
        has_unnecessary_intersections = self._check_specific_line_intersections(index)
        # 如果几何有效、没有悬挂节点且没有不必要的交叉，则认为数据合理
        is_valid = geometry_valid and not has_dangling_nodes and not has_unnecessary_intersections
        return is_valid

    @staticmethod
    def _find_dangling_nodes_for_specific_line(specific_line):
        """针对特定线查找悬挂节点"""
        endpoints = [geom.boundary for geom in specific_line.geometry if not geom.is_empty]
        if endpoints:
            all_points = MultiPoint([pt for line in endpoints for pt in line])
            points_counts = {pt: sum(pt.equals(other) for other in all_points) for pt in all_points}
            dangling_nodes = [pt for pt, count in points_counts.items() if count == 1]
            return len(dangling_nodes) > 0
        else:
            return False

    def _check_specific_line_intersections(self, index):
        """检查特定线与其他线的不必要相交"""
        specific_line = self.lines.iloc[index].geometry
        intersections = []
        for i, line_b in self.lines.iterrows():
            if i != index:  # 不与自身比较
                intersection = specific_line.intersection(line_b.geometry)
                if not intersection.is_empty and not isinstance(intersection, Point):
                    intersections.append(intersection)
        return len(intersections) > 0


class PolygonTopologyValidator:
    def __init__(self, polygon_file_path, boundary_file_path=None):
        """
        面拓扑规则合理性验证
        :param polygon_file_path: 面数据shp文件地址
        :param boundary_file_path: 边界多边形shp文件地址（可选）
        """
        # 加载面数据
        self.polygons = gpd.read_file(polygon_file_path)
        # 如果提供了边界文件，则加载边界多边形数据
        if boundary_file_path:
            self.boundary_polygons = gpd.read_file(boundary_file_path)
        else:
            self.boundary_polygons = None

    def _check_geometry_validity(self):
        """检查几何有效性"""
        return self.polygons.is_valid.all()

    def _check_overlap(self):
        """检查多边形之间的重叠情况"""
        overlaps = []
        for i, poly_a in self.polygons.iterrows():
            for j, poly_b in self.polygons.iterrows():
                if i < j:  # 避免重复比较
                    intersection = poly_a.geometry.intersection(poly_b.geometry)
                    if not intersection.is_empty and not isinstance(intersection, (Point, LineString)):
                        overlaps.append(intersection)
        return len(overlaps) > 0

    def _check_gaps(self):
        """检查多边形之间的空隙情况（适用于需要连续覆盖的情况）"""
        unioned_polygon = unary_union(self.polygons.geometry)
        boundary = unioned_polygon.boundary
        # 如果边界为空，则说明没有空隙（所有多边形连成一片）
        return not boundary.is_empty

    def _check_holes(self):
        """检查多边形内部是否存在孔洞（取决于应用需求）"""
        holes_exist = any(not poly.is_empty and poly.interiors for poly in self.polygons.geometry)
        return holes_exist

    def _check_polygons_within_boundaries(self):
        """检查所有多边形是否都在给定的边界内"""
        if self.boundary_polygons is None:
            print("No boundary provided for checking.")
            return True  # 没有提供边界，默认认为合理
        # 使用unary_union合并所有边界多边形
        boundary_union = unary_union(self.boundary_polygons.geometry)
        polygons_within = self.polygons.within(boundary_union)
        return polygons_within.all()

    def check_polygon_topology_validity(self, allow_holes=False, check_within_boundaries=True) -> bool:
        """
        检查矢量面数据的拓扑规则合理性。
        :param allow_holes: 是否允许多边形内存在孔洞，默认为 False。
        :param check_within_boundaries: 是否检查多边形是否位于边界内，默认为 True。
        :return:
        """
        geometry_valid = self._check_geometry_validity()
        has_overlaps = self._check_overlap()
        has_gaps = self._check_gaps()
        has_unwanted_holes = self._check_holes() and not allow_holes
        within_boundaries = self._check_polygons_within_boundaries() if check_within_boundaries else True
        # 如果几何有效、没有重叠、没有空隙、没有不希望出现的孔洞且（如果适用）在边界内，则认为数据合理
        is_valid = geometry_valid and not has_overlaps and not has_gaps and not has_unwanted_holes and within_boundaries
        return is_valid

    def check_specific_polygon(self, index, allow_holes=False) -> bool:
        """
        检查某个多边形的拓扑规则合理性。
        :param index: 要检查的多边形的索引。
        :param allow_holes: 是否允许该多边形内存在孔洞，默认为 False。
        :return:
        """
        specific_polygon = self.polygons.iloc[[index]]
        geometry_valid = specific_polygon.is_valid.all()
        has_overlaps = self._check_specific_overlap(index)
        has_gaps = self._check_specific_gap(index)
        has_unwanted_holes = self._check_specific_holes(specific_polygon) and not allow_holes
        # 如果几何有效、没有重叠、没有空隙且没有不希望出现的孔洞，则认为数据合理
        is_valid = geometry_valid and not has_overlaps and not has_gaps and not has_unwanted_holes
        return is_valid

    def _check_specific_overlap(self, index):
        """针对特定多边形检查重叠情况"""
        specific_polygon = self.polygons.iloc[index].geometry
        overlaps = []
        for i, poly_b in self.polygons.iterrows():
            if i != index:  # 不与自身比较
                intersection = specific_polygon.intersection(poly_b.geometry)
                if not intersection.is_empty and not isinstance(intersection, (Point, LineString)):
                    overlaps.append(intersection)
        return len(overlaps) > 0

    def _check_specific_gap(self, index):
        """针对特定多边形检查空隙情况（适用于需要连续覆盖的情况）"""
        specific_polygon = self.polygons.iloc[[index]]
        remaining_polygons = self.polygons.drop(index)
        if remaining_polygons.empty:
            return False  # 没有其他多边形，默认认为没有空隙
        unioned_remaining_polygon = unary_union(remaining_polygons.geometry)
        boundary = specific_polygon.unary_union.boundary.difference(unioned_remaining_polygon.boundary)
        # 如果边界不为空，则说明存在空隙
        return not boundary.is_empty

    def _check_specific_holes(self, specific_polygon):
        """针对特定多边形检查孔洞情况"""
        holes_exist = any(not poly.is_empty and poly.interiors for poly in specific_polygon.geometry)
        return holes_exist


class PointTopologyValidator:
    def __init__(self, point_file_path, boundary_file_path=None, line_file_path=None):
        """
        点拓扑规则合理性验证
        :param point_file_path: 点数据shp文件地址
        :param line_file_path: 线数据shp文件地址
        :param boundary_file_path: 边界多边形shp文件地址（可选）
        """
        # 加载点数据
        self.points = gpd.read_file(point_file_path)

        # 如果提供了边界文件，则加载边界多边形数据
        if boundary_file_path:
            self.boundary_polygons = gpd.read_file(boundary_file_path)
        else:
            self.boundary_polygons = None

        # 如果提供了线文件，则加载线数据
        if line_file_path:
            self.lines = gpd.read_file(line_file_path)
        else:
            self.lines = None

    def _check_geometry_validity(self):
        """检查几何有效性"""
        return self.points.is_valid.all()

    def _check_duplicates(self):
        """检查是否存在重复点"""
        unique_points = self.points.drop_duplicates(subset=['geometry'])
        return len(unique_points) != len(self.points)

    def _check_within_boundaries(self):
        """检查所有点是否都在给定的边界内"""
        if self.boundary_polygons is None:
            print("No boundary provided for checking.")
            return True  # 没有提供边界，默认认为合理
        # 使用unary_union合并所有边界多边形
        boundary_union = unary_union(self.boundary_polygons.geometry)
        points_within = self.points.within(boundary_union)
        return points_within.all()

    def _check_proximity_to_lines(self, max_distance=0.0):
        """检查点与线的距离是否在允许范围内（可选）"""
        if self.lines is None:
            print("No lines provided for proximity checking.")
            return True  # 没有提供线，默认认为合理
        distances = self.points.geometry.apply(lambda point: min(self.lines.distance(point)))
        return (distances <= max_distance).all()

    def check_point_topology_validity(self, check_within_boundaries=True, check_proximity_to_lines=True,
                                      max_distance=0.0) -> bool:
        """
        检查矢量点数据的拓扑规则合理性。
        :param check_within_boundaries: 是否检查点是否位于边界内，默认为 True。
        :param check_proximity_to_lines: 是否检查点到线的距离，默认为 True。
        :param max_distance: 允许的最大距离，单位与坐标系统一致，默认为 0.0 表示必须重合。
        :return:
        """
        geometry_valid = self._check_geometry_validity()
        has_duplicates = self._check_duplicates()
        within_boundaries = self._check_within_boundaries() if check_within_boundaries else True
        proximity_to_lines = self._check_proximity_to_lines(max_distance) if check_proximity_to_lines else True
        # 如果几何有效、没有重复点、都在边界内且与线的距离合理，则认为数据合理
        is_valid = geometry_valid and not has_duplicates and within_boundaries and proximity_to_lines
        return is_valid

    def check_specific_point(self, index, check_within_boundaries=True, check_proximity_to_lines=True,
                             max_distance=0.0) -> bool:
        """
        检查某个特定点的拓扑规则合理性。
        :param index: 要检查的点的索引。
        :param check_within_boundaries: 是否检查点是否位于边界内，默认为 True。
        :param check_proximity_to_lines: 是否检查点到线的距离，默认为 True。
        :param max_distance: 允许的最大距离，单位与坐标系统一致，默认为 0.0 表示必须重合。
        :return:
        """
        specific_point = self.points.iloc[[index]]
        geometry_valid = specific_point.is_valid.all()
        has_duplicates = self._check_specific_duplicates(index)
        within_boundaries = self._check_specific_within_boundaries(specific_point) if check_within_boundaries else True
        proximity_to_lines = self._check_specific_proximity_to_lines(specific_point,
                                                                     max_distance) if check_proximity_to_lines else True
        # 如果几何有效、不是重复点、在边界内且与线的距离合理，则认为数据合理
        is_valid = geometry_valid and not has_duplicates and within_boundaries and proximity_to_lines
        return is_valid

    def _check_specific_duplicates(self, index):
        """针对特定点检查是否是重复点"""
        specific_point = self.points.iloc[index].geometry
        other_points = self.points.drop(index).geometry
        duplicates = any(specific_point.equals(other) for other in other_points)
        return duplicates

    def _check_specific_within_boundaries(self, specific_point):
        """针对特定点检查是否位于边界内"""
        if self.boundary_polygons is None:
            print("No boundary provided for checking.")
            return True  # 没有提供边界，默认认为合理
        boundary_union = unary_union(self.boundary_polygons.geometry)
        point_within = specific_point.within(boundary_union)
        return point_within.all()

    def _check_specific_proximity_to_lines(self, specific_point, max_distance=0.0):
        """针对特定点检查与线的距离是否在允许范围内"""
        if self.lines is None:
            print("No lines provided for proximity checking.")
            return True  # 没有提供线，默认认为合理
        distance = min(self.lines.distance(specific_point.geometry))
        return distance <= max_distance
