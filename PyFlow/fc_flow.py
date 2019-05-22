# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- freecad wrapper for pyflow
#--
#-- microelly 2019 
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


import FreeCAD,FreeCADGui

# the dummy methods for the workbench
def test_BB():
	FreeCAD.Console.PrintMessage("\ntest_B\n")

def test_AA():
	FreeCAD.Console.PrintMessage("\ntest_A\n")



import FreeCAD,FreeCADGui
from PySide import QtCore
from PySide import QtGui

import os
import sys
import subprocess
import json
from time import clock
import pkgutil
import uuid


# Property dialog dockwindow inside FreeCAd methods

from PyFlow.Packages.PyflowBase.Tools.PropertiesTool import PropertiesTool

def onRequestFillPropertiesXX(propertiesFillDelegate):
	from PyFlow.Packages.PyflowBase.Tools.PropertiesTool import PropertiesTool
	try:
		toolInstance=FreeCAD.toolInstance
	except:
		toolInstance=PropertiesTool()
		toolInstance.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		FreeCAD.toolInstance=toolInstance

	toolInstance.show()
	toolInstance.clear()
	toolInstance.assignPropertiesWidget(propertiesFillDelegate)
	

def onRequestClearPropertiesXX():
	toolInstance.clear()

def createPropTool(arg=None):
	from PyFlow.Packages.PyflowBase.Tools.PropertiesTool import PropertiesTool
	try:
		toolInstance=FreeCAD.toolInstance
		toolInstance.show()
	except:
		toolInstance=PropertiesTool()
		FreeCAD.toolInstance=toolInstance
		toolInstance.setAttribute(QtCore.Qt.WA_DeleteOnClose)
	toolInstance.show()



# a hack to run the laucher widget subelements sinside freecad
# 

class myPyFlow(object):
	'''the FreeCAD wrapper for the PyFlow.App.instance
	'''

	def __init__(self,inside=True):

		FreeCAD.Console.PrintMessage("\nUsed QtGui .."+str(QtGui)+"\n")



		if inside: # create a widget with tteh canvas and some pseudo menues
			q=FreeCADGui.getMainWindow()

			bb=QtGui.QDockWidget()
			#

			q.addDockWidget(QtCore.Qt.TopDockWidgetArea, bb)

			bb.setWindowTitle("Node editor Version: Dock Window - 0.4")
			bb.setMinimumSize(600, 500)

			bb.centralWidget = QtGui.QWidget()
			bb.setWidget(bb.centralWidget)

			layout = QtGui.QVBoxLayout()
			bb.layout = layout
			bb.centralWidget.setLayout(layout)
			buttons=QtGui.QWidget()
			bl = QtGui.QHBoxLayout()
			buttons.setLayout(bl)

			pB = QtGui.QPushButton(QtGui.QIcon('icons:freecad.svg'), 'load File A')
			bl.addWidget(pB)
			pB.clicked.connect(self.loadA)

			pB = QtGui.QPushButton(QtGui.QIcon('icons:freecad.svg'), 'refresh')
			bl.addWidget(pB)
			pB.clicked.connect(self.refresh)
			
			pB = QtGui.QPushButton(QtGui.QIcon('icons:freecad.svg'), 'save')
			bl.addWidget(pB)
			pB.clicked.connect(self.save)

			pB = QtGui.QPushButton(QtGui.QIcon('icons:freecad.svg'), 'load dialog')
			bl.addWidget(pB)
			pB.clicked.connect(self.load)
			pB = QtGui.QPushButton(QtGui.QIcon('icons:freecad.svg'), 'Properties Tool')
			bl.addWidget(pB)
			pB.clicked.connect(createPropTool)

			layout.addWidget(buttons)

			bb.show()
			self.dockwidget=bb


		from PyFlow.App import PyFlow
		instance = PyFlow.instance()

		# start the Pyflow canvas inside FreeCAD
		a=instance.centralWidget().children()[1]

		# create the property dialog dockwindow
		createPropTool()

		# connect the canvas widget with the Property dialog dockwindow
		instance.canvasWidget.requestFillProperties.connect(onRequestFillPropertiesXX)
		instance.canvasWidget.requestClearProperties.connect(onRequestClearPropertiesXX)



		self.instance=instance

		if inside:
			import Qt.QtWidgets
			from Qt.QtWidgets import QWidget

			layout.addWidget(a)
