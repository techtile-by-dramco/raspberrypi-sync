obj-m += pps_gen_gpio.o


all:
	make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -j6 -C <path to>/linux M=$(PWD) modules

clean:
	make -C <path to>/linux M=$(PWD) clean
