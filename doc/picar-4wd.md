# PiCar-4WD document
## This document is used to introduce the structure, function, code and so on. In addition, it describes how the easy functions are realized. 
## Overview：PiCar-4WD is the 4WD car that is built based on the Raspberry Pi, with the functions, including line following, following, obstacle avoidance, speed testing,  remote control, radar testing.

### Main structures of package:
Open `picar-4wd`, there are 4 files of codes:
 - bin
 - data
 - exmaple
 - fwd_car
 - doc the contents are as follows:

#### picar-4wd: The files of fwd_car: adc，pin，i2c，pwm are the core driving libraries.   
`picar_4wd.__init__.py` is a functions of basic functions made of core driving libraries.  
The file, `picar_4wd.utils` contains the functions of system function about the Raspberry Pi. 

#### example: The performance functions that can be run directly.(eg. Line following)

#### data: Initialize the rotating direction of the wheels of the car and calibrate the servo.


#### bin: program some statements concerning starting up the service by means of command lines.

## Main functions realization uses the documents in the file fwd_car. Refer to the  relevant md ducument.

## picar-4wd. The car supports the command of the command lines, as shown below.
### command format：picar-4wd + command + control bit (this item is available for some specific commands.)  

#### Command 1：web-example
```python
pi@raspberrypi:picar-4wd web-example  ##start up web-example service (with the prerequisite that there is no setting of Start On Boot).
pi@raspberrypi:picar-4wd web-example enable  ##turn on web-example Start On Boot
pi@raspberrypi:picar-4wd web-example disable  ##turn off web-example Start On Boot
```
#### Command 2：soft-reset
```python
pi@raspberrypi:picar-4wd soft-reset  ## reset Mcu
```
#### Command 3：power-read
```python
pi@raspberrypi:picar-4wd power-read  ##check the voltage of the car
```
#### Command 3：test
```python
pi@raspberrypi:picar-4wd test motor  ##test the motor of the car
pi@raspberrypi:picar-4wd test servo  ##test the servo of the car
pi@raspberrypi:picar-4wd test grayscale  ##test the Grayscale Sensor of the car
```

## Play：get the product：
1. Boot the Raspberry Pi
2. Download the project picar-4wd by using cammand
```python
pi@raspberrypi:git clone https://github.com/sunfounder/picar-4wd ##download the project
```
3. With download done, you can get a picar-4wd directory，then click into it.
4. By using "sudo python3 setup.py install" download some relevant libraries and execute configurations for the Raspberry Pi. If the downloading runs well, you should notice the finish in the last line.
5. Download and configuration done, execute the command "picar-4wd web-example" to turn on the service (If you need other commands, such as Start on Boot and testing motor or servo, please refer to the commands lines above.)
6. Input the IP address that once appeared in the command lines at the client-side, and you can access the website.
7. If the Raspberry Pi has executed the first 4 steps, the car can be played by the execution of the fifth and sixth step.

