import OSC
import pigpio
import time
import rotary_encoder

pos = 0
c = OSC.OSCClient()
c.connect(('192.168.2.101',12289))

def cbf_encoder(way):
	global pos
	pos += way

	try:
		oscmsg = OSC.OSCMessage()
		oscmsg.setAddress("/Encoder")
		oscmsg.append(pos)
		c.send(oscmsg)
	except:
		print("Send data fail.")
	print("pos={}".format(pos))

def cbf_reed(gpio,level,tick):

	if level == 0: # change to low
		print("Reed switch : low ")
		try:
			oscmsg = OSC.OSCMessage()
			oscmsg.setAddress("/Reed")
			oscmsg.append("LOW")
			c.send(oscmsg)
		except:
			print("Send reed data fail.")

	if level == 1: # change to high
		print("Reed switch : high")
		try:
			oscmsg = OSC.OSCMessage()
			oscmsg.setAddress("/Reed")
			oscmsg.append("HIGH")
			c.send(oscmsg)
		except:
			print("Send reed data fail.")

def cbf_touch(gpio,level,tick):

	if level == 0: # change to low
		print("Touch sensor : low ")
		try:
			oscmsg = OSC.OSCMessage()
			oscmsg.setAddress("/Touch")
			oscmsg.append("LOW")
			c.send(oscmsg)
		except:
			print("Send touch data fail.")

	if level == 1: # change to high
		print("Touch sensor : high")
		try:
			oscmsg = OSC.OSCMessage()
			oscmsg.setAddress("/Touch")
			oscmsg.append("HIGH")
			c.send(oscmsg)
		except:
			print("Send touch data fail.")


pi = pigpio.pi()

pi.set_mode(25, pigpio.INPUT) #reed switch
pi.set_pull_up_down(25, pigpio.PUD_UP)
pi.set_glitch_filter(25, 100)
cb_reed = pi.callback(25,pigpio.EITHER_EDGE,cbf_reed)

pi.set_mode(24, pigpio.INPUT) #touch sensor
pi.set_pull_up_down(24, pigpio.PUD_UP)
pi.set_glitch_filter(24, 100)
cb_touch = pi.callback(24,pigpio.EITHER_EDGE,cbf_touch)

decoder = rotary_encoder.decoder(pi,5,6,cbf_encoder)

try:
	while True:
		# print ("Reed switch at gpio25 : {0} , Touch sensor at gpio24 : {1}".format(pi.read(25),pi.read(24)))
		time.sleep(1)

except KeyboardInterrupt:
	decoder.cancel()
	cb_reed.cancel()
	cb_touch.cancel()
	pi.stop()

