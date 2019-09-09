#fwd-car文档
##此文档用于介绍以及说明fwd-car项目的结构，功能，及代码组成，以及简单的功能是如何实现

##概述：fwd-car基于ezblock的树莓派扩展板制作（少了蓝牙，不是用ezblock进行互动，而是新的web应用），都是基于Pin，ADC，PWM等基类进行了上层开发，功能有巡线，跟随，避障，测速，遥控，开发完后整理成一个python的包的形式

###包文件主要结构：打开fwd-car文件夹后，代码分为4个文件夹，分别是bin,data,exmaple,fwd_car，作用如下：

####fwd-car: fwd_car中的adc，pin，i2c，pwm文件为最底层驱动库，fwd-car.__init__.py为由底层驱动库组成的基本功能函数集，fwd-car.utils文件为关于树莓派的一些系统查看函数

####example: 可以直接运行的功能例子函数（如巡线）

####data: 初始化小车的轮子正反反向和舵机校准

####bin: 编写了通过命令行去开始服务的语句

##主要功能实现使用fwd_car文件夹里的文件，详情查看相关的md文件

##fwd-car小车支持命令行指令，如下所示：
###指令格式为：fwd-car + 指令 + 控制位（这一项有些有，有些没有）
####指令一：web-example
```python
pi@raspberrypi:fwd-car web-example  ##开启web-example服务（前提没有设置开机自启动此项服务）
pi@raspberrypi:fwd-car web-example enable  ##开启web-example开机自启动
pi@raspberrypi:fwd-car web-example disable  ##取消web-example开机自启动
```
####指令二：soft-reset
```python
pi@raspberrypi:fwd-car soft-reset  ##复位Mcu
```
####指令三：power-read
```python
pi@raspberrypi:fwd-car power-read  ##查看小车电压
```
####指令四：test
```python
pi@raspberrypi:fwd-car test motor  ##测试小车电机
pi@raspberrypi:fwd-car test servo  ##测试小车舵机
pi@raspberrypi:fwd-car test grayscale  ##测试小车灰度传感器
```

##玩法：产品刚拿到手：
1. 树莓派开机
2. 通过命令下载fwd-car
```python
pi@raspberrypi:git clone https://github.com/sunfounder/fwd-car  ##下载项目
```
3. 下载完成后，你会看到fwd-car这个目录，然后进入这个目录
4. 通过命令"sudo python3 setup.py install"下载相关库和配置树莓派,如果下载配置正常，最后一行为一个finish
5. 下载和配置完成后，执行命令"fwd-car web-example"打开服务（如需其它指令如开机自启动或测试电机舵机，请看上方命令行指令）
6. 最后在客户端输入命令行出现的IP号即可进入网站
7. 如果树莓派已经执行过前4步，则之后都只需要执行第5和第6步即可玩小车，如果开启了自启动，则只需要等树莓派正常开启即可
