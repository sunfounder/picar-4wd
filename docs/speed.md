# class Speed

Usage:
```python
from picar_4wd.speed import Speed
                     
left_rear_speed = Speed(12)                  # create an Speed object from a pin
left_rear_speed.start()                      # start counter
sp_val = left_rear_speed()                   # get the speed 
```
## Constructors
```class  picar_4wd.speed.Speed(pin)```
Create an Speed object associated with the given pin . This allows you to get the speed values.

## Methods
- start - start the counter of speed.
```python
left_rear_speed = Speed(12)
left_rear_speed.start()
```