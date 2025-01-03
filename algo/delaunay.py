from meshpy.triangle import MeshInfo, build


def delaunay(points, polygon=True, diagonals=None):
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
    triangles_as_indices = [[i for i in triangle] for triangle in mesh.elements]
    return triangles_as_indices
