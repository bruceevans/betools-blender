#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

"""Constant values used across Be Tools modules"""

import os
from mathutils import Vector


BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MDL_FOLDER = os.path.join(BASE_FOLDER, r"resources\mdl")
IMG_FOLDER = os.path.join(BASE_FOLDER, r"resources\img")

CHECKER_MAPS = [
	('CHECKER', 'Checker', 'Standard checker map'),
	('GRAVITY', 'Gravity', 'Gravity map'),
	('SIMPLE', 'Simple Checker', 'Simple checker map')
]

MAP_SIZES = [
		('512', '512', ''),
		('1024', '1024', ''),
		('2048', '2048', ''),
		('4096', '4096', ''),
		('8192', '8192', '')
]

MATERIAL_SIZES = {
	"512": "512",
	"1024": "1K",
	"2048": "2K",
	"4096": "4K",
	"8192": "8K",
}

MIRROR_MODES = {
    "X" : (True, False, False),
    "Y" : (False, True, False),
    "Z" : (False, False, True)
}

PADDING_MULTIPLIERS = {
	'LEFTTOP': Vector((1, -1)),
    'CENTERTOP': Vector((0, -1)),
    'RIGHTTOP': Vector((-1, -1)),
    'LEFTCENTER': Vector((1, 0)),
    'CENTER': Vector((0, 0)),
    'RIGHTCENTER': Vector((-1, 0)),
    'LEFTBOTTOM': Vector((1, 1)),
    'CENTERBOTTOM': Vector((0, 1)),
    'RIGHTBOTTOM': Vector((-1, 1))
}

SELECTION_MODES = {
    (True, False, False)    : "VERTEX",
    (False, True, False)    : "EDGE",
    (False, False, True)    : "FACE"
}

# scale factors
UNITS = {
    "Centimeters" : 0.01,
    "Meters" : 1.00,
	"Inches" : 0.0254,
    "Feet" : 0.3048
}

TRIM_FIT_MODES = [
	('VERTICAL', 'Vertical', 'Scale the UV Shell vertically, ignore horizontal scale'),
	('HORIZONTAL', 'Horizontal', 'Scale the UV Shell horizontally, ignore vertical scale'),
	('VERTICAL_FIT', 'Vertical Fit', 'Scale the entire UV shell for best vertical fit'),
	('HORIZONTAL_FIT', 'Horizontal Fit', 'Scale the entire UV shell for best horizontal fit'),
	('BESTFIT', 'Best Fit', 'Scale the shell to the closest sized trim slot and fill the entire space')
]
