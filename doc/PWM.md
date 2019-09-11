# class PWM - pulse width modulation

Usage:
```python
from picar_4wd.pwm import PWM

pwm = PWM('P0')                    # create an pwm object from a pin
pwm.freq(50)                       # set freq 50Hz
pwm.prescaler(2)                   # set prescaler 
pwm.period(100)                    # set period 

pwm.pulse_width(10)                # set pulse_width 
pwm.pulse_width_percent(50)        # set pulse_width_percent 
```
## Constructors
```class picar_4wd.PWM(channel)```
Create an PWM object associated with the given pin. This allows you set up the pwm function on that pin.

## Methods
- freq - set the pwm channel freq.
```python
PWM.freq(50)
```
- prescaler - set the pwm channel prescaler.
```python
PWM.prescaler(50)
```
- period - set the pwm channel period.
```python
PWM.period(100)
```
- pulse_width - set the pwm channel pulse_width.
```python
PWM.pulse_width(10)
```
- pulse_width_percent - set the pwm channel pulse_width_percent.
```python
PWM.pulse_width_percent(50)
```