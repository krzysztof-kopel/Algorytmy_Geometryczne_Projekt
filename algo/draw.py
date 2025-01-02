import matplotlib.pyplot as plt
import numpy as np
def draw_polygon():
    plt.figure()
    plt.title("Kliknij, aby dodać wierzchołki wielokąta. Kliknij prawym przyciskiem myszy, aby zakończyć.")
    points = plt.ginput(n=-1, timeout=0)
    points = [list(point) for point in points]

    if len(points) < 3:
        print("Wielokąt musi mieć co najmniej 3 wierzchołki.")
        return np.array([])

    points = np.array(points)

    plt.plot(points[:, 0], points[:, 1], marker='o', color='blue')
    for i in range(len(points)):
        x_values = [points[i][0], points[(i + 1) % len(points)][0]]
        y_values = [points[i][1], points[(i + 1) % len(points)][1]]
        plt.plot(x_values, y_values, color='black')

    plt.fill(points[:, 0], points[:, 1], color='lightblue', alpha=0.3)
    plt.title("Wielokąt")
    plt.show()
    return points

