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

BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MDL_FOLDER = os.path.join(BASE_FOLDER, "resources\mdl")
IMG_FOLDER = os.path.join(BASE_FOLDER, "resources\img")
