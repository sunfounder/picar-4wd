from picar_4wd import Picar4WD

mycar = Picar4WD()
speed = 30


def main():
    while True:
        scan_list = mycar.scan_step(35)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)
        if tmp != [2, 2, 2, 2]:
            mycar.turn_right(speed)
        else:
            mycar.forward(speed)


if __name__ == "__main__":
    try:
        main()
    finally:
        mycar.stop()
