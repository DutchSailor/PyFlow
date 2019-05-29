from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


import FreeCAD
import Part

# exmaple shape
def createShape(a):

	pa=FreeCAD.Vector(0,0,0)
	pb=FreeCAD.Vector(a*50,0,0)
	pc=FreeCAD.Vector(0,50,0)
	shape=Part.makePolygon([pa,pb,pc,pa])
	return shape


def updatePart(name,shape):

	FreeCAD.Console.PrintError("update Shape for "+name+"\n")
	a=FreeCAD.ActiveDocument.getObject(name)
	if a== None:
		a=FreeCAD.ActiveDocument.addObject("Part::Feature",name)
	a.Shape=shape


def onBeforeChange_example(self,a,b,*args, **kwargs):
	FreeCAD.Console.PrintError("before:"+str(a)+"\nchange:"+str(b) +"\n")

def onChanged_example(self,a,*args, **kwargs):
	FreeCAD.Console.PrintError(str(a) +" Special 2 FreeCAD"+"\n")
	FreeCAD.Console.PrintError(str(self.owningNode().reshape) +" onChanged"+"\n")
	self.owningNode().reshape()
	FreeCAD.Console.PrintError("  FreeCAD"+"\n")


class FreeCAD_Placement(NodeBase):
	def __init__(self, name):
		super(FreeCAD_Placement, self).__init__(name)
		self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
		self.in2 = self.createInputPin('reshape', 'ExecPin', None, self.reshape)

		self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

		self.pb = self.createInputPin('Placement_Base', 'VectorPin')
		self.pb = self.createInputPin('Rotation_Axis', 'VectorPin')

		self.pb = self.createInputPin('Rotation_Angle', 'FloatPin')
		self.pb.onChanged=onChanged_example
		self.pb.onBeforeChange=onBeforeChange_example

		self.varc = self.createInputPin("arc", 'FloatPin')
		self.vobjname = self.createInputPin("objectname", 'StringPin')
		self.Shape="DAS IST SHAPE"
		FreeCAD.FCP=self


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

		FreeCAD.self=self
		self.outExec.call()

		# change the placement of Box example
		c=FreeCAD.ActiveDocument.getObject('Box')
		c.Placement.Base=10*self.pb.getData()
		c.Placement.Rotation.Angle=100*self.varc.getData()

	def reshape(self, *args, **kwargs):
		FreeCAD.Console.PrintError("!!shapte FreeCAD--aa\n")
		shape=createShape(self.pb.getData())
		updatePart(self.getName(),shape)
		FreeCAD.Console.PrintError("!!shapte FreeCAD\n")

	def foo(self, *args, **kwargs):
		FreeCAD.Console.PrintError("!!foo-example\n")
