M140 S{material_bed_temperature}
G28 X
G1 X0
G28 Y
G28 Z
M190 S{material_bed_temperature}
M109 S{material_print_temperature_layer_0}
G90 ;Absolute positioning
G1 Z1 F6000 ;Move the head up slightly
G92 E0 ;Reset extruder
G1 F200 E5 ;Extrude filament onto buildplate
G92 E0 ;Reset extruder
G1 X5 Y5 F6000;Move head away from blob
G1 X10 Y10 F6000;Move head away from blob
