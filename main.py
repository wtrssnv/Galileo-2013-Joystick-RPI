#!/usr/bin/python2

from core import Core
from menu import *

if __name__ == "__main__":    
    #Create the core with correct resolution
    core = Core((640,480), False, False)
    core.doInit()
    core.setActiveMode( Menu(core) )
    core.enterLoop()
