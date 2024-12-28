import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from doubly_connected_edge_list import EdgeList, Vertex, Edge

class PlanarDivisionDrawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.vertices = []
        self.edges = []
        self.lines = []
        self.edge_list = EdgeList()
        # Powiązanie wydarzenia kliknięcia przycisku z właściwą funkcją.
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)

    def on_click(self, event):
        if event.button == 1:
            vertex = (event.xdata, event.ydata)
            self.vertices.append(vertex)
            self.ax.plot(event.xdata, event.ydata, "ro")
            self.fig.canvas.draw()

        elif event.button == 3:
            if len(self.vertices) < 2:
                self.ax.set_title("Należy podać dwa wierzchołki w celu utworzenia krawędzi")
                return

            start = self.vertices[-2]
            end = self.vertices[-1]
            self.edges.append((start, end))

            line = Line2D([start[0], end[0]], [start[1], end[1]], color='blue')
            self.lines.append(line)
            self.ax.add_line(line)
            self.fig.canvas.draw()

    def convert_to_edge_list(self):
        vertex_objects = {}
        for x, y in self.vertices:
            vertex = Vertex(x, y)
            self.edge_list.vertices.append(vertex)
            vertex_objects[(x, y)] = vertex

        for start, end in self.edges:
            start_vertex = vertex_objects[start]
            end_vertex = vertex_objects[end]

            edge = Edge(start_vertex)
            twin = Edge(end_vertex)

            edge.twin = twin
            twin.twin = edge
