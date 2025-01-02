class TriangleNode:
    def __init__(self, body):
        self.children = []
        self.body = body

    def __getitem__(self, index):
        return self.body[index]

    def __setitem__(self, index, value):
        self.body[index] = value

    def __repr__(self):
        return str(self.body)

    def __iter__(self):
        return iter(self.body)

    def __contains__(self, item):
        return item in self.body

    def tolist(self):
        return self.body
