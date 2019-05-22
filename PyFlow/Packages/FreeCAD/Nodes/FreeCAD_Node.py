from PyFlow.Core import NodeBase
from PyFlow.Core import PinBase
from PyFlow.Core.Common import *

import FreeCAD,FreeCADGui
from Qt import QtWidgets,QtGui,QtCore


def getPinDomain():
	''' moegliche pins finden'''

	s=FreeCADGui.Selection.getSelection()[0]

	ll={}
	for prop in s.PropertiesList:
		v=getattr(s,prop)
		typ=v.__class__.__name__ 
		if v.__class__.__name__ =='Quantity':
			print v.Value.__class__.__name__
			typ=v.Value.__class__.__name__
		if typ in ['bool','float','unicode']:
			if prop not in ['MapReversed','AttacherType','MapPathParameter']:
				ll[prop]=typ

	return ll



class AAList(QtWidgets.QDialog):
	'''parameter anzeigen zum erzeugen'''

	def __init__(self,node,mode):
		super(AAList, self).__init__()
		self.node=node
		self.mode=mode
		self._listWidget = QtWidgets.QListWidget()

		ll=getPinDomain()
		if len(ll)==0:
			ll=["No poroperty to select"]
		self._listWidget.addItems(ll.keys())
		self.ll=ll

		self._red = QtGui.QBrush(QtCore.Qt.red)
		self._green = QtGui.QBrush(QtCore.Qt.green)

		layout = QtWidgets.QVBoxLayout(self)
		layout.addWidget(self._listWidget)

		self._listWidget.itemDoubleClicked.connect(self._handleDoubleClick)

	def _handleDoubleClick(self, item):
		color = item.background()
#		if color == self._green:
		try:
			typ=self.ll[item.text()]
		except:
			typ="unknown"

		FreeCAD.Console.PrintMessage("----------item:"+item.text()+":"+typ+"\n")

		item.setBackground(self._red if color == self._green else self._green)
		item.setSelected(False)
		FreeCAD.Console.PrintMessage("\n")
		FreeCAD.Console.PrintMessage(str(self.node))
		if self.mode=='out':
			p=self.node.addOutPin(name=item.text()+'_out',typ=typ)
		if self.mode=='in':
			p=self.node.addInPin(name=item.text()+'_in',typ=typ)
		self.p=p
		self.close()


class FreeCAD_Node(NodeBase):
	def __init__(self, name='NN'):
		super(FreeCAD_Node, self).__init__(name)
		self.inExecPin = self.createInputPin('inExec', 'ExecPin', None, self.compute)
		self.fco_label = self.createInputPin('FCO_Label', 'StringPin')
		self.fco_name = self.createInputPin('FCO_Name', 'StringPin')
		self.defaultPin = self.createOutputPin('changed', 'ExecPin')


	def addOutPin(self,name=None,typ=None):

		FreeCAD.Console.PrintMessage("out pin")
		if name != None:
			name = self.getUniqPinName(name)
			FreeCAD.Console.PrintMessage("add outpin :"+name +":"+str(typ)+"\n")
			if typ=='float':
				p = self.createOutputPin(name, 'FloatPin')
			elif typ=='bool':
				p = self.createOutputPin(name, 'BoolPin')
			elif typ=='unicode':
				p = self.createOutputPin(name, 'StringPin')
			else:
				p = self.createOutputPin(name, 'ExecPin')

			p.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic)
			pinAffects(self.inExecPin, p)
			return p
		else:
			d = AAList(self,'out')
			FreeCAD.Console.PrintWarning(str(d))
			d.exec_()
			return d.p


	def addInPin(self,name=None,typ=None):

		try:
			getPinDomain()
		except:
			FreeCAD.Console.PrintError("No properties/no selected object\n")
			return

		if name != None:
			FreeCAD.Console.PrintMessage("add in pin " + str(name)+"!\n")
			name = self.getUniqPinName(name)

			if typ=='float':
				p = self.createInputPin(name, 'FloatPin')
			elif typ=='bool':
				p = self.createInputPin(name, 'BoolPin')
			elif typ=='unicode':
				p = self.createInputPin(name, 'StringPin')
			else:
				p = self.createInputPin(name, 'ExecPin')

			p.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic)
			# effekt rein #+#
			return p
		else:
			d = AAList(self,'in')
			FreeCAD.Console.PrintWarning(str(d))
			d.exec_()
			return d.p


	@staticmethod
	def pinTypeHints():
		return {'inputs': ['ExecPin', 'StringPin'], 'outputs': ['ExecPin']}

	@staticmethod
	def category():
		return 'FlowControl'

	@staticmethod
	def keywords():
		return []

	@staticmethod
	def description():
		return 'Execute output depending on input string'

	def compute(self, *args, **kwargs):
		FreeCAD.Console.PrintMessage("compute " + str(self.getName())+"!A\n")
		FreeCAD.tt=self

		namePinOutputsMap = self.namePinOutputsMap
		FreeCAD.Console.PrintMessage(str(namePinOutputsMap)+"!--!\n")

		if string in namePinOutputsMap:
			FreeCAD.Console.PrintMessage(string+"\n")
			namePinOutputsMap[string].call(*args, **kwargs)
		else:
			FreeCAD.Console.PrintMessage("changed pin\n")
			self.defaultPin.call(*args, **kwargs)

		FreeCAD.Console.PrintMessage("compute " + str(self.getName())+"!-!!-!\n")
