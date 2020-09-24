#!/usr/bin/python3
import socket
import RPi.GPIO as GPIO

import time

try:
	pin_num = 37
	hostname = socket.gethostname()

	GPIO.setmode(GPIO.BOARD)

	GPIO.setup(pin_num, GPIO.OUT)

	print(f"Starting listening to port 37020 at {hostname}")
	

	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

	client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

	# Enable broadcasting mode
	client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	client.bind(("", 37020))
	while True:
	    data, addr = client.recvfrom(1024)
	    print(str(data))
	    if hostname in str(data):
	    	state = True
	    	for i in range(20):
	    		GPIO.output(pin_num, state)
	    		state = not state
	    		time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()