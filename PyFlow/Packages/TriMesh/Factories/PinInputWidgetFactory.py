
from PyFlow.Core.Common import *
from PyFlow.UI.Widgets.InputWidgets import *
from Qt.QtWidgets import QLineEdit

class NoneInputWidget(InputWidgetSingle):
    """
    String data input widget
    """

    def __init__(self, parent=None, **kwds):
        super(NoneInputWidget, self).__init__(parent=parent, **kwds)
        self.le = QLineEdit(self)
        self.le.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setWidget(self.le)
        self.le.textChanged.connect(lambda val: self.dataSetCallback(val))
        self.le.setEnabled(False)

    def blockWidgetSignals(self, bLocked):
        self.le.blockSignals(bLocked)

    def setWidgetValue(self, val):
        self.le.setText(str(val))

def getInputWidget(dataType, dataSetter, defaultValue, userStructClass):
    '''
    factory method
    '''
    if dataType in ["MeshPin"]:
    	return NoneInputWidget(dataSetCallback=dataSetter, defaultValue=None)
