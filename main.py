from engine import *

import tdl

import pdb

if __name__ == '__main__':
    eng = Engine()
    eng.initialization()

    while not tdl.event.isWindowClosed():
        stop = eng.update()
        
        if stop:
            break

        eng.rendering()
        tdl.flush()

    