#			instance.loadfile(fpath = '/home/thomas/Schreibtisch/z2.json')

		else:
			instance.show()
			instance.loadfile(fpath = '/home/thomas/Schreibtisch/z2.json')

	def refresh(self):
		'''refresh the gui'''

		data = self.instance.graphManager.serialize()
		self.instance.graphManager.deserialize(data)

		for graph in self.instance.graphManager.getAllGraphs():
			self.instance.canvasWidget.createWrappersForGraph(graph)

		self.instance.graphManager.selectRootGraph()

	def refresh2(self):
		self.instance.savefile('/home/thomas/Schreibtisch/refresh.json')
		self.instance.loadfile('/home/thomas/Schreibtisch/refresh.json')

	def loadA(self):
		self.loadfile('/home/thomas/Schreibtisch/aa2.json')

	def loadfile(self,filename):
		self.instance.loadfile(fpath = filename)

	def save(self):
		self.instance.save( save_as=True)

	def load(self):
		self.instance.load()


	def man(self):
		return self.instance.graphManager




def test_AA(inside=True):
	'''start the node graph editor'''

	if 1:
		import sys
		sms=sys.modules.keys()
		for m in sms:

			if m.startswith('PyFlow'):
				print m
				del(sys.modules[m])
	try:
		FreeCAD.toolInstance.deleteLater()
		del(FreeCAD.toolInstance)
	except:
		pass

	try:
		FreeCAD.open(u"/home/thomas/aa.FCStd")
		App.setActiveDocument("aa")
		App.ActiveDocument=App.getDocument("aa")
		Gui.ActiveDocument=Gui.getDocument("aa")
	except: 
		pass

	from PyFlow.Core.Common import *
	from PyFlow import(
		INITIALIZE,
		GET_PACKAGES
	)

	from PyFlow.Core import(
		GraphBase,
		PinBase,
		NodeBase,
		GraphManager
	)

	INITIALIZE()

	t=myPyFlow(inside)
	#t.loadfile( '/home/thomas/Schreibtisch/z2.json')

	FreeCAD.PF=t

	packages = GET_PACKAGES()


	fcn=packages['PyflowBase'].GetNodeClasses()["compound"]
	fc=fcn('group')
	t.man().activeGraph().addNode(fc)


	fn=packages['FreeCAD'].GetNodeClasses()["FreeCAD_Node"]

	f=fn('MyFreeCadN')
	f.setPosition(50,-100)
	t.man().activeGraph().addNode(f)

	try: 
		ss=FreeCADGui.Selection.getSelection()
		for i,s in enumerate(ss):
			f=fn(s.Label)
			f.setPosition(-100+i*120,120-i*30)
			t.man().activeGraph().addNode(f)
	except:
		f=fn('MyFreeCadN')
		f.setPosition(50,-100)
		t.man().activeGraph().addNode(f)

	t.man().selectGraph(fc.name)
	f=fn('My_Sub_FC')
	t.man().activeGraph().addNode(f)

	t.man().selectGraph(str('root'))

	intlib = packages['PyflowBase'].GetFunctionLibraries()["IntLib"]
	foos = intlib.getFunctions()

	addNode1 = NodeBase.initializeFromFunction(foos["add"])
	addNode2 = NodeBase.initializeFromFunction(foos["add"])
	addNode3 = NodeBase.initializeFromFunction(foos["add"])

	addNode1.setPosition(-200,-150)
	addNode2.setPosition(-150,-70)
	addNode3.setPosition(200,-100)
	addNode1.setData('a', 5)

	t.man().activeGraph().addNode(addNode1)
	t.man().activeGraph().addNode(addNode2)
	t.man().activeGraph().addNode(addNode3)

	connection = connectPins(addNode1[str('out')], addNode3[str('a')])
	connection = connectPins(addNode2[str('out')], addNode3[str('b')])

	FreeCAD.PF.dockwidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)

	#f.setName("hugo")
	FreeCAD.f=f

	t.refresh()


def test_BB():
	test_AA(inside=False)


'''

t=FreeCAD.PF
m=t.man()
m.graphsDict
g=m.activeGraph()
for n in g.getNodes():
	print n.getName()
	if n.getName()=='add1':
		n.setName("HUHU2")

t.refresh()	

'''



'''
FreeCAD.toolInstance.deleteLater()
del(FreeCAD.toolInstance)

Qt::WA_DeleteOnClose
setAttribute(Qt::WA_DeleteOnClose);
Qt.QtCore.Qt.WA_DeleteOnClose



FreeCAD.PF.dockwidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
'''
