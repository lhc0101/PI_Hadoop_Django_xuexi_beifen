import RPi.GPIO as GPIO 
from mfrc522 import SimpleMFRC522 as rc522
reader=rc522()
try: 
	data=raw_input("input data:") 
	print("input data is:"+ data)
	print("place your card to write")
	reader. write(data)
	print("write success")
except Exception as error: 
	print("error happened:"+str(error))
finally: GPIO.cleanup()