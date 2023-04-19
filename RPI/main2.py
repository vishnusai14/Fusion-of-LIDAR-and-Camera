import servo as sb
import tfmini
import time
import math
import socket
import pickle
server_port = 2222
server_ip = '172.31.44.94' 
buffer_size = 1024

rpi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rpi_socket.bind((server_ip, server_port))

class TfminiServoScanner():
    def __init__(self, 
        servo1_gpio,        #- [ ]      Gpio port assigned to the servo1
        servo2_gpio,        #- [ ]      Gpio port assigned to the servo2
        angle_min1=-0,    #- [deg]    Minimum angle of the servo1
        angle_max1=90,     #- [deg]    Maximum angle of the servo1
        angle_min2 = 50,   #- [deg]    Minimum angle of the servo2
        angle_max2 = 150,  #- [deg]    Maximum angle of the servo2
        duty_min1=250,    #- [us]     duty cycle corresponding to minimum angle1
        duty_max1=2000,    #- [us]     duty cycle corresponding to minimum angle1
        duty_min2=1000,    #- [us]     duty cycle corresponding to minimum angle2
        duty_max2=2000,    #- [us]     duty cycle corresponding to minimum angle2
        n_steps=10,         #- [ ]      number of measurements in the min-max range
        time_min_max=0.5,   #- [s]      time for the servo to move from min to max
        serial_port="/dev/ttyAMA0"      # serial port for tfmini
        ):
    
        #-- Create an object servo
        self.servo1 = sb.ServoAngle(servo1_gpio, angle_min1, angle_max1, duty_min1, duty_max1, 60)

        self.servo2 = sb.ServoAngle(servo2_gpio, angle_min2, angle_max2, duty_min2, duty_max2, 150)
        
        #-- Create an object laser
        self.laser = tfmini.TfMini(serial_port)
      
        #-- Calculate the angle step
        self._delta_angle1   = (angle_max1 - angle_min1)/(n_steps - 1)
        print((angle_max2 - angle_min2) / (n_steps - 1))
        print(n_steps)
        self._delta_angle2   = 10
        print("This is the self._delta_angle2 " + str(self._delta_angle2))
        
        #-- Calculate the servo speed
        self._time_min_max  = time_min_max
        self._servo_speed1   = (angle_max1 - angle_min1)/time_min_max
        self._servo_speed2   = (angle_max2 - angle_min2)/time_min_max
    
        #-- Calculate the minimum pause after each step command
        self._min_time_pause1     = self._delta_angle1/self._servo_speed1
        self._min_time_pause2     = self._delta_angle2/self._servo_speed2
        
        #-- initialize the rotational direction to 1
        self._move_dir1 = 1;
        self._move_dir2 = 1;
        
    def read_laser(self):       #- Read the laser and return the value
        return(self.laser.get_data())
        
    def reset_servo1(self):      #- Set the servo1 to min angle position
        self.servo1.set_to_min()
        self._move_dir1 = 1;
        time.sleep(self._time_min_max)

    def reset_servo2(self):      #- Set the servo2 to min angle position
        self.servo2.set_to_min()
        self._move_dir2 = 1;
        time.sleep(self._time_min_max)
            
    def move_servo1(self):       #- move the servo of one step
        angle1 = self.angle1
    
        #-- When reached the end, change direction
        if angle1 >= self.servo1.angle_max - self._delta_angle1:
            self._move_dir1 = -1
        
        if angle1 <= self.servo1.angle_min + self._delta_angle1:
            self._move_dir1 = 1    

        #- Get the commanded angle
        angle1 += self._delta_angle1*self._move_dir1
        
        #- Command the servo
        self.servo1.update(angle1 ,1, 0)
        
        #- Sleep
        time.sleep(self._min_time_pause1)
        
    def move_servo2(self):       #- move the servo of one step
        print("Moving Servo 2")
        angle2 = self.angle2
        print("This is the angle " + str(angle2))
        if angle2 == 100:
            angle2 = 50
        else :
            angle2 = angle2 + self._delta_angle2
        #-- When reached the end, change direction
        #if angle2 >= self.servo2.angle_max - self._delta_angle2:
        #self._move_dir2 = -1
        
        #if angle2 <= self.servo2.angle_min + self._delta_angle2:
        #	self._move_dir2 = 1    
        #print("This is the self._delta_angle2" + str(self._delta_angle2))
        #- Get the commanded angle
        #angle2 += self._delta_angle2*self._move_dir2
        #print("Updated angle" + str(angle2))
        #- Command the servo
        self.servo2.update(angle2,2,angle2)
        
        #- Sleep
        time.sleep(self._min_time_pause2)
        
    def scan(self, scale_factor=1.0, reset=False):
        if reset: 
            self.reset_servo1()
            #self.reset_servo2()
            ini_angle1 = self.angle1
            ini_angle2 = self.angle2
        
            self.servo1.update2(ini_angle1)
            self.servo2.update2(ini_angle2)
        
            ranges    = []
            angles    = []
            angle     = ini_angle1
            move_dir1 = self._move_dir1
            time_init = time.time()
        
        while True:
            dist  = self.read_laser()*scale_factor
            angle1 = self.angle1
            angle2 = self.angle2
            angle2 = 50
            print("d = %4.2f  a = %4.2f"%(dist, self.angle1))
            #msg = "d = " + str(dist) + " " + "a = " + str(self.angle) 
            #message, address = rpi_socket.recvfrom(buffer_size)
            #byte_to_send = str(msg).encode('utf-8')
            #rpi_socket.sendto(byte_to_send, address)
            ranges.append(dist)
            angles.append(angle1)

            self.move_servo1()

            #-- If changed sign: break
            if move_dir1*self._move_dir1 < 0:
                break
        #self.move_servo2()
        time_increment  = (time.time() - time_init)/(len(ranges) - 1)
        angle_increment = (angle1 - ini_angle1)/(len(ranges) - 1 )
        
        obj = {
            "ini_angle":ini_angle1,
            "angle1" :angle1,
            "angle2" : angle2,
            "angles" : angles,
            "time_increment":time_increment,
            "angle_increment":angle_increment,
            "ranges":ranges,
            "distance_min" : self.laser.distance_min,
            "distance_max" : self.laser.distance_max
            }
        print(obj)
        encode_obj = pickle.dumps(obj)
        message, address = rpi_socket.recvfrom(buffer_size)
        rpi_socket.sendto(encode_obj, address)

        
        return(ini_angle1, angle, time_increment, angle_increment, ranges)
        
    @property
    def angle1(self):
        return(self.servo1.angle)
    @property
    def angle2(self):
        return(self.servo2.angle)
        
    @property
    def time_between_measurements1(self):
        return(self._min_time_pause1)

    @property
    def time_between_measurements2(self):
        return(self._min_time_pause2)
        
    @property
    def step1(self):
        return(self._delta_angle1)
        
    @property
    def step2(self):
        return(self._delta_angle2)

        
if __name__ == "__main__":
    #-- Convention: counter clockwise is positive (left positive, right negative)
    tfminiscanner = TfminiServoScanner(23, 22, -90, 180, 50, 120, 1750, 1000, 2250, 750, 20, 0.5)
    
    tfminiscanner.reset_servo1()
    time.sleep(1)
    
    while True:
        tfminiscanner.scan(reset=True)
        
