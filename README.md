# HTTP-Controlled-Relay-Esp8266-
MicroPython code for Esp8266 controlled relays. (DIY Iot devices)

1. Flash the MicroPython firmware [https://docs.micropython.org](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html)
2. Install [Adafruit's Ampy](https://github.com/adafruit/ampy) tool and screen (ex pacman -S screen or apt-get install screen)
3. Edit the code. Change the network attributes, led, relay, or button GPIO pins in both boot.py and main.py. The button is not needed, but it is recommended. Adjust the code to your setup if needed.

###### Notes: Root access is required unless your user is a member of the "dialout" group. (Re-log for changes to take affect.) Additionally, boot.py will automagically call main.py after it's completed.
- To access the REPL prompt:
```screen /dev/ttyUSB0 115200```
- To put scripts onto the Esp8266 board:
```ampy -p /dev/ttyUSB0 put ~/Documents/esp8622/boot_alt.py boot.py```

- Calling the server:
```
curl http://192.168.1.49?state #request the current state of the relay without making changes
curl http://192.168.1.49?relay #change the relay. If it is on, it will turn off and vice versa
curl http://192.168.1.49?exit #exit the script. failsafe or accessibility reasons. 
```

*If you find that you cannot access the REPL because the server is running and you can't exit (no button nor ?/exit is working). With screen running, press the reset button on your board, and quickly ctrl+c to quit the boot.py and main.py before the server is able to start.*


<hr>
<p align="center">
  <img src="https://github.com/datguy-dev/HTTP-Controlled-Relay-Esp8266-/blob/master/pics/smallrelay/my_photo-5.jpg" title="Main Window"><br>
</p>
<hr>
<hr>
<p align="center">
  <img src="https://github.com/datguy-dev/HTTP-Controlled-Relay-Esp8266-/blob/master/pics/bigrelay/my_photo-8.jpg" title="Main Window"><br>
</p>
<hr>
