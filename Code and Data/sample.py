import random

input_file_path = 'kddcup.data_10_percent'
output_file_path = 'sample.txt'

with open(input_file_path, 'r') as input_file:
    lines = input_file.readlines()

last_column_values = [line.strip().split(',')[-1] for line in lines]
value_counts = {}
for value in last_column_values:
    value_counts[value] = value_counts.get(value, 0) + 1

total_rows = 5000
sampled_rows = []
for value, count in value_counts.items():
    proportion = count / len(lines)
    sample_size = int(total_rows * proportion)
    
    
    rows_for_value = [line for line in lines if line.strip().endswith(value)]
    sampled_rows.extend(random.sample(rows_for_value, min(sample_size, len(rows_for_value))))

random.shuffle(sampled_rows)

with open(output_file_path, 'w') as output_file:
    output_file.writelines(sampled_rows)

print(f"Sampled {len(sampled_rows)} rows and saved to {output_file_path}.")
