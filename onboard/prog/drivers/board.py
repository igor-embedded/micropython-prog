from machine import Pin, I2C
from prog.drivers.motorcontroller import MotorController
from prog.drivers.lcd import LCD
from prog.drivers.imu import IMU

__I2C_SCL = 5
__I2C_SDA = 4
__I2C_FREQ = 100000
__MOTOR_ADDR = 48
__MOTOR_FREQ = 1000


class Board():
    def __init__(self):
        self.i2c = I2C(scl=Pin(__I2C_SCL), sda=Pin(__I2C_SDA),
                       freq=__I2C_FREQ)
        self.motorcontroller = MotorController(i2c=self.i2c,
                                               addr=__MOTOR_ADDR,
                                               freq=__MOTOR_FREQ)
        self.lcd = LCD(self.i2c)
#        self.imu = IMU(self.i2c)

#        loop = asyncio.get_event_loop()
#        loop.run_forever()
#
#    def test_magnetometer(self):
#        print(self.__imu.read_compass())
