from meshpy.triangle import MeshInfo, build
from util.util import mat_det


class Division:
    def __init__(self):
        self.polygons = []
        # Pierwszy wielokąt reprezentuje super trójkąt.
        self.polygons.append(Polygon())
        # Domyślny poszukiwany punkt.
        self.searched_point = (25, 25)

    def __repr__(self):
        return f"Division(searched_point={self.searched_point} polygons={self.polygons})"

    @staticmethod
    def division_from_polygons_array(polygons: list[list[tuple[int, int]]]) -> 'Division':
        division = Division()
        for polygon_points in polygons:
            next_polygon = Polygon()
            next_polygon.points = polygon_points
            division.polygons.append(next_polygon)
        return division

    def triangulate_all(self):
        self.polygons[0].triangulate()
        for polygon in self.polygons[1:]:
            if len(polygon.points) == 0:
                continue
            polygon.triangulate()

    def set_supertriangle(self):
        points = [point for polygon in self.polygons for point in polygon.points]
        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)
        dif_x = max_x - min_x
        dif_y = max_y - min_y
        p1 = (min_x - dif_x, min_y - dif_y)
        p2 = (max_x + 2 * dif_x, min_y - dif_y)
        p3 = (min_x - dif_x, max_y + 2 * dif_y)
        self.polygons[0].points = [p1, p2, p3]
        
    def get_points_and_diagonals(self):
        all_points = list()
        all_segments = set()

        for polygon in self.polygons[1:]:
            all_points.extend(polygon.points)
            for i in range(len(polygon.points)):
                if not (polygon.points[(i + 1) % len(polygon.points)], polygon.points[i]) in all_segments:
                    all_segments.add((polygon.points[i], polygon.points[(i + 1) % len(polygon.points)]))
        all_points.extend(self.polygons[0].points)
        all_segments.add((self.polygons[0].points[0], self.polygons[0].points[1]))
        all_segments.add((self.polygons[0].points[1], self.polygons[0].points[2]))
        all_segments.add((self.polygons[0].points[2], self.polygons[0].points[0]))
        all_segments = list(all_segments)

        all_unique_points = []
        unique_points_set = set()
        for point in all_points:
            if point in unique_points_set:
                continue
            else:
                unique_points_set.add(point)
                all_unique_points.append(point)
        all_points = all_unique_points

        return all_points, all_segments


class Polygon:
    # W teorii moglibyśmy indeksować wielokąty po ich pozycji w tablicy w Division, ale tak chyba będzie lepiej zwrócić
    # jako output użytkownikowi.
    __current_id = 0

    def __init__(self):
        self.id = Polygon.__current_id
        Polygon.__current_id += 1
        self.points = []
        self.triangles = []

    def triangulate(self):
        n = len(self.points)
        segments = [(i, (i + 1) % n) for i in range(n)]
        mesh_info = MeshInfo()
        mesh_info.set_points(self.points)  # Lista punktów
        mesh_info.set_facets(segments)  # Lista segmentów jako par indeksów

        # Buduj siatkę z ograniczeniami
        mesh = build(mesh_info, quality_meshing=False)
        triangles = [[mesh.points[i] for i in triangle] for triangle in mesh.elements]
        triangles = [Triangle(*triangle, self) for triangle in triangles]
        self.triangles = triangles
        return triangles

    def __repr__(self):
        return f"Polygon(id={self.id}, points={self.points})"

class Triangle:
    def __init__(self, point_a, point_b, point_c, polygon_parent=None):
        # Upewniamy się że punkty są podane w odpowiedniej kolejności, to jest przeciwnie do ruchu wskazówek zegara.
        if mat_det(point_a, point_b, point_c) < 0:
            point_a, point_b = point_b, point_a
        self.a = tuple(point_a)
        self.b = tuple(point_b)
        self.c = tuple(point_c)
        self.polygon = polygon_parent

    def add_polygon(self, polygon):
        self.polygon = polygon

    def is_inside(self, point):

        det1 = mat_det(self.a, self.b, point)
        det2 = mat_det(self.b, self.c, point)
        det3 = mat_det(self.c, self.a, point)

        return det1 > 0 and det2 > 0 and det3 > 0
