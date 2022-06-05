# -*- coding: utf-8 -*-
from socket import timeout
import win32con
import win32gui
import time

#窗口句柄
windowClass=""
windowName=""
#定时事件时间
eventTime=10
#窗口最大化时间 不高于总时间
winMaxTime=5
#停止事件
stoped=1
#设置窗口句柄方法
def setWindowName(_className,_windowName):
    global windowClass
    global windowName
    windowClass=_className
    windowName=_windowName

#设置定时时间
def setEventTime(time):
    global eventTime
    eventTime=int(time)

#设置窗口最大化时间
def setMaxTime(time):
    global winMaxTime
    winMaxTime=int(time)

#停止事件
def stopEvent():
    return 0

#重置
def reset(_className,_windowName,_eventTime,_maxTime):
    stopEvent()
    setWindowName(_className,_windowName)
    setEventTime(_eventTime)
    setMaxTime(_maxTime)

#初始化
def init():
    _className=input('请输入窗口句柄名称\n')
    _windowName=input('请输入窗口名字\n')
    _eventTime=input('请输入事件循环时长\n')
    _maxTime=input('请输入窗口最大化时间\n')
    reset(_className,_windowName,_eventTime,_maxTime)
    doLoop()


#执行事件
def doEvent():
    resultWin=win32gui.FindWindow(windowClass,windowName)
    if resultWin==0:
        print('没有找到该窗口，请重新输入')
        init()
    else:
        #是否最小化
        isMin=win32gui.IsIconic(resultWin)
        if not isMin:
            print('该窗口此刻不是预期的状态(最小化),脚本可能不会按预期效果执行')
        #最大化一段时间
        win32gui.ShowWindow(resultWin,win32con.SW_SHOWMAXIMIZED)
        #TODO
        time.sleep(winMaxTime)
        isMin=win32gui.IsIconic(resultWin)
        if isMin:
            print('该窗口此刻不是预期的状态(最大化),脚本可能不会按预期效果执行')
        #最小化一段时间
        win32gui.ShowWindow(resultWin,win32con.SW_SHOWMINIMIZED)
        win32gui.SetForegroundWindow(resultWin)

#事件循环 TODO
def doLoop():
    doEvent()
    time.sleep(eventTime)
    doLoop()

if __name__=="__main__":
    #等待3秒
    time.sleep(3)
    init()
