import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as rc522
reader = rc522()

def rade_data():
	try:
		print("begin reading")
		id, data = reader.read()
		print("id is: "+str(id))
		print("data is: "+str(data))

	except Exception as error:
		print("error happened:"+str(error))
					
	finally:
		GPIO.cleanup()


def write_data():
	try:
		data=raw_input('input data:')
		print( 'input data is:'+ data)
		print( "place your card to write")
		reader.write(data)
		print( "write success")

	except Exception as error:
		print( "error happened:"+ str (error ))
	finally:
		GPIO.cleanup()


def main():
	print('***************************************************')
	print('*                                                 *')
	print('*             welcome to Miracle_SS               *')
	print('*                                                 *')
	print('***************************************************')



	while(1):

		i = input('Please choose the function you want:')
		if int(i) == 1:
			rade_data()
			continue
		elif int(i) == 2:
			write_data()
			continue
		elif int(i) == 0:
			print('Thank for you use!')
			break


main()
