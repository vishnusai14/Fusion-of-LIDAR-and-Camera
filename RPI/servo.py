class ServoBlaster():
    _servo_dict = { 4: 0, 
                    17: 1,
                    18: 2,
                    21: 3,
                    22: 4,
                    23: 5,
                    24: 6,
                    25: 7}
                    
    def __init__(self, gpio_port):
        
        self._gpio_port     = gpio_port
        self._servo_number  = self._servo_dict[gpio_port]

    def update(self, duty_us,servo,angle2):
        if servo == 1:
            print("This is the duty_uus : " + str(int(duty_us)))
            servoStr ="%u=%u\n" % (self._servo_number, int(duty_us*0.1))
            print(servoStr)
            with open("/dev/servoblaster", "wb") as f:
                f.write(servoStr.encode())
        if servo == 2:
            servoStr ="%u=%u\n" % (self._servo_number, angle2)
            print(servoStr)
            with open("/dev/servoblaster", "wb") as f:
                f.write(servoStr.encode())
    def update2(self,duty_us):
        servoStr = "%u=%u\n" %(self._servo_number, int(duty_us*0.1)
                               )
        with open("/dev/servoblaster", "wb") as f:
                f.write(servoStr.encode())
            
    
            
class ServoAngle():
    def __init__(self, gpio_port, angle_min, angle_max, min_duty, max_duty, ini_angle):
        self._gpio_port = gpio_port
        
        self._angle_to_duty = (max_duty - min_duty)/(angle_max - angle_min)
        self._duty_min        = min_duty
        self._angle_min        = angle_min
        self._angle_max        = angle_max
        
        self._angle = ini_angle
        
        self._servo            = ServoBlaster(gpio_port)
        
    def angle_to_duty(self, angle):
        duty = (angle - self._angle_min)*self._angle_to_duty + self._duty_min
        return (duty)
        
    def update(self, angle, servo, angle2):
        self._servo.update(self.angle_to_duty(angle), servo, angle2)
        self._angle = angle
    def update2(self, angle):
        self._servo.update2(self.angle_to_duty(angle))
        self._angle = angle
        
    def set_to_min(self):
        self.update2(self._angle_min)
        
    def set_to_max(self):
        self.update2(self._angle_max)    
        
    def set_to_middle(self):
        self.update2((self._angle_min + self._angle_max)*0.5)   

    @property
    def angle(self):
        return(self._angle)
        
    @property
    def angle_min(self):
        return(self._angle_min)
        
    @property
    def angle_max(self):
        return(self._angle_max)        
    
        
if __name__ == "__main__":
    import time
    #-- ROS Convention: counter clockwise is positive (left positive, right negative)
    servo_angle = ServoAngle(23, -85, 85, 2250, 750)
    
    angle = -85
    sleep = 0.01
    step = 2
    
    servo_angle.update(angle)
    time.sleep(1)
    
    while True:
        angle += step
        
        if angle > 85: 
            angle = -85
            print("Update Here")
        
        print ("%.0f"%angle)
        servo_angle.update(angle)
        
        if angle == -85:
            time.sleep(1)
        time.sleep(sleep)
