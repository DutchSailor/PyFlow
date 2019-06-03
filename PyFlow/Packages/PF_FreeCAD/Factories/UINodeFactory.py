from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.Packages.PF_FreeCAD.UI.UIFreeCAD_Node import UIFreeCAD_Node
from PyFlow.Packages.PF_FreeCAD.Nodes.FreeCAD_Node import FreeCAD_Node
from PyFlow.Packages.PF_FreeCAD.Nodes.FreeCAD_Placement import FreeCAD_Placement

#import FreeCAD


def createUINode(raw_instance):
    if isinstance(raw_instance, FreeCAD_Node):
        return UIFreeCAD_Node(raw_instance)
    if isinstance(raw_instance, FreeCAD_Placement):
        return UIFreeCAD_Node(raw_instance)

    return UINodeBase(raw_instance)
