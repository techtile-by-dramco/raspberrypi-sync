# Create PPS Loadable Kernel Module (Cross Compile)

## Download source of the used kernel version


## Create a folder with source file

```sh
mkdir pps_gen_gpio
cd pps_gen_gpio
wget https://raw.githubusercontent.com/techtile-by-dramco/raspberrypi-sync/master/PPS/Makefile
wget https://raw.githubusercontent.com/techtile-by-dramco/raspberrypi-sync/master/PPS/pps_gen_gpio.c
make
```

## Copy files to RPI
