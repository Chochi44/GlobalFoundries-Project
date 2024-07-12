import re

# function to replace 'xxFILL' with 'FILLKERNxx'
def replace_fill(match):
    word = match.group(0)
    prefix = word[:-4]
    # while excluding specific patterns
    if word.upper() in ["MXFILL", "BXFILL", "EXFILL", "XXFILL"]:
        return word
    return f"FILLKERN{prefix}"


file_path = '65LPe_V1830_input.psv'
with open(file_path, 'r') as file:
    lines = file.readlines()

# Process each line
modified_lines = []
for line in lines:
    # Use regex to find patterns ending with 'FILL' and apply the replacement function, case-insensitive
    modified_line = re.sub(r'\b([a-zA-Z]{2}FILL)\b', replace_fill, line, flags=re.IGNORECASE)
    modified_lines.append(modified_line)

new_file_path = '65LPe_V1830_output.psv'
with open(new_file_path, 'w') as new_file:
    new_file.writelines(modified_lines)

print(f"Modified file saved as: {new_file_path}")
