from algo.algorithm import hierarchy, find_smallest_triangle_in_hierarchy
from input_output.graphical_input import set_polygonal_division

division = set_polygonal_division()
topTriangleNode, drawer = hierarchy(division, True, division.searched_point)
drawer.draw()
resultant_polygon = find_smallest_triangle_in_hierarchy(topTriangleNode, division.searched_point)
print(resultant_polygon.id)
