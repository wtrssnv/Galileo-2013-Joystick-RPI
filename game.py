from mode import *
from pygame import *

import menu
import os
import sys
import wiringpi2

GRAVITY = 0.01
THRUSTER = 0.1
FUELUSE = 0.05
IMG_DIR = "imagenes"

class Game(Mode):

    def __init__(self, core):
        Mode.__init__(self, core, 30)

        self.pos = [620,0]
        self.speed = [-5,1]
        self.fuel = 100

        self.fonten = font.Font(None, 25)
        self.messagefont = font.Font(None, 25)
        self.motorsound = mixer.Sound("motor.wav")

        self.shipImages = [ image.load("ship-%i.png" % i).convert() for i in range(0,3) ]
        for i,s in enumerate(self.shipImages):
            self.shipImages[i].set_colorkey((0,0,255))

        self.animCounter = 0
        self.doAnimate = False

        self.io = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)
            
        self.io.pinMode(4, self.io.INPUT)
        self.io.pinMode(5, self.io.INPUT)
        self.io.pinMode(6, self.io.INPUT)
            
        self.io.pullUpDnControl(4, self.io.PUD_UP)
        self.io.pullUpDnControl(5, self.io.PUD_UP)
        self.io.pullUpDnControl(6, self.io.PUD_UP)
        

    def onDraw(self, screen, core, numTicks):
        
        screen.fill((255,255,255))
    	screen.fill((255,255,255),(0,475,640,5))
        screen.fill((0,0,0),(300,475,40,5))

        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        
        if self.pos[0] < 0:
        	self.pos[0] = 640
         
        if self.pos[0] > 640:
        	self.pos[0] = 0
    
        if self.pos[1] > (475 - 20):
            if self.pos[0] >= 300 and self.pos[0] <= 320 and self.speed[1] < 5:
                print("Has aterrizado bien")
                core.setActiveMode( menu.Menu(core, 1) )
            else:
                print("Woou! estrellado!!!")
                core.setActiveMode( menu.Menu(core, 2) )

            self.pos[1] = 455
            #run = False
    
        if self.doAnimate:
            if not mixer.get_busy():
                self.motorsound.play(0)

            self.animCounter += 1
            screen.blit(self.shipImages[1 + int(self.animCounter / 3)], (self.pos[0], self.pos[1], 20, 20))

            if self.animCounter == 5:
                self.animCounter = 0

            self.fuel -= FUELUSE
        else:
            screen.blit(self.shipImages[0], (self.pos[0], self.pos[1], 20, 20))

        keys = key.get_pressed()

        if self.fuel <= 0:
            self.fuel = 0
            self.doAnimate = False
            self.motorsound.stop()
        else:

            self.doAnimate = True
                       
            if keys[K_UP] or (self.io.digitalRead(5) == self.io.LOW):
                self.speed[1] -= THRUSTER
                print("Impulso:" + str(self.speed[1]) )
            elif keys[K_LEFT] or (self.io.digitalRead(4) == self.io.LOW):
                self.speed[0] -= THRUSTER
                print("Izauierda:" + str(self.speed[0]) )
            elif keys[K_RIGHT] or (self.io.digitalRead(6) == self.io.LOW):
                self.speed[0] += THRUSTER
                print("Derecha:" + str(self.speed[0]) )
            else:
                self.doAnimate = False
                self.motorsound.stop()

        self.speed[1] += GRAVITY

        screen.blit(self.fonten.render("Velocidad: %f" % self.speed[1], True, (0,0,0)), (10,10,40,100))
        screen.blit(self.fonten.render("Propergoles: %f" % self.fuel, True, (0,0,0)), (10,30,40,100))
