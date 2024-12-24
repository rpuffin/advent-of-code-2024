import re
import math

example_filepath = 'other/inputs/day7_example.txt'
input_filepath = 'other/inputs/day7_input.txt'
is_example = False
part = 2

# Parse the input
def parse_input(file_path):
	data = []
	with open(file_path) as file:
		while line := file.readline():
			# Parse input line by line
			data.append(list(map(int, re.findall(r'\d+', line))))

	return data


# Selecting which input to use
if is_example:
	data = parse_input(example_filepath)
else:
	data = parse_input(input_filepath)

if part == 1:
	# Part 1: Determine which calculation rows are possible when using addition and multiplication, and sum the values
	sum_possible_values = 0
	for row in data:
		target_value = row[:1][0]
		numbers = row[1:]

		summed_value = sum(numbers)
		multiplied_value = math.prod(numbers)

		if target_value == summed_value or target_value == multiplied_value:
			# Sum found, no need to go further
			sum_possible_values += target_value
			continue

		current_values = []
		is_first = True
		for number in numbers:
			if is_first == True:
				# Add value to the combination values list
				current_values.append(number)
				is_first = False
			else:
				# Add and multipy all test values with the current value and add it to a new list
				new_values = []
				for current_value in current_values:
					addition = current_value + number
					new_values.append(addition)
					
					multiplication = current_value * number
					new_values.append(multiplication)
				
				# Set all new values for adding/multiplying next number in order
				current_values = new_values

		if target_value in current_values:
			# The target value is among the test values
			sum_possible_values += target_value
			
	print(sum_possible_values)
		
else:
	# Part 2: Same as part 1, but concatenation is also an operation
	sum_possible_values = 0
	for row in data:
		target_value = row[:1][0]
		numbers = row[1:]

		summed_value = sum(numbers)
		multiplied_value = math.prod(numbers)

		if target_value == summed_value or target_value == multiplied_value:
			# Sum found, no need to go further
			sum_possible_values += target_value
			continue

		current_values = []
		is_first = True
		for number in numbers:
			if is_first == True:
				# Add value to the combination values list
				current_values.append(number)
				is_first = False
			else:
				# Add, multipy and concatenate all test values with the current value and add it to a new list
				new_values = []
				for current_value in current_values:
					addition = current_value + number
					new_values.append(addition)
					
					multiplication = current_value * number
					new_values.append(multiplication)

					concatinated = int(str(current_value) + str(number))
					new_values.append(concatinated)
				
				# Set all new values for adding/multiplying next number in order
				current_values = new_values

		if target_value in current_values:
			# The target value is among the test values
			sum_possible_values += target_value
			
	print(sum_possible_values)