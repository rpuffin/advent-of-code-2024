example_filepath = 'other/inputs/day6_example.txt'
input_filepath = 'other/inputs/day6_input.txt'
is_example = False
part = 1

# Parse the input
def parse_input(file_path):
	data = []
	with open(file_path) as file:
		while line := file.readline():
			# Parse input line by line
			data.append(list(line.replace('\n', '')))

	return data


# Get new direction when guard is turning
def get_new_guard_direction(direction):
	if direction[0] < 0:
		direction = [0, 1]
	elif direction[0] > 0:
		direction = [0, -1]
	elif direction[1] < 0:
		direction = [-1, 0]
	elif direction[1] > 0:
		direction = [1, 0]

	return direction


# Get the guards path without extra obstacles
def get_path(map, guard_position, guard_direction):
	is_guard_gone = False
	visited_locations = []
	visited_locations.append([guard_position, guard_direction])

	# Path until edge of map is reached
	while is_guard_gone == False:
		new_x = guard_position[0] + guard_direction[0]
		new_y = guard_position[1] + guard_direction[1]

		if new_x < 0 or new_x > max_x or new_y < 0 or new_y > max_y:
			# Edge of the map
			is_guard_gone = True
		elif (map[new_x][new_y]) == '#':
			# Encountered obstacle, change direction
			guard_direction = get_new_guard_direction(guard_direction)
			visited_locations.append([guard_position, guard_direction])
		else:
			# Guard can move
			guard_position = [new_x, new_y]
			visited_locations.append([guard_position, guard_direction])

	return visited_locations


# Check if a placed obstacle causes a loop
def test_obstacle(current_position, current_direction, map, new_obstacle):
	# Save every visited position together with direction, if we come to the same position with the same direction again we have a loop
	visited_string = str(current_position[0]) + ',' + str(current_position[1]) + ',' + str(current_direction[0]) + ',' + str(current_direction[1])
	visited = [visited_string]

	is_loop = False
	is_end = False

	# Place the new obstacle
	map[new_obstacle[0]][new_obstacle[1]] = '#'

	# Path until edge of map is reached or loop is detected
	while is_end == False:
		new_x = current_position[0] + current_direction[0]
		new_y = current_position[1] + current_direction[1]

		if new_x < 0 or new_x > max_x or new_y < 0 or new_y > max_y:
			# Edge of the map
			is_end = True
			break
		elif (map[new_x][new_y]) == '#':
			# Encountered obstacle, change direction
			current_direction = get_new_guard_direction(current_direction)
		else:
			# Guard can move
			current_position = [new_x, new_y]

		visited_string = str(current_position[0]) + ',' + str(current_position[1]) + ',' + str(current_direction[0]) + ',' + str(current_direction[1])
		
		if visited_string in visited:
			# Found a loop
			is_loop = True
			is_end = True

		visited.append(visited_string)

	return is_loop


# Selecting which input to use
if is_example:
	data = parse_input(example_filepath)
else:
	data = parse_input(input_filepath)

# Set up guard
is_guard_gone = False
guard_direction = [-1, 0]

# Find guard location
guard_row = [x for x in data if '^' in x][0]
guard_position = [data.index(guard_row), guard_row.index('^')]

max_x = len(data) - 1
max_y = len(data[0]) - 1
		
if part == 1:
	# Part 1: Count distinct positions visited by the guard
	# Register starting location
	location_string = str(guard_position[0]) + ',' + str(guard_position[1])
	visited_location_list = [location_string]

	while is_guard_gone == False:
		new_x = guard_position[0] + guard_direction[0]
		new_y = guard_position[1] + guard_direction[1]

		if new_x < 0 or new_x > max_x or new_y < 0 or new_y > max_y:
			# Edge of the map, end looping
			is_guard_gone = True
		elif (data[new_x][new_y]) == '#':
			# Encountered obstacle, change direction
			guard_direction = get_new_guard_direction(guard_direction)
		else:
			# Guard can move to new position, save position as visited
			location_string = str(new_x) + ',' + str(new_y)
			if location_string not in visited_location_list:
				visited_location_list.append(location_string)
			guard_position = [new_x, new_y]

	print(len(visited_location_list))
else:
	# Part 2: Find all different positions for an obstacle that would make the guard loop
	# Save guard starting position, an obstacle can't be placed here
	start_position_string = str(guard_position[0]) + ',' + str(guard_position[0])

	# Get the path guard takes without the extra obstacle
	path = get_path(data, guard_position, guard_direction)

	loop_obstacles = []
	loop_testing = []
	walked_path = []
	for location_data in path:
		# Save every visited location, placing an obstacle on these would cause the guard to not get to the current location
		walked_path.append(str(location_data[0][0]) + ',' + str(location_data[0][1]))

		# Obstacle position, placed in front of guard
		obstacle_x = location_data[0][0] + location_data[1][0]
		obstacle_y = location_data[0][1] + location_data[1][1]
		obstacle_string = str(obstacle_x) + ',' + str(obstacle_y)
		is_loop = False

		# Only check path if the obstacle is placed inside the map boundries, 
		# there isn't already an obstacle
		# location not previously visited
		# and location is not starting position for the guard
		check_path = (
			obstacle_x >= 0 and obstacle_x <= max_x
			and obstacle_y >= 0 and obstacle_y <= max_y
			and data[obstacle_x][obstacle_y] != '#'
			and obstacle_string not in walked_path
			and obstacle_string != start_position_string
		)
		
		if check_path:
			# Send in current location, current direction, a copy of the map and the new obstacle position
			is_loop = test_obstacle(location_data[0], location_data[1], [row[:] for row in data], [obstacle_x, obstacle_y])
		
		print(str(location_data) + ' - ' + str(is_loop))
		if is_loop == True:
			if obstacle_string not in loop_obstacles:
				loop_obstacles.append(obstacle_string)

	print(len(loop_obstacles))
