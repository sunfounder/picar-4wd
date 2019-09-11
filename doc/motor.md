# class Motor - analog to digital converter

Usage:
```python
from picar_4wd.Motor import Motor

mt = Motor(PWM("P13"), Pin("D4"), is_reversed=False)                    # create a Motor object from a Pin object and a PWM object
mt.set_power(10)                   # set the power value
```
## Constructors
```class picar_4wd.Motor(pwm,pin,is_reversed=False)```
Create an Motor object associated with the given pin. This allows you to then set the values on that pin.

## Methods
- set_power - set the power of motor the value between 0 and 4095.
```python
Motor(PWM("P13"), Pin("D4"), is_reversed=False) .set_power(10)
```