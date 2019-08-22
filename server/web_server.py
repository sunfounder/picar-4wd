from new_car import *
from edge_examine import Edge_examine_func
from follow import Follow
from remote_control import Remote_control
from velocity_measurement import speed_val
from follow_line import follow_line_func
import Obstacle_avoidance as oa

import asyncio
import websockets
import json

#接收数据字典
recv_dict = {'mode':1,'rc':2,'csb':['off','off','off'],'fl':['off',0],'ed':['off',1],'sp':0,'sr':'off','sps':['off',1,0],'csbs':['off',0]}
#发送数据字典
send_dict = {'fl':[0,0,0],'csb':3,'sp':4,'csbs':[0,0],'pi_msg':{'a':1}} 

  
#接收函数
async def recv_server_func(websocket):
    global recv_dict
    while 1:
        recv_dict = await websocket.recv()
        recv_dict = json.loads(recv_dict)
        print(recv_dict)
        Remote_control(recv_dict['rc'],recv_dict['sp'])
        if  recv_dict['sps'][0] =='on':#测试电机
            set_motor_speed(int(recv_dict['sps'][1]), int(recv_dict['sps'][2]))
        if  recv_dict['sr'] =='on':#复位
            soft_reset()#执行一次
        if  recv_dict['csbs'][0] =='on':
            send_dict['csbs'] = oa.distance_at(int(recv_dict['csbs'][1]))
        
#发送函数
async def send_server_func(websocket): 
    global send_dict
    while 1:
        send_dict['sp'] = speed_val()
        send_dict['csb'] = oa.web_csb_val_list
        # send_dict['pi_msg'] = pi_read()
        await websocket.send(json.dumps(send_dict))
        await asyncio.sleep(0.02)

#主服务程序
async def main_func():
    global recv_dict,send_dict
    while 1:
        motor = False
        us_mode = 0

        ed_list = Get_adc_value()
        send_dict['fl'] = ed_list
       
        if recv_dict['ed'][0] == 'on':#悬崖
            Edge_examine_func(recv_dict['ed'][1],ed_list)#110

        if recv_dict['fl'][0] =='on':#巡线
            follow_line_func(recv_dict['fl'][1],ed_list)#400

        if recv_dict['csb'] == ['on', 'off', 'on']:#避障
            # print("AO")
            motor = True
            us_mode = 0
            oa.pre_obstacle_avoidance(motor, us_mode)

        elif recv_dict['csb'] == ['off', 'on', 'on']:#跟随
            # print("F")
            motor = True
            us_mode = 1
            oa.pre_obstacle_avoidance(motor, us_mode)

        elif  recv_dict['csb'] == ['off', 'off', 'on']:#自动扫描获取数据
            # print("US ON")
            motor = False
            us_mode = 1
            oa.pre_obstacle_avoidance(motor, us_mode)
        # oa.pre_obstacle_avoidance(motor, us_mode)
      
        await asyncio.sleep(0.01)
        
async def main_logic_1(websocket,path):
    while 1:
        await recv_server_func(websocket)

async def main_logic_2(websocket,path):
    while 1:
        await send_server_func(websocket)

try:
    # start_http_server()
    start_server_1 = websockets.serve(main_logic_1,"192.168.18.223",8765)
    start_server_2 = websockets.serve(main_logic_2,"192.168.18.223",8766)
    print('Start!')
    tasks = [main_func(),start_server_1,start_server_2]
    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
    asyncio.get_event_loop().run_forever()
finally:
    print("Finished")
#     close_http_server()