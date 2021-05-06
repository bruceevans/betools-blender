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
		('32', '32', ''), 
		('64', '64', ''), 
		('128', '128', ''), 
		('256', '256', ''), 
		('512', '512', ''), 
		('1024', '1024', ''), 
		('2048', '2048', ''), 
		('4096', '4096', ''),
		('8192', '8192', '')
	]

"""
MAP_SIZES = {
		'32': ('32', '32', ''), 
		'64': ('64', '64', ''), 
		'128': ('128', '128', ''), 
		'256': ('256', '256', ''), 
		'512': ('512', '512', ''), 
		'1024': ('1024', '1024', ''), 
		'2048': ('2048', '2048', ''), 
		'4096': ('4096', '4096', ''),
		'8192': ('8192', '8192', '')
}
"""

BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MDL_FOLDER = os.path.join(BASE_FOLDER, "resources\mdl")
IMG_FOLDER = os.path.join(BASE_FOLDER, "resources\img")
