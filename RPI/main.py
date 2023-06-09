
import servo as sb
import tfmini
import time
import math
import socket
import pickle
server_port = 2222
server_ip = '192.168.0.102'
buffer_size = 1024

#rpi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#rpi_socket.bind((server_ip, server_port))

class TfminiServoScanner():
	def __init__(self, 
		servo_gpio,         #- [ ]      Gpio port assigned to the servo 
		angle_min=-90,      #- [deg]    Minimum angle of the servo
		angle_max=90,       #- [deg]    Maximum angle of the servo
		duty_min=1000,      #- [us]     duty cycle corresponding to minimum angle
		duty_max=2000,      #- [us]     duty cycle corresponding to minimum angle
		n_steps=10,         #- [ ]      number of measurements in the min-max range
		time_min_max=0.5,   #- [s]      time for the servo to move from min to max
		serial_port="/dev/ttyAMA0"      # serial port for tfmini
		):
    
		#-- Create an object servo
		self.servo = sb.ServoAngle(servo_gpio, angle_min, angle_max, duty_min, duty_max)
        
		#-- Create an object laser
		self.laser = tfmini.TfMini(serial_port)
      
		#-- Calculate the angle step
		self._delta_angle   = (angle_max - angle_min)/(n_steps - 1)
        
		#-- Calculate the servo speed
		self._time_min_max  = time_min_max
		self._servo_speed   = (angle_max - angle_min)/time_min_max
        
		#-- Calculate the minimum pause after each step command
		self._min_time_pause     = self._delta_angle/self._servo_speed
        
		#-- initialize the rotational direction to 1
		self._move_dir = 1;
        
	def read_laser(self):       #- Read the laser and return the value
		return(self.laser.get_data())
        
	def reset_servo(self):      #- Set the servo to min angle position
		self.servo.set_to_min()
		self._move_dir = 1;
		time.sleep(self._time_min_max)
        
	def move_servo(self):       #- move the servo of one step
		angle = self.angle
        
		#-- When reached the end, change direction
		if angle >= self.servo.angle_max - self._delta_angle:
			self._move_dir = -1
        
		if angle <= self.servo.angle_min + self._delta_angle:
			self._move_dir = 1    

		#- Get the commanded angle
		angle += self._delta_angle*self._move_dir
        
		#- Command the servo
		self.servo.update(angle)
        
		#- Sleep
		time.sleep(self._min_time_pause)
        
	def scan(self, scale_factor=1.0, reset=False):
		if reset: 
			self.reset_servo()
        
			ini_angle = self.angle
        
			self.servo.update(ini_angle)
        
			ranges    = []
			angle     = ini_angle
			move_dir  = self._move_dir
			time_init = time.time()
        
		while True:
			dist  = self.read_laser()*scale_factor
			angle = self.angle
			print("d = %4.2f  a = %4.2f"%(dist, self.angle))
			#msg = "d = " + str(dist) + " " + "a = " + str(self.angle) 
			#message, address = rpi_socket.recvfrom(buffer_size)
			#byte_to_send = str(msg).encode('utf-8')
			#rpi_socket.sendto(byte_to_send, address)
			ranges.append(dist)

			self.move_servo()

            #-- If changed sign: break
			if move_dir*self._move_dir < 0:
				break
                
		time_increment  = (time.time() - time_init)/(len(ranges) - 1)
		angle_increment = (angle - ini_angle)/(len(ranges) - 1 )
		
		obj = {
			"ini_angle":ini_angle,
			"angle" :angle,
			"time_increment":time_increment,
			"angle_increment":angle_increment,
			"ranges":ranges,
			"distance_min" : self.laser.distance_min,
			"distance_max" : self.laser.distance_max
		}
		print(obj)
		encode_obj = pickle.dumps(obj)
		#message, address = rpi_socket.recvfrom(buffer_size)
		#rpi_socket.sendto(encode_obj, address)
		
        
		return(ini_angle, angle, time_increment, angle_increment, ranges)
        
	@property
	def angle(self):
		return(self.servo.angle)
        
	@property
	def time_between_measurements(self):
		return(self._min_time_pause)
        
	@property
	def step(self):
		return(self._delta_angle)
        
        
if __name__ == "__main__":
    #-- Convention: counter clockwise is positive (left positive, right negative)
	tfminiscanner = TfminiServoScanner(23, -85, 85, 2250, 750, 20, 0.5)
    
	tfminiscanner.reset_servo()
	time.sleep(1)
    
	while True:
		tfminiscanner.scan(reset=True)
        
