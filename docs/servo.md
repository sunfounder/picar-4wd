# class Servo - 3-wire pwm servo driver

Usage:
```python
from picar_4wd.servo import Servo
from picar_4wd.pwm import PWM

ser = Servo(PWM("P0"))                     # create an Servo object from a pin
ser.set_angle(60)                   # set the servo angle
```
## Constructors
```class picar_4wd.servo.Servo(pin)```
Create an Servo object associated with the given pin which start with "P". This allows you to set the angle values.

## Methods
- set_angle(angle) - set the angle values between -90 and 90.
```python
set_angle(90)
```