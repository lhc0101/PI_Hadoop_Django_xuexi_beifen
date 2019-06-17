import RPi.GPIO 
import time 
import datetime 

GPIO_DHT11=20
GPIO_LED=11
SLEEP_SECOND = 2
LED_OPENED=True 
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(GPIO_LED,RPi.GPIO.OUT)
RPi.GPIO.output(GPIO_LED,RPi.GPIO.HIGH)
def setupDHT11():
	RPi.GPIO.setup(GPIO_DHT11,RPi.GPIO.OUT)
	RPi.GPIO.output(GPIO_DHT11,RPi.GPIO.LOW)
	time.sleep(0.02)
	RPi.GPIO.output(GPIO_DHT11,RPi.GPIO.HIGH)
	RPi.GPIO.setup(GPIO_DHT11,RPi.GPIO.IN)
def read():
	data=[]
	while RPi. GPIO.input(GPIO_DHT11)==RPi.GPIO.LOW: 
		continue 
	while RPi. GPIO.input(GPIO_DHT11)==RPi.GPIO.HIGH: 
		continue 
	j=0
	whilej<40: 
		k=8
		while RPi.GPIO.input(GPIO_DHT11)==RPi.GPIO.LOW: 
			continue 
		while RPi.GPIO.input(GPIO DHT11)==RPi.GPIO.HIGH: 
			k+=1
			if k>180: 
				break 
		if k<8: 
			data.append(e)
		else: 
			data.append(1)
		j+=1
	return data
def checkData(data): 
	globa1 LED_OPENED 
	humidity_bit=data[0:8]
	humidity_point_bit =data[8:16]
	temperature_bit =data[16:24]
	temperature_point_bit=data[24:32]
	check_bit=data[32:40]
	humidity=0 
	humidity_point=0 
	temperature=0 
	temperature_point=0
	check=0 
	for i in range(8): 
		humidity+=humidity_bit[i]*2**(7-i)
		humidity_point+=humidity_point_bit[i]*2 **(7-i)
		temperature+=temperature_bit[i]2**(7-i)
		temperature_point+=temperature_point_bit[i]*2**(7-i)
		check+=check_bit[i]*2**(7-i)
	tmp=humidity+humidity_point+temperature+temperature_point 
	if check==tmp: 
		if not LED_OPENED: 
			RPi.GPTO.output(GPIO_LED,RPi.GPTO.HIGH)
			print("got right data now, open the LED")
			LED_OPENED=True 
		print("temperature:{e}C, humidity:{1}%%". format(temperature, humidity))
		return temperature, humidity 
		if LED OPENED: 
			print("got wrong data now, close the LED")
			RPi. GPIO. output(GPIO_LED, RPi. GPIO. LOW)
			LED_OPENED=False
		return None, None
while True: 
	print("time:"+str(datetime. datetime. now()))
	setupDHT11()
	data=read()
	temperature, humidity =checkData(data)
	time.sleep(SLEEP_SECOND)