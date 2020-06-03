# RPi_WiFi_autoconnect
WiFi automatic connection for Raspberry Pi via QRcode

This is a simple example of automatically connecting to a Wifi network when starting Raspberry Pi. In the script, the camera is connected, the QR code is searched in the field of view. And, if there is a code with the correct structure - a connection to the network specified in the code.

This is a convenient way to use your Raspberry Pi in a situation where you do not want to connect a monitor and keyboard, but you need to quickly connect to Wifi networks.

# Connection

For the query "script for connecting wifi via python" - you will find many articles and libraries. Most of them will not work for Raspberry Pi. The official connection method involves connecting through wpa_supplicant. So, it used in this example.
If you want the new network to remain after the reboot, you will need to make changes to the _/etc/rc.local_ file, which will disable automatic network management:

```
dhcpcd -x || :
```

If you use the current script without this change, then the saved network will be taken by default. And, if it does not exist, it will begin to connect to a new one.

Here is guides that i use for connection part:

https://www.raspberrypi.org/forums/viewtopic.php?t=207585
https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

Connection part in `script.py` file.

# QR code

OpenCV  has a built-in module for reading GR codes. But, unfortunately, it does not work on many assemblies. For example, in OpenVino.
So, we will use Zbar scaner. There is a few implimentation of it. This implimentation work for RPi - https://github.com/NaturalHistoryMuseum/pyzbar/ . You can install it with:

```
pip install pyzbar
```

I used standart QR code text for WiFi connection. Today always every mobile have it (just find button "show qr code for connection"). 

If you want create yourself - here is pattern for QRCode text:

```
WIFI:T:WPA;P:qwerty123456;S:TestNet;;
```

Just insert your password after "P:" and before ";", and network ssid after "S:" and before ";". Then create QR code from this string. You can use this site -https://www.the-qrcode-generator.com/ . Or this python library - https://pypi.org/project/qrcode/ .

![example](sample.png)

#Work on the startup

It is assumed that you use this script without a monitor and without the Internet. Therefore, it should start at the start itself. I explored several approaches for automatically running scripts on Raspberry Pi. For my purposes, this approach was most suitable - https://stackoverflow.com/questions/60431499/running-an-openvino-python-script-on-boot-for-raspberry-pi

 You create a service that will run the script when launched in the conditions you need (under the required user, with the required rights, in the required order).
 
In my case - i created file "openvino-app-script" in my home folder with this text:

```
#!/bin/bash
cd face_detect     
python3 QRCode.py
```
Change it permissions and ownership with `chmod u+x ~/openvino-app-script`
Then create service defenition with `sudo nano /etc/systemd/system/openvino-app.service` and with this structure:

```
[Unit]
Description=OpenVINO Python Script
After=network.target

[Service]
ExecStart=/home/pi/openvino-app-script
WorkingDirectory=/home/pi/face_detect
User=pi

[Install]
WantedBy=graphical.target
```

And activate it with `sudo systemctl enable openvino-app.service`

#Few word about cameras

In my script I use USB camera. But you can swithc on RRi camera by changing `RPicamera = True`

#Working not on RPi

This script work on any PC if you switch testmod to True: `testmod=True`. But it will not provide wifi connection, just qr code detection|recognition part.
If you want to start on other platform - find how wifi service work on it.
