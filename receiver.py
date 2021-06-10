
import socket
import cv2
import pickle
import struct

receiver = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
receiver.connect(("192.168.56.1", 5490))

data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = receiver.recv(4096)
        
        if not packet: 
            break
        data+=packet
    packed_msg = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg)[0]
    
    while len(data) < msg_size:
        data += receiver.recv(4096)
    frame = data[:msg_size]
    data  = data[msg_size:]
    video = pickle.loads(frame)
    cv2.imshow("Video from receiver",video)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break
receiver.close()