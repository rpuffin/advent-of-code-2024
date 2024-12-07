import regex

example_filepath = 'inputs/day4_example.txt'
input_filepath = 'inputs/day4_input.txt'
is_example = False
part = 2

def parse_input(file_path):
	data = []
	with open(file_path) as file:
		while line := file.readline():
			# Parse input line by line
			data.append(list(line.replace('\n', '')))
	
	return data


def get_match_count(matrix):
	word_count = 0
	for row in matrix:
		row_list = ''.join(row)
		matches = regex.findall('XMAS|SAMX', str(row_list), overlapped=True)
		word_count += len(matches)
	
	return word_count


# Selecting which input to use
if is_example:
	data = parse_input(example_filepath)
else:
	data = parse_input(input_filepath)

if part == 1:
	# Part 1: Count occurances of XMAS in all directions 
	# Create lists for rows, columns, both diagonals
	max_col = len(data[0])
	max_row = len(data)
	cols = [[] for _ in range(max_col)]
	rows = [[] for _ in range(max_row)]
	fdiag = [[] for _ in range(max_row + max_col - 1)]
	bdiag = [[] for _ in range(len(fdiag))]
	min_bdiag = -max_row + 1

	for x in range(max_col):
		for y in range(max_row):
			cols[x].append(data[y][x])
			rows[y].append(data[y][x])
			fdiag[x + y].append(data[y][x])
			bdiag[x - y - min_bdiag].append(data[y][x])

	# Sum matches for rows, columns, both diagonals
	word_count = get_match_count(cols)
	word_count += get_match_count(rows)
	word_count += get_match_count(fdiag)
	word_count += get_match_count(bdiag)

	print(word_count)
else:
	# Part 2: Count occurances of MAS shaped like an X
	a_coordinates = []

	# Get all coordinates for the letter A
	for x,row in enumerate(data):
		for y,col in enumerate(row):
			# Edge coordinates cannot be valid
			if col == 'A' and x != 0 and x != len(data[0]) - 1 and y != 0 and y != len(data) - 1:
				a_coordinates.append([x,y])

	word_count = 0
	# Check diagonal coordinates of each A coordinate
	for coords in a_coordinates:
		output_data = {}
		upper_left = data[coords[0] - 1][coords[1] - 1]
		upper_right = data[coords[0] - 1][coords[1] + 1]
		lower_left = data[coords[0] + 1][coords[1] - 1]
		lower_right = data[coords[0] + 1][coords[1] + 1]
		letters = [upper_left, upper_right, lower_left, lower_right]
		
		if upper_left != lower_right and upper_right != lower_left and letters.count('M') == 2 and letters.count('S') == 2:
			word_count += 1

	print(word_count)

