# import uasyncio as asyncio
from machine import I2C
import time
import math

__COMPASS_AVG_1_SAMPLE = (0x00 << 5)
__COMPASS_AVG_2_SAMPLE = (0x01 << 5)
__COMPASS_AVG_4_SAMPLE = (0x02 << 5)
__COMPASS_AVG_8_SAMPLE = (0x03 << 5)

__COMPASS_DATA_RATE_0_75_HZ = (0x00 << 2)
__COMPASS_DATA_RATE_1_5_HZ = (0x01 << 2)
__COMPASS_DATA_RATE_3_HZ = (0x02 << 2)
__COMPASS_DATA_RATE_7_5_HZ = (0x03 << 2)
__COMPASS_DATA_RATE_15_HZ = (0x04 << 2)
__COMPASS_DATA_RATE_30_HZ = (0x05 << 2)
__COMPASS_DATA_RATE_75_HZ = (0x06 << 2)

__COMPASS_MEAS_NORMAL = (0x00)
__COMPASS_MEAS_POSITIVE = (0x01)
__COMPASS_MEAS_NEGATIVE = (0x02)

__COMPASS_GAIN_0_88 = (0x00 << 5)
__COMPASS_GAIN_1_3 = (0x01 << 5)
__COMPASS_GAIN_1_9 = (0x02 << 5)
__COMPASS_GAIN_2_5 = (0x03 << 5)
__COMPASS_GAIN_4_0 = (0x04 << 5)
__COMPASS_GAIN_4_7 = (0x05 << 5)
__COMPASS_GAIN_5_6 = (0x06 << 5)
__COMPASS_GAIN_8_1 = (0x07 << 5)

__COMPASS_CONTINUOUS_MEAS = (0x0)
__COMPASS_SINGLE_MEAS = (0x1)

__COMPASS_REG_A = (__COMPASS_AVG_8_SAMPLE | __COMPASS_DATA_RATE_75_HZ | \
                   __COMPASS_MEAS_NORMAL)
__COMPASS_REG_B = __COMPASS_GAIN_1_3
__COMPASS_REG_MODE = __COMPASS_SINGLE_MEAS

__COMPASS_WRITE_A = str((0x00 << 8) | __COMPASS_REG_A)
__COMPASS_WRITE_B = str((0x01 << 8) | __COMPASS_REG_B)
__COMPASS_WRITE_MODE = '\x02\x01'

__COMPASS_ADDR = 0x1E
__COMPASS_CFG_REG_A = b'\x00\x78'
__COMPASS_CFG_CMD = b'\x02\x01'
#__ACCEL_ADDR
#__GYRO_ADDR

__SAMPLES_LOG_2 = 2
__SAMPLES = (1 << __SAMPLES_LOG_2)
#__COMPASS_SAMPLES = __SAMPLES
__COMPASS_SAMPLES = 4

__X = 0
__Y = 1
__Z = 2

class Meas3D():
    __measurements = None
    __index = None
    __size = None
    __average = None
    __current = None
    __total = None

    def __init__(self, size):
        self.__size = size
        self.__measurements = [[0, 0, 0] for i in range(0, size)]
        self.__total = [0, 0, 0]
        self.__average = [0, 0, 0]
        self.__current = [0, 0, 0]
        self.__index = 0

    def update(self, new_measurement):
        for i in range(0, 3):
            self.__total[i] -= self.__measurements[self.__index][i]
            self.__total[i] += new_measurement[i]
            self.__measurements[self.__index][i] = new_measurement[i]
            self.__average[i] = self.__total[i] / self.__size
            self.__current[i] = new_measurement[i]
        self.__index = (self.__index + 1) % self.__size

    def read(self):
#        return self.__average
        return self.__current

def try_op(i2c, address, val, read=True):
    retval = None
    while True:
        try:
            if read:
                retval = i2c.readfrom(address, val)
            else:
                retval = i2c.writeto(address, val)
        except Exception as exception:
            continue
        else:
            break
    return retval


