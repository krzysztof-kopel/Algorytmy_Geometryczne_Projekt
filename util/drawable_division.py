from util.planar_division import Division

class DrawableDivision(Division):
    def __init__(self, division: Division):
        super().__init__()
        self.copy_data_from_division(division)

    def copy_data_from_division(self, division: Division):
        self.polygons = division.polygons
        self.searched_point = division.searched_point
