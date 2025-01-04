from copy import deepcopy

from algo.algorithm import hierarchy, find_smallest_triangle_in_hierarchy
from input_output.file_input import get_division_from_file
from util.drawable_division import DrawableDivision

division = get_division_from_file("input_output_files/test_output_presentation.txt")
division_copy = deepcopy(division)
topTriangleNode, drawer = hierarchy(division, True, division.searched_point)
resultant_polygon, drawer = find_smallest_triangle_in_hierarchy(topTriangleNode, division.searched_point, drawer)

drawable_first_division = DrawableDivision(division_copy)
drawable_first_division.colored_triangle = resultant_polygon
drawer.divisions.append(drawable_first_division)
print(f"Poszukiwany punkt znajduje się w wielokącie nr {resultant_polygon.id}")
drawer.draw()
