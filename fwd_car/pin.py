import RPi.GPIO as GPIO

class Pin(object):
    OUT = GPIO.OUT                  # 将I/O口定义为输出模式
    IN = GPIO.IN                    # 将I/O口定义为输入模式
    IRQ_FALLING = GPIO.FALLING      # 设置为低电平触发
    IRQ_RISING = GPIO.RISING        # 设置为高电平触发
    IRQ_RISING_FALLING = GPIO.BOTH  # 设置为边缘模式
    PULL_UP = GPIO.PUD_UP           # 设置为上拉模式
    PULL_DOWN = GPIO.PUD_DOWN       # 设置为下拉模式
    PULL_NONE = None                # 设置为非上拉下拉模式
    _dict = {                       # 树莓派pin引脚列表
        "D0":  17,
        "D1":  18,
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25,
        "D7":  4,
        "D8":  5,
        "D9":  6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  19,
        "LED": 26,
    }

    def __init__(self, *value):
        super().__init__()          # 解决多继承问题，继承父类属性，可重定向父类属性
        GPIO.setmode(GPIO.BCM)      # 树莓派GPIO引脚编号的模式
        GPIO.setwarnings(False)     # 禁用警告
        if len(value) > 0:          # 当有值时，取第一个值当作引脚值
            pin = value[0]
        if len(value) > 1:          # 当有多个值时， 取第二个值为输入或输出模式
            mode = value[1]
        else:
            mode = None
        if len(value) > 2:          # 当有3个或以上的值，去第三个为上拉或者下拉模式
            setup = value[2]
        else:
            setup = None
        if isinstance(pin, str):    # 当value第一个值为字符串时，通过_dict字典找到对应的引脚
            try:
                self._bname = pin
                self._pin = self.dict()[pin]
            except Exception as e:
                print(e)
                self._error('Pin should be in %s, not %s' % (self._dict, pin))
        elif isinstance(pin, int):  # 当pin为整数型时，直接取值
            self._pin = pin
        else:
            self._error('Pin should be in %s, not %s' % (self._dict, pin))
        self._value = 0
        self.init(mode, pull=setup)
    #    self._info("Pin init finished.")
        
    def init(self, mode, pull=PULL_NONE):   # 设置模式
        self._pull = pull
        self._mode = mode
        if mode != None:
            if pull != None:
                GPIO.setup(self._pin, mode, pull_up_down=pull)
            else:
                GPIO.setup(self._pin, mode)

    def dict(self, *_dict):                 # 判断给定的字符是否在_dict中
        if len(_dict) == 0:                 # 没有给值直接返回字典中所有元素
            return self._dict
        else:
            if isinstance(_dict, dict):
                self._dict = _dict
            else:
                self._error(
                    'argument should be a pin dictionary like {"my pin": ezblock.Pin.cpu.GPIO17}, not %s' % _dict)

    def __call__(self, value):
        return self.value(value)

    def value(self, *value):                 # 如果value为空，设置引脚为输入模式， 返回引脚的值
        if len(value) == 0:
            self.mode(self.IN)
            result = GPIO.input(self._pin)
        #    self._debug("read pin %s: %s" % (self._pin, result))
            return result
        else:                               # 如果value不为空， 取出第一个值，设置为输出模式，将值传给引脚
            value = value[0]
            self.mode(self.OUT)
            GPIO.output(self._pin, value)
            return value

    def on(self):                           # 将引脚设置为高电平
        return self.value(1)

    def off(self):                          # 将引脚设置为低电平
        return self.value(0)

    def high(self):                         # 调用on函数，将引脚设置为高电平
        return self.on()

    def low(self):                          # 调用off函数，将引脚设置为低电平
        return self.off()

    def mode(self, *value):                 #  当参数value没有值传入进来，返回所有模式列表，当参数value有值传入进来，设置引脚的输入输出模式
        if len(value) == 0:
            return self._mode
        else:
            mode = value[0]
            self._mode = mode
            GPIO.setup(self._pin, mode)

    def pull(self, *value):     # 返回上拉下拉列表
        return self._pull

    def irq(self, handler=None, trigger=None):      # 中断函数
        self.mode(self.IN)
        GPIO.add_event_detect(self._pin, trigger, callback=handler)

    def name(self):                                 # 打印树莓派引脚的名字 如：GPIO23
        return "GPIO%s"%self._pin

    def names(self):
        return [self.name, self._bname]

    class cpu(object):
        GPIO17 = 17
        GPIO18 = 18
        GPIO27 = 27
        GPIO22 = 22
        GPIO23 = 23
        GPIO24 = 24
        GPIO25 = 25
        GPIO26 = 26
        GPIO4  = 4
        GPIO5  = 5
        GPIO6  = 6
        GPIO12 = 12
        GPIO13 = 13
        GPIO19 = 19
        GPIO16 = 16
        GPIO26 = 26
        GPIO20 = 20
        GPIO21 = 21

        def __init__(self):
            pass
