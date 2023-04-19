# import rospy
# from sensor_msgs.msg import LaserScan
import socket
import pickle
import math


import math

SERVO_GPIO          = 23
SRV_ANGLE_MIN       = math.radians(-85)
SRV_ANGLE_MAX       = math.radians(85)
SRV_DUTY_ANGLE_MIN  = 2250
SRV_DUTY_ANGLE_MAX  = 750
SRV_TIME_MIN_MAX    = 0.4
LASER_ANGLE_SAMPLES = 50
FILE_NAME = 'data.csv'
FILE_NAME_2 = 'data2.csv'


def tfmini_laserscan_publisher(frame_id):

    # scan_pup= rospy.Publisher('tfmini_laser', LaserScan, queue_size=0)

   
    # scan  = LaserScan()

    # scan.header.frame_id   = frame_id; 
    #-- Convention: counter clockwise is positive (left positive, right negative)

    xyz = []                            
    scan_num = 0            
    #-- Initialize the message

    while 1:
        try:
            msg = "need data"
            byte_to_send = msg.encode('utf-8')
            server_address = ('192.168.129.94', 2222)
            buffer_size = 1024
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.sendto(byte_to_send, server_address)
            data, address = client.recvfrom(buffer_size)
            data = pickle.loads(data)
            #print(data)
            ini_angle = math.radians(data['ini_angle'])
            end_angle = math.radians(data['angle1'])
            time_increment = data['time_increment']
            angle_increment = math.radians(data['angle_increment'])
            ranges = data['ranges']
            # scan.range_min = data['distance_min']*0.01
            angles = data['angles']
            angle2 = data['angle2']
            #print(ranges)
            #print(angles)
            #print(angle2)
            rthetha = []
            
            for i in range(len(ranges)):
                x = ranges[i] * math.cos(math.radians(angles[i]))
                y = ranges[i] * math.sin(math.radians(angles[i]))
                distance = ranges[i]
                # x = ranges[i] * math.sin(math.radians(angles[i])) * math.cos(math.radians(angle2))
                # y = ranges[i] * math.sin(math.radians(angles[i])) * math.sin(math.radians(angle2))
                # z = ranges[i] * math.cos(math.radians(angles[i]))
                # rthetha.append([ranges[i], angles[i]])
                print((x,y,distance))
                # xyz.append((x,y,z))
                # with open(FILE_NAME, 'a') as csvfile:
                #     csvwriter = csv.writer(csvfile)
                #     csvwriter.writerow([x, y, z])
                # with open(FILE_NAME_2, 'a') as csvfile2:
                #     csvwriter = csv.writer(csvfile2)
                #     csvwriter.writerow([ranges[i], angles[i]])

            scan_num += 1
            print("Total Number of Scan : " + str(scan_num))
            # scan.range_max = 100
            # scan.angle_min = ini_angle
            # scan.angle_max = end_angle
            # scan.angle_increment = angle_increment
            # scan.time_increment = time_increment
            # scan.ranges = ranges
            

            # scan_pup.publish(scan)
        except KeyboardInterrupt:
            break



if __name__ == "__main__":
    # rospy.init_node("tfmini_laserscan")
    tfmini_laserscan_publisher(frame_id="map")