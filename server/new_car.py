from pwm import PWM
from adc import ADC 
from pin import Pin
import time
import subprocess, os
####
PERIOD = 4095
PRESCALER = 10
TIMEOUT = 0.02
speed = 0
MAX_PW = 2500
MIN_PW = 500
_freq = 50
_arr = 4095
CPU_CLOCK = 72000000
#19是按键引脚
#21是单片机复位脚
#复位触发引脚
soft_reset_pin = Pin("D16")  

#电池引脚
power_read_pin = ADC('A4')
#复位引脚
soft_reset_pin = Pin("D16")
#舵机
servo_pin = PWM('P0')
#电机
motor1_pwm_pin = PWM("P13")#motor 1
motor2_pwm_pin = PWM("P12")#motor 2
motor3_pwm_pin = PWM("P8")#motor 3
motor4_pwm_pin = PWM("P9")#motor 4
#电机方向控制脚
motor1_dir_pin = Pin("D4")#motor 1
motor2_dir_pin = Pin("D5")#motor 2
motor3_dir_pin = Pin("D11")#motor 3
motor4_dir_pin = Pin("D15")#motor 4
#三路adc
S0 = ADC('A5')
S1 = ADC('A6')
S2 = ADC('A7')


motor_direction_pins = [motor1_dir_pin, motor2_dir_pin, motor3_dir_pin, motor4_dir_pin]
motor_speed_pins = [motor1_pwm_pin, motor2_pwm_pin, motor3_pwm_pin, motor4_pwm_pin]

cali_dir_value = [1, 1, 1, 1]
cali_speed_value = [0, 0, 0, 0]

servo_pin.period(4095)
prescaler = int(float(CPU_CLOCK) / _freq/ _arr)
servo_pin.prescaler(prescaler)

simi_val = 10
#初始化引脚
for pin in motor_speed_pins:
    pin.period(PERIOD)
    pin.prescaler(PRESCALER)
def soft_reset():
    print('soft_reset')
    soft_reset_pin.low()
    time.sleep(0.001)
    soft_reset_pin.high()

def power_read():
    power_val = power_read_pin.read()
    return power_val


def map_angle(x,min_val,max_val,aim_min,aim_max):
    x = aim_min + abs((x - min_val) / (max_val- min_val) * (aim_max-aim_min))
    return x

def angle(angle):
    global simi_val
    try:
        angle = int(angle)
    except:
        raise ValueError("Angle value should be int value, not %s"%angle)
    if angle < -90:
        angle = -90
    if angle > 90:
        angle = 90
    angle = angle + simi_val
    High_level_time = map_angle(angle, -90, 90, MIN_PW, MAX_PW)
    pwr =  High_level_time / 20000
    value = int(pwr*4095)
    servo_pin.pulse_width(value)

def set_motor_speed(motor, speed):
    motor -= 1
    if speed >= 0:
        direction = 1 * cali_dir_value[motor]
    elif speed < 0:
        direction = -1 * cali_dir_value[motor]
    speed = abs(speed)
    if speed != 0:
        speed = int(speed /2 ) + 50
    speed = speed - cali_speed_value[motor]
    if direction < 0:
        motor_direction_pins[motor].high()
    else:
        motor_direction_pins[motor].low()
        
    motor_speed_pins[motor].pulse_width_percent(speed*0.9)

def motor_speed_calibration(value):
    global cali_speed_value
    if value < 0:
        cali_speed_value[0] = 0
        cali_speed_value[1] = abs(value)
    else:
        cali_speed_value[0] = abs(value)
        cali_speed_value[1] = 0

def motor_direction_calibration(motor, value):
    # 0: positive direction
    # 1:negative direction
    motor -= 1
    if value == 1:
        cali_dir_value[motor] = -cali_dir_value[motor]

def Get_adc_value():
    adc_value_list = []
    adc_value_list.append(S0.read())
    adc_value_list.append(S1.read())
    adc_value_list.append(S2.read())
    return adc_value_list

def forward(speed):
    set_motor_speed(1, speed)
    set_motor_speed(2, speed)
    set_motor_speed(3, speed)
    set_motor_speed(4, -1*speed)

