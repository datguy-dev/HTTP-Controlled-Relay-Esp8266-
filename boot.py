# This file is executed on every boot (including wake-boot from deepsleep)
import gc, machine, network, time, sys

# Adjust LED and Relay Pins to your setup

network_Attrs = {
    'ipv4': '192.168.1.49',  # BE SURE TO EDIT THESE
    'mask': '255.255.255.0',
    'dns': '8.8.8.8',
    'gateway': '192.168.1.1',
    'ssid': 'Access Point SSID',
    'pass' :'Access Point Password',
}

# network indicator led on gpio 15
led = machine.Pin(12, machine.Pin.OUT)

# if doesnt connect to network after X tries
fails = 0
fails_Limit = 15

sta_if = network.WLAN(network.STA_IF)
if sta_if.isconnected():
    pass
else:
    print('[-]connecting to network')
    sta_if.active(True)
    sta_if.ifconfig((network_Attrs['ipv4'], network_Attrs['mask'], network_Attrs['gateway'], network_Attrs['dns']))
    sta_if.connect(network_Attrs['ssid'], network_Attrs['pass'])
    while not sta_if.isconnected():
        sys.stdout.write('.')
        if led.value():
            led.off()
        else:
            led.on()
        fails += 1
        if fails >= fails_Limit:
            print('[!]unable to connect to the network')
            for i in range(fails_Limit):
                led.on()
                time.sleep(0.1)
                led.off()
                time.sleep(0.1)
            sys.exit(1)
        else:
            time.sleep(1)

print()
print('[+] connected ({0})'.format(sta_if.ifconfig()))
gc.collect()

# > now main.py runs
