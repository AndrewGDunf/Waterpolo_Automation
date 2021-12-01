from time import sleep
import board
import analogio           
import digitalio

sen0 = analogio.AnalogIn(board.A0)  			# setting the analog input to variable sen 0, corresponds with 15cm measurement
# sen1 = analogio.AnalogIn(board.A1)  
# sen2 = analogio.AnalogIn(board.A2)  
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

a = 0							# intialise count variable

def get_voltage(pin):					# function returns the voltage value, standard analog input conversion
    return (pin.value * 3.3) / 65536

def get_distance(v):					# function returns the distance value according to a voltage, 
    return ((56.25)/(v-0.125)-10)

while True:
    v0 = get_voltage(sen0)				# send sensor variable to the get_voltage function
    #v1 = get_voltage(sen1)
    #v2 = get_voltage(sen2)
    
    d0 = get_distance(v0)				# send voltage variable to the get_distance function
    #d1 = get_distance(v1)
    #d2 = get_distance(v2)

    if d0 >= 20 and d0 <= 150:
    	a = a + 1
        print(a, "value in cm", d0)
        led.value = True
        sleep(0.1)
        led.value = False
    
