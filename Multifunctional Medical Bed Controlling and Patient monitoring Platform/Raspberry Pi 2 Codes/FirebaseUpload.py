from firebase import firebase
import time
import serial
import datetime as dt

ser=serial.Serial('/dev/ttyUSB0',9600)
time.sleep(1)
ser.flushInput()

firebase = firebase.FirebaseApplication('https://patient-monitoring-syste-6132a.firebaseio.com/')

dataAr=[0,0,0,0,0,0,0,0]
uploadEnable=True

while True:
    temparray = [int(x) for x in str(ser.readline()).split("^")[1:-1]]
    print (temparray)
    now=datetime.now()
    if uploadEnable:
        resultHalf = firebase.post('patientMonitor',{'datetime':now.strftime("%d/%m/%Y %H:%M:%S"),'us1':str(dataAr[0]),'us2':str(dataAr[1]),'toco':str(dataAr[2])})
        #result = firebase.post('patientMonitor',{'datetime':now.strftime("%d/%m/%Y %H:%M:%S"),'us1':str(dataAr[0]),'us2':str(dataAr[1]),'toco':str(dataAr[2]),'ECG':str(dataAr[3]),'Spo2':str(dataAr[4]),'Art':str(dataAr[5]),'Resp':str(dataAr[6])})
