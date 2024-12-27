example_filepath = 'other/inputs/day8_example.txt'
input_filepath = 'other/inputs/day8_input.txt'
is_example = False
part = 2

# Parse the input
def parse_input(file_path):
	data = []
	with open(file_path) as file:
		while line := file.readline():
			# Parse input line by line
			data.append(list(line.replace('\n', '')))

	return data


# Order data
def get_ordered_data(data):
	ordered_data = {}
	for x, row in enumerate(data):
		for y, cell in enumerate(row):
			if cell != '.':
				if cell in ordered_data:
					ordered_data[cell].append([x, y])
				else:
					coords = [[x, y]]
					ordered_data[cell] = coords

	return ordered_data


# Check if a set of coordinates is within the map
def check_coordinates_valid(coords):
	return coords[0] >= 0 and coords[0] <= max_x and coords[1] >= 0 and coords[1] <= max_y


# Get antinode coordinates, recursively if resonance is added
def get_antinode_coordinates(antinodes, coords, distance, direction, is_resonance):
	antinode_coords = [coords[0] + distance[0] * direction, coords[1] + distance[1] * direction]
	if check_coordinates_valid(antinode_coords):
		if str(antinode_coords) not in antinodes:
			antinodes.append(str(antinode_coords))

		if is_resonance:
			antinodes = get_antinode_coordinates(antinodes, antinode_coords, distance, direction, is_resonance)

	return antinodes


# Selecting which input to use
if is_example:
	data = parse_input(example_filepath)
else:
	data = parse_input(input_filepath)

# Save max coordinates for checking coordinate validity
max_x = len(data) - 1
max_y = len(data[0]) - 1

# Order all antennas coordinates according to frequency
frequencies = get_ordered_data(data)

if part == 1:
	# Part 1: Number of unique locations containing an antinode

	# Get all antinodes
	antinodes = []
	checked_coordinates = []
	for frequency, coords in frequencies.items():
		# Loop coords in 2 levels to get all coordinate combinations
		for idx, main_coord in enumerate(coords):
			for idy, secondary_coord in enumerate(coords):
				if idx == idy:
					# No need to check the coordinate against itself
					continue

				if str(main_coord) + str(secondary_coord) in checked_coordinates or str(secondary_coord) + str(main_coord) in checked_coordinates:
					# No need to check the same coordinate pair more than once
					continue

				# Calculate distance between the the coordinate pairs
				x_dist = secondary_coord[0] - main_coord[0]
				y_dist = secondary_coord[1] - main_coord[1]

				# Save antinodes for main and secondary coordinates if valid and not already registered
				antinodes = get_antinode_coordinates(antinodes, main_coord, [x_dist, y_dist], -1, False)
				antinodes = get_antinode_coordinates(antinodes, secondary_coord, [x_dist, y_dist], 1, False)
				
				# Register checked coordinate pairs to be able to determine if a pair has already been checked
				checked_coordinates.append(str(main_coord) + str(secondary_coord))

	print(len(antinodes))

else:
	# Part 2: Number of unique locations containing an antinode, using resonant harmonics

	# Get all antinodes
	antinodes = []
	checked_coordinates = []
	for frequency, coords in frequencies.items():
		# Loop coords in 2 levels to get all coordinate combinations
		for idx, main_coord in enumerate(coords):
			for idy, secondary_coord in enumerate(coords):
				if idx == idy:
					# No need to check the coordinate against itself
					continue

				if str(main_coord) + str(secondary_coord) in checked_coordinates or str(secondary_coord) + str(main_coord) in checked_coordinates:
					# No need to check the same coordinate pair more than once
					continue
				
				# Add antenna coordinates as antinode coordinates
				if str(main_coord) not in antinodes:
					antinodes.append(str(main_coord))

				if (str(secondary_coord)) not in antinodes:
					antinodes.append(str(secondary_coord))

				# Calculate distance between the the coordinate pairs
				x_dist = secondary_coord[0] - main_coord[0]
				y_dist = secondary_coord[1] - main_coord[1]

				# Save antinodes for main and secondary coordinates if valid and not already registered
				antinodes = get_antinode_coordinates(antinodes, main_coord, [x_dist, y_dist], -1, True)
				antinodes = get_antinode_coordinates(antinodes, secondary_coord, [x_dist, y_dist], 1, True)

				# Register checked coordinate pairs to be able to determine if a pair has already been checked
				checked_coordinates.append(str(main_coord) + str(secondary_coord))

	print(len(antinodes))