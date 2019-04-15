class PhysMotor():
    MOTOR_A = 0
    MOTOR_B = 1
    MOTORS_NUMBER = 2
    MOTORS_ID = [0x10, 0x11]
    DIR_STOP = 0x00
    DIR_CCW = 0x01
    DIR_CW = 0x02
    MAX_PWM = 0xfff

    def __init__(self, number):
        self.number = number
        self.id = self.MOTORS_ID[number]
        self.direction = self.DIR_STOP
        self.pwm = 0


class MotorController():
    def __init__(self, i2c, addr, freq):
        self.__i2c = i2c
        self.__addr = addr
        self.__write_freq(freq)
        self.__motors = [PhysMotor(m)
                         for m in range(0, PhysMotor.MOTORS_NUMBER)]

    def __write_freq(self, freq):
        self.__freq = freq
        msg = bytearray(4)
        msg[3] = self.__freq & 0xff
        msg[2] = (self.__freq >> 8) & 0xff
        msg[1] = (self.__freq >> 16) & 0xff
        msg[0] = (self.__freq >> 24) & 0x0f
        try:
            self.__i2c.writeto(self.__addr, msg)
        except Exception as e:
            return False
        return True

    def actuate(self, motor):
        msg = bytearray(4)
        msg[3] = self.__motors[motor].pwm & 0xff
        msg[2] = (self.__motors[motor].pwm >> 8) & 0xff
        msg[1] = self.__motors[motor].dir
        msg[0] = self.__motors[motor].id
        try:
            self.__i2c.writeto(self.__addr, msg)
        except Exception as e:
            return False
        return True

    def update(self, motor, dir, pwm=None):
        self.__motors[motor].dir = dir
        if pwm is not None:
            pwm = pwm if pwm < PhysMotor.MAX_PWM else PhysMotor.MAX_PWM
            self.__motors[motor].pwm = pwm
        self.actuate(motor)

    def stop(self, motor):
        self.update(motor=motor, dir=PhysMotor.DIR_STOP)
