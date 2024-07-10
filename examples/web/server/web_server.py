import picar_4wd as fc
from picar_4wd.utils import pi_read
from remote_control import Remote_control
from picar_4wd import getIP

import asyncio
# import websockets
from websockets.server import serve
import json
import time

fc.start_speed_thread()
speed_count = 0
gs_list = []


recv_dict = {
    'RC':'forward',
    'GS': "off",
    'RD':'off',
    'OA':'off',
    'OF':'off',
    'TL':['off',400],
    'CD':['off',110],
    'PW':1,
    'SR':0,
    'ST':'off',
    'US':['on',0],
    'MS':['off',0,0]
}

send_dict = {
    'GS': [0,0,0],
    'US':[0,0],
    'MS':[0,0],
    'ST':{'a':1}
} 

async def recv_server_func(websocket):
    global recv_dict,send_dict
    # while 1:
    #     tmp = await websocket.recv()
    async for message in websocket:
        tmp = json.loads(message)
        for key in tmp:
            recv_dict[key] = tmp[key]
        recv_dict['PW'] = int(recv_dict['PW'])
        Remote_control(recv_dict['RC'],recv_dict['PW'])
        # print(recv_dict)
        if  recv_dict['MS'][0] =='on':
            fc.set_motor_power(int(recv_dict['MS'][1]), int(recv_dict['MS'][2]))
        if  recv_dict['SR'] =='on':
            fc.soft_reset()

async def send_server_func(websocket): 
    global send_dict, recv_dict, gs_list 
    while 1:
        send_dict ={}
        send_dict['MS'] = [round(fc.speed_val()/2.0),time.time()] 
        
        if recv_dict['ST'] == 'on': 
            send_dict['ST'] = pi_read() 

        if  recv_dict['US'][0] =='on':
            send_dict['US'] = [int(recv_dict['US'][1]),fc.get_distance_at(int(recv_dict['US'][1]))]
        else:
            send_dict['US'] = fc.angle_distance
        
        if  recv_dict['GS'] =='on': 
            send_dict['GS'] = gs_list
        await websocket.send(json.dumps(send_dict))
        await asyncio.sleep(0.01)
        
async def main_func():
    global recv_dict,send_dict,gs_list
    while 1:
        gs_list = fc.get_grayscale_list()
        
        if recv_dict['CD'][0] == 'on':
            if fc.is_on_edge(recv_dict['CD'][1],gs_list):
                fc.backward(20)
                time.sleep(0.5)
                fc.stop()

        if recv_dict['TL'][0] =='on':
            if fc.get_line_status(recv_dict['TL'][1],gs_list) == 0:
                fc.forward(recv_dict['PW'])      
            elif fc.get_line_status(recv_dict['TL'][1],gs_list) == -1:
                fc.turn_left(recv_dict['PW'])
            elif fc.get_line_status(recv_dict['TL'][1],gs_list) == 1:
                fc.turn_right(recv_dict['PW']) 

        if recv_dict['OA'] == 'on':
            scan_list = fc.scan_step(35)
            if scan_list:
                tmp = scan_list[3:7]
                if tmp != [2,2,2,2]:
                    fc.turn_right(recv_dict['PW'])
                else:
                    fc.forward(recv_dict['PW'])

        elif recv_dict['OF'] == 'on':
            scan_list = fc.scan_step(23)
            
            if scan_list != False:
                scan_list = [str(i) for i in scan_list]
                scan_list = "".join(scan_list)
                paths = scan_list.split("2")
                length_list = []
                for path in paths:
                    length_list.append(len(path))
                if max(length_list) == 0:
                    fc.stop() 
                else:
                    i = length_list.index(max(length_list))
                    pos = scan_list.index(paths[i])
                    pos += (len(paths[i]) - 1) / 2
                    delta = len(scan_list) / 3
                    if pos < delta:
                        fc.turn_left(recv_dict['PW'])
                    elif pos > 2 * delta:
                        fc.turn_right(recv_dict['PW'])
                    else:
                        if scan_list[int(len(scan_list)/2-1)] == "0":
                            fc.backward(recv_dict['PW'])
                        else:
                            fc.forward(recv_dict['PW'])
    
        elif  recv_dict['RD'] == 'on':
            fc.scan_step(35)
      
        await asyncio.sleep(0.01)
        
async def receive_task():
    async with serve(recv_server_func, "*", 8765):
        await asyncio.Future()  # run forever

async def send_task():
    async with serve(send_server_func, "*", 8766):
        await asyncio.Future()  # run forever

async def main():
    # main_task = asyncio.create_task(main_func())
    print('Start!')

    # 创建并同时运行receive_task, send_task 和 main_func
    await asyncio.gather(
        receive_task(),
        send_task(),
        main_func()  # 假设main_func是另一个需要并发运行的异步函数
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        print("Finished")
        fc.stop()