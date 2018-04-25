# Toyota Radar spoofer and can controller
Reverse engineered can bus messages to enable the automotive Radar found on 2016+ Toyotas with TSS (corolla, Rav4, Highlander, camry). If you got your radar hooked up by are disappointed by invalid tracks, this will help you turn the radar on so you see something!

## Requirements
You'll need:
- Python3
- pip3 install cantools
- pip3 install can

## Quickstart
you need to run
```
git submodule update --init
```
to fetch the forked opendbc repo thats part of this repository.

__Make sure that can1 is connected to the RADAR can bus (Pin 5/6 on the radar unit) and can0 to the CAR CAN bus. (pin 3/2)__

Just run ./spoof_dsu.py and you should see output on your terminal like:

```
faraz@faraz-XPS-15-9560:~/Code/toyoyta_radar_control_can$ ./spoof_dsu.py 
Got VALID track at dist: 2.44
Got VALID track at dist: 2.44
Got VALID track at dist: 2.4
Got VALID track at dist: 2.4
Got VALID track at dist: 2.4
Got VALID track at dist: 2.4
Got VALID track at dist: 2.4
Got VALID track at dist: 2.4
```

Rejoice! Your radar is alive!

## How do I wire up this radar?
Heres the pinout to get you started:
![Radar pinout](/images/connector.jpg "Radar connector")

|Pin| Usage|
|---|------|
|3|Car can High|
|2|Car can Low|
|5|Radar can High|
|6|Radar can Low|
|8|12V VCC|
|1|GND|

## Some CAN help please?
I have used these two CAN adaptors successfully:

- Carloop with CAN Hitch: https://www.amazon.com/Carloop-CAN-Hitch-Particle-microcontroller/dp/B06XXRBVFW/ref=sr_1_1?ie=UTF8&qid=1524621189&sr=8-1&keywords=carloop+can+hitch

You'll need to buy a particle photon and flash it with the SocketCAN application they have for it to work with Socketcan on linux/mac

- http://canable.io/ - The default SL-CAN implementation sucks! (it errors out my socket can interface after a while). You'll need to reflash the STM with the new candlelight_fw which  used the gs_usb driver so it drivers without socketcan. In this mode this adaptor is rock solid.

You can also use comma.ai's Panda if you can hunt down the can pins on the OBD connector

And thats it!

## My radar still does not speak!
Ive been told that the 2018 Toyotas might have a different unit (made by Continental instead of Denso) so consider this code fully tested ONLY on the 2017 Denso radar units. 

