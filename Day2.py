import re

example_filepath = 'other/inputs/day2_example2.txt'
input_filepath = 'other/inputs/day2_input.txt'
is_example = False
part = 1

def parse_input(file_path):
	data = []
	with open(file_path) as file:
		while line := file.readline():
			# Get all numbers from line and put in input list
			numbers = re.findall(r'\d+', line)
			data.append(list(map(int, numbers)))

	return data


# Checking levels for part 2
def check_levels(report):
	direction = 0
	unsafe_indices = []

	for x in range(len(report) - 1):
		distance = report[x + 1] - report[x]

		if direction == 0:
			if distance > 0:
				direction = 1
			elif distance < 0:
				direction = -1

		if distance == 0 or abs(distance) > 3:
			unsafe_indices.append(x)

		if (direction > 0 and distance < 0) or (direction < 0 and distance > 0):
			unsafe_indices.append(x)

	return unsafe_indices


# Checking levels for part 2
def check_levels2(report):
	positive_distances = 0
	negative_distances = 0
	unsafe_positive_indices = []
	unsafe_negative_indices = []

	for x in range(len(report) - 1):
		distance = report[x + 1] - report[x]

		# distance = 0 and distance > 3 are unsafe for both
		if distance == 0 or abs(distance) > 3:
			unsafe_positive_indices.append(x)
			unsafe_negative_indices.append(x)

		if distance < 0:
			negative_distances += 1
			unsafe_positive_indices.append(x)

		if distance > 0:
			positive_distances += 1
			unsafe_negative_indices.append(x)

	# Return 
	if positive_distances > negative_distances:
		return unsafe_positive_indices
	else:
		return unsafe_negative_indices


# Selecting which input to use
if is_example:
	reports = parse_input(example_filepath)
else:
	reports = parse_input(input_filepath)

if part == 1:
	# Part 1: Count all safe reports
	num_safe_reports = 0
	for report in reports:
		if len(check_levels(report)) == 0:
			num_safe_reports += 1
	
	print(num_safe_reports)
else:
	# Part 2: Count all safe reports, allowing for one bad level in each report
	num_safe_reports = 0
	for report in reports:
		unsafe_level_removed = False
		unsafe_indices = check_levels2(report)

		if len(unsafe_indices) > 0:
			for index in unsafe_indices:
				# Try removing unsafe index and unsafe index + 1 to see if it makes the report safe
				new_unsafe_indices = check_levels2(report[:index] + report[(index + 1):])
				report1_safe = len(new_unsafe_indices) == 0

				new_unsafe_indices2 = check_levels2(report[:(index + 1)] + report[(index + 2):])
				report2_safe = len(new_unsafe_indices2) == 0

				if unsafe_level_removed == False and (report1_safe == True or report2_safe == True):
					unsafe_level_removed = True
					if report1_safe == True:
						unsafe_indices = new_unsafe_indices
					if report2_safe == True:
						unsafe_indices = new_unsafe_indices2

		if len(unsafe_indices) == 0:
			num_safe_reports += 1

	
	print(num_safe_reports)

