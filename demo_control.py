import pigpio
import time
pi = pigpio.pi()

pi.set_mode(25, pigpio.INPUT) #reed switch
pi.set_pull_up_down(25, pigpio.PUD_UP)
pi.set_mode(24, pigpio.INPUT) #touch sensor
pi.set_pull_up_down(24, pigpio.PUD_UP)

while True:
	print ("Reed switch at gpio25 : {0} , Touch sensor at gpio24 : {1}".format(pi.read(25),pi.read(24))
	time.sleep(1)
