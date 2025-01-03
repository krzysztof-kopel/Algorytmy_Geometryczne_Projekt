import matplotlib.pyplot as plt

from util.planar_division import Division

class DivisionDrawer:
    def __init__(self, division, with_supertriangle):
        self.division = division
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.supertriangle = with_supertriangle
        if not with_supertriangle:
            self.ax.set_xlim(min(point[0] for polygon in division.polygons[1:] for point in polygon.points) - 5,
                             max(point[0] for polygon in division.polygons[1:] for point in polygon.points) + 5)
            self.ax.set_ylim(min(point[1] for polygon in division.polygons[1:] for point in polygon.points) - 5,
                             max(point[1] for polygon in division.polygons[1:] for point in polygon.points) + 5)
        else:
            self.ax.set_xlim(min(point[0] for polygon in division.polygons for point in polygon.points) - 5,
                             max(point[0] for polygon in division.polygons for point in polygon.points) + 5)
            self.ax.set_ylim(min(point[1] for polygon in division.polygons for point in polygon.points) - 5,
                             max(point[1] for polygon in division.polygons for point in polygon.points) + 5)

    def draw(self, with_triangles):
        self.ax.plot(self.division.searched_point[0], self.division.searched_point[1], 'go')
        black_lines = set()
        if self.supertriangle:
            polygons = self.division.polygons
        else:
            polygons = self.division.polygons[1:]
        for polygon in polygons:
            for i in range(len(polygon.points)):
                point = polygon.points[i]
                self.ax.plot(point[0], point[1], 'bo')
                x, y = zip(*[point, polygon.points[(i + 1) % len(polygon.points)]])
                self.ax.plot(x, y, 'k-')
                black_lines.add((point, polygon.points[(i + 1) % len(polygon.points)]))
                black_lines.add((polygon.points[(i + 1) % len(polygon.points)], point))
            if with_triangles:
                for triangle in polygon.triangles:
                    if (triangle.coordinates[0], triangle.coordinates[1]) not in black_lines and (triangle.coordinates[1], triangle.coordinates[0]) not in black_lines:
                        x = (triangle.coordinates[0][0], triangle.coordinates[1][0])
                        y = (triangle.coordinates[0][1], triangle.coordinates[1][1])
                        self.ax.plot(x, y, 'r-')

                    if (triangle.coordinates[1], triangle.coordinates[2]) not in black_lines and (triangle.coordinates[2], triangle.coordinates[1]) not in black_lines:
                        x = (triangle.coordinates[1][0], triangle.coordinates[2][0])
                        y = (triangle.coordinates[1][1], triangle.coordinates[2][1])
                        self.ax.plot(x, y, 'r-')

                    if (triangle.coordinates[2], triangle.coordinates[0]) not in black_lines and (triangle.coordinates[0], triangle.coordinates[2]) not in black_lines:
                        x = (triangle.coordinates[2][0], triangle.coordinates[0][0])
                        y = (triangle.coordinates[2][1], triangle.coordinates[0][1])
                        self.ax.plot(x, y, 'r-')
        self.fig.canvas.draw()
        plt.show()

def draw_polygonal_division(division: Division, with_triangles: bool = False):
    drawer = DivisionDrawer(division, True)
    drawer.draw(with_triangles=with_triangles)

if __name__ == "__main__":
    from file_input import get_division_from_file
    division = get_division_from_file("../input_output_files/test_output_presentation.txt")
    division.triangulate_all()
    drawer = DivisionDrawer(division, True)
    drawer.draw(with_triangles=True)
