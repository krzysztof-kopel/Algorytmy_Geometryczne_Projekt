from meshpy.triangle import MeshInfo, build
from util import mat_det


class Division:
    def __init__(self):
        self.polygons = []
        # Pierwszy wielokąt reprezentuje wszystko co znajduje się "na zewnątrz" podziału planarnego.
        self.polygons.append(Polygon())

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
        mesh = build(mesh_info)
        triangles = [[mesh.points[i] for i in triangle] for triangle in mesh.elements]
        self.triangles.append(triangles)
        return triangles

class Triangle:
    def __init__(self, point_a, point_b, point_c):
        # Upewniamy się że punkty są podane w odpowiedniej kolejności, to jest przeciwnie do ruchu wskazówek zegara.
        if mat_det(point_a, point_b, point_c) < 0:
            point_a, point_b = point_b, point_a
        self.a = point_a
        self.b = point_b
        self.c = point_c

    def is_inside(self, point):

        det1 = mat_det(self.a, self.b, point)
        det2 = mat_det(self.b, self.c, point)
        det3 = mat_det(self.c, self.a, point)

        return det1 > 0 and det2 > 0 and det3 > 0
