# Create PPS Loadable Kernel Module

## Install and run rpi-source, to get the correct linux kernel source

```sh
sudo apt-get install git bc bison flex libssl-dev libncurses5-dev
sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/local/bin/rpi-source && sudo chmod +x /usr/local/bin/rpi-source && /usr/local/bin/rpi-source -q --tag-update
rpi-source
```

## Create a folder with source file

```sh
mkdir pps_gen_gpio
cd pps_gen_gpio
wget https://raw.githubusercontent.com/techtile-by-dramco/raspberrypi-sync/master/PPS/Makefile
wget https://raw.githubusercontent.com/techtile-by-dramco/raspberrypi-sync/master/PPS/pps_gen_gpio.c
make
```
