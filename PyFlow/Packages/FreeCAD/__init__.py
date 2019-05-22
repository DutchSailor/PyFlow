PACKAGE_NAME = 'FreeCAD'
from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Pins
#from PyFlow.Packages.FreeCAD.Pins.QuatPin import QuatPin

# Function based nodes
from PyFlow.Packages.FreeCAD.Nodes.FreeCAD_Placement import FreeCAD_Placement
from PyFlow.Packages.FreeCAD.Nodes.FreeCAD_Node import FreeCAD_Node


# Factories
from PyFlow.Packages.FreeCAD.Factories.PinInputWidgetFactory import getInputWidget
from PyFlow.Packages.FreeCAD.Factories.UINodeFactory import createUINode
from PyFlow.Packages.FreeCAD.Factories.UIPinFactory import createUIPin


_FOO_LIBS = {
}

_NODES = {
	FreeCAD_Placement.__name__: FreeCAD_Placement,
	FreeCAD_Node.__name__: FreeCAD_Node,
}

_PINS = {
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
