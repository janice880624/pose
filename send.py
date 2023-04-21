import socket
import cv2
import math
import pickle
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
cap = cv2.VideoCapture(0)
print(cap.isOpened())
ret,frame = cap.read()
print(ret)
max_length = 65000
ip = "192.168.101.201"
PORT = 5001

while True:

    ret,frame = cap.read()
    retval, buffer = cv2.imencode(".jpg", frame)
    if retval:
        # convert to byte array
        buffer = buffer.tobytes()
        # get size of the frame
        buffer_size = len(buffer)
        num_of_packs = 1
        if buffer_size > max_length:
            num_of_packs = math.ceil(buffer_size/max_length)
        frame_info = {"packs":num_of_packs}
        # send the number of packs to be expected
        send_time = time.time()
        info = {'frame_info':frame_info,'send_time':round(send_time,5)}
        s.sendto(pickle.dumps(info), (ip, PORT))
        left = 0
        right = max_length
        for i in range(num_of_packs):
            # truncate data to send
            data = buffer[left:right]
            left = right
            right += max_length
            # send the frames accordingly
            s.sendto(data, (ip,PORT))
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

