class EdgeList:
    def __init__(self):
        self.faces = []
        self.half_edges = []
        self.vertices = []

    def __repr__(self):
        vertices = "\n".join([repr(v) for v in self.vertices])
        edges = "\n".join([repr(e) for e in self.half_edges])
        faces = "\n".join([repr(f) for f in self.faces])
        return f"EdgeList:\n\nVertices:\n{vertices}\n\nEdges:\n{edges}\n\nFaces:\n{faces}"


class Vertex:
    def __init__(self, coord_x, coord_y):
        self.x = coord_x
        self.y = coord_y
        self.half_edge = None

    def __repr__(self):
        return f"Vertex(x={self.x}, y={self.y}, half_edge={id(self.half_edge)})"


class Face:
    def __init__(self, identifier):
        self.id = identifier
        self.outer_half_edge: Edge = None
        self.inner_half_edges = []

    def __repr__(self):
        outer_id = id(self.outer_half_edge) if self.outer_half_edge else None
        inner_ids = [id(edge) for edge in self.inner_half_edges]
        return f"Face(outer_half_edge={outer_id}, inner_half_edges={inner_ids})"


class Edge:
    def __init__(self, start: Vertex):
        self.start: Vertex = start
        self.twin: Edge = None
        self.incident_face = None
        self.next = None
        self.prev = None

    def __repr__(self):
        twin_id = id(self.twin) if self.twin else None
        next_id = id(self.next) if self.next else None
        prev_id = id(self.prev) if self.prev else None
        face_id = id(self.incident_face) if self.incident_face else None
        return (f"Edge(start=({self.start.x}, {self.start.y}), "
                f"twin={twin_id}, next={next_id}, prev={prev_id}, face={face_id})")
