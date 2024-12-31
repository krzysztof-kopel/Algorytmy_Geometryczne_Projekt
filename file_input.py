from planar_division import Division, Polygon

def get_division_from_file(file_path: str) -> Division:
    division = Division()
    with open(file_path) as file:
        division.searched_point = tuple(map(lambda x: int(x), file.readline().strip()[1:-1].split(', ')))
        number_of_polygons = int(file.readline())
        for _ in range(number_of_polygons):
            polygon = Polygon()
            current_line_array = list(map(lambda x: x[1:-1], file.readline().strip().split('; ')))
            for point in current_line_array:
                x, y = map(lambda x: int(x), point.split(', '))
                polygon.points.append((x, y))
            division.polygons.append(polygon)
    return division

if __name__ == "__main__":
    division = get_division_from_file("test_input.txt")
    print(division)
