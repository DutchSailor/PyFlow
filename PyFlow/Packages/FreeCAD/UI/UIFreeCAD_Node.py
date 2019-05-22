from PyFlow.UI.Canvas.UINodeBase import UINodeBase

import FreeCAD,FreeCADGui


class UIFreeCAD_Node(UINodeBase):
	def __init__(self, raw_node):
		super(UIFreeCAD_Node, self).__init__(raw_node)
		actionAddOut = self._menu.addAction("add out pin !!")
		actionAddOut.triggered.connect(self.onAddOutPin)
		actionAddIn = self._menu.addAction("add in pin !!")
		actionAddIn.triggered.connect(self.onAddInPin)
		actionAddIn = self._menu.addAction("rename")
		actionAddIn.triggered.connect(self.rename)

		self.resizable = True

	def onAddOutPin(self):
		rawPin = self._rawNode.addOutPin()
		uiPin = self._createUIPinWrapper(rawPin)
		return uiPin

	def onAddInPin(self):
		rawPin = self._rawNode.addInPin()
		uiPin = self._createUIPinWrapper(rawPin)
		return uiPin

	def rename(self):
		n=self._rawNode.getName()
		FreeCAD.Console.PrintMessage(str(n))
		self._rawNode.setName(n+"H")
		FreeCAD.PF.refresh()
		return self
