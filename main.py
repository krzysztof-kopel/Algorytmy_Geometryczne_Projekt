from copy import deepcopy

from algorytm.algorithm import hierarchy, find_smallest_triangle_in_hierarchy
from input_output.graphical_input import set_polygonal_division
from util.drawable_division import DrawableDivision

division = set_polygonal_division()
division_copy = deepcopy(division)
topTriangleNode, drawer = hierarchy(division, True, division.searched_point)
resultant_polygon, drawer = find_smallest_triangle_in_hierarchy(topTriangleNode, division.searched_point, drawer)

drawable_first_division = DrawableDivision(division_copy)
drawable_first_division.colored_triangle = resultant_polygon
drawer.divisions.append(drawable_first_division)
print(f"Poszukiwany punkt znajduje się w wielokącie nr {resultant_polygon.id}")
drawer.draw()
