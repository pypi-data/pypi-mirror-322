# README

## Hardware

We are using a [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) to run a [MCP4151-103E_P](resources/datasheets/MCP4151.pdf) digital potentiometer (digipot) to attenuate an incoming signal by a controlled amount. On the rpi a socket server recieves input from a client to adjust the wiper of the digipot. 

The MCP4151 is connected to the rpi using a [breakout board](resources/PCBs/breakout/) and a [customized hat](resources/PCBs/digipigi_hat/) hat. Both can be ordered from [JLCPCB](https://jlcpcb.com). 

## Software

  The digipot is controlled by a socket server. The software setup is handled with [Ansible](https://docs.ansible.com/ansible/latest/index.html).

### How to run the ansible playbooks


Start by using the Raspberry Pi Imager. Choose:
- Device: Raspberry Pi 5
- OS: Raspberry OS
- Set hostname: digipigiX.local
- Set username: sebi
- Set password: Autogenerate with Password app
- Configure WiFi
- Set locale settings
- Turn on SSH and copy public key

First, commission all hosts
```bash
ansible-playbook -i inventory.ini setup_hosts.yml 
```
Then, run the [calibration](resources/python/calibrate.ipynb), which stores the relevant calibration data in `hosts_vars/digipigiX_xxx.yml`. Then, set up the properly calibrated device using 
```bash
ansible-playbook setup_digimodule.yml
```

## How to use and characteristics

The digipigi can be used via the module [digipigi](resources/python/digipigi.py). It's use is detailed in a [notebook](resources/python/demo.ipynb).

In order to give a feeling for the performance of the digipigi, we provide here a plot of the attenuation factor as calibrated for a DC input signal:

![DC Calibration](resources/images/dc.png)

For three wiper positions we also show the time trace of attenuated square wave signal:

![AC Calibration](resources/images/ac.png)

The odd square wave length is due to my inability to time the recording of the ad2 via its API properly. 




