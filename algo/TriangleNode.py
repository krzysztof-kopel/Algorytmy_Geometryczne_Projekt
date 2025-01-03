from util.util import mat_det

class TriangleNode:
    def __init__(self, body, points, polygon=None):
        self.children = set()
        self.body = body
        self.points = points
        self.coordinates = [self.points[i] for i in self.body]
        self.parent = polygon

    def __getitem__(self, index):
        return self.body[index]

    def __setitem__(self, index, value):
        self.body[index] = value

    def __repr__(self):
        return str(self.body) + ":" + str(self.children)

    def __str__(self):
        return str(self.body)

    def __iter__(self):
        return iter(self.body)

    def __contains__(self, item):
        return item in self.body

    def tolist(self):
        return self.body

    def add_potential_child(self, child):
        self.children.add(child)

    def is_inside(self, point):

        det1 = mat_det(self.coordinates[0], self.coordinates[1], point)
        det2 = mat_det(self.coordinates[1], self.coordinates[2], point)
        det3 = mat_det(self.coordinates[2], self.coordinates[0], point)

        return det1 > 0 and det2 > 0 and det3 > 0