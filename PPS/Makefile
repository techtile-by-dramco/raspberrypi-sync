all:
	make -C /lib/modules/$(shell uname -r)/build M=$(pwd) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(pwd) clean

modules_install: all
	$(MAKE) -C $(KERNEL_SRC) M=$(SRC) modules_install
	$(DEPMOD)
