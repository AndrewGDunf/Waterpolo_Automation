# Write your code here :-)
from time import sleep
import board
import analogio

sen0 = analogio.AnalogIn(board.A0)  			# setting the analog input to variable sen 0, corresponds with 15cm measurement
sen1 = analogio.AnalogIn(board.A1)  			# setting the analog input to variable sen 1, corresponds with 30cm measurement
sen2 = analogio.AnalogIn(board.A2)  			# setting the analog input to variable sen 2, corresponds with 45cm measurement

def get_voltage(pin):					# function returns the voltage value, standard analog input conversion
    return (pin.value * 3.3) / 65536

def get_distance(v):					# function returns the distance value according to a voltage, 
    return ((56.25)/(v-0.125)-10) 		

while True:						
    v0 = get_voltage(sen0)				# send sensor variable to the get_voltage function
    v1 = get_voltage(sen1)
    v2 = get_voltage(sen2)

    d0 = get_distance(v0)				# send voltage variable to the get_distance function
    d1 = get_distance(v1)
    d2 = get_distance(v2)
    if d0 > 0 and d0 < 30:				# if statement determining if the distance falls with the detection range
        output_string = 'y  '				# if yes, send a y respresenting "yes"
    else:
        output_string = 'n  '				# otherwise send a n, representing a "no"

    if d1 > 0 and d1 < 30:				#if statement for d1
        output_string += ' y  '
    else:
        output_string += ' n  '

    if d2 > 0 and d2 < 30:				#if statement for d2
        output_string += ' y  '
    else:
        output_string += ' n  '

    print(output_string)				# print the result of the output_string variable
    print(round(d0),round(d1),round(d2))		# and print the distances round to the nearest interger in cm
    print("   ")
    sleep(0.5)
# Write your code here :-)
