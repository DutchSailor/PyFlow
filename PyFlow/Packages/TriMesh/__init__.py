PACKAGE_NAME = 'TriMesh'

from PyFlow.Core.Interfaces import IPackage

# Pins
from PyFlow.Packages.TriMesh.Pins.MeshPin import MeshPin

# Function based nodes
from PyFlow.Packages.TriMesh.FunctionLibraries.triMeshLib import triMeshLib
from PyFlow.Packages.TriMesh.Nodes.displayMesh import displayMesh

_FOO_LIBS = {
    triMeshLib.__name__: triMeshLib(PACKAGE_NAME),
}

_NODES = {
    displayMesh.__name__:displayMesh
}

_PINS = {
    MeshPin.__name__: MeshPin,

}


class TriMesh(IPackage):
    def __init__(self):
        super(TriMesh, self).__init__()

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

    @staticmethod
    def GetNodeClasses():
        return _NODES

    @staticmethod
    def GetPinClasses():
        return _PINS
