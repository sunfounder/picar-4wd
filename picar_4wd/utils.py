

import subprocess
import os
import time

def soft_reset():
    from picar_4wd.pin import Pin
    soft_reset_pin = Pin("D16")
    # print('soft_reset')
    soft_reset_pin.low()
    time.sleep(0.001)
    soft_reset_pin.high()
    time.sleep(0.001)

def mapping(x,min_val,max_val,aim_min,aim_max):
    x = aim_min + abs((x - min_val) / (max_val- min_val) * (aim_max-aim_min))
    return x

def cpu_temperature():          # cpu_temperature
    raw_cpu_temperature = subprocess.getoutput("cat /sys/class/thermal/thermal_zone0/temp")
    cpu_temperature = round(float(raw_cpu_temperature)/1000,2)               # convert unit
    #cpu_temperature = 'Cpu temperature : ' + str(cpu_temperature)
    return cpu_temperature

def gpu_temperature():          # gpu_temperature(
    raw_gpu_temperature = subprocess.getoutput( '/opt/vc/bin/vcgencmd measure_temp' )
    gpu_temperature = round(float(raw_gpu_temperature.replace( 'temp=', '' ).replace( '\'C', '' )), 2)
    #gpu_temperature = 'Gpu temperature : ' + str(gpu_temperature)
    return gpu_temperature

def cpu_usage():                # cpu_usage
    # result = str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print($2)}'").readline().strip())
    result = os.popen("mpstat").read().strip()
    result = result.split('\n')[-1].split(' ')[-1]
    result = round(100 - float(result), 2)
    result = str(result)
    # print(result)
    return result

def disk_space():               # disk_space
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()         
        if i==2:
            return line.split()[1:5]    

def ram_info():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return list(map(lambda x:round(int(x) / 1000,1), line.split()[1:4]))   

def pi_read():
    result = {
        "cpu_temperature": cpu_temperature(), 
        "gpu_temperature": gpu_temperature(),
        "cpu_usage": cpu_usage(), 
        "disk": disk_space(), 
        "ram": ram_info(), 
        "battery": power_read(), 
    }
    return result 

def power_read():
    from picar_4wd.adc import ADC
    power_read_pin = ADC('A4')
    power_val = power_read_pin.read()
    power_val = power_val / 4095.0 * 3.3
    # print(power_val)
    power_val = power_val * 3
    power_val = round(power_val, 2)
    return power_val

def getIP(ifaces=['wlan0', 'eth0']):
    import re
    if isinstance(ifaces, str):
        ifaces = [ifaces]
    for iface in list(ifaces):
        search_str = 'ip addr show {}'.format(iface)
        result = os.popen(search_str).read()
        com = re.compile(r'(?<=inet )(.*)(?=\/)', re.M)
        ipv4 = re.search(com, result)
        if ipv4:
            ipv4 = ipv4.groups()[0]
            return ipv4
    return False


def main():
    import sys
    if len(sys.argv) >= 2:
        print("Welcome to SunFounder PiCar-4WD.")
        command = sys.argv[1]
        if command == "soft-reset":
            print("soft-reset")
            soft_reset()
        elif command == "power-read":
            print("power-read")
            print("Power voltage: {}V".format(power_read()))
        elif command == "web-example":
            if len(sys.argv) >= 3:
                opt = sys.argv[2]
                if opt == "enable":
                    os.system("sudo update-rc.d picar-4wd-web-example defaults")
                    print("web-example start on boot is enabled")
                elif opt == "disable":
                    os.system("sudo update-rc.d picar-4wd-web-example remove")
                    print("web-example start on boot is disabled")
                else:
                    usage(command)
            else:
                print("Run: `picar-4wd web-example enable/disable` to enable/disable start on boot")
                os.system("sudo python3 /home/pi/picar-4wd/examples/web/start.py")
        elif command == "test":
            from picar_4wd import forward,get_distance_at,get_grayscale_list,stop
            if len(sys.argv) >= 3:
                opt = sys.argv[2]
                if opt == "motor":
                    print("Motor test start!, Ctrl+C to Stop")
                    forward(10)
                    try:
                        while True:
                            pass
                    except KeyboardInterrupt:
                        stop()
                elif opt == "servo":
                    print(get_distance_at(0))
                elif opt == "grayscale":
                    print(get_grayscale_list())
                else:
                    usage(command)
        else:
            print('Command error, "%s" is not in list' % sys.argv[1])
            usage()
    else:
        usage()
    destroy()

# def main():
#     try:
#         _main()
#     finally:

def destroy():
    quit()
 
def usage(cmd=None):
    general = '''
Usage:  picar-4wd [Command] [option]

Commands:
    soft-reset
    power-read
    web-example
    test
'''
    web_example = '''
Usage: picar-4wd web-example [option]

Options:
    enable    Enable start on boot
    disable   Disable start on boot
'''
    test = '''
Usage: picar-4wd test [option]

Options:
    motor      test the motor
    servo      test the servo
    grayscale  test the grayscale

'''
    if cmd == None:
        print(general)
    elif cmd == "web-example":
        print(web_example)
    elif cmd == "test":
        print(test)
    destroy()
        