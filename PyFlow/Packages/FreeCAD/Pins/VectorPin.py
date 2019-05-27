from blinker import Signal
import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow import getAllPinClasses
from PyFlow import CreateRawPin
from PyFlow import findPinClassByType
from PyFlow import getPinDefaultValueByType

import FreeCAD
from FreeCAD import Vector
#-----------------


class VectorEncoder(json.JSONEncoder):
    def default(self, vec):
        if isinstance(vec, Vector):
            return {Vector.__name__: [vec.x,vec.y,vec.z]}
        json.JSONEncoder.default(self, vec)


class VectorDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(VectorDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return Vector(vec3Dict[Vector.__name__])


#---------------------
class VectorPin(PinBase):
    """doc string for VectorPin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(VectorPin, self).__init__(name, parent, direction, **kwargs)
        self.typeChanged = Signal(str)
        self.dataTypeBeenSet = Signal()
        self.setDefaultValue(None)
        self._free = True
        self._isVector = True
        self.super = None
        self.activeDataType = self.__class__.__name__
        # if True, setType and setDefault will work only once
        self.singleInit = False
        self.changeTypeOnConnection = True
        self._data=FreeCAD.Vector(1,2,3)


    @staticmethod
    def jsonEncoderClass():
        return VectorEncoder

    @staticmethod
    def jsonDecoderClass():
        return VectorDecoder

    @PinBase.dataType.getter
    def dataType(self):
        return self.activeDataType

    @staticmethod
    def supportedDataTypes():
        return tuple([pin.__name__ for pin in getAllPinClasses() if pin.IsValuePin()])

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def defColor():
        return (255, 200, 2, 255)

    @staticmethod
    def color():
        return (255, 200, 2, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'VectorPin', ""

    @staticmethod
    def processData(data):
        return data

    def setData(self, data):
        if self.activeDataType != self.__class__.__name__:
            assert(self.super is not None)
            if not self.isList():
                data = self.super.processData(data)
            else:
                data = [self.super.processData(i) for i in data]
        self._data = data
        PinBase.setData(self, self._data)

    def serialize(self):
        dt = super(VectorPin, self).serialize()
        constrainedType = self.activeDataType
        if constrainedType != self.__class__.__name__:
            pinClass = findPinClassByType(constrainedType)
            # serialize with active type's encoder
            dt['value'] = json.dumps(self.currentData(), cls=pinClass.jsonEncoderClass())
        return dt

    def pinConnected(self, other):
        self._data = getPinDefaultValueByType(other.dataType)
        self.onPinConnected.send(other)
        if self.changeTypeOnConnection:
            traverseConstrainedPins(self, lambda pin, other=other: self.updateOnConnectionCallback(pin, other))
        super(VectorPin, self).pinConnected(other)

    def updateOnConnectionCallback(self, pin, other):
        free = pin.checkFree([])
        if other.dataType != pin.activeDataType and free:
            pin._free = False
            pin.setType(other)

    def updateOnDisconnectionCallback(self, pin, other):
        free = self.checkFree([])
        if free:
            pin.setDefault()

    def pinDisconnected(self, other):
        super(VectorPin, self).pinDisconnected(other)
        if self.changeTypeOnConnection:
            traverseConstrainedPins(self, lambda pin, other=other: self.updateOnDisconnectionCallback(pin, other))

    def checkFree(self, checked=[], selfChek=True):
        # if self.constraint is None:
        if self.constraint is None or self.dataType == self.__class__.__name__:
            return True
        else:
            con = []
            if selfChek:
                free = not self.hasConnections()
                if not free:
                    for c in getConnectedPins(self):
                        if c not in checked:
                            con.append(c)
            else:
                free = True
                checked.append(self)
            free = True
            for port in self.owningNode().constraints[self.constraint] + con:
                if port not in checked:
                    checked.append(port)
                    if not isinstance(port, VectorPin):
                        free = False
                    elif free:
                        free = port.checkFree(checked)
            return free

    def setDefault(self):
        if self.activeDataType != self.__class__.__name__ and self.singleInit:
            # Marked as single init. Type already been set. Skip
            return

        self.super = None
        self.activeDataType = self.__class__.__name__

        self.call = lambda: None

        self.dataTypeBeenSet.send()

        self.setDefaultValue(None)
        if not self.hasConnections():
            self._free = True

        self.supportedDataTypes = lambda: tuple([pin.__name__ for pin in getAllPinClasses() if pin.IsValuePin()])

    def setType(self, other):
        if not self.changeTypeOnConnection:
            return

        if self.activeDataType != self.__class__.__name__ and self.singleInit:
            # Marked as single init. Type already been set. Skip
            return

        if self.activeDataType == self.__class__.__name__ or self.activeDataType in other.supportedDataTypes():
            self.super = other.__class__
            self.activeDataType = other.dataType
            self.color = other.color
            self._data = getPinDefaultValueByType(self.activeDataType)
            self.setDefaultValue(self._data)
            self.dirty = other.dirty
            self.jsonEncoderClass = other.jsonEncoderClass
            self.jsonDecoderClass = other.jsonDecoderClass
            self.typeChanged.send(self.activeDataType)
            self.supportedDataTypes = other.supportedDataTypes
            self._free = self.activeDataType == self.__class__.__name__

#-----------------

    def currentData(self):
        #FreeCAD.Console.PrintMessage("data  "+" "+str(self._data)+"!\n")
        if self._data is None:
            return self._defaultValue
        return self._data
