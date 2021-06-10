import socket
import cv2
import pickle
import struct

# Socket Create
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('192.168.56.1', 5490))
server.listen(5)

while True:
    receiver, addr = server.accept()
    if receiver:
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            img,frame = cap.read()
            cphoto = frame[100:400 ,200:500]
            rphoto = cv2.resize(cphoto ,(100,100))
            frame[0:100 ,0:100] = rphoto
            grey_photo = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB )
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            receiver.sendall(message)
            cv2.imshow('Video from Server',frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key ==ord('q'):
                receiver.close()