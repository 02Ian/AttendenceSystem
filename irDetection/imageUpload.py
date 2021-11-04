from datetime import datetime

import boto3
import time  # Required to use delay functions
import serial
import cv2
from csv import writer
from botocore.client import Config

ArduinoSerial = serial.Serial('com3', 9600)  # Create Serial port object called arduinoSerialData

if not ArduinoSerial.isOpen():
    ArduinoSerial.open()
time.sleep(2)  # wait for 2 secounds for the communication to get established
print("scan")

# print(ArduinoSerial.readline())
ardinosInput = ArduinoSerial.readline()
# print(ardinosInput)
if ardinosInput.find("in".encode()):
    print("No 'in' here!")
else:
    videoCaptureObject = cv2.VideoCapture(0)
    result = True
    while (result):
        ret, frame = videoCaptureObject.read()
        cv2.imwrite("C:/Users/abhis/PycharmProjects/Signal/SavedImages/CapturedImage.jpg", frame)
        result = False
    videoCaptureObject.release()
    cv2.destroyAllWindows()


def markAttendance(strName):
    # Import writer class from csv module
    # List
    datetimeEntryValue = datetime.datetime.now()
    convertedFormat = datetimeEntryValue.strftime("%b-%d-%Y %H:%M:%S")
    strNameCsvData = strName.split("@")
    locationCsvData = strNameCsvData[1].split(".")

    List = [strNameCsvData[0], locationCsvData[0], convertedFormat, datetimeEntryValue.strftime("%A")]

    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open("C:/Users/abhis/PycharmProjects/Signal/Attendence.csv", 'a') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)

        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(List)

        # Close the file object
        f_object.close()


def face_comparision():
    strName = "NotFound"
    ACCESS_KEY_ID = 'AKIATTDRTDVKCAQA4GHT'
    ACCESS_SECRET_KEY = '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'
    BUCKET_NAME = 'facerekognition04'
    BUCKET_NAME1 = 'capturedimage'

    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )

    client = boto3.client('s3', region_name='us-west-2')
    client.upload_file('C:/Users/abhis/PycharmProjects/Signal/SavedImages/CapturedImage.jpg', BUCKET_NAME1,
                       'CapturedImage.jpg')
    client = boto3.client('rekognition', region_name='us-east-2')

    objects = s3.list_objects(Bucket=BUCKET_NAME)["Contents"]
    print(objects)
    for objectElement in objects:
        response = client.compare_faces(
            SourceImage={
                'S3Object': {
                    'Bucket': BUCKET_NAME1,
                    'Name': 'CapturedImage.jpg'  # CapturedImage.jpg
                }
            },
            TargetImage={
                'S3Object': {
                    'Bucket': BUCKET_NAME,
                    'Name': objectElement["Key"]
                }
            },
        )
        if len(response['FaceMatches']) > 0:
            if (response['FaceMatches'][0]['Similarity'] > 80):
                strName = objectElement["Key"]
                break
    return response['SourceImageFace'], response['FaceMatches'], strName


source_face, matches, strName = face_comparision()

print("Source Face ({Confidence}%)".format(**source_face))
print(strName)
for match in matches:
    print("Target Face ({Confidence}%)".format(**match['Face']))
    print("  Similarity : {}%".format(match['Similarity']))

markAttendance(strName)

if (strName == "NotFound"):
    ArduinoSerial.write(str.encode('0'))  # send 0
    print("LED turned OFF")
else:
    ArduinoSerial.write(str.encode('1'))  # send 1
    markAttendance(strName)
    print("LED turned ON")





