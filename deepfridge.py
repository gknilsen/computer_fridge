# Python deep fridge front-end 
# Author: Geir K. Nilsen <geir.kjetil.nilsen@gmail.com>
#

import serial
import time
import subprocess
import sys

dev = '/dev/ttyACM0'
baud_rate = 9600

try:
    ser = serial.Serial(dev, baud_rate, timeout=10)
    print('Initializing serial connection to %s with %d bps...' % (dev, baud_rate))
    time.sleep(1)
except serial.SerialException:
    print('Could not connect to %s' % dev)
    sys.exit(-1)

print('OK')
print('Deep Fridge v0.1')
cmd = ''

while ((cmd != 'exit') and (cmd != 'quit')):
    cmd = input('>')
    ser.flushInput()
    ser.flushOutput()
    if cmd == 'get temp':
        ser.write('t'.encode())
        resp = ser.readline()
        try:
            print("Temperature: %.2f degree(s) Celsius" % float(resp))
        except ValueError:
            print("Error reading temperature from DHT11 sensor")
    if cmd == 'get hum':
        ser.write('h'.encode())
        resp = ser.readline()
        try:          
            print("Humidity: %.2f %%" % float(resp))
        except ValueError:
            print("Error reading humidity from DHT11 sensor")        
    if cmd == 'set comp off':
        ser.write('0'.encode())
        print('Compressor is now off')
    if cmd == 'set comp on':
        ser.write('1'.encode())
        print('Compressor is now on')
    if cmd == 'set light on':
        ser.write('2'.encode())
        print('Light is now on')
    if cmd == 'set light off':
        ser.write('3'.encode())
        print('Light is now off')

    if cmd == 'eject out':
        ser.write('4'.encode())
        for p in range(11):
            resp = ser.readline()
            print('%d%% ' % (int(resp.rstrip().decode('utf-8'))*10), end='', flush=True)
        print()

    if cmd == 'eject in':
        ser.write('5'.encode())
        for p in range(11):
            resp = ser.readline()
            print('%d%% ' % (int(resp.rstrip().decode('utf-8'))*10), end='', flush=True)
        print()


    if cmd == 'set motor left':
        ser.write('6'.encode())
        print('Motor in now on')

    if cmd == 'set motor right':
        ser.write('7'.encode())
        print('Motor out now on')

    if cmd == 'set motor off':
        ser.write('8'.encode())
        print('Motor now off')
    # Incomplete help
    if cmd == 'help':
        print('set comp on|off: start/stop compressor')
        print('get temp: get DHT-11 temperature')
        print('get hum: get DHT-11 humidity')
        print('eject in|out: eject the retractable shelf inwards|outwards')
        print('set light on|off: turn light on/off')
        print('get fanN: get fan speed in RPM for fan N')
        print('get cpu_temp: get CPU temperature')
        print('get gpu_temp: get GPU temperature')
        print('get cpu_util: get CPU utilization')
        print('get gpu_util: get GPU utilization')
        print('quit/exit: leave')
    # Experimental fan and CPU/GPU monitoring
    if cmd == 'get fan1':
        p1 = subprocess.Popen(('sensors', 'it8665-isa-0290'), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(('grep', 'fan1'), stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p3 = subprocess.Popen(('cut', '-c14-21'), stdin=p2.stdout, stdout=subprocess.PIPE)
        p2.stdout.close()
        output = p3.communicate()[0]
        print(output.decode(), end='')
    if cmd == 'get fan2':
        p1 = subprocess.Popen(('sensors', 'it8665-isa-0290'), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(('grep', 'fan2'), stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p3 = subprocess.Popen(('cut', '-c14-21'), stdin=p2.stdout, stdout=subprocess.PIPE)
        p2.stdout.close()
        output = p3.communicate()[0]
        print(output.decode(), end='')
    if cmd == 'get fan3':
        p1 = subprocess.Popen(('sensors', 'it8665-isa-0290'), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(('grep', 'fan3'), stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p3 = subprocess.Popen(('cut', '-c14-21'), stdin=p2.stdout, stdout=subprocess.PIPE)
        p2.stdout.close()
        output = p3.communicate()[0]
        print(output.decode(), end='')
    if cmd == 'get fan4':
        p1 = subprocess.Popen(('sensors', 'it8665-isa-0290'), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(('grep', 'fan4'), stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p3 = subprocess.Popen(('cut', '-c14-21'), stdin=p2.stdout, stdout=subprocess.PIPE)
        p2.stdout.close()
        output = p3.communicate()[0]
        print(output.decode(), end='')
    if cmd == 'get cpu_temp':
        p1 = subprocess.Popen(('sensors', 'it8665-isa-0290'), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(('grep', 'temp1'), stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p3 = subprocess.Popen(('cut', '-c16-19'), stdin=p2.stdout, stdout=subprocess.PIPE)
        p2.stdout.close()
        output = p3.communicate()[0]
        print(output.decode(), end='')
        p3.stdout.close()
    if cmd == 'get gpu_temp':
        p1 = subprocess.Popen(args=('nvidia-smi', '-q', '-d', 'temperature'), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(('grep', 'GPU Current'), stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p3 = subprocess.Popen(('cut', '-c39-40'), stdin=p2.stdout, stdout=subprocess.PIPE)
        p2.stdout.close()
        output = p3.communicate()[0]
        print(output.decode(), end='')
        p3.stdout.close()
    if cmd == 'get cpu_util':
        p1 = subprocess.Popen(args=('mpstat'), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(('grep', 'all'), stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p3 = subprocess.Popen(('cut', '-c21-24'), stdin=p2.stdout, stdout=subprocess.PIPE)
        p2.stdout.close()
        output = p3.communicate()[0]
        print(output.decode(), end='')
        p3.stdout.close()
    if cmd == 'get gpu_util':
        p1 = subprocess.Popen(args=('nvidia-smi', '-q', '-d', 'utilization'), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(('grep', 'Gpu'), stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p3 = subprocess.Popen(('cut', '-c39-40'), stdin=p2.stdout, stdout=subprocess.PIPE)
        p2.stdout.close()
        output = p3.communicate()[0]
        print(output.decode(), end='')
        p3.stdout.close()
ser.close()
print('Good bye')
