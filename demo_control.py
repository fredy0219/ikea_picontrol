import pigpio
import time
import rotary_encoder

def callback(way):
    global pos
    pos += way
    print("pos={}".format(pos))

pi = pigpio.pi()

pi.set_mode(25, pigpio.INPUT) #reed switch
pi.set_pull_up_down(25, pigpio.PUD_UP)
pi.set_mode(24, pigpio.INPUT) #touch sensor
pi.set_pull_up_down(24, pigpio.PUD_UP)

decoder = rotary_encoder.decoder(pi,5,6,callback)

try:
	while True:
		print ("Reed switch at gpio25 : {0} , Touch sensor at gpio24 : {1}".format(pi.read(25),pi.read(24)))
		time.sleep(1)

except KeyboardInterrupt:
	decoder.cancle()
	pi.stop()

