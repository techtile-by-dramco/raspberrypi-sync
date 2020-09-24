#!/bin/bash

mac=$( cat /sys/class/net/eth0/address )
echo $mac


newhost=$( curl "XXXXX?mac=$mac" )
echo $newhost

hostn=$( cat /etc/hostname )
echo $hostn

if [ -z "$newhost" ]
then
     echo "\$newhost is empty"
else
	if [ "$newhost" == "$hostn" ]; then
	    echo "same hostname as before"
	else
		# newhost

		#change hostname in /etc/hosts & /etc/hostname
		sed -i "s/$hostn/$newhost/g" /etc/hosts
		sed -i "s/$hostn/$newhost/g" /etc/hostname


		hostnamectl set-hostname "$newhost"
		systemctl restart avahi-daemon
	fi
fi
