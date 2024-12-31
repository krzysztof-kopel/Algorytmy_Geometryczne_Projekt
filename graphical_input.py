import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from planar_division import Division


class PolygonDrawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.polygons = []
        self.current_polygon = []
        self.current_polygon_start_point = None
        self.all_points = []
        self.searched_point = None
        self.current_click_event = self.fig.canvas.mpl_connect("button_press_event", self.on_click)

        self.ax.set_title("Obecnie rysujesz wielokąt nr 0")
        self.ax.set_aspect('equal')
        self.ax.set_xlim(0, 50)
        self.ax.set_ylim(0, 50)

        button_ax = plt.axes([0.3, 0.015, 0.4, 0.04])
        self.button = Button(button_ax, 'Dodaj poszukiwany punkt')
        self.button.on_clicked(self.on_button_click)

    def on_click(self, event):
        if event.inaxes != self.ax:
            return

        if event.button == 1:
            point = (event.xdata, event.ydata)

            existing_point = self.find_nearby_point(event.xdata, event.ydata)
            if existing_point is not None:
                point = existing_point
            else:
                self.all_points.append(point)

            if self.current_polygon_start_point is None:
                self.current_polygon_start_point = point
                self.current_polygon.append(point)
                self.ax.plot(point[0], point[1], 'go')
                self.ax.set_title(f"Kliknij kolejny punkt, aby dodać go do wielokąta nr {len(self.polygons)}")
            elif self.current_polygon_start_point != point:
                self.current_polygon.append(point)
                if existing_point is None:
                    self.ax.plot(point[0], point[1], 'bo')

                if len(self.current_polygon) > 1:
                    x, y = zip(*self.current_polygon[-2:])
                    self.ax.plot(x, y, 'g-')
            else:
                self.ax.plot(self.current_polygon_start_point[0], self.current_polygon_start_point[1], 'bo')
                if len(self.current_polygon) > 1:
                    x, y = zip(*[self.current_polygon[-1], self.current_polygon[0]])
                    self.ax.plot(x, y, 'r-')
                for i in range(len(self.current_polygon) - 1):
                    x, y = zip(*[self.current_polygon[i], self.current_polygon[i + 1]])
                    self.ax.plot(x, y, 'r-')
                self.polygons.append(self.current_polygon)
                self.current_polygon = []
                self.current_polygon_start_point = None
                self.ax.set_title(f"Kliknij dowolny punkt, aby rozpocząć rysowanie wielokąta nr {len(self.polygons)}")

            self.fig.canvas.draw()

    def on_point_search_click(self, event):
        if event.inaxes != self.ax:
            return
        self.ax.set_title("Można zamknąć to okno.\nPodział planarny i poszukiwany punkt zostały zapisane")
        self.fig.canvas.mpl_disconnect(self.current_click_event)
        self.searched_point = (event.xdata, event.ydata)
        self.ax.plot(event.xdata, event.ydata, 'go')
        self.fig.canvas.draw()

    def find_nearby_point(self, x, y):
        for point in self.all_points:
            if ((point[0] - x) ** 2 + (point[1] - y) ** 2) ** 0.5 < 1:
                return point
        return None

    # noinspection PyUnusedLocal
    def on_button_click(self, event):
        self.button.set_active(False)
        self.fig.canvas.mpl_disconnect(self.current_click_event)
        self.current_click_event = self.fig.canvas.mpl_connect("button_press_event", self.on_point_search_click)
        self.ax.set_title("Wybierz poszukwiany punkt")
        self.fig.canvas.draw()

    def set_division(self):
        plt.show()
        division = Division.division_from_polygons_array(self.polygons)
        division.searched_point = self.searched_point
        return division

if __name__ == "__main__":
    drawer = PolygonDrawer()
    division = drawer.set_division()
    print(division)
