PACKAGE_NAME = 'FreeCAD'
from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Pins
from PyFlow.Packages.FreeCAD.Pins.QuatPin import QuatPin
from PyFlow.Packages.FreeCAD.Pins.FloatVector3Pin import FloatVector3Pin
from PyFlow.Packages.FreeCAD.Pins.FloatVector4Pin import FloatVector4Pin
from PyFlow.Packages.FreeCAD.Pins.Matrix33Pin import Matrix33Pin
from PyFlow.Packages.FreeCAD.Pins.Matrix44Pin import Matrix44Pin

# Function based nodes
from PyFlow.Packages.FreeCAD.FunctionLibraries.Matrix33 import Matrix33
from PyFlow.Packages.FreeCAD.FunctionLibraries.Matrix44 import Matrix44
from PyFlow.Packages.FreeCAD.FunctionLibraries.QuatLib import QuatLib
from PyFlow.Packages.FreeCAD.FunctionLibraries.Vector3 import Vector3
from PyFlow.Packages.FreeCAD.FunctionLibraries.Vector4 import Vector4

from PyFlow.Packages.FreeCAD.Nodes.FreeCAD_Placement import FreeCAD_Placement


# Factories
from PyFlow.Packages.FreeCAD.Factories.PinInputWidgetFactory import getInputWidget
from PyFlow.Packages.FreeCAD.Factories.UINodeFactory import createUINode
from PyFlow.Packages.FreeCAD.Factories.UIPinFactory import createUIPin


_FOO_LIBS = {
#    Matrix33.__name__: Matrix33(PACKAGE_NAME),
#    Matrix44.__name__: Matrix44(PACKAGE_NAME),
#    QuatLib.__name__: QuatLib(PACKAGE_NAME),
#    Vector3.__name__: Vector3(PACKAGE_NAME),
#    Vector4.__name__: Vector4(PACKAGE_NAME)
}

_NODES = {
	FreeCAD_Placement.__name__: FreeCAD_Placement,
}

_PINS = {
#    FloatVector3Pin.__name__: FloatVector3Pin,
#    FloatVector4Pin.__name__: FloatVector4Pin,
#    Matrix33Pin.__name__: Matrix33Pin,
#    Matrix44Pin.__name__: Matrix44Pin,
#    QuatPin.__name__: QuatPin
}


_TOOLS = OrderedDict()


class FreeCAD(IPackage):
    def __init__(self):
        super(FreeCAD, self).__init__()

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

    @staticmethod
    def GetNodeClasses():
        return _NODES

    @staticmethod
    def GetPinClasses():
        return _PINS

    @staticmethod
    def GetToolClasses():
        return _TOOLS

    @staticmethod
    def UIPinsFactory():
        return createUIPin

    @staticmethod
    def UINodesFactory():
        return createUINode

    @staticmethod
    def PinsInputWidgetFactory():
        return getInputWidget
