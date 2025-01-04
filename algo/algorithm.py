from copy import deepcopy
from algo.delaunay import *
from input_output.division_drawer import DivisionDrawer
from util.planar_division import Division, Polygon, Triangle
from util.drawable_division import DrawableDivision


def triangulation_as_graph(triangles_as_indices, n):
    graph = [set() for _ in range(n)]
    for p1, p2, p3 in triangles_as_indices:
        if p1 < n and p2 < n:
            graph[p1].add(p2)
            graph[p2].add(p1)
        if p1 < n and p3 < n:
            graph[p1].add(p3)
            graph[p3].add(p1)
        if p2 < n and p3 < n:
            graph[p2].add(p3)
            graph[p3].add(p2)
    return graph


def independent_vertices(triangles_as_indices, n) -> list:
    graph = triangulation_as_graph(triangles_as_indices, n)
    visited = [False for _ in range(n)]
    independent = []

    queue = []
    for p in triangles_as_indices[0]:
        if p < n:
            queue.append(p)
            break
    if len(queue) == 0:
        return []
    while queue:
        index = queue.pop()
        visited[index] = True
        dependant = False
        for v in graph[index]:
            if v in independent:
                dependant = True
            if not visited[v] and v not in queue:
                queue.append(v)
        if not dependant:
            independent.append(index)
    return independent


def triangles_to_polygon(central_point, triangles: list) -> list:
    starting_triangle = triangles[0]
    triangles_cp = deepcopy(triangles)
    triangles_cp.pop(0)
    polygon = []
    index = starting_triangle.tolist().index(central_point)
    polygon.append(starting_triangle[(index + 1) % 3])
    polygon.append(starting_triangle[(index + 2) % 3])
    while len(triangles_cp) > 1:
        found = False
        for i in range(len(triangles_cp)):
            index = triangles_cp[i].tolist().index(central_point)
            if triangles_cp[i][(index + 1) % 3] == polygon[-1]:
                polygon.append(triangles_cp[i][(index + 2) % 3])
                triangles_cp.pop(i)
                found = True
                break
        if not found: break
    return polygon


def translate_triangulation_indices(triangles: list, triangles_points: list, original_points: list):
    translated_triangles = []
    translation = dict()
    for index in range(len(triangles_points)):
        translation[index] = original_points.index(triangles_points[index])
    for triangle in triangles:
        x, y, z = triangle
        translated_triangles.append([translation[x], translation[y], translation[z]])
    return translated_triangles


def hierarchy(division: Division, drawable: bool=False, searched_point: tuple[int, int]=None) -> tuple[Triangle, DivisionDrawer | None]:
    divisions_to_draw = []
    if len(division.polygons[0].points) == 0:
        division.set_supertriangle()
    if drawable:
        divisions_to_draw.append(deepcopy(division))
    division.triangulate_all()
    if drawable:
        divisions_to_draw.append(deepcopy(division))
    triangles_to_parents = dict()
    for polygon in division.polygons[1:]:
        for triangle in polygon.triangles:
            triangles_to_parents[tuple(sorted([triangle.coordinates[0], triangle.coordinates[1], triangle.coordinates[2]]))] = polygon

    all_points, all_segments = division.get_points_and_diagonals()

    temp_triangles = delaunay(all_points, polygon=False, diagonals=all_segments)
    triangles = [Triangle(all_points, body_indices=triangle) for triangle in temp_triangles]
    for triangle in triangles:
        triangle_as_point_tuple = tuple(sorted((triangle.coordinates[0], triangle.coordinates[1], triangle.coordinates[2])))
        if triangle_as_point_tuple in triangles_to_parents:
            triangle.parent = triangles_to_parents[triangle_as_point_tuple]
        else:
            triangle.parent = division.polygons[0]

    if drawable:
        polygon_triangles = [i.to_polygon() for i in triangles]
        division = Division()
        division.searched_point = searched_point
        division.polygons = polygon_triangles
        divisions_to_draw.append(deepcopy(division))
    removed_points = dict()

    while len(triangles) > 1:
        to_remove = independent_vertices(triangles, len(all_points) - 3)
        # Wierzchołki usuwamy "od lewej do prawej" (wg współrzędnej x), aby osoba prezentująca wiedziała,
        # który wierzchołek będzie usunięty jako następny.
        to_remove.sort(key=lambda x: all_points[x][0])
        if drawable:
            division = DrawableDivision(Division())
            division.searched_point = searched_point
            division.colored_points = [all_points[i] for i in to_remove]
            division.polygons = [i.to_polygon() for i in triangles]
            divisions_to_draw.append(deepcopy(division))
        for i in to_remove:
            removed_points[i] = []
            for triangle in triangles:
                if i in triangle:
                    removed_points[i].append(triangle)

        if drawable:
            to_remove_used = 1
        for point in to_remove:
            if drawable:
                division = DrawableDivision(Division())
                division.searched_point = searched_point
                division.not_allowed_point = all_points[point]
                division.colored_points = [all_points[i] for i in to_remove[to_remove_used:]]
                division.polygons = [i.to_polygon() for i in triangles]
                divisions_to_draw.append(deepcopy(division))
            polygon_indices = triangles_to_polygon(point, removed_points[point])
            polygon = []
            for index in polygon_indices:
                polygon.append(all_points[index])

            temp_new_triangles = delaunay(polygon)
            temp_new_triangles = translate_triangulation_indices(temp_new_triangles, polygon, all_points)
            new_triangles = [Triangle(all_points, body_indices=triangle) for triangle in temp_new_triangles]
            for triangle in removed_points[point]:
                for n_triangle in new_triangles:
                    n_triangle.add_potential_child(triangle)
                if triangle in triangles:
                    triangles.remove(triangle)

            triangles.extend(new_triangles)
            if drawable:
                division = DrawableDivision(Division())
                division.searched_point = searched_point
                division.colored_points = [all_points[i] for i in to_remove[to_remove_used:]]
                to_remove_used += 1
                division.polygons = [i.to_polygon() for i in triangles]
                divisions_to_draw.append(deepcopy(division))
    drawer = None
    if drawable:
        drawer = DivisionDrawer(divisions_to_draw, True)
    return triangles[0], drawer

def find_smallest_triangle_in_hierarchy(header: Triangle, point) -> 'Polygon':
    while len(header.children) > 0:
        for c in header.children:
            if c.is_inside(point):
                header = c
                break
    return header.parent
