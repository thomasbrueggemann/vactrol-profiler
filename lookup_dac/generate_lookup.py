import datetime
import sys

if len(sys.argv) < 4:
	print("Usage: python generate_lookup.py <input_file_path> <max_resistence> <output_folder>")
	sys.exit(1)

result = []

with open(sys.argv[1], 'r') as file:
	profile_result = file.read()

	for entry in profile_result.split(';'):
		parts = entry.split(',')
		
		if len(parts) != 2:
			continue

		voltage = int(parts[0])
		resistence = int(parts[1])

		result.append({'voltage': voltage, 'resistence': resistence})

result.sort(key=lambda x: x['resistence'], reverse=True)

linear_values = []

max_val = int(sys.argv[2])
include_inverse = False

for step in range(0, 255):
	desired = max_val / 256 * step
	closest_entry = min(result, key=lambda x: abs(x['resistence'] - desired))

	desired_inverse = max_val - desired
	closest_entry_inverse = min(result, key=lambda x: abs(x['resistence'] - desired_inverse))

	linear_values.append({'main': closest_entry, 'inverse': closest_entry_inverse})

# Write result to a CSV file
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

cpp_code = ""
last_i = None
unq_values = 0

for step, entry in enumerate(linear_values):
	i = entry['main']['voltage']
	inverse_i = entry['inverse']['voltage']

	if last_i is not None and i == last_i:
		continue

	#print(entry['main']['resistence'])

	if include_inverse:
		cpp_code += f"    {{ {i}, {inverse_i} }},\n"
	else:
		cpp_code += f"    {{ {i} }},\n"

	last_i = i
	unq_values += 1


header_cpp_code = f"#ifndef LOOKUP_HPP\n#define LOOKUP_HPP\n\nint lookup[{unq_values}][{int(include_inverse) + 1}] = "
header_cpp_code += "{\n"

cpp_code += "};\n\n#endif // LOOKUP_HPP\n"

final_cpp_code = header_cpp_code + cpp_code

with open(f'{sys.argv[3]}/lookup_{max_val}.hpp', 'w') as cpp_file:
	cpp_file.write(final_cpp_code)