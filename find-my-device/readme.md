# Find my device

Put `find-my-device.py` in `\~/scripts/`.
Put the service file in `/lib/systemd/system/`.


```sh
sudo chmod 644 /lib/systemd/system/find-my-device.service
chmod +x /home/pi/scripts/find-my-device.py
sudo systemctl daemon-reload
sudo systemctl enable find-my-device.service
sudo systemctl start find-my-device.service
```

# Get hostname
Put `get-hostname.sh` in `\~/scripts/`.

```sh
sudo crontab -e
```

Add the following:

The 10 seconds are to be sure that internet is active.
```sh
@reboot sleep 10 && sudo /home/pi/scripts/get-hostname.sh
```