import datetime
import sys

result = []

with open('profile_result.txt', 'r') as file:
	profile_result = file.read()

	for entry in profile_result.split(';'):
		parts = entry.split(',')
		
		if len(parts) != 3:
			continue

		pwm = int(parts[0])
		digipot = int(parts[1])
		resistence = int(parts[2])

		result.append({'pwm': pwm, 'digipot': digipot, 'resistence': resistence})

result.sort(key=lambda x: x['resistence'], reverse=True)

linear_values = []
if len(sys.argv) < 2:
	print("Usage: python generate_lookup.py <max_resistence>")
	sys.exit(1)

max_val = int(sys.argv[1])
include_inverse = False

for step in range(0, 255):
	desired = max_val / 256 * step
	closest_entry = min(result, key=lambda x: abs(x['resistence'] - desired))

	desired_inverse = max_val - desired
	closest_entry_inverse = min(result, key=lambda x: abs(x['resistence'] - desired_inverse))

	linear_values.append({'main': closest_entry, 'inverse': closest_entry_inverse})

# Write result to a CSV file
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

cpp_code = f"#ifndef LOOKUP_HPP\n#define LOOKUP_HPP\n\nint lookup[256][{int(include_inverse) + 2}] = "
cpp_code += "{\n"

for step, entry in enumerate(linear_values):
	i = entry['main']['pwm']
	j = entry['main']['digipot']
	inverse_i = entry['inverse']['pwm']
	inverse_j = entry['inverse']['digipot']

	print(entry)

	if include_inverse:
		cpp_code += f"    {{ {i}, {j}, {inverse_i}, {inverse_j} }},\n"
	else:
		cpp_code += f"    {{ {i}, {j} }},\n"

cpp_code += "};\n\n#endif // LOOKUP_HPP\n"

with open(f'lookup_{max_val}.hpp', 'w') as cpp_file:
	cpp_file.write(cpp_code)