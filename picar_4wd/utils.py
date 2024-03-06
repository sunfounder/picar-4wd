import subprocess
import os
import time
import psutil

user_name = os.getlogin()


def run_command(cmd=""):
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    result = process.stdout.read().decode('utf-8')
    status = process.poll()
    return status, result


def run_command_in_background(cmd=""):
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return process.pid


def soft_reset():
    from .pin import Pin
    soft_reset_pin = Pin("D16")
    soft_reset_pin.low()
    time.sleep(0.01)
    soft_reset_pin.high()
    time.sleep(0.01)
    soft_reset_pin.close()


def mapping(x, min_val, max_val, aim_min, aim_max):
    x = aim_min + abs(
        (x - min_val) / (max_val - min_val) * (aim_max - aim_min))
    return x


def cpu_temperature():  # cpu_temperature
    return round(psutil.sensors_temperatures()['cpu_thermal'][0].current, 2)


def cpu_usage():
    return psutil.cpu_percent()


def disk_space():  # disk_space
    disk = [0] * 4
    result = psutil.disk_usage('/')
    disk[0] = round(result.total / 1024 / 1024 / 1024, 2)  # GB
    disk[1] = round(result.used / 1024 / 1024 / 1024, 2)  # GB
    disk[2] = round(result.free / 1024 / 1024 / 1024, 2)  # GB
    disk[3] = result.percent  # percent
    return disk


def ram_info():
    ram = [0] * 3
    result = psutil.virtual_memory()
    ram[0] = result.total / 1024 / 1024  # MB
    ram[1] = result.used / 1024 / 1024  # MB
    ram[2] = result.percent  # percent
    return ram


def pi_read():
    result = {
        "cpu_temperature": cpu_temperature(),
        "cpu_usage": cpu_usage(),
        "disk": disk_space(),
        "ram": ram_info(),
        # "battery": power_read(), # adc can not read with multiple threads
        "battery": 0,
    }
    return result


def power_read():
    from picar_4wd.adc import ADC
    power_read_pin = ADC('A4')
    power_val = power_read_pin.read()
    power_val = power_val / 4095.0 * 3.3
    # print(power_val)
    power_val = power_val * 3
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
