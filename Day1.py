import re

example_filepath = 'inputs/day1_example.txt'
input_filepath = 'inputs/day1_input.txt'
is_example = False
part = 2

def parse_input(file_path):
	list_1 = []
	list_2 = []
	with open(file_path) as file:
		while line := file.readline():
			# Get all numbers from line and put in lists
			numbers = re.findall(r'\d+', line)
			list_1.append(int(numbers[0]))
			list_2.append(int(numbers[1]))

	return [list_1, list_2]


# Selecting which input to use
if is_example:
	lists = parse_input(example_filepath)
else:
	lists = parse_input(input_filepath)

if part == 1:
	# Part 1: Calculate total distance between pairs
	# Sort lists
	lists[0].sort()
	lists[1].sort()

	location_sum = 0
	for idx, location in enumerate(lists[0]):
		location_sum += abs(location - lists[1][idx])

	print(location_sum)
else:
	# Part 2: Calculate similiarity between pair lists, multipying each element in the left list with numbers of occurances in the right list
	similarity_score = 0
	for location in lists[0]:
		similarity_score += location * lists[1].count(location)
	
	print(similarity_score)