def backward(speed):
    set_motor_speed(1,  -1*speed)
    set_motor_speed(2,  -1*speed)
    set_motor_speed(3,  -1*speed)
    set_motor_speed(4,  speed)

def turn_left(speed):
     set_motor_speed(1, -1 * speed)
     set_motor_speed(2, speed)
     set_motor_speed(3, -1*speed)
     set_motor_speed(4, -1*speed)


def turn_right(speed):
     set_motor_speed(1, speed)
     set_motor_speed(2, -1*speed)
     set_motor_speed(3,  speed)
     set_motor_speed(4,  speed)

def stop():
    set_motor_speed(1, 0)
    set_motor_speed(2, 0)
    set_motor_speed(3, 0)
    set_motor_speed(4, 0)

def turn_back(speed):
    set_motor_speed(1, -1 *speed)
    set_motor_speed(2,  speed)
    set_motor_speed(3, -1 *speed)
    set_motor_speed(4,  speed)



def head_rotate():
    for i in range(-90,90):
        angle(i)
        time.sleep(0.01)
    for i in range(90,-90):
        angle(i)
        time.sleep(0.01)

def Get_distance(timeout_val = 0.01):
    timeout = timeout_val
    trig = Pin('D8')
    echo = Pin('D9')

    trig.low()
    time.sleep(0.01)
    trig.high()
    time.sleep(0.000015)
    trig.low()
    pulse_end = 0
    pulse_start = 0
    timeout_start = time.time()
    while echo.value()==0:
        pulse_start = time.time()
        if pulse_start - timeout_start > timeout:
            return -1
    while echo.value()==1:
        pulse_end = time.time()
        if pulse_end - timeout_start > timeout:
            return -2
    during = pulse_end - pulse_start
    cm = round(during * 340 / 2 * 100, 2)
    #print(cm)
    return cm

def cpu_temperature():          # 检测CPU温度
        raw_cpu_temperature = subprocess.getoutput("cat /sys/class/thermal/thermal_zone0/temp")
        cpu_temperature = float(raw_cpu_temperature)/1000               # 换算成摄氏温度
        #cpu_temperature = 'Cpu temperature : ' + str(cpu_temperature)
        return cpu_temperature

def gpu_temperature():          # 检测GPU温度===GPU---用于图形处理
    raw_gpu_temperature = subprocess.getoutput( '/opt/vc/bin/vcgencmd measure_temp' )
    gpu_temperature = float(raw_gpu_temperature.replace( 'temp=', '' ).replace( '\'C', '' ))
    #gpu_temperature = 'Gpu temperature : ' + str(gpu_temperature)
    return gpu_temperature

def cpu_usage():                # CPU占用率
    # result = str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print($2)}'").readline().strip())
    result = os.popen("mpstat").read().strip()
    result = result.split('\n')[-1].split(' ')[-1]
    result = round(100 - float(result), 2)
    result = str(result)
    # print(result)
    return result

def disk_space():               # 磁盘占有率
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()         # readline一次读取p中的一行内容， 占用内存小；read--一次性读取p中的所有内容，占用内存大
        if i==2:
            return line.split()[1:5]    # 以第二个到第五个（空格、换行(\n)、制表符(\t)）等为分隔符，将line字符串分成4段

def disk_used():
    disk_used = float(disk_space()[1][:-1])
    return disk_used

def ram_info():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return line.split()[1:4]    # 以第二个到第四个（空格、换行(\n)、制表符(\t)）等为分隔符，将line字符串分成4段

def ram_used():
    ram_used = round(int(ram_info()[1]) / 1000,1)  # round---返回浮点数，四舍五入保留一位小数
    return ram_used

def pi_read():
    result = {
        "cpu_temperature": cpu_temperature(), 
        "gpu_temperature": gpu_temperature(),
        "cpu_usage": cpu_usage(), 
        "disk_used": disk_used(), 
        "ram_used": ram_used(), 
    }
    return result 


if __name__ == "__main__":
# soft_reset()
    while 1:
        # angle(0)
        pi_read()
        # cpu_usage()
        # soft_reset()
        # # time.sleep(2)
     