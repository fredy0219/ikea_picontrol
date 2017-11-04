import pigpio
import time
import rotary_encoder

pos = 0

def callback(way):
    global pos
    pos += way
    print("pos={}".format(pos))

def cbf_reed(gpio,level,tick):

	if level == 0: # change to low
		print("Reed switch : low ")

	if level == 1: # change to high
		print("Reed switch : high")

def cbf_touch(gpio,level,tick):

	if level == 0: # change to low
		print("Touch sensor : low ")

	if level == 1: # change to high
		print("Touch sensor : high")

pi = pigpio.pi()

pi.set_mode(25, pigpio.INPUT) #reed switch
pi.set_pull_up_down(25, pigpio.PUD_UP)
cb_reed = pi.callback(25,pigpio.EITHER_EDGE,cbf_reed)

pi.set_mode(24, pigpio.INPUT) #touch sensor
pi.set_pull_up_down(24, pigpio.PUD_UP)
cb_touch = pi.callback(24,pigpio.EITHER_EDGE,cbf_touch)

decoder = rotary_encoder.decoder(pi,5,6,callback)

try:
	while True:
		# print ("Reed switch at gpio25 : {0} , Touch sensor at gpio24 : {1}".format(pi.read(25),pi.read(24)))
		time.sleep(1)

except KeyboardInterrupt:
	decoder.cancle()
	cb_reed.cancle()
	cb_touch.cancel()
	pi.stop()

