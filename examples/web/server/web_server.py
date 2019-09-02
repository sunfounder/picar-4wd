import fwd_car as fc
from fwd_car.utils import pi_read
from remote_control import Remote_control
from fwd_car import getIP

import asyncio
import websockets
import json
import time

fc.start_speed_thread()
speed_count = 0
gs_list = []
# #接收数据字典
# recv_dict = {
#     'mode':1,
#     'rc':0,
#     'csb':['off','off','off'],
#     'fl':['off',400],
#     'ed':['off',110],
#     'sp':0,
#     'sr':'off',
#     'pi_msg':'off',
#     'sps':['off',4,0],
#     'csbs':['off',0]
    
# }

#接收数据字典
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

#发送数据字典
# send_dict = {'TL':[0,0,0],'US':3,'sp':0,'csbs':[0,0],'pi_msg':{'a':1},'sps':0} 

#发送数据字典
# send_dict = {'fl':[0,0,0],'csb':3,'sp':0,'pi_msg':{'a':1},'sps':0} 
#发送数据字典
send_dict = {
    'GS': [0,0,0],
    'US':[0,0],
    'MS':[0,0],
    'ST':{'a':1}
} 
  
#接收函数
# async def recv_server_func(websocket):
#     global recv_dict,send_dict
#     while 1:
#         tmp = await websocket.recv()
#         tmp = json.loads(tmp)
#         for key in tmp:
#             recv_dict[key] = tmp[key]
#         recv_dict['sp'] = int(recv_dict['sp'])
#         print(recv_dict)
#         Remote_control(recv_dict['rc'],recv_dict['sp'])
#         if  recv_dict['sps'][0] =='on':#测试电机
#             fc.set_motor_speed(int(recv_dict['sps'][1]), int(recv_dict['sps'][2]))
#             # print(int(recv_dict['sps'][1]), int(recv_dict['sps'][2]))
#             send_dict['sp'] = fc.speed_val()

#         if  recv_dict['sr'] =='on':#复位
#             fc.soft_reset()#执行一次

#         if  recv_dict['csbs'][0] =='on':
#             send_dict['csbs'] = [recv_dict['csbs'][1], fc.get_distance_at(int(recv_dict['csbs'][1]))]


async def recv_server_func(websocket):
    global recv_dict,send_dict
    while 1:
        tmp = await websocket.recv()
        tmp = json.loads(tmp)
        for key in tmp:
            recv_dict[key] = tmp[key]
        recv_dict['PW'] = int(recv_dict['PW'])
        Remote_control(recv_dict['RC'],recv_dict['PW'])
        if  recv_dict['MS'][0] =='on':#测试电机
            fc.set_motor_power(int(recv_dict['MS'][1]), int(recv_dict['MS'][2]))
        if  recv_dict['SR'] =='on':#复位
            fc.soft_reset()#执行一次
        print("recv_dict")


# #发送函数
# async def send_server_func(websocket): 
#     global send_dict,recv_dict
#     while 1:
#         global sp_count
#         sp_count +=1
#         send_dict['sp'] = fc.speed_val()
#         print(send_dict)
#         if sp_count >= 50:
#             sp_count = 0  
#             send_dict['sps'] = fc.speed_val(recv_dict['sps'][1])
#         send_dict['csb'] = fc.angle_distance
#         # print(send_dict)
        # print(recv_dict)
#         if recv_dict['pi_msg'] == 'on': 
#             send_dict['pi_msg'] = pi_read()
#         await websocket.send(json.dumps(send_dict))
#         await asyncio.sleep(0.02)

#发送函数
async def send_server_func(websocket): 
    global send_dict, recv_dict, gs_list 
    while 1:
        send_dict ={}
        send_dict['MS'] = [round(fc.speed_val()/2.0),time.time()] 
        
        # global speed_count
        # speed_count += 1
        # if speed_count >= 50: 
        #     speed_count = 0
        #     send_dict['MS'] = [round(fc.speed_val()/2.0,2),int(time.time())]
        #     print(send_dict)
        #     send_dict['MS'][0] = fc.speed_val()
        #     send_dict['MS'][1] = int(time.time())

        if recv_dict['ST'] == 'on': #树莓派系统信息
            send_dict['ST'] = pi_read() 

        if  recv_dict['US'][0] =='on':#超声波测试
            send_dict['US'] = [int(recv_dict['US'][1]),fc.get_distance_at(int(recv_dict['US'][1]))]
        else:
            send_dict['US'] = fc.angle_distance
        
        if  recv_dict['GS'] =='on':#循迹模块
            # print(gs_list) 
            send_dict['GS'] = gs_list
        print("send_dict")
        await websocket.send(json.dumps(send_dict))
        await asyncio.sleep(0.02)
        
#主服务程序
async def main_func():
    global recv_dict,send_dict,gs_list
    while 1:
        gs_list = fc.get_grayscale_list()
        
        # if speed_count >= 100:
        #     speed_count = 0
        #     send_dict['MS'] = [fc.speed_val(),int(time.time())]
        #     print(send_dict)
        # send_dict['GS'] = gs_list
        # edge detect
        if recv_dict['CD'][0] == 'on':#悬崖
            if fc.is_on_edge(recv_dict['CD'][1],gs_list):
                fc.backward(20)
                time.sleep(0.5)
                fc.stop()

        if recv_dict['TL'][0] =='on':#巡线
            if fc.get_line_status(recv_dict['TL'][1],gs_list) == 0:
                fc.forward(recv_dict['PW'])      
            elif fc.get_line_status(recv_dict['TL'][1],gs_list) == -1:
                fc.turn_left(recv_dict['PW'])
            elif fc.get_line_status(recv_dict['TL'][1],gs_list) == 1:
                fc.turn_right(recv_dict['PW']) 

        if recv_dict['OA'] == 'on':#避障
            scan_list = fc.scan_step(35)
            if scan_list:
                tmp = scan_list[3:7]
                # print(tmp)
                if tmp != [2,2,2,2]:
                    fc.turn_right(recv_dict['PW'])
                else:
                    fc.forward(recv_dict['PW'])

        elif recv_dict['OF'] == 'on':#跟随
            scan_list = fc.scan_step(23)
            
            if scan_list != False:
                # print(scan_list)
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
    
        elif  recv_dict['RD'] == 'on':#自动扫描获取数据
            fc.scan_step(35)
        # print("main")
      
        await asyncio.sleep(0.01)
        
async def main_logic_1(websocket,path):
    while 1:
        await recv_server_func(websocket)

async def main_logic_2(websocket,path):
    while 1:
        await send_server_func(websocket)

try:
    for _ in range(10):
        ip = getIP()
        if ip:
            print("IP Address: "+ ip)
            # start_http_server()
            break
        time.sleep(1)
    start_server_1 = websockets.serve(main_logic_1, ip, 8765)
    start_server_2 = websockets.serve(main_logic_2, ip, 8766)
    print('Start!')
    tasks = [main_func(),start_server_1,start_server_2]
    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
    asyncio.get_event_loop().run_forever()
 
finally:
    print("Finished")
    fc.stop()