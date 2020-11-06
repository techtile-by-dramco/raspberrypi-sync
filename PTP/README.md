# PTP on Raspberry Pi 4 with Raspbian

This guide explains how to enable support for Precision Time Protocol (PTP) to
a Raspberry Pi 4 running the Raspbian operating system. 

This notes were tested with Raspbian Buster Lite, running kernel
`5.10.y`. 

## Preliminary operations

* Download Raspbian
* flash it on an SD card
* boot the OS

The following commands should be run from a terminal on the Raspberry Pi target:
a local or SSH connection for the Raspbian default user pi is assumed from
now on. Note that SSH server is not enabled by default on Raspbian
distribution.

## (optionally) upgrade the distribution

```bash
sudo apt update
sudo apt upgrade
```

## Install ptp related packages

```bash
sudo apt update
sudo apt install ethtool linuxptp git bc bison flex libssl-dev make exfat-fuse exfat-utils python-setuptools python3-setuptools
```

## Enable software timestamping in ptp4l configuration

Raspberry Pi ethernet phy does not support hardware timestamping: hence
software emulation must be enabled in ptp4l configuration. It can be done by
patching ptp4l configuration file as follows:

```bash
sed -i -e 's/time_stamping.*$/time_stamping\t\tsoftware/' /etc/linuxptp/ptp4l.conf
```

## Build a new kernel with PTP support enabled

In order to build the kernel with required patches and configuration options,
kernel sources must be fetched and some required build tools must be installed.

```bash
git clone --depth=1 --branch rpi-5.10.y https://github.com/raspberrypi/linux
cd linux
KERNEL=kernel7l
make bcm2711_defconfig
# change in .config: CONFIG_LOCALVERSION="-v7l-MIDAS_KERNEL"
make -j6 Image modules dtbs
```

This will build the kernel in its default configuration and will take a
**long** time. If anything fails, up to here please see the
[kernel building raspberrypi.org official
page](https://www.raspberrypi.org/documentation/linux/kernel/building.md).

### Apply required configuration changes

Some extra configuration options must be applied to the default
`bcm2711_defconfig`. This can be done as follows. Run these commands from
within the linux kernel sources directory.

```bash
echo 'CONFIG_NETWORK_PHY_TIMESTAMPING=y' >> .config
echo 'CONFIG_PTP_1588_CLOCK=y' >> .config
```

The above commands work if you already built the default kernel before applying
the pathes. Otherwise you can enable them manually with any default kernel
configuration target like `make menuconfig`.

### Build kernel with PTP enabling changes

It is now possible to build the kernel with the changes we made to support PTP:

```bash
make olddefconfig
make -j6 Image modules dtbs
```

The new kernel image, modules and dtbs must be installed over the current ones.
Backing up current files is suggested in case something goes wrong and you want
to rollback.

```bash
sudo make modules_install
sudo cp /boot/$KERNEL.img /boot/$KERNEL-backup.img
sudo cp arch/arm64/boot/Image /boot/$KERNEL.img
sudo cp arch/arm64/boot/dts/broadcom/*.dtb /boot/
sudo cp arch/arm64/boot/dts/overlays/*.dtb* /boot/overlays/
sudo cp arch/arm64/boot/dts/overlays/README /boot/overlays/
```

Enable the ptp4l service so it starts at boot:
```bash
sudo systemctl enable ptp4l.service
```
The RaspberryPi is now ready to run ptp4l and can be rebooted for changes to
take effect.

If you want to cross-compile the kernel on a faster host instead of running the
process on the Raspberrypi itself, please refer to the general kernel
cross-compile instruction
[here](https://www.raspberrypi.org/documentation/linux/kernel/building.md).


### Enable PPS

Apply patch:
```bash
cd ~
git clone https://github.com/versatile-by-dramco/raspberrypi-sync.git
cd linux
git checkout -b pps-generator-patches
git am ~/raspberrypi-ptp/patches/pps-add-gpio-PPS-signal-generator.patch
```
Add the PPS configuration
```bash
echo 'CONFIG_PPS_GENERATOR_GPIO=y' >> .config
```

Rebuild kernel and install:
```bash
KERNEL=kernel7l
make bcm2711_defconfig
make olddefconfig
make -j6 zImage modules dtbs
sudo make modules_install
sudo cp arch/arm/boot/dts/*.dtb /boot/
sudo cp arch/arm/boot/dts/overlays/*.dtb* /boot/overlays/
sudo cp arch/arm/boot/dts/overlays/README /boot/overlays/
sudo cp arch/arm/boot/zImage /boot/$KERNEL.img
```


## Troubleshooting

* As mentioned above, you can use `ethtool` to verify that software Tx
timestamping is available on the ethernet interface. The expected output of the
command should be:

```
pi@raspberrypi:~ $ ethtool -T eth0
Time stamping parameters for eth0:
Capabilities:
        software-transmit     (SOF_TIMESTAMPING_TX_SOFTWARE)
        software-receive      (SOF_TIMESTAMPING_RX_SOFTWARE)
        software-system-clock (SOF_TIMESTAMPING_SOFTWARE)
PTP Hardware Clock: none
Hardware Transmit Timestamp Modes: none
Hardware Receive Filter Modes: none
```

If you don't see `SOF_TIMESTAMPING_TX_SOFTWARE` listed, you might be running an
older kernel which requires patching the timestamping support (see
[kernel-patching.md](kernel-patching.md)).

* ptp4l is automatically started as a systemd service at boot in Raspbian. You
can inspect the service status with `systemctl status ptp4l`. If in the log the
message `failed to create a clock` appears, it likely means the required kernel
configuration bits were not enabled.
