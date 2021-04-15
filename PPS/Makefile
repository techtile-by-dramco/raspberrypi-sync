all:
	make -j$(shell nproc) -C /lib/modules/$(shell uname -r)/build M=$(pwd) modules

clean:
	make -j$(shell nproc) -C /lib/modules/$(shell uname -r)/build M=$(pwd) clean

modules_install: all
	$(MAKE) -j$(nproc) -C $(KERNEL_SRC) M=$(SRC) modules_install
	$(DEPMOD)
