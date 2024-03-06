from picar_4wd.utils import pi_read, getIP, soft_reset
from picar_4wd import Picar4WD

import asyncio
import websockets
import threading
import json
import time

# --- init picar_4wd ---
mycar = Picar4WD()
mycar.start_speed_thread()

# --- variables ---
PORT = 8765

OBSTACLE_AVOID_REFERENCE = 35
line_reference = 400
cliff_reference = 110

speed_count = 0
gs_list = []
speed_data = []
scan_list = False
pi_info = {}
power = 0
client_num = 0
recv_dict = {
    'RC': 'off',
    'GS': "off",
    'RD': 'off',
    'OA': 'off',
    'OF': 'off',
    'TL': ['off', line_reference],
    'CD': ['off', cliff_reference],
    'PW': 0,
    'SR': 0,
    'ST': 'off',
    'US': ['off', 0],
    'MS': ['off', 0, 0]
}

send_dict = {
    'GS': [0, 0, 0],
    'US': [0, 0],
    'MS': [0, 0],
    'ST': {
        'a': 1
    },
}

adc_thread_lock = threading.Lock()


# ------------------ track line  ------------------
def track_line(ref, power):
    if mycar.get_line_status(ref, gs_list) == 0:
        mycar.forward(power)
    elif mycar.get_line_status(ref, gs_list) == -1:
        mycar.turn_left(power)
    elif mycar.get_line_status(ref, gs_list) == 1:
        mycar.turn_right(power)


# ------------------ obstacle_avoid ------------------
def obstacle_avoid(power):
    if not scan_list:
        return

    tmp = scan_list[3:7]
    if tmp != [2, 2, 2, 2]:
        mycar.turn_right(power)
    else:
        mycar.forward(power)


# ------------------ obstacle_follow ------------------
def obstacle_follow(power):
    if not scan_list:
        return

    scan_list_temp = [str(i) for i in scan_list]
    scan_list_temp = "".join(scan_list_temp)
    paths = scan_list_temp.split("2")
    length_list = []
    for path in paths:
        length_list.append(len(path))
    if max(length_list) == 0:
        mycar.stop()
    else:
        i = length_list.index(max(length_list))
        pos = scan_list_temp.index(paths[i])
        pos += (len(paths[i]) - 1) / 2
        delta = len(scan_list_temp) / 3
        if pos < delta:
            mycar.turn_left(power)
        elif pos > 2 * delta:
            mycar.turn_right(power)
        else:
            if scan_list_temp[int(len(scan_list_temp) / 2 - 1)] == "0":
                mycar.backward(power)
            else:
                mycar.forward(power)


# ------------------ remote_control ------------------
def remote_control(car, control_flag, speed=50):
    speed = int(speed)
    if control_flag == 'forward':
        car.forward(speed)
    elif control_flag == 'backward':
        car.backward(speed)
    elif control_flag == 'turn_left':
        car.turn_left(speed)
    elif control_flag == 'turn_right':
        car.turn_right(speed)
    else:
        car.stop()


# ------------------ websockets serve ------------------
async def websockets_handler(websocket):
    global recv_dict, send_dict, client_num
    # ---- clien connected ----
    _client_ip = websocket.remote_address[0]
    print(f'client {_client_ip} connected')
    client_num += 1
    print(f'client {client_num}')
    # ---- event loop ----
    while True:
        try:
            # -- recv --
            try:
                tmp = await asyncio.wait_for(websocket.recv(), timeout=0.001)
                print("websocket.recv() temp: %s" % tmp)

                tmp = json.loads(tmp)
                for key in tmp:
                    recv_dict[key] = tmp[key]
            except asyncio.TimeoutError as e:
                pass

            # -- send --
            try:
                send_tmp = send_dict.copy()
                await websocket.send(json.dumps(send_tmp))
            except Exception as e:
                print('send Exception: %s' % e)

            # --- delay ---
            await asyncio.sleep(0.01)

        except websockets.exceptions.ConnectionClosed as connection_code:
            print(f'client {_client_ip} disconneted')
            print(f'{connection_code}')
            break
    client_num -= 1


async def websocket_serve_set():
    async with websockets.serve(websockets_handler, "0.0.0.0", PORT):
        await asyncio.Future()  # run forever


def websocket_run():
    asyncio.run(websocket_serve_set())


def start_serve():
    serve_thread = threading.Thread(target=websocket_run)
    serve_thread.daemon = True
    serve_thread.start()


# ------------------ system_info_read_thread ------------------
def system_info_read_handler():
    global send_dict, pi_info

    while True:
        # pi system info
        if recv_dict['ST'] == 'on':
            with adc_thread_lock:
                send_dict['ST'] = pi_read()
        else:
            # print('system_info_read pass')
            pass
        time.sleep(0.5)


def start_system_info_thread():
    _thread = threading.Thread(target=system_info_read_handler)
    _thread.daemon = True
    _thread.start()


# ------------------ main ------------------
def main():
    global send_dict, recv_dict, gs_list, scan_list
    global power, cliff_reference, line_reference

    try:
        # --- get ip ---
        for _ in range(10):
            ip = getIP()
            if ip:
                # print("IP Address: "+ ip)
                break
            time.sleep(1)
        # --- start ---
        print(f'web server start at: http://{ip}')
        start_serve()
        start_system_info_thread()

        # --- main loop ---
        while True:
            # ------------------ get data ------------------
            # speed
            send_dict['MS'] = [round(mycar.speed_val() / 2.0), time.time()]

            # ultrasonic
            if recv_dict['RD'] == 'on':
                scan_list = mycar.scan_step(OBSTACLE_AVOID_REFERENCE)
            elif recv_dict['US'][0] == 'on':
                mycar.get_distance_at(int(recv_dict['US'][1]))

            send_dict['US'] = mycar.angle_distance

            # grayscale
            if recv_dict['GS'] == 'on' or recv_dict['CD'][0] == 'on':
                with adc_thread_lock:
                    gs_list = mycar.get_grayscale_list()
                    send_dict['GS'] = gs_list

            # ------------------ control ------------------
            # --- power set ---
            power = int(recv_dict['PW'])

            # --- reset ---
            if recv_dict['SR'] == 'on':
                soft_reset()

            # --- single wheel control (setting) ---
            if recv_dict['MS'][0] == 'on':
                mycar.set_motor_power(int(recv_dict['MS'][1]),
                                      int(recv_dict['MS'][2]))

            # --------------- manual ---------------
            # --- cliff detect ---
            if recv_dict['CD'][0] == 'on':
                cliff_reference = recv_dict['CD'][1]
                if mycar.is_on_edge(cliff_reference, gs_list):
                    if recv_dict['RC'] == 'backward':
                        remote_control(mycar, 'backward', power)
                    else:
                        mycar.stop()
                    continue  # Do not execute the content below

            _is_auto = False
            # --- track line ---
            if recv_dict['TL'][0] == 'on':
                _is_auto = True
                line_reference = recv_dict['TL'][1]
                track_line(line_reference, power)

            # --- obstacle avoid and obstacle follow ---
            if recv_dict['OA'] == 'on':
                _is_auto = True
                obstacle_avoid(power)
            elif recv_dict['OF'] == 'off':
                _is_auto = True
                obstacle_follow(power)

            # --- move ---
            if _is_auto and recv_dict['RC'] not in ['rest', 'off', 'stop']:
                remote_control(mycar, recv_dict['RC'], power)
            else:
                remote_control(mycar, recv_dict['RC'], power)

            # ------------------- delay -------------------
            time.sleep(0.01)

    finally:
        print("Finished")
        mycar.stop()


if __name__ == "__main__":
    main()
