import socket
import pickle
import cv2
import threading
import csv
import ast
import numpy as np
import math


FILE_NAME = 'data.csv'


def draw_counter(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh_frame = cv2.threshold(gray_frame, 25, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((5, 5), np.uint8)
    thresh_frame = cv2.morphologyEx(thresh_frame, cv2.MORPH_OPEN, kernel)
    counters = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    counters = counters[0] if len(counters) == 2 else counters[1]
    blank_image = np.ones((450, 600, 3), np.uint8)

    # Set the minimum area for a contour
    min_area = 5000

    # Draw the contours on the original image and the blank image
    for c in counters:
        area = cv2.contourArea(c)
        if area > min_area:
            cv2.drawContours(frame, [c], 0, (36, 255, 12), 2)
            cv2.drawContours(blank_image, [c], 0, (255, 255, 255), 2)


def write_points(frame):
    with open(FILE_NAME, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            for p in row:
                point = ast.literal_eval(p)
                cv2.putText(frame, str(point[2]), (int(point[0]) + 90, int(point[1]) + 300),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (209, 80, 0, 255), 1)


def camera_view(vcap):
    while True:
        ret, frame = vcap.read()
        if frame is not None:
            write_points(frame)
            draw_counter(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(22) & 0xFF == ord('q'):
                break
        else:
            print("Frame is None")
            break
    vcap.release()
    cv2.destroyAllWindows()


def tfmini_laser_scan_publisher():
    # scan_pup= rospy.Publisher('tfmini_laser', LaserScan, queue_size=0)

    # scan  = LaserScan()

    # scan.header.frame_id   = frame_id; 
    # -- Convention: counter clockwise is positive (left positive, right negative)

    scan_num = 0
    # -- Initialize the message

    while 1:
        xyz = []
        try:
            msg = "need data"
            byte_to_send = msg.encode('utf-8')
            server_address = ('172.31.44.94', 2222)
            buffer_size = 1024
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.sendto(byte_to_send, server_address)
            data, address = client.recvfrom(buffer_size)
            data = pickle.loads(data)
            # print(data)
            # ini_angle = math.radians(data['ini_angle'])
            # end_angle = math.radians(data['angle1'])
            # time_increment = data['time_increment']
            # angle_increment = math.radians(data['angle_increment'])
            ranges = data['ranges']
            # scan.range_min = data['distance_min']*0.01
            angles = data['angles']
            # angle2 = data['angle2']
            # print(ranges)
            # print(angles)
            # print(angle2)

            print(xyz)
            for i in range(len(ranges)):
                if angles[i] == -90 or angles[i] == 90:
                    x = 0
                else:
                    x = ranges[i] * math.cos(math.radians(angles[i]))
                if angles[i] == 0:
                    y = 0
                else:
                    y = ranges[i] * math.sin(math.radians(angles[i]))
                distance = ranges[i]

                if i > 1:
                    if not (abs(ranges[i] - ranges[i - 1]) < 30):
                        xyz.append([x, y, distance])
                else:
                    xyz.append([x, y, distance])
                # xyz.append((x,y,z))
            # print(xyz)

            with open(FILE_NAME, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(xyz)
                # with open(FILE_NAME_2, 'a') as csvfile2:
                #     csvwriter = csv.writer(csvfile2)
                #     csvwriter.writerow([ranges[i], angles[i]])
            # points = xyz
            scan_num += 1
            # print("Total Number of Scan : " + str(scan_num))
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
    thread1 = threading.Thread(target=tfmini_laser_scan_publisher)
    thread1.start()

    thread2 = threading.Thread(target=camera_view, args=(cv2.VideoCapture('http://mypi:8080/?action=stream'),))
    thread2.start()
