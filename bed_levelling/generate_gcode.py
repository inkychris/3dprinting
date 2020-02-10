import argparse

parser = argparse.ArgumentParser(description='Generate bed-levelling gcode for cartesian printer')
parser.add_argument('--x-max', type=int, default=200, help='Maximum X axis coordinate (mm)')
parser.add_argument('--y-max', type=int, default=200, help='Maximum Y axis coordinate (mm)')
parser.add_argument('--inset', type=int, default=50, help='Distance in from edge of build-plate to stop at (mm)')
parser.add_argument('--wait-time', type=int, default=10, help='Time to pause at each point (seconds)')
parser.add_argument('--bed-temp', type=int, default=55, help='Bed temperature (Celsius)')
parser.add_argument('--iterations', type=int, default=5, help='Number of times to visit each coordinate')
parser.add_argument('-o', '--output-file', type=str, help='File to write gcode to')

args = parser.parse_args()


class Gcode:
    def __init__(self, *args):
        self.lines = [*args]

    def __lshift__(self, other):
        self.lines.append(other)
        return self

    def __str__(self):
        return '\n'.join(self.lines)

    def move(self, x=None, y=None, z=None):
        result = 'G1'
        if x: result += f' X{x}'
        if y: result += f' Y{y}'
        if z: result += f' Z{z}'
        self.lines.append(result)
        return self

    def home_x(self):
        self.lines.append('G28 X0')
        self.lines.append('G1 X0')
        return self

    def home_y(self):
        self.lines.append('G28 Y0')
        self.lines.append('G1 Y0')
        return self

    def home_z(self):
        self.lines.append('G28 Z0')
        self.lines.append('G1 Z0')
        return self

    def message(self, string):
        self.lines.append(f'M117 {string}')
        return self

    def sleep(self, seconds):
        self.lines.append(f'G4 S{seconds}')
        return self


gcode = Gcode('; Bed Levelling' ,'G90')

if args.bed_temp > 0:
    gcode << f'M140 S{args.bed_temp}'

gcode.home_x()
gcode.home_y()
gcode.home_z()

if args.bed_temp > 0:
    gcode << f'M190 S{args.bed_temp}'

coordinates = [
    (args.inset, args.inset),
    (args.x_max - args.inset, args.y_max - args.inset),
    (args.inset, args.y_max - args.inset),
    (args.x_max - args.inset, args.inset),
]

for iteration in range(1, args.iterations + 1):
    for i, coords in enumerate(coordinates):
        gcode.move(z=1)
        gcode.move(x=coords[0], y=coords[1])
        gcode.home_z()
        gcode.message(f'Loop {iteration}/{args.iterations} [{i + 1}/{len(coordinates)}]')
        gcode.sleep(args.wait_time)

gcode.message('Bed-levelling Complete!')
gcode.move(z=1)
gcode.home_x()
gcode.home_y()

file = args.output_file or f'bed-levelling-{args.inset}.gcode'
with open(file, 'w') as outfile:
    outfile.write(str(gcode))
print(f"gcode written to '{file}'")
