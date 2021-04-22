# Create PPS Loadable Kernel Module

## Install required packages and kernel headers
```sh
sudo apt install git bc bison flex libssl-dev make raspberrypi-kernel-headers
```


## Create a folder with source file

```sh
mkdir pps_gen_gpio
cd pps_gen_gpio
wget https://raw.githubusercontent.com/techtile-by-dramco/raspberrypi-sync/master/PPS/Makefile
wget https://raw.githubusercontent.com/techtile-by-dramco/raspberrypi-sync/master/PPS/pps_gen_gpio.c
make
```
## Move the files to the pi
```sh
scp pps_gen_gpio/ pi@techtile-pi.local:~/pps_gen_gpio
```


## Create device tree overlay on th RPI

```sh
wget https://raw.githubusercontent.com/techtile-by-dramco/raspberrypi-sync/master/PPS/pps-gen-gpio-overlay.dts
dtc -@ -I dts -O dtb -o pps-gen-gpio.dtbo pps-gen-gpio-overlay.dts
sudo cp pps-gen-gpio.dtbo /boot/overlays/
```
Add the new overlay to the config 
```sh
sudo echo "dtoverlay=pps-gen-gpio" >> /boot/config.txt
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
