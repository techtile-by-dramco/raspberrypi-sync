#!/bin/bash

mac=$( cat /sys/class/net/eth0/address )
echo $mac


newhost=$( curl "https://dramco.be/api/midas/get-hostname.php?mac=$mac" )
echo $newhost

if [ -z "$newhost" ]
then
     echo "\$newhost is empty"
else
    hostn=$( cat /etc/hostname )
	echo $hostn

	# newhost

	#change hostname in /etc/hosts & /etc/hostname
	sed -i "s/$hostn/$newhost/g" /etc/hosts
	sed -i "s/$hostn/$newhost/g" /etc/hostname


	hostnamectl set-hostname "$newhost"
	systemctl restart avahi-daemon
fi