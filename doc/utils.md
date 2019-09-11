# fwd.car.utils - basic driver

Usage:
```python
import subprocess
import os
import time

msg_dict = {}

soft_reset()               #reset the MCU

power_val = power_read()             # gain the power of picar_4wd

msg_dict = pi_read()               #gain the message of pi

```
## Constructors
```picar_4wd.utils```
The __init__.py supply the utile api for picar_4wd.

## Methods
- soft_reset() - reset the MCU .
```python
soft_reset()
```
- pi_read() - get the msg of pi such as ram.disk....
```python
- msg_dict = pi_read()
```
- power_read() - gain the power of picar_4wd.
```python
power_val = power_read() 
```
- getIP() - get the ip of pi.
```python
getIP()
```
