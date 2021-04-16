obj-m+=pps_gen_gpio.o

all:
	make -j6 -C /lib/modules/$(shell uname -r)/build M=$(pwd) modules

clean:
	make -j6 -C /lib/modules/$(shell uname -r)/build M=$(pwd) clean

modules_install: all
	$(MAKE) -j6 -C $(KERNEL_SRC) M=$(SRC) modules_install
	$(DEPMOD)
