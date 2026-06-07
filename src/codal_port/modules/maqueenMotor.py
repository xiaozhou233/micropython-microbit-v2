class maqueenMotor:
  def __init__(self):
    self.I2C = i2c
    self.I2C.init(freq=100000,sda=pin20,scl=pin19)

  def run(self, motor, dir,speed):
    buf = bytearray(3)
    if motor == 0:
      buf[0] = 0x00
    else:
      buf[0] = 0x02
    buf[1] = dir
    buf[2] = speed
    self.I2C.write(0x10,buf)

  def stop(self, motor):
    self.run(motor,0,0)
    
    
class maqueenServo:
  def __init__(self):
    self.I2C = i2c
    self.I2C.init(freq=100000,sda=pin20,scl=pin19)

  def run(self, servo, speed):
    buf = bytearray(3)
    buf[0] = servo
    buf[1] = speed
    self.I2C.write(0x10,buf)

  def stop(self, servo):
    self.run(servo,0,0)


