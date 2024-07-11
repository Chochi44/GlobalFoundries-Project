import gdspy


def read_fill_layers(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    fill_layers = []
    frame_layer = None
    frame_name = None
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3:
            layer_number = int(parts[0])
            layer_name = parts[2]
            if "FILLKERN" in layer_name:
                fill_layers.append((layer_number, layer_name))
            if "FRAME" in layer_name:
                frame_layer = layer_number
                frame_name = layer_name
    return fill_layers, frame_layer, frame_name


def calculate_frame_size(num_rect, rect_width, rect_height, spacing, frame_thickness, text_height):
    num_per_row = 10
    num_rows = (num_rect + num_per_row - 1) // num_per_row
    frame_width = (num_per_row * (rect_width + spacing)) + spacing + 2 * frame_thickness
    frame_height = (num_rows * (rect_height + spacing + text_height + spacing)) + spacing + frame_thickness + 10
    return frame_width, frame_height


lib = gdspy.GdsLibrary("Project library")
cell = lib.new_cell('Project Cell')

rectangle_width = 20
rectangle_height = 30
spacing = 10
frame_thickness = 5
text_height = 3
num_per_row = 10

fill_layer_info, frame_layer, frame_name = read_fill_layers("65LPe.map")

if frame_layer is None or frame_name is None:
    raise ValueError("Frame layer or frame name not found in the layer map")

num_rectangles = len(fill_layer_info)

frame_width, frame_height = calculate_frame_size(num_rectangles, rectangle_width, rectangle_height, spacing,
                                                 frame_thickness, text_height)

outer_frame_points = [
    (0, 0),
    (frame_width, 0),
    (frame_width, frame_height),
    (0, frame_height),
    (0, 0)
]
inner_frame_points = [
    (frame_thickness, frame_thickness),
    (frame_width - frame_thickness, frame_thickness),
    (frame_width - frame_thickness, frame_height - frame_thickness),
    (frame_thickness, frame_height - frame_thickness),
    (frame_thickness, frame_thickness)
]
outer_frame = gdspy.Polygon(outer_frame_points, layer=frame_layer)
inner_frame = gdspy.Polygon(inner_frame_points, layer=frame_layer)
frame = gdspy.boolean(outer_frame, inner_frame, 'not', layer=frame_layer)
cell.add(frame)

x_start = frame_thickness + spacing
y_start = frame_height - frame_thickness - rectangle_height - spacing - text_height

for i, (layer_number, text) in enumerate(fill_layer_info):
    x_pos = x_start + (i % num_per_row) * (rectangle_width + spacing)
    y_pos = y_start - (i // num_per_row) * (rectangle_height + spacing + text_height + spacing)
    rect = gdspy.Rectangle((x_pos, y_pos), (x_pos + rectangle_width, y_pos + rectangle_height), layer=layer_number)
    cell.add(rect)

    text_x = x_pos + (rectangle_width / 2) - (len(text) * text_height / 4)
    text_y = y_pos - text_height - 2
    text_label = gdspy.Text(text, text_height, (text_x, text_y), layer=layer_number)
    cell.add(text_label)

frame_text = gdspy.Text(frame_name, text_height, (frame_width / 2 - 15, frame_height - frame_thickness - text_height),
                        layer=frame_layer)
cell.add(frame_text)

lib.write_gds('project_layout.gds')

gdspy.LayoutViewer()
