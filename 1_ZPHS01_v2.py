import serial
import time
import subprocess
import traceback
import getrpimodel
import struct
import platform
import sys
import json
import os.path
import requests
import RPi.GPIO as GPIO
# codigo base gracias a UedaTakeyuki github
# setting
version = "3.1.3"
pimodel        = getrpimodel.model()
pimodel_strict = getrpimodel.model_strict()
retry_count    = 3
# setting

if os.path.exists('/dev/serial0'):
  partial_serial_dev = 'serial0'
elif pimodel == "3 Model B" or pimodel == "4 Model B" or pimodel_strict == "Zero W":
  partial_serial_dev = 'ttyS0'
else:
  partial_serial_dev = 'ttyAMA0'

serial_dev = '/dev/%s' % partial_serial_dev
#stop_getty = 'sudo systemctl stop serial-getty@%s.service' % partial_serial_dev
#start_getty = 'sudo systemctl start serial-getty@%s.service' % partial_serial_dev

# major version of running python
p_ver = platform.python_version_tuple()[0]


def start_getty():
  start_getty = ['sudo', 'systemctl', 'start', 'serial-getty@%s.service' % partial_serial_dev]
  p = subprocess.call(start_getty)

def stop_getty():
  stop_getty = ['sudo', 'systemctl', 'stop', 'serial-getty@%s.service' % partial_serial_dev]
  p = subprocess.call(stop_getty)


def connect_serial():
  return serial.Serial(serial_dev,
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1.0)


def read_concentration():
  try:
    ser = connect_serial()
    for retry in range(retry_count):
      result=ser.write(b"\x11\x02\x01\x00\xec\x00\x00\x00\x00")# Send： 11 02 01 00 EC measurement
      #result=ser.write(b"\x11\x03\x03\x01\x90\x58\x00\x00\x00")#CO2 zero point calibration,respond： 16 01 03 E6//
      #result=ser.write(b"\x11\x03\x0c\x02\x1e\xc0\x00\x00\x00")# start dust measurement,Respond： 16 02 0C 02 DA //the module is in “on-state dust measurement” 
      #result=ser.write(b"\x11\x03\x0c\x01\x1e\xc1\x00\x00\x00")# stop dust measurement,Respond： 16 02 0C 01 DB //the module is in “off-state dust measurement”
      #print(result)
      s=ser.read(14)
      #print(len(s))
      #print(s)
      #print(s[0])

      #print('check',s[13])

      if p_ver == '2':
        if len(s) >= 9 and s[0] == "\xff" and s[1] == "\x86" and checksum(s[1:-1]) == s[-1]:
          return {'PM2.5': ord(s[3]) +ord(s[4]),
                  'PM10': ord(s[4]) + ord(s[5]),
                  'PM1.0': ord(s[6]) + ord(s[7]),
                  'PM2.5_0': ord(s[2]),
                  'PM10_0': ord(s[4]),
                  'PM1.0_0':ord(s[6])
                  }
      else:
        if len(s) >= 9 and s[0] == 0x16 and s[1] == 0x0B and s[2] == 0x01  and (checksum2(s[0:-1])) == (s[-1]):
          
          return  {'CO2': s[3]*256 + s[4],
                  'VOC': s[5]*256 + s[6],
                  'Humidity': s[7]*256 + s[8],
                  'Tempe': (s[9]*256+s[10]-500)/10,
                  'PM2.5': s[11]*256+s[12]
                  }
        print('hola3')
  except:
     traceback.print_exc()
  return ""

def zh07():
  pm25 = read_concentration()
  #print(pm25)
  if not pm25:
    return {}
  else:
    return pm25

def read(serial_console_untouched=False):
  if not serial_console_untouched:
    stop_getty()

  result = zh07()

  if not serial_console_untouched:
    start_getty()
  return result
  if result is not None:
     return result


def checksum(array):
  if p_ver == '2' and isinstance(array, str):
    array = [ord(c) for c in array]
  csum = sum(array) % 0x100
  #print(csum)
  if csum == 0:
    return struct.pack('B', 0)
  else:
    return struct.pack('B', 0xff - csum+1)
def checksum2(array):
  if p_ver == '2' and isinstance(array, str):
    array = [ord(c) for c in array]
  csum = sum(array)% 0x100
  if csum == 0:
    return struct.pack('B', 0)
  else:
    #return struct.pack('B', csum)
    return (0xff-csum+1)

if __name__ == '__main__':
#  value = read()
#  print (value)
   while True:
      value = read()
      if value is not None:
         try:
            print ("Co2=", value["CO2"],"TVOC=",value['VOC'],"Humidity=",value['Humidity'],"Tempe=",value['Tempe'],"PM 2.5=",value['PM2.5'])
            #enviar_apiv1(value)
         except Exception as e:
            print('Error data check .....trying again...')      #error
            
      else:
         print ("None")
      time.sleep(2)

sys.exit(0)
