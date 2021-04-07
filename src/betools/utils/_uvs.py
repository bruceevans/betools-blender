
import bpy
import bmesh
import operator
import time

from mathutils import Vector
from collections import defaultdict
from math import pi


## -- UV Transforms -- ##

def uvTranslate(uvLayers):
    """ Translate uv selection
    """

def uvScale(uvLayers):
    """ Scale uv selection
    """

def uvRotate(uvLayers):
    """ Rotate uv selection
    """
## -- Selection Ops -- ##

def storeSelection():
    """ Store uv selection, mode, and pivot
    """

def restoreSelection():
    """ Restore uv selection, mode, and pivot
    """
    
## Multiple items selected

def verts2uvs(bmesh, uvLayers):
    """ Get mesh vertices from uvs
    """

def edges2uvs(bmesh, uvLayers):
    """ Get uvs from selected edges
    """

def faces2uvs(bmesh, uvLayers):
    """ Get uvs from selected faces
    """

def uvs2verts(bmesh, uvLayers):
    """ Get mesh verts from selected uvs
    """

def uvs2edges(bmesh, uvLayers):
    """ Get mesh edges from selected uvs
    """

def uvs2faces(bmesh, uvLayers):
    """ Get mesh faces from selected uvs
    """

## Single item selected

def vert2uv(bmesh, uvLayers):
    """ Get uv from selected vertex
    """

def uv2vert(bmesh, uvLayers):
    """ get vertex from selected uv
    """

def getSelectionBoundingBox():
    """ Get the bounding box of the selected uvs
    """

def getIslandsFromSelection(bmesh=None, uvLayers=None):
    """ Get the uv islands from selection
    """

