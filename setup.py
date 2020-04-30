# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from os import system
from os import listdir
import sys
import tty
import termios
import asyncio

errors = []

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()


def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    # print(result)
    # print(status)
    return status, result


def do(msg="", cmd=""):
    print(" - %s..." % (msg), end='\r')
    print(" - %s... " % (msg), end='')
    status, result = eval(cmd)
    # print(status, result)
    if status == 0 or status == None or result == "":
        print('Done')
    else:
        print('Error')
        errors.append("%s error:\n  Status:%s\n  Error:%s" %
                      (msg, status, result))

class Modules(object):
    ''' 
        To setup /etc/modules
    '''

    def __init__(self, file="/etc/modules"):
        self.file = file
        with open(self.file, 'r') as f:
            self.configs = f.read()
        self.configs = self.configs.split('\n')

    def remove(self, expected):
        for config in self.configs:
            if expected in config:
                self.configs.remove(config)
        return self.write_file()

    def set(self, name):
        have_excepted = False
        for i in range(len(self.configs)):
            config = self.configs[i]
            if name in config:
                have_excepted = True
                tmp = name
                self.configs[i] = tmp
                break

        if not have_excepted:
            tmp = name
            self.configs.append(tmp)
        return self.write_file()

    def write_file(self):
        try:
            config = '\n'.join(self.configs)
            # print(config)
            with open(self.file, 'w') as f:
                f.write(config)
            return 0, config
        except Exception as e:
            return -1, e

class Config(object):
    ''' 
        To setup /boot/config.txt
    '''

    def __init__(self, file="/boot/config.txt"):
        self.file = file
        with open(self.file, 'r') as f:
            self.configs = f.read()
        self.configs = self.configs.split('\n')

    def remove(self, expected):
        for config in self.configs:
            if expected in config:
                self.configs.remove(config)
        return self.write_file()

    def set(self, name, value=None):
        have_excepted = False
        for i in range(len(self.configs)):
            config = self.configs[i]
            if name in config:
                have_excepted = True
                tmp = name
                if value != None:
                    tmp += '=' + value
                self.configs[i] = tmp
                break

        if not have_excepted:
            tmp = name
            if value != None:
                tmp += '=' + value
            self.configs.append(tmp)
        return self.write_file()

    def write_file(self):
        try:
            config = '\n'.join(self.configs)
            # print(config)
            with open(self.file, 'w') as f:
                f.write(config)
            return 0, config
        except Exception as e:
            return -1, e

def install():
    print("Install dependency")
    do(msg="update apt-get",
        cmd='run_command("sudo apt-get update")')
    do(msg="install pip",
        cmd='run_command("sudo apt-get install python3-pip -y")')
    # do(msg="install git",
    #     cmd='run_command("sudo apt-get install git-core -y")')
    do(msg="install sysstat",
        cmd='run_command("sudo apt-get install sysstat -y")')
    do(msg="install i2c-tools",
        cmd='run_command("sudo apt-get install i2c-tools -y")')


    print("Setup interfaces")
    do(msg="turn on I2C",
        cmd='Config().set("dtparam=i2c_arm", "on")') 
    do(msg="Add I2C module",
        cmd='Modules().set("i2c-dev")') 

    if ".picar-4wd" not in listdir("/home/pi"):
        do(msg="create .picar-4wd directory",
            cmd='run_command("sudo mkdir /home/pi/.picar-4wd/")') 
    do(msg="copy picar-4wd-config",
        cmd='run_command("sudo cp ./data/config /home/pi/.picar-4wd/")')
    do(msg="change directory owner",
        cmd='run_command("sudo chown -R pi:pi /home/pi/.picar-4wd/")')

    print("Setup picar-4wd web-example service") 
    do(msg="copy picar-4wd web-example file",
        cmd='run_command("sudo cp ./bin/picar-4wd-web-example /etc/init.d/picar-4wd-web-example")')
    do(msg="add excutable mode for picar-4wd-web-example",
        cmd='run_command("sudo chmod +x /etc/init.d/picar-4wd-web-example")')

install()

setup(
    name='picar-4wd',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version="0.0.1",

    description='PiCar-4WD for Raspberry Pi',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/sunfounder/picar-4wd',

    # Author details
    author='SunFounder',
    author_email='service@sunfounder.com',

    # Choose your license
    license='GNU',
    zip_safe=False,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    # What does your project relate to?
    keywords='4wd raspberry pi car sunfounder',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['examples', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['RPi.GPIO', 'smbus', 'websockets'],
 
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'picar-4wd=picar_4wd.utils:main', 
        ],
    },
)

if len(errors) == 0:
    print("Setup Finished")
    print('If you want to reboot please press y, if not press n')
    input_val = readkey()
    print(input_val)
    if input_val == 'y':
        do(msg="System reboot now",
        cmd='run_command("sudo reboot")')
    elif input_val == 'n':
        print("reboot cancel")
else:
    print("\n\nError happened in install process:")
    for error in errors:
        print(error)
    print("Try to fix it yourself, or contact service@sunfounder.com with this message")
