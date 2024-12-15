import re

example_filepath = 'other/inputs/day5_example.txt'
input_filepath = 'other/inputs/day5_input.txt'
is_example = False
part = 2

# Parse the input
def parse_input(file_path):
	rules = []
	pages = []
	with open(file_path) as file:
		while line := file.readline():
			# Parse input line by line
			line = line.replace('\n', '')
			matches =  re.findall(r'\d+', line)
			if len(matches) > 0:
				if '|' in line:
					rules.append(list(map(int, matches)))
				elif ',' in line:
					pages.append(list(map(int, matches)))

	
	return [rules, pages]


# Sort page order rules into a dictionary
# Enabling looking up each page and see pages coming before and after
def sort_rule_orders(rules):
	rule_orders = {}
	for rule in rules:
		page1 = int(rule[0])
		page2 = int(rule[1])
		# Add page before
		if page1 not in rule_orders:
			new_rule1 = [[],[page2]]
			rule_orders[page1] = new_rule1
		else:
			rule_orders[page1][1].append(page2)

		# Add page after
		if page2 not in rule_orders:
			new_rule2 = [[page1],[]]
			rule_orders[page2] = new_rule2
		else:
			rule_orders[page2][0].append(page1)
	
	return rule_orders


# Check page orders validity and sort them based on validity
def validate_page_orders(pages, rule_orders):
	valid_orders = []
	invalid_orders = []
	for page_order in pages:
		is_valid = check_page_order_valid(page_order, rule_orders)
		if is_valid:
			valid_orders.append(page_order)
		else:
			invalid_orders.append(page_order)

	return [valid_orders, invalid_orders]


# Checks if page order is correct
def check_page_order_valid(page_order, rule_orders):
	is_valid = True
	for idx in range(len(page_order)):
		page = page_order[idx]
		before = page_order[:idx]
		after = page_order[idx+1:]

		if page in rule_orders:
			if any(x in before for x in rule_orders[page][1]) or any(x in after for x in rule_orders[page][0]):
				# This page is not in the correct order
				is_valid = False
				break

	return is_valid


# Sort an invalid page order
def sort_invalid_order(page_order, rule_orders):
	is_invalid = True
	while is_invalid == True:
		# Some pages can require multiple moves, keep sorting until the order is completely correct
		for idx in range(len(page_order)):
			page = page_order[idx]
			before = page_order[:idx]
			after = page_order[idx+1:]

			if page in rule_orders:
				if any(x in before for x in rule_orders[page][1]):
					# This page should be printed earlier
					page_order[idx], page_order[idx-1] = page_order[idx-1], page_order[idx]

				elif any(x in after for x in rule_orders[page][0]):
					# This page should be printed later
					page_order[idx], page_order[idx+1] = page_order[idx+1], page_order[idx]

		is_invalid = not check_page_order_valid(page_order, rule_orders)

	return page_order


# Selecting which input to use
if is_example:
	data = parse_input(example_filepath)
else:
	data = parse_input(input_filepath)

rules = data[0]
pages = data[1]

rule_orders = sort_rule_orders(rules)
validated_page_orders = validate_page_orders(pages, rule_orders)
	
if part == 1:
	# Part 1: Sum middle page numbers of all correct page orders
	validated_sum = 0
	for page_order in validated_page_orders[0]:
		validated_sum += page_order[int((len(page_order) - 1)/2)]

	print(validated_sum)
else:
	# Part 2: Sort all incorrect page numbers orders and sum all middle pages
	validated_sum = 0
	for page_order in validated_page_orders[1]:
		sorted_order = sort_invalid_order(page_order, rule_orders)
		validated_sum += sorted_order[int((len(page_order) - 1)/2)]

	print(validated_sum)
		