#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
import psutil
import signal
import ctypes,sys
import win32api
import win32con
import sys
import random

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def autostartup():
    name = "BanProcess"
    path = sys.argv[0]
    print(path)
    KeyName = 'Software\Microsoft\Windows\CurrentVersion\Run'
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
    win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
    win32api.RegCloseKey(key)    
    
    


'''
用于屏蔽不需要的进程
将需要屏蔽的程序名字填入banlist.txt中
'''


if __name__ == '__main__': 
    if is_admin():        
        autostartup()
        if not os.path.exists("banlist.txt"):
            f = open("banlist.txt", mode="w", encoding="utf-8")
            f.close()        
        f = open("banlist.txt")
        banlist = []
        line = f.readline()
        while line:
            banlist.append(line.strip())
            line = f.readline()
        f.close()
        
        #避免同一个程序的多个副本运行
        selfproc = []
        for i in psutil.process_iter():
            if str(sys.argv[0].split("\\")[-1]) in str(i):
                selfproc.append(i.pid)
        if len(selfproc) > 2:
            for i in selfproc[2:]:
                os.kill(i,signal.SIGILL)  
                
        while True:
            '''
            获取进程列表
            '''
            for i in psutil.process_iter():
                for j in banlist:
                    if j in str(i):
                        os.kill(i.pid,signal.SIGILL)
            t = random.randrange(3,10)
            time.sleep(t)
            continue
        
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                
