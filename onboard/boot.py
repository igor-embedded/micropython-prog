# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
# import uos, machine, os
import machine
import os
# uos.dupterm(None, 1) # disable REPL on UART(0)

from deploy import deploy


def reset():
    machine.reset()


listing = os.listdir()

if 'wipe.py' in listing:
    from wipe import clear

# from infra.setup import setup
# setup()

if 'prog' in listing:
    from prog.prog import Program
    p = Program()
    p.run()
