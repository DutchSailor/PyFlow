

import FreeCAD

def test_BB():
	FreeCAD.Console.PrintMessage("\ntest_B\n")


def test_AA():
	FreeCAD.Console.PrintMessage("\ntest_A\n")


#-----------------------


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

#---------------------

from PyFlow.Packages.PyflowBase.Tools.PropertiesTool import PropertiesTool

def onRequestFillPropertiesXX(propertiesFillDelegate):
	try:
		toolInstance=FreeCAD.toolInstance
	except:
		toolInstance=PropertiesTool()
		FreeCAD.toolInstance=toolInstance

	toolInstance.show()
	toolInstance.clear()
	toolInstance.assignPropertiesWidget(propertiesFillDelegate)
	

def onRequestClearPropertiesXX():
	toolInstance.clear()

def createPropTool():
	try:
		toolInstance=FreeCAD.toolInstance
	except:
		toolInstance=PropertiesTool()
		FreeCAD.toolInstance=toolInstance
	toolInstance.show()






#--------------------



class myPyFlow(object):

	def __init__(self,inside=True):


		FreeCAD.Console.PrintMessage(str(QtGui))

		if inside:
			q=FreeCADGui.getMainWindow()

			bb=QtGui.QDockWidget()
			q.addDockWidget(QtCore.Qt.TopDockWidgetArea, bb)

			bb.setWindowTitle("Node editor Version: Dock Window - 0.3")
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
			pB = QtGui.QPushButton(QtGui.QIcon('icons:freecad.svg'), 'run a test action 4')
			bl.addWidget(pB)


			layout.addWidget(buttons)

			bb.show()

		from PyFlow.App import PyFlow
		instance = PyFlow.instance()
		a=instance.centralWidget().children()[1]

		createPropTool()

		instance.canvasWidget.requestFillProperties.connect(onRequestFillPropertiesXX)
		instance.canvasWidget.requestClearProperties.connect(onRequestClearPropertiesXX)




		self.instance=instance

		if inside:
			import Qt.QtWidgets
			from Qt.QtWidgets import QWidget

			layout.addWidget(a)
			instance.loadfile(fpath = '/home/thomas/Schreibtisch/z2.json')

		else:
			instance.show()
			instance.loadfile(fpath = '/home/thomas/Schreibtisch/aa2.json')

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


	try:
		FreeCAD.open(u"/home/thomas/aa.FCStd")
		App.setActiveDocument("aa")
		App.ActiveDocument=App.getDocument("aa")
		Gui.ActiveDocument=Gui.getDocument("aa")
	except: pass


	from PyFlow.Tests.TestsBase import *
	from PyFlow.Core.Common import *
	from collections import Counter


	
	t=myPyFlow(inside) # wrapper for freecad
	t.loadfile( '/home/thomas/Schreibtisch/z2.json')

	# t.instance is PyFlow.instance() !
	FreeCAD.PF=t
	#return


	packages = GET_PACKAGES()
	intlib = packages['PyflowBase'].GetFunctionLibraries()["IntLib"]
	foos = intlib.getFunctions()

	addNode1 = NodeBase.initializeFromFunction(foos["add"])
	addNode2 = NodeBase.initializeFromFunction(foos["add"])
	addNode3 = NodeBase.initializeFromFunction(foos["add"])

	addNode1.setPosition(-100,0)
	addNode2.setPosition(0,150)
	addNode3.setPosition(100,0)
	addNode1.setData('a', 5)

	t.man().activeGraph().addNode(addNode1)
	t.man().activeGraph().addNode(addNode2)
	t.man().activeGraph().addNode(addNode3)

	connection = connectPins(addNode1[str('out')], addNode2[str('a')])
	connection = connectPins(addNode2[str('out')], addNode3[str('a')])

	t.refresh2()
	#FreeCAD.t=t


def test_BB():
	test_AA(inside=False)
