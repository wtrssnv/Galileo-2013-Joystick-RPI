# mode.py: Clase base para los modos
# Un modo es una entidad autocontenida que puede ejecutarse por el core
# y puede recivir enventos e instrucciones cuando los dibuja.

class Mode(object):
    def __init__(self, core, fps = 50):
        self.fps = fps
        self.core = core

    def handleEvent(self, event, core, numTicks):
        pass

    def onQuit(self):
        return True


    def onSwitchOut(self, core):
        pass


    def onSwitchIn(self, core):
        pass


    def onPreDraw(self, core, numTicks):
        pass


    def onComputations(self, core, numTicks):
        pass


    def onDraw(self, screen, core, numTicks):
        pass
