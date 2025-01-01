from meshpy.triangle import MeshInfo, build
from util import mat_det


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
        for polygon in self.polygons:
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


class Polygon:
    # W teorii moglibyśmy indeksować wielokąty po ich pozycji w tablicy w Division, ale tak chyba będzie lepiej zwrócić
    # jako output użytkownikowi.
    __current_id = 1

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
        triangles = [Triangle(*triangle) for triangle in triangles]
        self.triangles = triangles
        return triangles

    def __repr__(self):
        return f"Polygon(id={self.id}, points={self.points})"

class Triangle:
    def __init__(self, point_a, point_b, point_c):
        # Upewniamy się że punkty są podane w odpowiedniej kolejności, to jest przeciwnie do ruchu wskazówek zegara.
        if mat_det(point_a, point_b, point_c) < 0:
            point_a, point_b = point_b, point_a
        self.a = tuple(point_a)
        self.b = tuple(point_b)
        self.c = tuple(point_c)

    def is_inside(self, point):

        det1 = mat_det(self.a, self.b, point)
        det2 = mat_det(self.b, self.c, point)
        det3 = mat_det(self.c, self.a, point)

        return det1 > 0 and det2 > 0 and det3 > 0
