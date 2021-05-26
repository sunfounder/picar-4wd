# class Pin - control I/O pins

Usage:
```python
from picar_4wd.pin import Pin

pin = Pin("D0")                     # create an Pin object from a pin
val = pin.value()                    # read an analog value
```
## Constructors
```class picar_4wd.pin.Pin(value)```
A pin is the basic object to control I/O pins. It has methods to set the mode of the pin (input, output, etc) and methods to get and set the digital logic level. For analog control of a pin, see the ADC class.

## Methods
- init(self, mode, pull=PULL_NONE) - set up the mode and pull mode of the pin.
```python
Pin.init(IN,PULL_UP)
```

- value(self, *value) - set or get the value of the pin.
```python
Pin.value()   #get the value of the pin

pin.value(1)  #set the value of the pin
```

- high(self) - Set to high level.
```python
Pin.high()
```

- low(self) - Set to low level.
```python
Pin.low()
```

- mode(self, *value) - set or get the mode of the pin.
```python
Pin.mode()   #get the mode of the pin

Pin.mode(IN)   #set the mode of the pin
```

- pull(self, *value) - Set to pull mode.
```python
Pin.pull(PULL_UP)
```

- irq(self, handler=None, trigger=None) - set the irq of the pin.
```python
def irq_test():
    print("high")

Pin.irq(IRQ_RISING,irq_test) 
```
- name(self) - Return the pin num of the rpi.
```python
pin_name = Pin.name()
```
- names(self) - Return the pin names and the  pin num of the rpi.
```python
pin_names = []
pin_names = Pin.names()
```