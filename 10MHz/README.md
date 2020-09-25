# Configuring and building device tree for GPCLK at 10 MHz

## Install device tree compiler
```sh
sudo apt install device-tree-compiler
```

## Download device tree source file
```sh
wget https://raw.githubusercontent.com/versatile-by-dramco/raspberrypi-sync/master/10MHz/dt-blob.dts
```

## Compile device tree source and put resuling device tree blob under /boot
warnings stating that "node has a unit name, but no reg property" can be ignored
```sh
sudo dtc -I dts -O dtb -o /boot/dt-blob.bin dt-blob.dts
```

## Reboot
```sh
sudo reboot
```

>> New hardware configuration should be active. If for any reason the raspberry pi will not boot, just remove dt-blob.bin from /boot to undo the changes.
