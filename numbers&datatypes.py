def find_layer_info(file_path, layer_name):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        columns = line.split()
        if len(columns) >= 3 and columns[2] == layer_name:
            return columns[0], columns[1]

    return None


# Example usage
layer_name = input("Enter the layer name: ")
result = find_layer_info(r"65LPe.map", layer_name)

if result:
    print(f"Layer: {result[0]}, Data type: {result[1]}")
else:
    print("Layer name not found.")
