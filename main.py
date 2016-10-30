from engine import *

import tdl

import pdb

if __name__ == '__main__':
    eng = Engine(90,50)

    while not tdl.event.isWindowClosed():
        stop = eng.update()
        
        if stop:
            break

        eng.rendering()
        tdl.flush()

    