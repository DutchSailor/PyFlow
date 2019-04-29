from PyFlow.Core import NodeBase

import pyqtgraph.opengl as gl

class displayMesh(NodeBase):
    def __init__(self, name):
        super(displayMesh, self).__init__(name)
        self.inExec = self.addInputPin('exec', 'ExecPin', None, self.compute)
        self.outExec = self.addOutputPin('exec', 'ExecPin')        
        self.itemPin = self.addInputPin("Item", 'MeshPin', defaultValue=None)
        self.color = self.addInputPin("color","FloatVector4Pin")
        self.meshdata = None
        self.item = None

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['glviewPin', 'MeshPin'], 'outputs': []}

    @staticmethod
    def category():
        return 'Display'

    def kill(self):
        if self._wrapper().graph().window().view and self.item:
            if self.item in self._wrapper().graph().window().view.items:
                self._wrapper().graph().window().view.items.remove(self.item)
                self._wrapper().graph().window().view.updateGL()
                del(self.item)
        super(displayMesh, self).kill()

    def compute(self):
        if self.itemPin.dirty:
            self.meshData = gl.MeshData(vertexes=self.itemPin.getData().vertices ,faces=self.itemPin.getData().faces)
        if not self.item:
            self.item = gl.GLMeshItem(meshdata=self.meshData,smooth=True, color=tuple(self.color.getData().xyzw.tolist()), shader='edgeHilight')
        else:
            self.item.setMeshData(meshdata=self.meshData)
        if self.item not in self._wrapper().graph().window().view.items:
            self._wrapper().graph().window().view.addItem(self.item)            
        self.outExec.call()