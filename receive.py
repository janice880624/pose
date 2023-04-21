
import numpy as np
import socket
import pickle
import cv2
import time
import mediapipe as mp
PORT = 5001
ip = '192.168.101.201'
max_length = 65540
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((ip, PORT))

frame_info = None
buffer = None
frame = None

# mp_holistic = mp.solutions.holistic
# holistic = mp_holistic.Holistic(
#     min_detection_confidence=0.5, min_tracking_conf%idence=0.5)
# mpDraw = mp.solutions.drawing_utils

while True:
    data, address = s.recvfrom(max_length)
    if len(data) < 100:
        info = pickle.loads(data)
        receive_time = time.time()
        send_time = info['send_time']
        frame_info = info['frame_info']
        transmission_time = round(receive_time-send_time, 5)
        if frame_info:
            nums_of_packs = frame_info["packs"]
            for i in range(nums_of_packs):
                data, address = s.recvfrom(max_length)
                if i == 0:
                    buffer = data
                else:
                    buffer += data
            frame = np.frombuffer(buffer, dtype=np.uint8)
            frame = frame.reshape(frame.shape[0], 1)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            frame = cv2.flip(frame, 1)
            if frame is not None and type(frame) == np.ndarray:
                # result = holistic.process(frame)
                # mpDraw.draw_landmarks(
                #     frame, result.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                # mpDraw.draw_landmarks(
                #     frame, result.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                # mpDraw.draw_landmarks(
                #     frame, result.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                process_time = time.time()
                cv2.putText(frame, 'Transmission Time:'+str(transmission_time),
                            (10, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, 'Process Time:'+str(round(process_time - send_time, 5)),
                            (10, 80), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow("Stream", frame)
                if cv2.waitKey(1) == 27:
                    break
