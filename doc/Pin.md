# class Pin - control I/O pins

Usage:
```python
from picar_4wd.pin import Pin

pin = Pin("D0")                     # create an Pin object from a pin
val = pin.value()                    # read an analog value
```
## Constructors
```class picar_4wd.Pin(value)```
A pin is the basic object to control I/O pins. It has methods to set the mode of the pin (input, output, etc) and methods to get and set the digital logic level. For analog control of a pin, see the ADC class.

## Methods
- read - Read the value on the analog pin and return it. The returned value will be between 0 and 4095.
```python
ADC.read()
```