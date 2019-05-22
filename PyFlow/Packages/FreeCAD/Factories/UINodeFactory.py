from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.Packages.FreeCAD.UI.UIFreeCAD_Node import UIFreeCAD_Node
from PyFlow.Packages.FreeCAD.Nodes.FreeCAD_Node import FreeCAD_Node

import FreeCAD

def createUINode(raw_instance):
    if isinstance(raw_instance, FreeCAD_Node):
        return UIFreeCAD_Node(raw_instance)
    return UINodeBase(raw_instance)
