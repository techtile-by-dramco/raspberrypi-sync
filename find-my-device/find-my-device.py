#!/usr/bin/python3
import socket
import RPi.GPIO as GPIO
import select

import time


try:
	pin_num = 37
	state = False
	blink = False
	blink_timer = False
	blink_cnt = 0

	hostname = socket.gethostname()

	GPIO.setmode(GPIO.BOARD)

	GPIO.setup(pin_num, GPIO.OUT)

	print(f"Starting listening to port 37020 at {hostname}")

	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
	

	client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

	# Enable broadcasting mode
	client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	client.bind(("", 37020))

	client.setblocking(0)

	while True:
		if blink:
			if blink_timer:
				if blink_cnt > 0:
					blink_cnt -= 1
					GPIO.output(pin_num, state)
					state = not state
					time.sleep(0.2)
				else:
					blink_timer = False
					GPIO.output(pin_num, False)
					blink = False
			else:
				GPIO.output(pin_num, state)
				state = not state
				time.sleep(0.2)

		read_sockets, write_sockets, error_sockets = select.select([client], [], [], 0)
		for sock in read_sockets:
			#incoming message from remote server
			if sock == client:
				data, addr = client.recvfrom(1024)
				data = str(data).strip()
				print(data)
				if hostname in data:
					idx = data.find(hostname)
					data_cmd = data[idx:]
					data_cmd = data_cmd.split(":")
					print(data_cmd)
					if len(data_cmd) == 1:
						print("Blink default")
						blink = not blink
						blink_timer = True
						blink_cnt = 40
					else:
						if "start" in data_cmd[1]:
							print("Blink start")
							blink = True
							blink_timer = False
						elif "stop" in data_cmd[1]:
							print("Blink stop")
							blink = False
							blink_timer = False
							GPIO.output(pin_num, False)
						else:
							print("Fallback to default")
							blink = not blink
							blink_timer = True
							blink_cnt = 40
except KeyboardInterrupt:
	GPIO.cleanup()
