# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import glob
import platform
import re
import random
import string

print('''
--------------------------------
修改Teamviewer for Mac的ID
--------------------------------
''')
#  必须是Mac系统，否则本脚本无效
if platform.system() != 'Darwin':
    print('必须是MAC OS X系统.')
    sys.exit();

if os.geteuid() != 0:
    print('必须用root权限执行脚本.')
    sys.exit();
#  如果在root权限，os.environ['SUDO_USER']返回用户名，如lining
if os.environ.has_key('SUDO_USER'):
    USERNAME = os.environ['SUDO_USER']
    if USERNAME == 'root':
       print('请通过sudo命令切换到root权限')
       sys.exit();
else:
    print('请通过sudo命令切换到root权限')
    sys.exit();
#  下面两个目录是要搜索包含teamviewer字样的文件
HOMEDIRLIB = '/Users/' + USERNAME  + '/library/preferences/'
GLOBALLIB  =  '/library/preferences/'

CONFIGS = []

#  获取配置文件的完全路径
def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

for file in listdir_fullpath(HOMEDIRLIB):
    if 'teamviewer'.lower() in file.lower():
        CONFIGS.append(file)

if not CONFIGS:
    print ('''
为发现配置文件，没什么可以删除的
''')
# 删除配置文件
else:
    print("发现配置文件:\n")
    for file in CONFIGS:
        print file

    print('''
这些配置文件将被永久删除
''')
    raw_input("请按<Enter>键盘删除文件或按<CTR+C>组合键退出程序")

    for file in CONFIGS:
        try:
            os.remove(file)    # 删除文件
        except:
            print("不能删除文件，是否权限不够?")
            sys.exit();
    print("搞定!")

# 下面的文件会替换里面的值
TMBINARYES = [
'/Applications/TeamViewer.app/Contents/MacOS/TeamViewer',
'/Applications/TeamViewer.app/Contents/MacOS/TeamViewer_Service',
'/Applications/TeamViewer.app/Contents/Helpers/TeamViewer_Desktop',
]
#  这些文件必须存在，否则退出程序
for file in TMBINARYES:
    if os.path.exists(file):
        pass
    else:
        print("File not found: " + file)
        print ("Install TeamViewer correctly")
        sys.exit();

#  开始替换上述文件中的值
def idpatch(fpath,platf,serial):
    file = open(fpath, 'r+b')
    binary = file.read()
    # 定义模板
    PlatformPattern = "IOPlatformExpert.{6}"
    SerialPattern =  "IOPlatformSerialNumber%s%s%sUUID"
    # 开始替换
    binary = re.sub(PlatformPattern, platf, binary)
    binary = re.sub(SerialPattern % (chr(0), "[0-9a-zA-Z]{8,8}", chr(0)), SerialPattern%(chr(0), serial, chr(0)), binary)
    # 更新待修改的文件
    file = open(fpath,'wb').write(binary)
    return True
#  产生随机数，用于生成随机的ID
def random_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

RANDOMSERIAL = random_generator()
RANDOMPLATFORM = "IOPlatformExpert" + random_generator(6)

#  开始依次替换前面文件中的内容
for file in TMBINARYES:
        try:
            idpatch(file,RANDOMPLATFORM,RANDOMSERIAL)
        except:
            print "错误：不能修改： " + file
            sys.exit();

print "PlatformDevice: " + RANDOMPLATFORM
print "PlatformSerial: " + RANDOMSERIAL

print('''
ID需要成功
!!! 必须重启计算机才能生效，good luck !!!!
''')