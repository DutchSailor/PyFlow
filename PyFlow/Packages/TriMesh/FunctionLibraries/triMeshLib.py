from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *

from pyrr import Vector3
import numpy

import trimesh

class triMeshLib(FunctionLibraryBase):
    '''doc string for Matrix33'''
    def __init__(self,packageName):
        super(triMeshLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('MeshPin', None), meta={'Category': 'input', 'Keywords': ['create', 'obj']})
    def readObj(path=('StringPin', r"C:\Users\pedro\Google Drive\RECURSOS\3D\MODELS\OTHER\Love.obj")):
        return trimesh.load_mesh(path)

    @staticmethod
    @IMPLEMENT_NODE(returns=('MeshPin',None), meta={'Category': 'transform', 'Keywords': ['create', 'obj']})
    def transformMesh(mesh=('MeshPin', None),transform=("FloatVector3Pin",Vector3())):
        mesh.apply_translation(numpy.asanyarray(transform.xyz.tolist(), dtype=numpy.float64).reshape(3))
        return mesh