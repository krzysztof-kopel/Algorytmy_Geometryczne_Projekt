from file_input import save_division_to_file
from graphical_input import set_polygonal_division

division = set_polygonal_division()
save_division_to_file(division, "test_output.txt")
