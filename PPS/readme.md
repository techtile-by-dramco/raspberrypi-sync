# Create PPS Loadable Kernel Module

## Install required packages and kernel headers
```sh
sudo apt update && sudo apt upgrade
sudo apt install git bc bison flex libssl-dev make raspberrypi-kernel-headers
```


## Create a folder with source file
If you get a missing sperator error during make, than probably the tab below all: is converted to spaces.
Remove the spaces and insert one tab.
```sh
mkdir pps_gen_gpio
cd pps_gen_gpio
wget https://raw.githubusercontent.com/techtile-by-dramco/raspberrypi-sync/master/PPS/Makefile
wget https://raw.githubusercontent.com/techtile-by-dramco/raspberrypi-sync/master/PPS/pps_gen_gpio.c
make
```

## Create device tree overlay on th RPI

```sh
wget https://raw.githubusercontent.com/techtile-by-dramco/raspberrypi-sync/master/PPS/pps-gen-gpio-overlay.dts
dtc -@ -I dts -O dtb -o pps-gen-gpio.dtbo pps-gen-gpio-overlay.dts
sudo cp pps-gen-gpio.dtbo /boot/overlays/
```
Add the new overlay to the config 
```sh
sudo bash -c 'echo "dtoverlay=pps-gen-gpio" >> /boot/config.txt'
```

Reboot your pi
```sh
sudo reboot
```

Check if the new overlay is loaded, i.e., it should contain pps-gen-gpio:
```sh
dtc -I fs /proc/device-tree
```


## Load the kernel module
```sh
sudo insmod pps_gen_gpio.ko
lsmod # should show the new module
dmesg # should show some info about the module
```

# Install the kernel module
```sh
sudo cp ~/pps_gen_gpio/pps_gen_gpio.ko /lib/modules/$(uname -r)/kernel/drivers/pps/
sudo bash -c 'echo "pps_gen_gpio" >> /etc/modules-load.d/pps_gen_gpio.conf'
sudo depmod
```

Reboot your pi
```sh
sudo reboot
```
