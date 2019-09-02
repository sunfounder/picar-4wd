import fwd_car as fc

speed = 30

def main():
    while True:
        scan_list = fc.scan_step(23)
        # print(scan_list)
        if not scan_list:
            continue

        scan_list = [str(i) for i in scan_list]
        scan_list = "".join(scan_list)
        paths = scan_list.split("2")
        length_list = []
        for path in paths:
            length_list.append(len(path))
        # print(length_list)
        if max(length_list) == 0:
            fc.stop() 
        else:
            i = length_list.index(max(length_list))
            pos = scan_list.index(paths[i])
            pos += (len(paths[i]) - 1) / 2
            # pos = int(pos)
            delta = len(scan_list) / 3
            # delta *= us_step/abs(us_step)
            if pos < delta:
                fc.turn_left(speed)
            elif pos > 2 * delta:
                fc.turn_right(speed)
            else:
                if scan_list[int(len(scan_list)/2-1)] == "0":
                    fc.backward(speed)
                else:
                    fc.forward(speed)

if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()
