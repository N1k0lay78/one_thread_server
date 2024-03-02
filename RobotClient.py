from socket import socket
import cv2
import numpy
from time import time, sleep

host = "192.168.1.29"
host = "localhost"
port = 8123
enc = "utf-8"

conn = socket()
conn.connect((host, port))
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()

    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()

    conn.send( bytes(str(len(stringData)).ljust(16), enc))
    conn.send( stringData);
    

conn.close()