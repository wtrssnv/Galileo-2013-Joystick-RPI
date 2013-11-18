# core.py: La clase core, contiene el bucle principal y los métodos relevantes.

from pygame import *
import sys, math

class Core(object):
    def __init__(self, resolution, fullscreen, drawFPS = False):
        self.activeMode = None
        self.lastMode = None

        self.runLoop = True
        self.res = resolution
        self.useFullscreen = fullscreen
        self.screen = None
        self.clock = None

        self.drawFPS = drawFPS
        self.numFrames = 0
        
    #Establecer el modo activo
    def setActiveMode(self, newMode, discard=False):
        if self.activeMode != None:
            self.activeMode.onSwitchOut(self)

        if not discard:
            self.lastMode = self.activeMode
        
        newMode.onSwitchIn(self)
        self.activeMode = newMode

    #Reestablece el modo
    def revertLastMode(self):
        if self.lastMode == None:
            return None

        self.activeMode.onSwitchOut(self)
        tmp = self.activeMode
        self.activeMode = self.lastMode
        self.activeMode.onSwitchIn(self)
        self.lastMode = tmp

        return tmp

    def doInit(self):
        #Inicializa pygame
        init()

        if self.useFullscreen:
            self.screen = display.set_mode(self.res, FULLSCREEN)
        else:
            self.screen = display.set_mode(self.res)

        self.fpsFont = font.Font(None, 20)

    #Prepara al modo activo para su salida del programa
    def pleaseExit(self):
        if self.activeMode.onQuit():
            self.runLoop = False

    def enterLoop(self):
        if self.screen == None:
            raise Exception("Screen not set, pygame not initialized")
        
        if self.activeMode == None:
            raise Exception("Critical: No mode set, nothing to do!")

        lastDraw = 0
        while self.runLoop:
            if time.get_ticks() - lastDraw > (1000.0 / self.activeMode.fps):
                #Momento para pintar

                #Calcula los frames por segundo
                fps = math.floor(1 / (float(time.get_ticks() - lastDraw) / 1000.0))

                lastDraw = time.get_ticks()

                self.activeMode.onPreDraw(self, time.get_ticks())
                self.activeMode.onDraw(self.screen, self, time.get_ticks())
                
                if self.drawFPS:
                    fpsSurf = self.fpsFont.render(str(fps), False, (255,0,0))
                    self.screen.blit(fpsSurf, (20,20))

                display.update()
            else:
                #No se puede pintar todavía, deja hacer otras tareas
                for e in event.get():
                    if e.type == QUIT:
                        if self.activeMode.onQuit():
                            self.runLoop = False
                            break
                    else:
                        self.activeMode.handleEvent(e, self, time.get_ticks())
            
                self.activeMode.onComputations(self, time.get_ticks())
            

        #Paramos
        quit()
