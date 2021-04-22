obj-m += pps_gen_gpio.o

all:
	make -j6 -C /lib/modules/$(shell uname -r)/build  M=$(PWD) modules
	
