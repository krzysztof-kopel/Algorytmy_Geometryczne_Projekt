from util.planar_division import Division

class DrawableDivision(Division):
    def __init__(self):
        super().__init__()
        self.points_to_mark = []
        self.triangle_to_color = None

    def copy_data_from_division(self, division: Division):
        self.polygons = division.polygons
        self.searched_point = division.searched_point
