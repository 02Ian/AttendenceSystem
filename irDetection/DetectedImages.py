import time  # Required to use delay functions

import serial
import cv2
import os

ArduinoSerial = serial.Serial('com3', 9600)  # Create Serial port object called arduinoSerialData
if not ArduinoSerial.isOpen():
    ArduinoSerial.open()
time.sleep(2)  # wait for 2 secounds for the communication to get established

print(ArduinoSerial.readline())
ardinosInput = ArduinoSerial.readline()
print(ardinosInput)
if ardinosInput.find("in".encode()):
    print("No 'in' here!")
else:
    videoCaptureObject = cv2.VideoCapture(0)
    result = True
    while(result):
        ret,frame = videoCaptureObject.read()
        cv2.imwrite("C:/Users/abhis/PycharmProjects/Signal/SavedImages/CapturedImage.jpg",frame)
        result = False
    videoCaptureObject.release()
    cv2.destroyAllWindows()

os.system('python imageUpload.py')
