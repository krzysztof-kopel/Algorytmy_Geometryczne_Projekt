from copy import deepcopy
from TriangleNode import TriangleNode
from delaunay import *


def triangulation_as_graph(triangles_as_indices, n):
    graph = [set() for i in range(n)]
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


def independent_veritices(triangles_as_indices, n) -> list:
    graph = triangulation_as_graph(triangles_as_indices, n)
    visited = [False for i in range(n)]
    independent = []
    queue = [n - 1]
    while queue:
        index = queue.pop()
        visited[index] = True
        dependant = False
        for v in graph[index]:
            if v in independent:
                dependant = True
            if not visited[v]:
                queue.append(v)
        if not dependant:
            independent.append(v)
    return independent


def triangles_to_polygon(central_point, triangles: list, points: list) -> list:
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


def hierarchy(points) -> TriangleNode:
    super_triangle = supertriangle(points)
    removed_points = dict()
    all_points = points.tolist() + super_triangle
    print(all_points)
    temp_triangles = delaunay(all_points, polygon=False,
                              diagonals=[[super_triangle[0], super_triangle[1]], [super_triangle[1], super_triangle[2]],
                                         [super_triangle[2], super_triangle[0]]])
    triangles = [TriangleNode(triangle) for triangle in temp_triangles]
    while True:
        print("start")
        print("triangles", triangles)
        to_remove = independent_veritices(triangles, len(points))
        to_remove.sort(reverse=True)
        print("to remove", to_remove)
        for i in to_remove:
            removed_points[i] = []
            for triangle in triangles:
                if i in triangle:
                    removed_points[i].append(triangle)
        print("---")
        for point in removed_points:
            polygon_indices = triangles_to_polygon(point, removed_points[point], all_points)
            print("poligon indices", polygon_indices)
            if len(polygon_indices) < 3:
                print(point, removed_points[point], triangles)
            polygon = []
            for index in polygon_indices:
                polygon.append(all_points[index])
            temp_new_triangles = delaunay(polygon)
            temp_new_triangles = translate_triangulation_indices(temp_new_triangles, polygon, all_points)
            new_triangles = [TriangleNode(triangle) for triangle in temp_new_triangles]
            for triangle in removed_points[point]:
                if triangle in triangles:
                    triangles.remove(triangle)
            triangles.extend(new_triangles)

