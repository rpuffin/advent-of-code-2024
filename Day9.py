example_filepath = 'other/inputs/day9_example.txt'
input_filepath = 'other/inputs/day9_input.txt'
is_example = False
part = 2

# Parse the input
def parse_input(file_path):
	data = []
	with open(file_path) as file:
		while line := file.readline():
			# Parse input line by line
			data = list(map(int, list(line.replace('\n', ''))))

	return data


# Selecting which input to use
if is_example:
	data = parse_input(example_filepath)
else:
	data = parse_input(input_filepath)

if part == 1:
	# Part 1: Calculate checksum (summed ID multiplied by position) for the filesystem

	# Loop through disk map, setting up block list and saving index of empty blocks
	file_id = 0
	blocks = []
	empty_indices = []
	for idx in range(0, len(data), 2):
		# Add file
		for x in range(data[idx]):
			blocks.append(file_id)

		# Add empty blocks
		if idx + 1 <= len(data) - 1:
			for y in range(data[idx + 1]):
				blocks.append('.')
				empty_indices.append(len(blocks) - 1)

		file_id += 1

	# Loop through block list in reverse to sort blocks
	for idx, block in reversed(list(enumerate(blocks))):
		# Only attempt to move if block is not empty and there are empty blocks to the left of the block
		if block != '.' and len(empty_indices) > 0 and empty_indices[0] < idx:
			blocks[empty_indices[0]] = block
			blocks[idx] = '.'
			del empty_indices[0]
			empty_indices.append(idx)
			empty_indices.sort()

	# Calculate the checksum
	checksum = 0
	for idx, block in enumerate(blocks):
		if block == '.':
			break
		
		checksum += idx * block

	print(checksum)
else:
	# Part 2: Calculate checksum (summed ID multiplied by position) for the filesystem when whole files are moved instead of individual blocks

	# Loop through disk map, setting up block list, saving start index and size of files and empty sections
	file_id = 0
	blocks = []
	files = []
	empty_sections = []
	for idx in range(0, len(data), 2):
		# Add file
		file_start_index = 0
		for x in range(data[idx]):
			blocks.append(file_id)
			if x == 0:
				file_start_index = len(blocks) - 1

		files.append([file_start_index, data[idx]])

		# Add empty blocks
		if idx + 1 <= len(data) - 1 and data[idx + 1] > 0:
			empty_start_index = 0
			for y in range(data[idx + 1]):
				blocks.append('.')
				if y == 0:
					empty_start_index = len(blocks) - 1

			empty_sections.append([empty_start_index, data[idx + 1]])

		file_id += 1

	# Loop through files in reverse to sort
	for file in reversed(files):
		for idx, section in enumerate(empty_sections):
			# Check if section is to the left of file and if section size is big enough
			if section[0] < file[0] and section[1] >= file[1]:
				# File can move to section, save file index and size as an empty section and adjust file index
				new_empty_section = [file[0], file[1]]
				file[0] = section[0]
				
				# Adjust empty section index and size, or remove it if size is 0
				section_size = section[1] - file[1]
				if section_size > 0:
					section[0] += file[1]
					section[1] = section_size
				else:
					del empty_sections[idx]

				# Check if the new empty section can be merged with another section
				empty_section_merged = False
				for section in empty_sections:
					if section[0] + section[1] + 1 == new_empty_section[0]:
						empty_section_merged = True
						section[1] += new_empty_section[1]
						break

				# New empty section could not be merged, add as a separate section
				if empty_section_merged == False:
					empty_sections.append(new_empty_section)

				break

	# Calculate the checksum
	checksum = 0
	for idx, file in enumerate(files):
		for x in range(file[1]):
			checksum += idx * (file[0] + x)

	print(checksum)