import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from util.drawable_division import DrawableDivision
from util.planar_division import Division


class DivisionDrawer:
    def __init__(self, divisions: DrawableDivision | Division | list[DrawableDivision | Division], with_supertriangle):
        if type(divisions) is DrawableDivision:
            self.divisions = [divisions]
        elif type(divisions) is Division:
            self.divisions = [DrawableDivision(division)]
        else:
            self.divisions = divisions
            for i in range(len(self.divisions)):
                if type(self.divisions[i]) is Division:
                    self.divisions[i] = DrawableDivision(self.divisions[i])
        self.current_division_num = 0
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_aspect('equal')
        self.ax.set_title("Użyj przycisków na dole ekranu, aby oglądać kolejne kroki wizualizacji")
        self.supertriangle = with_supertriangle
        if not with_supertriangle:
            self.ax.set_xlim(min(point[0] for polygon in divisions[0].polygons[1:] for point in polygon.points) - 5,
                             max(point[0] for polygon in divisions[0].polygons[1:] for point in polygon.points) + 5)
            self.ax.set_ylim(min(point[1] for polygon in divisions[0].polygons[1:] for point in polygon.points) - 5,
                             max(point[1] for polygon in divisions[0].polygons[1:] for point in polygon.points) + 5)
        else:
            self.ax.set_xlim(min(point[0] for polygon in divisions[0].polygons for point in polygon.points) - 5,
                             max(point[0] for polygon in divisions[0].polygons for point in polygon.points) + 5)
            self.ax.set_ylim(min(point[1] for polygon in divisions[0].polygons for point in polygon.points) - 5,
                             max(point[1] for polygon in divisions[0].polygons for point in polygon.points) + 5)

        # Buttons for navigation
        self.ax_next = plt.axes((0.6, 0.02, 0.05, 0.05))  # Next button
        self.ax_prev = plt.axes((0.4, 0.02, 0.05, 0.05))  # Previous button

        self.button_next = Button(self.ax_next, '→')
        self.button_prev = Button(self.ax_prev, '←')

        self.button_next.on_clicked(self.next_division)
        self.button_prev.on_clicked(self.prev_division)

        self.later_part_start = None

    def start_config(self):
        self.ax.set_aspect('equal')
        self.ax.set_title("Użyj przycisków na dole ekranu, aby oglądać kolejne kroki wizualizacji")

    def next_division(self, event):
        if self.current_division_num < len(self.divisions) - 1:
            self.current_division_num += 1
            self.draw(self.supertriangle, self.current_division_num)

    def prev_division(self, event):
        if self.current_division_num > 0:
            self.current_division_num -= 1
            self.draw(self.supertriangle, self.current_division_num)

    def draw(self, with_triangles=True, div_number=0):
        current_division = self.divisions[div_number]
        self.ax.clear()
        self.start_config()
        self.ax.plot(current_division.searched_point[0], current_division.searched_point[1], 'go')
        black_lines = set()
        if self.supertriangle:
            polygons = current_division.polygons
        else:
            polygons = current_division.polygons[1:]
        for polygon in polygons:
            for i in range(len(polygon.points)):
                point = polygon.points[i]
                if point == current_division.not_allowed_point:
                    continue
                self.ax.plot(point[0], point[1], 'bo')
                if polygon.points[(i + 1) % len(polygon.points)] == current_division.not_allowed_point:
                    continue
                x, y = zip(*[point, polygon.points[(i + 1) % len(polygon.points)]])
                self.ax.plot(x, y, 'k-')
                black_lines.add((point, polygon.points[(i + 1) % len(polygon.points)]))
                black_lines.add((polygon.points[(i + 1) % len(polygon.points)], point))
            if with_triangles:
                for triangle in polygon.triangles:
                    if (triangle.coordinates[0], triangle.coordinates[1]) not in black_lines and (
                    triangle.coordinates[1], triangle.coordinates[0]) not in black_lines:
                        x = (triangle.coordinates[0][0], triangle.coordinates[1][0])
                        y = (triangle.coordinates[0][1], triangle.coordinates[1][1])
                        self.ax.plot(x, y, 'r-')

                    if (triangle.coordinates[1], triangle.coordinates[2]) not in black_lines and (
                    triangle.coordinates[2], triangle.coordinates[1]) not in black_lines:
                        x = (triangle.coordinates[1][0], triangle.coordinates[2][0])
                        y = (triangle.coordinates[1][1], triangle.coordinates[2][1])
                        self.ax.plot(x, y, 'r-')

                    if (triangle.coordinates[2], triangle.coordinates[0]) not in black_lines and (
                    triangle.coordinates[0], triangle.coordinates[2]) not in black_lines:
                        x = (triangle.coordinates[2][0], triangle.coordinates[0][0])
                        y = (triangle.coordinates[2][1], triangle.coordinates[0][1])
                        self.ax.plot(x, y, 'r-')
        for point in current_division.colored_points:
            self.ax.plot(point[0], point[1], 'ro')
        if current_division.colored_triangle is not None:
            x_coords = [point[0] for point in current_division.colored_triangle.coordinates]
            y_coords = [point[1] for point in current_division.colored_triangle.coordinates]
            self.ax.fill(x_coords, y_coords, 'orange', alpha=0.5)
        self.fig.canvas.draw()
        plt.show()

def draw_polygonal_division(division: Division, with_triangles: bool = False):
    curr_drawer = DivisionDrawer(division, True)
    curr_drawer.draw(with_triangles, 0)

if __name__ == "__main__":
    from file_input import get_division_from_file
    division = get_division_from_file("../input_output_files/test_output_presentation.txt")
    division2 = get_division_from_file("../input_output_files/test_input.txt")
    division.triangulate_all()
    drawer = DivisionDrawer([division2, division], True)
    drawer.draw()
