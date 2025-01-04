from util.planar_division import Division

class DrawableDivision(Division):
    def __init__(self):
        super().__init__()
        self.points_to_mark = []
        self.triangle_to_color = None
