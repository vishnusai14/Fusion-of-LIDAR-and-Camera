import socket 
import time
buffer_size = 1024
msg = 'Heoolllo'
server_port = 2222
server_ip = '192.168.0.106'
byte_to_send = msg.encode('utf-8')
rpi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rpi_socket.bind((server_ip, server_port))
print("server is up")
message, address = rpi_socket.recvfrom(buffer_size)
print(address)
rpi_socket.sendto(byte_to_send, address)
