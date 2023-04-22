import svgwrite
import numpy as np

b_col = "#1F2232"
a_col = "#bd93f9"
c_col = "#8be9fd"

back_radius = 170/2
letter_offset = np.array([-2, -2])
width = 20
hole_radius = 60/2
a_top_height = 0
a_bottom_height = 95/2
c_end_angle = -np.degrees(np.arccos(hole_radius / (hole_radius+width))) + 90
gap_angle=10
c_start_angle = c_end_angle + 90


def arc(center, angle0, angle1, radius, color, width):
    r0 = np.radians(angle0 % 360)
    r1 = np.radians(angle1 % 360)
    if r0 > r1:
        r1 += 2*np.pi
    while r0 < r1:
        rmax = min(r1-r0, np.pi)
        p0 = center + radius * np.array([np.sin(r0), np.cos(r0)])
        p1 = center + radius * np.array([np.sin(r0+rmax), np.cos(r0+rmax)])
        path = "M %f,%f a %f,%f %f 0,0 %f,%f" %(p0[0], p0[1], radius, radius, 0, p1[0]-p0[0], p1[1]-p0[1])
        dwg.add(dwg.path(d=path, fill="none", stroke=color, stroke_width=width))
        r0 += np.pi-0.1

size = np.array([back_radius*2, back_radius*2])
dwg = svgwrite.Drawing('output.svg', (int(size[0]), int(size[1]))) # weird error with size

# Background
dwg.add(dwg.circle(size/2, r=back_radius, fill=b_col))

# Common for A and C
radius = hole_radius + width/2
letter_center = size/2 + letter_offset

# A
dwg.add(dwg.rect(letter_center + (hole_radius, a_top_height), (width, a_bottom_height - a_top_height), fill=a_col))
arc(letter_center, c_end_angle, c_start_angle, radius, a_col, width)

# C
arc(letter_center, c_start_angle+gap_angle, c_end_angle-gap_angle, radius, c_col, width)

# Gaps
arc(letter_center, c_end_angle-gap_angle, c_end_angle, radius, b_col, back_radius)

dwg.save(pretty=True)
