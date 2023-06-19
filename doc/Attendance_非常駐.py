#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from plyer import notification
import datetime, binascii, nfc, csv, time,sys,os
import pandas as pd
import threading
from tkinter import *
import tkinter as tk
from nfc.clf import rcs380
from pystray import Icon, Menu, MenuItem
from PIL import Image
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass

entry_list=[]
INPUT=False

# def resource_path(filename):
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, filename)
#     return os.path.join(os.path.abspath("."), filename)

def label1_comment(comment):
    label1.config(text=comment)
    label1.update()

def ENTRY(event):
    global INPUT
    INPUT=True

def DELETE():
    global INPUT
    textbox.delete(0, tk.END)
    INPUT=False

def quit_me(root_window):   #https://qiita.com/mmura001/items/ca1906bc579f336fbc1c
    #thread1.join()
    root_window.quit()
    root_window.destroy()
    sys.exit()

root = tk.Tk()
root.geometry('350x160')
root.title('Attendance')
label = tk.Label(text='State').grid(row= 0, column=1)
label1 = tk.Label(root,text='hold your card')
label1.grid(row= 0, column=2)
textbox=tk.Entry(width=20)
textbox.grid(row= 1, column=2)
button_execute = tk.Button(root, text="...")
button_execute.bind("<Key-Return>", ENTRY)
button_execute.bind("<Button>", ENTRY)
button_execute.grid(row= 1, column=3)

label2 = tk.Label(text='Command').grid(row= 2, column=1)
buttonA = tk.Button(root, text = 'Registration').grid(row= 3, column=1)
labelA1 = tk.Label(text='*Unimplemented').grid(row= 3, column=2)
buttonB = tk.Button(root, text = 'Viewer').grid(row= 4, column=1)
labelB1 = tk.Label(text='*Unimplemented').grid(row= 4, column=2)

root.protocol("WM_DELETE_WINDOW", lambda :quit_me(root))

def format_timedelta(timedelta):            #https://www.memory-lovers.blog/entry/2019/12/12/103000
    total_sec = timedelta.total_seconds()
    hours = total_sec // 3600               # hours
    remain = total_sec - (hours * 3600)     # remaining seconds
    minutes = remain // 60                  # minutes
    seconds = remain - (minutes * 60)       # remaining seconds
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))      # total time

def log(user_name,time,flag):
    time_str=time.strftime('%Y-%m-%d %H:%M:%S')
    with open('.\\CSV\\log.csv', 'a', encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        if flag:
            writer.writerow([time,user_name,'Entry'])
        else:
            writer.writerow([time,user_name,'Exit'])

def Noti(user_name,time,flag):
    time_str=time.strftime('%Y-%m-%d %H:%M:%S')
    if flag:
        title_str=user_name+', Hello'
        message_str='Entry: '+time_str
    else:
        delta=format_timedelta(time-temp)
        title_str=user_name+', See you next time.'
        message_str='Exit: '+time_str+'\n'+'Staying Time:'+str(delta)

    notification.notify(
        title=title_str,
        message=message_str,
        app_name='Attendance'
    )

def on_connect(tag):
    idm = binascii.hexlify(tag.idm)
    idm_str=idm.decode()
    entry_list.append(idm_str)
    certification(idm_str, tag)
    label1_comment('on-connect')
    #print('on-connect')
    return True

def on_release(tag):
    idm = binascii.hexlify(tag.idm)
    idm_str=idm.decode()
    entry_list.remove(idm_str)
    certification(idm_str, tag)
    label1_comment('on-release')
    #print('on-release')
    time.sleep(3)
    label1_comment('Hold your card')
    return True

def registration(idm_str, tag):
    label1_comment('Please enter your username')
    #print('Please enter your username')
    while True:
        if INPUT==True:
            break
    new_name=textbox.get()
    DELETE()
    with open('.\\CSV\\userlist.csv', 'a', encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow([idm_str,new_name])
    regi_comment='Registered '+new_name
    label1_comment(regi_comment)
    #print(regi_comment)
    time.sleep(3)

def certification(idm_str, tag):
    global flag
    global temp
    df = pd.read_csv('.\\CSV\\userlist.csv', encoding="UTF-8",header=0)
    uer_list=dict(zip(df['IDm'],df['name']))
    if idm_str in entry_list:
        flag=True
        if idm_str in uer_list:
            user_name=uer_list[idm_str]
            time_1=datetime.datetime.now()
            temp=time_1
            Noti(user_name,time_1,flag)
            log(user_name,time_1,flag)
        else:
            label1_comment('New user detected')
            time.sleep(2)
            #print('New user detected')
            registration(idm_str, tag)
            certification(idm_str,tag)
    else:
        flag=False
        user_name=uer_list[idm_str]
        time_2=datetime.datetime.now()
        Noti(user_name,time_2,flag)
        log(user_name,time_2,flag)

def NFC():
    while True:
        with nfc.ContactlessFrontend('usb') as clf:
            rdwr_options = {'on-connect': on_connect,'on-release': on_release}
            clf.connect(rdwr=rdwr_options)

thread1 = threading.Thread(target=NFC)
thread1.setDaemon(True)
thread1.start()      
root.mainloop()