def try_writeto(i2c, address, data):
    retval = None
    while True:
        try:
            retval = i2c.writeto(address, data)
        except Exception as exception:
            continue
        else:
            break
    return retval

def try_readfrom(i2c, address, bytenum):
    retval = None
    while True:
        try:
            retval = i2c.readfrom(address, bytenum)
        except Exception as exception:
            continue
        else:
            break
    return retval

#def try_writeto(i2c, address, data):
#    return try_op(i2c, address=address, val=data, read=False)

#def try_readfrom(i2c, address, bytenum):
#    return try_op(i2c, address=address, val=bytenum, read=True)

class Compass():
    __i2c = None
    __measurements = None
    number = -180
    counter = 0

    def __init__(self, i):
        self.__measurements = Meas3D(__COMPASS_SAMPLES)
        self.__i2c = i
        try_writeto(self.__i2c, __COMPASS_ADDR, __COMPASS_WRITE_A)
        try_writeto(self.__i2c, __COMPASS_ADDR, __COMPASS_WRITE_B)

    def __read_sensor(self):
#        while True:
#            try:
#                self.__i2c.writeto(__COMPASS_ADDR, __COMPASS_WRITE_MODE)
#                time.sleep_ms(6)
#                self.__i2c.writeto(__COMPASS_ADDR, b'\x03')
#                reading = self.__i2c.readfrom(__COMPASS_ADDR, 6)
#                [x, y, z] = [((reading[i] << 8) | reading[i + 1])
#                             for i in range(0, 6, 2)]
#            except Exception as exception:
#                continue
#            else:
#                break
        try_writeto(self.__i2c, __COMPASS_ADDR, __COMPASS_WRITE_MODE)
        time.sleep_ms(6)
        try_writeto(self.__i2c, __COMPASS_ADDR, b'\x03')
        reading = try_readfrom(self.__i2c, __COMPASS_ADDR, 6)
        [x, y, z] = [((reading[i] << 8) | reading[i + 1])
                     for i in range(0, 6, 2)]

#        x = x * 0.00092
#        y = y * 0.00092
#        z = z * 0.00092
#        heading = math.atan2(y, x)
#        if heading < 0:
#            heading += 2 * math.pi
#        if heading > 2 * math.pi:
#            heading -= 2 * math.pi
#        heading_deg = heading * 180 / math.pi
#        print('[{:^8}, {:^8}, {:^8}, {:^8}, {:^8}]' \
#                .format(x, y, z, heading, heading_deg))
#        print('[{:^8}, {:^8}, {:^8}]'.format(x, y, z))
        return (x, y, z)
#        alpha = math.atan2(y, x)
#        if alpha > 2 * 3.14:
#            alpha -= 2 * 3.14
#        alpha = alpha * 180 / 3.14
#        beta = math.atan2(z, x)
#        if beta > 2 * 3.14:
#            beta -= 2 * 3.14
#        beta = beta * 180 / 3.14
#        gamma = math.atan2(z, y)
#        if gamma > 2 * 3.14:
#            gamma -= 2 * 3.14
#        gamma = gamma * 180 / 3.14
#        print('[{:^8}, {:^8}, {:^8}][{:^8}, {:^8}, {:^8}]' \
#                .format(x, y, z, alpha, beta, gamma))
#        return [alpha, beta, gamma]
        return [heading_deg, heading_deg, heading_deg]

    def update(self):
        m = self.__read_sensor()
#        print([hex(m[0]), hex(m[1]), hex(m[2])])
        self.__measurements.update(m)

    def read(self):
        return self.__measurements.read()

class IMU():
    __i2c = None
    __compass = None

#    async def __run(self):
    def __run(self):
        while True:
            self.__compass.update()
            read = self.__compass.read()
#            print(read)
#            await asyncio.sleep_ms(100)

    def __init__(self, i):
        self.__i2c = i
        self.__compass = Compass(self.__i2c)
#        loop = asyncio.get_event_loop()
#        loop.create_task(self.__run())
