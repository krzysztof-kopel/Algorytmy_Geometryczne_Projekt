from meshpy.triangle import MeshInfo, build


def delaunay(points, polygon=True, diagonals=None, as_indices=True):
    def cleanup(mesh, points, as_indices):
        triangles = [[mesh.points[i] for i in triangle] for triangle in mesh.elements]
        triangles_as_indices = [[i for i in triangle] for triangle in mesh.elements]
        n = len(triangles)
        indices_to_remove = []
        for i in range(n):
            for point in triangles[i]:
                if point not in points:
                    indices_to_remove.append(i)
        indices_to_remove.sort(reverse=True)
        for i in indices_to_remove:
            triangles.pop(i)
            triangles_as_indices.pop(i)
        if as_indices:
            return triangles_as_indices
        else:
            return triangles

    n = len(points)
    segments = []
    if polygon:
        segments = [(i, (i + 1) % n) for i in range(n)]
    if diagonals:
        diagonals_as_indices = [(points.index(p1), points.index(p2)) for p1, p2 in diagonals]
        segments.extend(diagonals_as_indices)
    mesh_info = MeshInfo()
    if polygon or diagonals:
        mesh_info.set_points(points)  # Lista punktów
    mesh_info.set_facets(segments)  # Lista segmentów jako par indeksów

    # Buduj siatkę z ograniczeniami
    mesh = build(mesh_info, allow_boundary_steiner=False, quality_meshing=False, allow_volume_steiner=False)

    triangles = cleanup(mesh, points, as_indices)
    return triangles

def supertriangle(points):
    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_y = max(point[1] for point in points)
    dif_x = max_x - min_x
    dif_y = max_y - min_y
    p1 = [min_x -  dif_x, min_y - dif_y]
    p2 = [max_x + 2 * dif_x, min_y - dif_y]
    p3 = [min_x - dif_x, max_y + 2 * dif_y]
    return [p1, p2, p3]
