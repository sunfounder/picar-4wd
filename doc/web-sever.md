# web-server- server process

Usage:
```python
import picar_4wd as fc
from picar_4wd.utils import pi_read
from remote_control import Remote_control
from picar_4wd import getIP

import asyncio
import websockets
import json
import time

start_server_1 = websockets.serve(main_logic_1, ip, 8765)
start_server_2 = websockets.serve(main_logic_2, ip, 8766)
tasks = [main_func(),start_server_1,start_server_2]
asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
asyncio.get_event_loop().run_forever()

```
## Constructors
```picar_4wd.__init__```
The web-server.py supply the server api for picar_4wd.

## Methods
- recv_server_func(websocket) - recv the data from client .

- send_server_func(websocket) - send the data to the client.

- main_func() - the main logic api.
```python
status = get_line_status(410,fl_list) 
```
- main_logic_1(websocket,path) - build a run forever recv api .

- main_logic_2(websocket,path) - build a run forever recv api.

