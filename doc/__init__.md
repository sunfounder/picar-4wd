# picar_4wd.__intit__ - basic driver

Usage:
```python
from picar_4wd import *

gs_list = []
picar_4wd_speed = 0

forward(50)               #set up the forward speed

gs_list = get_grayscale_list()             # get the data of grayscale

picar_4wd_speed = speed_val()               # get picar_4wd speed

```
## Constructors
```picar_4wd.__init__```
The __init__.py supply the basic driver for picar_4wd.

## Methods
- start_speed_thread() - start the thread of speed api .
```python
start_speed_thread()
```
- is_on_edge(ref, gs_list) - ed_judging whether on the edge.
```python
status = is_on_edge(110, gs_list)
```
- get_line_status(ref,fl_list) - get the line status.
```python
status = get_line_status(410,fl_list) 
```
- get_distance_at(angle) - get the angle and distance.
```python
ad_list = []
ad_list = get_distance_at(0) 
```
- get_status_at(angle, ref1=35, ref2=10) - get the status of distance.
```python

status = get_status_at(0) 
```
- scan_step(ref) - scan a range of angle.
```python
scan_step() 
```
- forward(power) - let the car forward.
```python
forward(10)
```
- backward(power) - let the car backward.
```python
backward(10)
```
- turn_left(power) - let the car turn_left.
```python
turn_left(10)
```
- turn_right(power) - let the car turn_right.
```python
turn_right(10)
```
- stop() - let the car stop
```python
stop()
```
- set_motor_power(motor, power) - set the motor power.
```python
set_motor_power(1, 20)
```
- speed_val() - return the speed of the picar_4wd
```python
speed = speed_val()
```
