""" prepare the system """

from infra.networking import Networking
import gc
import webrepl


def setup():
    networking = Networking()
    print(networking.info())
    webrepl.start()
    gc.collect()
