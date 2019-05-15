from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *

import FreeCAD

class FreeCAD_Placement(NodeBase):
	def __init__(self, name):
		super(FreeCAD_Placement, self).__init__(name)
		self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

		self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

		self.vx = self.createInputPin("x", 'FloatPin')
		self.vy = self.createInputPin("y", 'FloatPin')
		self.vz = self.createInputPin("z", 'FloatPin')
		self.varc = self.createInputPin("arc", 'FloatPin')
		self.vobjname = self.createInputPin("objectname", 'StringPin')

	@staticmethod
	def pinTypeHints():
#		return {'inputs': ['AnyPin'], 'outputs': ['AnyPin']}
		return {'inputs': ['FloatPin','FloatPin','FloatPin','FloatPin','StringPin'], 'outputs': []}


	@staticmethod
	def category():
		return 'DefaultLib'

	@staticmethod
	def keywords():
		return ['freecad']

	@staticmethod
	def description():
		return "change Placement of the FreeCAD object"

	def compute(self, *args, **kwargs):
		FreeCAD.Console.PrintError("OUT FreeCAD"+"\n")
		FreeCAD.self=self
		a=self.vx.getData()
		FreeCAD.Console.PrintError("--- FreeCAD"+"\n")
		FreeCAD.Console.PrintError("x "+str(self.vx.getData())+ "\n")
		FreeCAD.Console.PrintError("--- FreeCAD"+"\n")
		FreeCAD.Console.PrintError("y "+str(self.vy.getData())+ "\n")
		FreeCAD.Console.PrintError(str(self.vz.getData())+ "\n")
		FreeCAD.Console.PrintError(str(self.varc.getData())+ "\n")

		self.outExec.call()

		c=FreeCAD.ActiveDocument.getObject(self.vobjname.getData())
		c.Placement.Base.x=10*self.vx.getData()
		c.Placement.Base.y=10*self.vy.getData()
		c.Placement.Base.z=10*self.vz.getData()
		c.Placement.Rotation.Angle=10*self.varc.getData()
