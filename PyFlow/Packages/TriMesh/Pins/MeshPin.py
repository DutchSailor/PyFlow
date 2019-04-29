from PyFlow.Core import PinBase
from PyFlow.Core.Common import *

import trimesh

class MeshPin(PinBase):
    """doc string for BoolPin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(MeshPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(False)

    @staticmethod
    def isPrimitiveType():
        return True

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('MeshPin')

    @staticmethod
    def pinDataTypeHint():
        return 'MeshPin', False

    @staticmethod
    def color():
        return (255,105,180)

    @staticmethod
    def processData(data):
        if isinstance(data,trimesh.base.Trimesh):
            return data
        else:
            raise("error")
        return 

    def serialize(self):
        data = PinBase.serialize(self)
        data['value'] = None
        return data

    def setData(self, data):
        try:
            self._data = self.processData(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)

