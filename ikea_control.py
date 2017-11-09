import OSC
import pigpio
import time

c = OSC.OSCClient()
c.connect(('192.168.2.101',12289))

pin_bird_cage = 23
pin_black_board = 27
pin_magic_hat = 22

def cbf_bird_cage(gpio,level,tick):
	print "#Tigger log -> "
	check_bird_cage(level)

def cbf_black_board(gpio,level,tick):
	print ("#Tigger log -> ")
	check_black_board(level)

def cbf_magic_hat(gpio,level,tick):
	print ("#Tigger log -> ")
	check_magic_hat(level)

def check_bird_cage(status):

	if status == 0: # change to low
		print("Bird_cage : low ")
		try:
			oscmsg = OSC.OSCMessage()
			oscmsg.setAddress("/bird_cage")
			oscmsg.append("off")
			c.send(oscmsg)
		except:
			print("Send reed data fail.")

	if status == 1: # change to high
		print("Bird_cage : high")
		try:
			oscmsg = OSC.OSCMessage()
			oscmsg.setAddress("/bird_cage")
			oscmsg.append("on")
			c.send(oscmsg)
		except:
			print("Send reed data fail.")

def check_black_board(status):

	if status == 0: # change to low
		print("Black board : low ")
		try:
			oscmsg = OSC.OSCMessage()
			oscmsg.setAddress("/black_board")
			oscmsg.append("on")
			c.send(oscmsg)
		except:
			print("Send touch data fail.")

	if status == 1: # change to high
		print("Black board : high")
		try:
			oscmsg = OSC.OSCMessage()
			oscmsg.setAddress("/black_board")
			oscmsg.append("off")
			c.send(oscmsg)
		except:
			print("Send touch data fail.")

def check_magic_hat(status):

	if status == 0: # change to low
		print("Magic sensor : low ")
		try:
			oscmsg = OSC.OSCMessage()
			oscmsg.setAddress("/magic_hat")
			oscmsg.append("on")
			c.send(oscmsg)
		except:
			print("Send light data fail.")

	if status == 1: # change to high
		print("Magic sensor : high")
		try:
			oscmsg = OSC.OSCMessage()
			oscmsg.setAddress("/magic_hat")
			oscmsg.append("off")
			c.send(oscmsg)
		except:
			print("Send light data fail.")



if __name__ == '__main__':
	print("main program start")
	pi = pigpio.pi()

	pi.set_mode(pin_bird_cage, pigpio.INPUT) #reed switch
	pi.set_pull_up_down(pin_bird_cage, pigpio.PUD_UP)
	pi.set_glitch_filter(pin_bird_cage, 100)
	cb_bird_cage = pi.callback(pin_bird_cage,pigpio.EITHER_EDGE,cbf_bird_cage)

	pi.set_mode(pin_black_board, pigpio.INPUT) #touch sensor
	pi.set_pull_up_down(pin_black_board, pigpio.PUD_UP)
	pi.set_glitch_filter(pin_black_board, 100)
	cb_black_board = pi.callback(pin_black_board,pigpio.EITHER_EDGE,cbf_black_board)

	pi.set_mode(pin_magic_hat, pigpio.INPUT) #touch sensor
	pi.set_pull_up_down(pin_magic_hat, pigpio.PUD_UP)
	pi.set_glitch_filter(pin_magic_hat, 100)
	cb_magic_hat = pi.callback(pin_magic_hat,pigpio.EITHER_EDGE,cbf_magic_hat)

	current_milli_time = lambda: int(round(time.time() * 1000))
	temp_milli_time = current_milli_time()

	try:
		while True:
			if current_milli_time() - temp_milli_time >3000:
				check_bird_cage(pi.read(pin_bird_cage))
				check_black_board(pi.read(pin_bird_cage))
				check_magic_hat(pi.read(pin_magic_hat))
				temp_milli_time = current_milli_time()

	except KeyboardInterrupt:
		cb_bird_cage.cancel()
		cb_black_board.cancel()
		cb_magic_hat.cancel()
		pi.stop()

