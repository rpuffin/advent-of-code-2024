import re

example_filepath = 'other/inputs/day3_example.txt'
input_filepath = 'other/inputs/day3_input.txt'
is_example = False
part = 2

def parse_input(file_path):
	data = []
	with open(file_path) as file:
		while line := file.readline():
			# Get all matches from line and put in input list
			if part == 1:
				matches = re.findall(r'(?:mul\(\d{1,3},\d{1,3}\))', line)
			else:
				matches = re.findall(r'(?:mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\))', line)
			data += matches
	
	return data


# Selecting which input to use
if is_example:
	instructions = parse_input(example_filepath)
else:
	instructions = parse_input(input_filepath)

if part == 1:
	# Part 1: Do all correct muliplication instructions mul() and sum them
	total_sum = 0
	for instruction in instructions:
		matches = re.findall(r'\d+', instruction)
		total_sum += int(matches[0]) * int(matches[1])

	print(total_sum)
else:
	# Part 2: Do all correct muliplication instructions mul() and sum them, taking into account do() and don't() instructions
	total_sum = 0
	enabled = True
	for instruction in instructions:
		if instruction == 'do()':
			enabled = True
		elif instruction == 'don\'t()':
			enabled = False
		else:
			if (enabled == True):
				matches = re.findall(r'\d+', instruction)
				total_sum += int(matches[0]) * int(matches[1])

	print(total_sum)