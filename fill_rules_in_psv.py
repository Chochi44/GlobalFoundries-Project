def process_fill_layers(input_file, output_file):
    unwanted_patterns = ["MxFILL", "BxFILL", "ExFILL", "xxFILL"]

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if "FILL" in line and not any(pattern in line for pattern in unwanted_patterns):
                parts = line.split("FILL")
                prefix = parts[0]
                suffix = "FILL".join(parts[1:])
                new_prefix = prefix + "FILLKERN"
                new_line = new_prefix + suffix
                outfile.write(new_line)
            else:
                outfile.write(line)


input_file_path = '65LPe_V1830_input.psv'
output_file_path = '65LPe_V1830_output.psv'

process_fill_layers(input_file_path, output_file_path)
