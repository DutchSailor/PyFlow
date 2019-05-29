PACKAGE_NAME = 'PF_FreeCAD'
from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Pins
from PyFlow.Packages.PF_FreeCAD.Pins.VectorPin import VectorPin

# Function based nodes
from PyFlow.Packages.PF_FreeCAD.Nodes.FreeCAD_Placement import FreeCAD_Placement
from PyFlow.Packages.PF_FreeCAD.Nodes.FreeCAD_Node import FreeCAD_Node
from PyFlow.Packages.PF_FreeCAD.Nodes.FreeCAD_Vector import FreeCAD_Vector
from PyFlow.Packages.PF_FreeCAD.Nodes.FreeCAD_Console import FreeCAD_Console


# Factories
from PyFlow.Packages.PF_FreeCAD.Factories.PinInputWidgetFactory import getInputWidget
from PyFlow.Packages.PF_FreeCAD.Factories.UINodeFactory import createUINode
from PyFlow.Packages.PF_FreeCAD.Factories.UIPinFactory import createUIPin


_FOO_LIBS = {
}

_NODES = {
	FreeCAD_Placement.__name__: FreeCAD_Placement,
	FreeCAD_Node.__name__: FreeCAD_Node,
	FreeCAD_Vector.__name__: FreeCAD_Vector,
	FreeCAD_Console.__name__: FreeCAD_Console,
}

_PINS = {
    VectorPin.__name__: VectorPin,

}


_TOOLS = OrderedDict()


class PF_FreeCAD(IPackage):
    def __init__(self):
        super(PF_FreeCAD, self).__init__()

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
