import cadquery as cq

dims = {
    'shield': {
        'width': 16.79,
        'height': 14.98,
        'depth': 33.02,
        'thickness': 0.38,
        'y_offset': 7.75
    },
    'pins': {
        'spacing': 2.03,
        'radius': 0.445,
        'per_row': 6,
        'starting_points': [
            (1.015, 18.42),
            (2.03, 20.96)
        ],
        'length': 3.20
    },
    'center_taps': {
        'spacing': 2.54,
        'radius': 0.515,
        'count': 4,
        'x_offset': 3.55,
        'y_offset': 23.50,
        'length': 3.20
    }
}

shield = cq.Workplane('XZ') \
    .box(
    dims['shield']['width'],
    dims['shield']['height'],
    dims['shield']['depth'],
    (True, False, True)) \
    .shell(-dims['shield']['thickness']) \
    .fillet(dims['shield']['thickness'] / 2) \
    .translate((0, dims['shield']['y_offset'], 0))

# create center point lists for first two rows of pins
pin_centers = []
pin_spacing = dims['pins']['spacing']

# create one side of pin centers
for point in dims['pins']['starting_points']:
    # unpack point tuple
    start_x, y = point
    for i in range(dims['pins']['per_row'] // 2):
        pin_centers.append((start_x + pin_spacing * i, y))

# create other side of pin centers
pin_centers_mirror = [(-point[0], point[1]) for point in pin_centers]
pin_centers.extend(pin_centers_mirror)

# push center points, draw circles, then extrude them
pins = cq.Workplane('front') \
    .pushPoints(pin_centers) \
    .circle(dims['pins']['radius']) \
    .extrude(-dims['pins']['length'])

# create center point lists for last row of pins
ct_centers = []
ct_spacing = dims['center_taps']['spacing']

# create one side of ct centers
for i in range(dims['center_taps']['count'] // 2):
    ct_centers.append((dims['center_taps']['x_offset'] + i* ct_spacing, dims['center_taps']['y_offset']))
    
# create other side of ct centers
ct_centers_mirror = [(-point[0], point[1]) for point in ct_centers]
ct_centers.extend(ct_centers_mirror)

# push center points, draw circles, then extrude them
center_taps = cq.Workplane('front') \
    .pushPoints(ct_centers) \
    .circle(dims['center_taps']['radius']) \
    .extrude(-dims['center_taps']['length'])

show_object(shield, name='shield')
show_object(pins, name='pins')
show_object(center_taps, name='center_taps')