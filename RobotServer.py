from socket import socket
from loguru import logger
import numpy
import cv2

# https://stackoverflow.com/questions/20820602/image-send-via-tcp
# host = "192.168.1.29"
host = "localhost"
port = 8123
enc = "utf-8"

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

sock = socket()
sock.bind((host, port))
logger.info("SERVER START")
sock.listen(1)
robot = sock.accept()[0]
logger.info("ROBOT CONNECTED")


while True:
    length = recvall(robot,16)
    if length:
        stringData = recvall(robot, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        decimg=cv2.imdecode(data,1)
        cv2.imshow('SERVER',decimg)
    if cv2.waitKey(1) == ord('q'):
        pass

logger.info("ROBOT DISCONNECTED")