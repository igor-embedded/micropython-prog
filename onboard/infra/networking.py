""" dual mode wifi client / AP """

import json
import network
import time
import os


class WIFI():
    __wifi = None
    __down = True
    __cfg = None
    __cfg_path = "infra/cfg/"

    def up(self):
        self.__wifi.active(True)
        self.__down = False

    def down(self):
        self.__wifi.active(False)
        self.__down = True

    def is_down(self):
        return self.__down

    def ifconfig(self):
        if self.__wifi is not None:
            return self.__wifi.ifconfig()
        return None

    def __init__(self, cfg_file):
        p = self.__cfg_path + cfg_file
        with open(self.__cfg_path + cfg_file, 'r') as infile:
            self.__cfg = json.load(infile)


#       Example of AP.json file:
#       {'essid': 'AP_Name', 'password': 'WPA2_long_pwd'}
class AP(WIFI):
    def __init__(self, down=True):
        super().__init__(cfg_file="AP.json")
        self.__wifi = network.WLAN(network.AP_IF)
        self.up()
        self.__wifi.config(essid=self.__cfg['essid'],
                           authmode=network.AUTH_WPA2_PSK,
                           password=self.__cfg['password'])
        if down:
            self.down()


#       Example of APs.json file:
#       [{'essid': 'KNOWN_ESSID_1', 'password': 'KNOWN_PASSWORD_1'}
#        {'essid': 'KNOWN_ESSID_2', 'password': 'KNOWN_PASSWORD_2'}]
class WLAN(WIFI):
    __connected = False
    __found = []
    __attempts = 2000
    __delay_ms = 50

    def __scan_for_ap(self):
        available_aps = self.__wifi.scan()
        for avail in available_aps:
            essid = avail[0].decode("UTF-8")
            for ap in self.__cfg:
                if ap['essid'] == essid:
                    self.__found.append(essid)

    def __connect_to_ap(self):
        for essid in self.__found:
            for ap in self.__cfg:
                if ap['essid'] == essid:
                    self.__wifi.connect(ap['essid'], ap['password'])
                    i = 0
                    while i < self.__attempts:
                        i += 1
                        if self.__wifi.isconnected():
                            self.__connected = True
                            return
                        else:
                            time.sleep_ms(self.__delay_ms)

    def connect(self):
        if self.__down:
            self.up()
        self.__found = []
        self.__scan_for_ap()
        self.__connect_to_ap()
        if not self.__connected:
            self.down()

    def down(self):
        super().down()
        self.__connected = False

    def __init__(self, down=True):
        super().__init__(cfg_file="APs.json")
        self.__wifi = network.WLAN(network.STA_IF)
        if not down:
            self.connect()


class Networking():
    __ap = None
    __wlan = None

    def __init__(self):
        self.__wlan = WLAN(down=False)
        self.__wlan.connect()
        if self.__wlan.is_down():
            self.__ap = AP(down=True)
            self.__ap.up()

    def info(self):
        if not self.__wlan.is_down():
            return self.__wlan.ifconfig()
        elif self.__ap and not self.__ap.is_down():
            return self.__ap.ifconfig()
        return None
