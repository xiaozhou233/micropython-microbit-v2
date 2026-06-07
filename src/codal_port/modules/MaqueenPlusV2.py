class MaqueenPlusV2:
    I2CADDR                 = 0x10
    ADC0_REGISTER           = 0X1E
    ADC1_REGISTER           = 0X20
    ADC2_REGISTER           = 0X22
    ADC3_REGISTER           = 0X24
    ADC4_REGISTER           = 0X26
    LEFT_LED_REGISTER       = 0X0B
    RIGHT_LED_REGISTER      = 0X0C
    LEFT_MOTOR_REGISTER     = 0X00
    RIGHT_MOTOR_REGISTER    = 0X02
    LINE_STATE_REGISTER     = 0X1D
    VERSION_CNT_REGISTER    = 0X32
    VERSION_DATA_REGISTER   = 0X33

    LeftMotor   = 0
    RightMotor  = 1
    AllMotor    = 2

    Forward    = 0
    Backward   = 1

    LeftLed   = 0
    RightLed  = 1
    AllLed    = 2

    Close = 0
    Open  = 1

    L1 = 0
    M  = 1
    R1 = 2
    L2 = 3
    R2 = 4

    def __init__(self):
        self.I2C = i2c
        self.I2C.init(freq=100000,sda=pin20,scl=pin19)

    def motorRun(self, motor, dir, speed):
        if motor == self.LeftMotor:
            buf = bytearray(3)
            buf[0] = 0x00
            buf[1] = dir
            buf[2] = speed
        elif motor == self.RightMotor:
            buf = bytearray(3)
            buf[0] = 0x02
            buf[1] = dir
            buf[2] = speed
        else:
            buf = bytearray(5)
            buf[0] = 0x00
            buf[1] = dir
            buf[2] = speed
            buf[3] = dir
            buf[4] = speed
        self.I2C.write(0x10,buf)

    def motorStop(self, motor):
        self.motorRun(motor,0,0)

    def controlLed(self, led, state):
        if led == self.LeftLed:
            buf = bytearray(2)
            buf[0] = self.LEFT_LED_REGISTER  
            buf[1] = state
        elif led == self.RightLed:
            buf = bytearray(2)   
            buf[0] = self.RIGHT_LED_REGISTER  
            buf[1] = state
        else:
            buf = bytearray(3)
            buf[0] = self.LEFT_LED_REGISTER  
            buf[1] = state
            buf[2] = state
        self.I2C.write(0x10,buf)
    
    def getLineSensorState(self, sensor):
        data = self.read([self.LINE_STATE_REGISTER], 1)
        if sensor == self.L1:
            state = 1 if data[0] & 0x08 == 0x08 else 0
        elif sensor == self.M:
            state = 1 if data[0] & 0x04 == 0x04 else 0
        elif sensor == self.R1:
            state = 1 if data[0] & 0x02 == 0x02 else 0
        elif sensor == self.L2:
            state = 1 if data[0] & 0x10 == 0x10 else 0
        elif sensor == self.R2:
            state = 1 if data[0] & 0x01 == 0x01 else 0
        else:
            state = 0
        return state

    def getLineSensorData(self, sensor):
        if sensor == self.L1:
            buf = self.read([self.ADC3_REGISTER], 2)
            data = buf[1] << 8 | buf[0]
        elif sensor == self.M:
            buf = self.read([self.ADC2_REGISTER], 2)
            data = buf[1] << 8 | buf[0]
        elif sensor == self.R1:
            buf = self.read([self.ADC1_REGISTER], 2)
            data = buf[1] << 8 | buf[0]
        elif sensor == self.L2:
            buf = self.read([self.ADC4_REGISTER], 2)
            data = buf[1] << 8 | buf[0]
        elif sensor == self.R2:
            buf = self.read([self.ADC0_REGISTER], 2)
            data = buf[1] << 8 | buf[0]
        else:
            data = 0
        return data

    def getVersion(self):
        len = self.read([self.VERSION_CNT_REGISTER], 1)
        version = self.read([self.VERSION_DATA_REGISTER], len[0])
        return str(version, "utf-8")
    
    def read(self, reg, len):
        self.I2C.write(0x10, bytearray(reg))
        return self.I2C.read(0x10, len)

