# Configuring and building device tree for GPCLK at 10 MHz

## Install device tree compiler
```sh
sudo apt install device-tree-compiler
```

## Download device tree source file
```sh
wget https://raw.githubusercontent.com/raspberrypi/firmware/master/extra/dt-blob.dtswget https://raw.githubusercontent.com/raspberrypi/firmware/master/extra/dt-blob.dts
```

>> Modify dt-blob.dts to your liking (see our example file -> ctrl+f "MIDAS")

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
