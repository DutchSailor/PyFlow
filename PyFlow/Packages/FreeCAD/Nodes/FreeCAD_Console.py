from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *

import FreeCAD

class FreeCAD_Console(NodeBase):
    def __init__(self, name):
        super(FreeCAD_Console, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.entity = self.createInputPin('entity', 'AnyPin')
        self.entity.enableOptions(PinOptions.ListSupported)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['AnyPin'], 'outputs': ['AnyPin']}

    @staticmethod
    def category():
        return 'DefaultLib'

    @staticmethod
    def keywords():
        return ['print']

    @staticmethod
    def description():
        return "FreeCAD.Console output"

    def compute(self, *args, **kwargs):
        print(self.entity.getData())
        FreeCAD.Console.PrintMessage(str(self.entity.getData())+"! ")
        self.outExec.call()
