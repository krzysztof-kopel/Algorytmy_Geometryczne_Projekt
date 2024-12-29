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
    def __init__(self, coord_x, coord_y, identifier):
        self.id = identifier
        self.x = coord_x
        self.y = coord_y
        self.half_edge = None

    def __repr__(self):
        return f"Vertex(id={self.id}, x={self.x}, y={self.y}, half_edge={self.half_edge.id})"


class Face:
    def __init__(self, identifier):
        self.id = identifier
        self.outer_half_edge: Edge = None
        self.inner_half_edges = []

    def __repr__(self):
        return f"Face(id={self.id}, outer_half_edge={self.outer_half_edge.id}, inner_half_edges={[e.id for e in self.inner_half_edges]})"


class Edge:
    def __init__(self, start: Vertex, identifier):
        self.id = identifier
        self.start: Vertex = start
        self.twin: Edge = None
        self.incident_face = None
        self.next = None
        self.prev = None

    def __repr__(self):
        return (f"Edge(id={self.id} start=({self.start.x}, {self.start.y}), end=({self.twin.start.x}, {self.twin.start.y}),"
                f"twin={self.twin.id}, next={self.next.id}, prev={self.prev.id}, face={self.incident_face.id})")
