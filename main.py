from input_output.file_input import save_division_to_file
from input_output.graphical_input import set_polygonal_division

division = set_polygonal_division()
save_division_to_file(division, "input_output_files/test_output.txt")
