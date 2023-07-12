# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from os import system, geteuid, getlogin
from os import listdir
import sys
import time
import threading

if geteuid() != 0:
    print("Script must be run as root. Try 'sudo python3 setup.y install'")
    sys.exit(1)

sys.path.append("./picar_4wd")
from version import __version__

# Get the long description from the relevant file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

errors = []

avaiable_options = ["--no-dep",]
options = []
if len(sys.argv) > 1:
    options = list.copy(sys.argv[1:])

for option in sys.argv:
    if option in avaiable_options:
        sys.argv.remove(option)
 
# utils
# =================================================================
def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    # print(result)
    # print(status)
    return status, result

at_work_tip_sw = False
def working_tip():
    char = ['/', '-', '\\', '|']
    i = 0
    global at_work_tip_sw
    while at_work_tip_sw:  
            i = (i+1)%4 
            sys.stdout.write('\033[?25l') # cursor invisible 
            # cursor visible # \033[?25h
            sys.stdout.write('%s\033[1D'%char[i])
            sys.stdout.flush()
            time.sleep(0.5)

    sys.stdout.write(' \033[1D')
    sys.stdout.write('\033[?25h') # cursor visible 
    sys.stdout.flush()

def do(msg="", cmd=""):
    print(" - %s... " % (msg), end='', flush=True)
    # at_work_tip start 
    global at_work_tip_sw
    at_work_tip_sw = True
    _thread = threading.Thread(target=working_tip)
    _thread.daemon = True
    _thread.start()
    # process run
    # status, result = run_command(cmd)
    status, result = eval(cmd)
    # print(status, result)
    # at_work_tip stop
    at_work_tip_sw = False
    _thread.join()
    # status
    if status == 0 or status == None or result == "":
        print('Done')
    else:
        print('\033[1;35mError\033[0m')
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

# install
# =================================================================
APT_INSTALL_LIST = [ 
    "python3-pip",
    "sysstat",
    "i2c-tools",
]

PIP_INSTALL_LIST = [
    "RPi.GPIO",
    "smbus",
    "websockets",
]

def install():
    user_name = getlogin()

    if "--no-dep" not in options:
        print("Install dependencies with apt-get")
        do(msg="update apt-get",
            cmd='run_command("apt-get update")')
        for dep in APT_INSTALL_LIST:
            do(msg=f"install {dep}",
                cmd=f'run_command("apt-get install {dep} -y")')

        print("Install dependencies with pip3")
        for dep in PIP_INSTALL_LIST:
            do(msg=f"install {dep}",
                cmd=f'run_command("pip3 install {dep}")')

    print("Setup interfaces")
    do(msg="turn on I2C",
        cmd='Config().set("dtparam=i2c_arm", "on")') 
    do(msg="Add I2C module",
        cmd='Modules().set("i2c-dev")') 

    if ".picar-4wd" not in listdir(f"/home/{user_name}"):
        do(msg="create .picar-4wd directory",
            cmd=f'run_command("sudo mkdir /home/{user_name}/.picar-4wd/")') 
    do(msg="copy picar-4wd-config",
        cmd=f'run_command("sudo cp ./data/config /home/{user_name}/.picar-4wd/config")')
    do(msg="change directory owner",
        cmd=f'run_command("sudo chown -R {user_name}:{user_name} /home/{user_name}/.picar-4wd/")')

    print("Setup picar-4wd web-example service")
    do(msg="copy picar-4wd web-example file",
        cmd='run_command("sudo cp ./bin/picar-4wd-web-example /etc/init.d/picar-4wd-web-example")')
    do(msg="add excutable mode for picar-4wd-web-example",
        cmd='run_command("sudo chmod +x /etc/init.d/picar-4wd-web-example")')

setup(
    name='picar-4wd',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,

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
    install_requires=[],
 
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'picar-4wd=picar_4wd.utils:main', 
        ],
    },
)

print("")
try:
    install()
finally:
    sys.stdout.write(' \033[1D')
    sys.stdout.write('\033[?25h') # cursor visible 
    sys.stdout.flush()

if len(errors) == 0:
    print("Setup Finished")
    print("\033[1;32mWhether to restart for the changes to take effect(Y/N):\033[0m")
    while True:
        key = input().lower()
        if key == 'y':
            print("System reboot now")
            run_command("sudo reboot")
        elif key == 'N' or key == 'n':
            print("reboot cancel")
            sys.exit(0)
        else:
            continue
else:
    print("\n\nError happened in install process:")
    for error in errors:
        print(error)
    print("Try to fix it yourself, or contact service@sunfounder.com with this message")
