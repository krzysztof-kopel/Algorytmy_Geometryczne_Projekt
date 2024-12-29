class EdgeList:
    def __init__(self):
        self.faces = []
        self.half_edges = []
        self.vertices = []

class Vertex:
    def __init__(self, coord_x, coord_y):
        self.x = coord_x
        self.y = coord_y
        self.half_edge = None

class Face:
    def __init__(self, identifier):
        self.id = identifier
        self.outer_half_edge: Edge = None
        self.inner_half_edges = []

class Edge:
    def __init__(self, start: Vertex):
        self.start: Vertex = start
        self.twin: Edge = None
        self.incident_face = None
        self.next = None
        self.prev = None
