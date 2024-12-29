import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

from doubly_connected_edge_list import EdgeList, Vertex, Edge, Face

class PlanarDivisionDrawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Dodaj wierzchołek lewym przyciskiem myszy.\nDodaj krawędź, klikając dwa wierzchołki prawym przyciskiem myszy.")
        self.vertices = []
        self.edges = []
        self.selected_vertices = []
        self.edge_list = EdgeList()
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        # Powiązanie wydarzenia kliknięcia przycisku z właściwą funkcją.
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)

    def on_click(self, event):
        if event.button == 1:
            self.add_vertex(event.xdata, event.ydata)
        elif event.button == 3:
            self.select_vertex(event.xdata, event.ydata)

    def add_vertex(self, x, y):
        if x is not None and y is not None:
            self.vertices.append((x, y))
            self.ax.add_patch(Circle((x, y), 0.01, color='blue'))
            self.fig.canvas.draw()

    def select_vertex(self, x, y):
        if x is None or y is None:
            return

        radius = 0.02
        selected_vertex = None
        for vx, vy in self.vertices:
            if (vx - x)**2 + (vy - y)**2 <= radius**2:
                selected_vertex = (vx, vy)
                break

        if selected_vertex:
            self.selected_vertices.append(selected_vertex)

            self.ax.add_patch(Circle(selected_vertex, 0.012, color='red', fill=False))
            self.fig.canvas.draw()

            if len(self.selected_vertices) == 2:
                self.add_edge(*self.selected_vertices)
                self.selected_vertices = []

    def add_edge(self, start, end):
        if start != end and (start, end) not in self.edges and (end, start) not in self.edges:
            self.edges.append((start, end))

            line = Line2D([start[0], end[0]], [start[1], end[1]], color='black')
            self.ax.add_line(line)
            self.fig.canvas.draw()

    def convert_to_edge_list(self):
        vertex_map = {}

        i = 0
        for x, y in self.vertices:
            vertex = Vertex(x, y, i)
            i += 1
            self.edge_list.vertices.append(vertex)
            vertex_map[(x, y)] = vertex

        edge_map = {}
        for start, end in self.edges:
            start_vertex = vertex_map[start]
            end_vertex = vertex_map[end]

            edge = Edge(start_vertex, i)
            i += 1
            twin = Edge(end_vertex, i)
            i += 1

            edge.twin = twin
            twin.twin = edge

            start_vertex.half_edge = edge
            end_vertex.half_edge = twin

            self.edge_list.half_edges.extend([edge, twin])
            edge_map[(edge.start, edge.twin.start)] = edge
            edge_map[(twin.start, twin.twin.start)] = twin

        for (vertex_start, vertex_end), edge in edge_map.items():
            next_edges = [e for e in self.edge_list.half_edges if e.start.x == vertex_end.x and e.start.y == vertex_end.y]
            for i in range(len(next_edges)):
                next_edge = next_edges[i]
                if edge.twin == next_edge:
                    continue
                edge.next = edge_map[(next_edge.start, next_edge.twin.start)]
                edge_map[(next_edge.start, next_edge.twin.start)].prev = edge

        visited_edges = set()
        current_face_id = 0
        for edge in self.edge_list.half_edges:
            if edge not in visited_edges:
                face = Face(current_face_id)
                current_face_id += 1
                self.edge_list.faces.append(face)

                current_edge = edge
                face.outer_half_edge = current_edge
                while current_edge and current_edge not in visited_edges:
                    visited_edges.add(current_edge)
                    current_edge.incident_face = face
                    current_edge = current_edge.next

    def run(self):
        plt.show()
        self.convert_to_edge_list()


if __name__ == "__main__":
    drawer = PlanarDivisionDrawer()
    drawer.run()
    print(drawer.edge_list)
