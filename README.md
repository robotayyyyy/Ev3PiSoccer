# Ev3PiSoccer

## Propose
I just wana adapt image processing to a simple robot with a casual task, put the ball to the goal. My Idea is using the Raspberry pi for immage processing task and send the message to the EV3 robot via bluetooth. The result as follows.

[](https://youtu.be/1NdWqt1gIag)

## Equipment
1. Raspberry pi (for this work, I used pi3 modelB)
1. pi's battery
1. webcam
1. Lego EV3 

## Software
1. [EV3 software](https://education.lego.com/en-us/downloads/mindstorms-ev3/software) for control robot like a child! It looks kiddy and can handle multi-tasks like a pro! 
1. [Pyzo](https://pyzo.org/start.html) for implement python in pi.
1. [optional][Teanviewer](https://www.teamviewer.com) for GUI remote. Yeh, I'm a noob who love GUI. 

## Pi settup
You need a day for more for setting up the pi and I'm not kidding.
* First we need [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) for pi's os.
* After that we need [openCV](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/), please follow the instruction strictly. For making opevCV process, I recoment using 2 core of cpu insted of 4 (type `make -j2` insted of `make -j4`). Trust me or your pi stop working!
* We also need to enable Serial Port in interface section in pi configuration.![](./img/0.PNG)
* A software for connect bluetooth. I recommend **Bluetooth Manager**. Open terminal then type `sudo apt-get install bluetooth bluez blueman`
* [optional] if wifi in your place using WPA2-enterprise, type `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf` then add the following code at the end of the file.
```
network={
	ssid="XXXXX"
	mode=0
	identity="XXXXX"
	password="XXXXX" 
	key_mgmt=WPA-EAP
	pairwise=CCMP TKIP
	group=CCMP TKIP
	eap=PEAP	
	phase1="peapver=0"
	phase2="MSCHAPV2"
} 
```
change XXXXX to yours. By the way, [these guys](/etc/wpa_supplicant/wpa_supplicant.conf) deserve a credit.

## Connecting pi to EV3
One can connect Raspberry pi to EV3 by bluetooth as following instruction.
* I added a device by default bluetooth app **not the one that you just installed**. 

![](./img/1.PNG)

* Select your EV3. For me, I named it **SoccerBot**.

![](./img/2.PNG)

* Now switch to your EV3, accept it.

![](./img/3.PNG)

* Enter pin code on EV3.

![](./img/4.PNG)

* Enter pin code on your pi.

![](./img/5.PNG)

* Now the devices are connected. It mean they know each other but still no process together.

![](./img/6.PNG)

* To start process, open **Bluetooth Manager** (yeh the one that you just installed) then right click at your device and click Serial Port.

![](./img/7.PNG)

* Watch for the address of device. For this case, it's **/dev/rfcomm0**.

![](./img/8.PNG)

## Use it
Just start **ballDetect.py** on your pi and run **evpi.ev3** on your EV3
