# SHOULD SEE ME
try:
    import usocket as socket
except:
    import socket
import errno, machine, sys, ure
from time import sleep as delay


def Maintain():
    import esp, gc

    # gc.collect() after boot.py
    # Memory Stats: Allocated(12352) Free(23616) Diff(-Freed 560) Total(4194304) in bytes
    # gc.collect() after idling
    # Memory Stats: Allocated(12352) Free(23616) Diff(-Freed 832) Total(4194304) in bytes
    # gc.collect() after a single request
    # Memory Stats: Allocated(12608) Free(23360) Diff(-Freed 1248) Total(4194304) in bytes

    mem_before = gc.mem_free()
    gc.collect()
    mem_after = gc.mem_free()
    if mem_before > mem_after:
        mem_diff = '+Freed {}'.format(mem_before - mem_after)
    else:
        mem_diff = '-Freed {}'.format(mem_after - mem_before)

    mem_total = esp.flash_size()
    print('Memory Stats: Allocated({1}) Free({2}) Diff({3}) Total({0}) in bytes'.format(
        mem_total, gc.mem_alloc(), gc.mem_free(), mem_diff
    ))
    return


def Relay():
    # changes to relay to on if off and vice versa depending on the pin current value.
    if pins['relay'].value():
        pins['led1'].off()
        pins['relay'].off()
    else:
        pins['led1'].on()
        pins['relay'].on()
    return pins['relay'].value()

# gpio pin setup
pins = {
    'led1': machine.Pin(12, machine.Pin.OUT),
    'relay': machine.Pin(4, machine.Pin.OUT),
}
pins['relay'].off()

# response from server
CONTENT = b'''\
HTTP/1.0 %d %s

%d
'''

# keep track of cycles and run maintenance later
time_outs = 0
is_waiting = True

s = socket.socket()
ai = socket.getaddrinfo('0.0.0.0', 80)
addr = ai[0][-1]
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.settimeout(3)
s.bind(addr)
s.listen(5)
print('[+] Server http://myIpv4:80/')

while True:
    try:
        if is_waiting:
            print('[~] waiting for request')
            is_waiting = False

        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        req = client_sock.recv(256)  # 4096
        print('\t\tRequest from {0}:\n\t\t{1}'.format(client_addr, req))
        if ure.search(b'/?state', req):
            print('\t\t[+] got state')
            client_sock.write(CONTENT % (200, 'OK', pins['relay'].value()))
            client_sock.close()
        elif ure.search(b'/?relay', req):
            print('\t\t[+] got relay')
            Relay()
            client_sock.write(CONTENT % (200, 'OK', pins['relay'].value()))
            client_sock.close()
        elif ure.search(b'/?exit', req):
            print('\t\t[+] got exit')
            client_sock.write(CONTENT % (200, 'OK', pins['relay'].value()))
            client_sock.close()
            sys.exit(0)
        else:
            print('\t\t[-] bad request')
            client_sock.write(CONTENT % (400, 'Bad Request', 2))
            client_sock.close()
            pass
        if client_sock:
            client_sock.close()

        # this is only used to prevent the annoyance of repeating "waiting" messages
        is_waiting = True

    except KeyboardInterrupt:
        print('[!] exiting...')
        sys.exit(0)
    except Exception as e:
        if e.args[0] == errno.ETIMEDOUT:
            # toggle server is listening message
            time_outs += 1
            if time_outs > 200:
                # if socket timeout = 3. Then x * 3 -> run Maintain() ((200 * 3 = 600 seconds = 10 minutes))
                Maintain()
                time_outs = 0
            # LED routine
            pins['led1'].on()
            delay(1)
            pins['led1'].off()
            pass
        else:
            print('[!] unexpected exception. exiting...')
            print('[>] details:\n\n{0}'.format(e))
            sys.exit()