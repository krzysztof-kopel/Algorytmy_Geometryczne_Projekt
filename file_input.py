from planar_division import Division, Polygon

def get_division_from_file(file_path: str) -> Division:
    division = Division()
    with open(file_path) as file:
        division.searched_point = tuple(map(lambda x: float(x), file.readline().strip()[1:-1].split(', ')))
        number_of_polygons = int(file.readline())
        for _ in range(number_of_polygons):
            polygon = Polygon()
            current_line_array = list(map(lambda x: x[1:-1], file.readline().strip().split('; ')))
            for point in current_line_array:
                x, y = map(lambda x: float(x), point.split(', '))
                polygon.points.append((x, y))
            division.polygons.append(polygon)
    return division

def save_division_to_file(division: Division, file_path: str) -> None:
    with open(file_path, "w") as file:
        file.write(f"({division.searched_point[0]}, {division.searched_point[1]})\n")
        file.write(f"{len(division.polygons) - 1}\n")
        for polygon in division.polygons[1:]:
            file.write("; ".join([f"({point[0]}, {point[1]})" for point in polygon.points]) + "\n")

if __name__ == "__main__":
    division = get_division_from_file("test_input.txt")
    print(division)
