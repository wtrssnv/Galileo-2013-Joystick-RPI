from pygame import *
from mode import *
from game import Game

class Menu(Mode):
    def __init__(self, core, status = 0):
        Mode.__init__(self, core, 30)
        self.status = status

        self.statusFont = font.Font(None, 30)
        self.infoFont = font.Font(None, 30)

    def onDraw(self, screen, core, numTicks):
        screen.fill((255,255,255))

        if self.status != 0:
            texts = {"1": "Aterrizaje correcto", "2": "Houston Houston tenemos un problema!"}
            text = self.statusFont.render(texts[ str(self.status) ], True, (0,0,0))

            draw.rect(screen, (0,0,0), Rect(50, 80, 540, 200), 1)
            screen.blit(text, (50 + ((540 / 2) - (text.get_width() / 2)), 80 + ((200/2) - (text.get_height() / 2))))
            
        info = self.infoFont.render("[J]ugar          [S]alir", True, (0,0,0))
        screen.blit(info, (320 - (info.get_width() / 2), 380))

    def handleEvent(self, e, core, numTicks):
        if e.type == KEYDOWN:
            if e.key == K_j:
                core.setActiveMode( Game(core) )
            elif e.key == K_s:
                core.pleaseExit()
