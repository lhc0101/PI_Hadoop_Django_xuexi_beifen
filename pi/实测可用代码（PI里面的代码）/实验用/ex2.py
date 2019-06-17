import RPi.GPIO as GPIO 
from mfrc522 import SimpleMFRC522 as rc522
reader=rc522()
try: 
	print("begin reading")
	id, data=reader.read()
	print("id is"+str(id))
	print("data is"+str(data)) 
except Exception as error: 
	print("error happened:"+str(error))
finally: 
	GPIO.cleanup()