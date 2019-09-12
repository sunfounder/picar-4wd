# class Ultrasonic 
Usage:
```python
from picar_4wd.Ultrasonic import Ultrasonic
                     
us = Ultrasonic(Pin('D8'), Pin('D9'))                  # create an Ultrasonic object from the given pin
dis_val = us.get_distance()                      # get the distance
```
## Constructors
```class  picar_4wd.Ultrasonic.Ultrasonic(pin)```
Create an Ultrasonic object associated with the given pin . This allows you to get the Ultrasonic values.

## Methods
- get_distance() - get the distance.
```python
dis_val = us.get_distance()                      # get the distance
```