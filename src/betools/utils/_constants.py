#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import os
import sys

SELECTION_MODES = {
    (True, False, False)    : "VERTEX",
    (False, True, False)    : "EDGE",
    (False, False, True)    : "FACE"
}

MIRROR_MODES = {
    "X" : (True, False, False),
    "Y" : (False, True, False),
    "Z" : (False, False, True)
}

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

CHECKER_MAPS = [
	('CHECKER', 'Checker', 'Standard checker map'),
	('GRAVITY', 'Gravity', 'Gravity map'),
	('SIMPLE', 'Simple Checker', 'Simple checker map')
]

BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MDL_FOLDER = os.path.join(BASE_FOLDER, "resources\mdl")
IMG_FOLDER = os.path.join(BASE_FOLDER, "resources\img")
