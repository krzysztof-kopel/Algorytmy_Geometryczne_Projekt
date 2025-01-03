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
        for i in range(2):
            if child[i] in self.body:
                if child[(i + 1) % 3] in self.body or child[(i + 2) % 3] in self.body:
                    self.children.add(child)
                break

    def is_inside(self, point):
        def orientation(a, b, c):
            return (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])

        det1 = orientation(self.coordinates[0], self.coordinates[1], point)
        det2 = orientation(self.coordinates[1], self.coordinates[2], point)
        det3 = orientation(self.coordinates[2], self.coordinates[0], point)

        return det1 > 0 and det2 > 0 and det3 > 0