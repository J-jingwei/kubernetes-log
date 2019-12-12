#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' kubernetes api log GUI '''
__author__ = 'jiangjw'

'''
1、这个程序实现文本框输入。
2、使用grid方法按照Excel表格方式对组件位置进行安排
3、通过Button提交按钮实现获取服务的日志信息。

使用方法:根据kubernetes命名空间，以及获取一个token填入指定位置，即可打包使用！
查看命名空间: kubectl get namespaces
获取token:    kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')
打包命令:   pyinstaller -F search_log.py
'''

'''
更新信息：
3.0 更新为token方式√;
    更新滚动条√;
    满足日志过滤条件上下文查找√;
    加入日志显示正序倒序选项√;
    页面轻微调整√。
3.1 更新字体;
3.2 更新pod启动时间;
    增加pod状态区锁定;
    更新关键字该行红色;
open 脱敏处理;
'''

from tkinter import *
import tkinter.font as tkFont
import list_pod_log
import list_pod_status

# 需修改部分
Token = '请输入获取到的token'
APISERVER = 'https://192.168.1.92:6443'  # 修改kubernetes-master的位置
namespace = str('请输入对应的命名空间')  # 修改这变更查询的命名空间

root = Tk()
# icoPath = os.path.join('C:\\', 'Users', 'Administrator', 'Downloads', 'xxx.ico')
# root.iconbitmap(icoPath)
root.title("kubernetes简易日志查询工具")
# 定义一个字体
ft = tkFont.Font(family='Fixdsys', size=10, weight=tkFont.BOLD)
# 设置label，提示
label1 = Label(root, text='服务关键字（1）必填：').grid(row=0, column=0)
label2 = Label(root, text='服务关键字（2）：').grid(row=1, column=0)
label3 = Label(root, text='日志关键字（1）：').grid(row=2, column=0)
label4 = Label(root, text='日志关键字（2）：\n（1，2过滤关系为与）').grid(row=3, column=0)
label5 = Label(root, text='pod状态（无需输入）格式：状态=>启动时间：').grid(row=0, column=2)
label6 = Label(root, text='日志显示默认为正序，\n倒序请选中倒序后查询：').grid(row=2, column=2)
label7 = Label(root, text='是否启动查看关键字\n上下文多少行\n（未选择日志关键字请勿点选其他）：').grid(row=0, column=3)

v1 = StringVar()
v2 = StringVar()
v3 = StringVar()
v4 = StringVar()
t1 = StringVar()
e1 = Entry(root, textvariable=v1)  # Entry 是 Tkinter 用来接收字符串等输入的控件.
e2 = Entry(root, textvariable=v2)
e3 = Entry(root, textvariable=v3)
e4 = Entry(root, textvariable=v4)

scroll = Scrollbar()  # 加入滚动条
te0 = Text(root, width=29, height=2, font=ft)  # 加入两个文本框
te1 = Text(root, width=140, height=50, font=ft)
te0.config(state=DISABLED)  # 锁te0区域，不让输入

scroll['command'] = te1.yview  # 将滚动条与e1文本框绑定
scroll.grid(row=5, rowspan=4, columnspan=4, sticky=S + W + E + N)

e1.grid(row=0, column=1, padx=15, pady=5)  # 设置输入框显示的位置，以及长和宽属性
e2.grid(row=1, column=1, padx=15, pady=5)
e3.grid(row=2, column=1, padx=15, pady=5)
e4.grid(row=3, column=1, padx=15, pady=5)
te0.grid(row=1, column=2, padx=15, pady=5, sticky=E)
te1.grid(row=5, rowspan=3, columnspan=4, padx=15, pady=5, sticky=S + W + E + N)


# 获取过滤后pod的状态
def podStasus():
    input1 = str(e1.get())
    input2 = str(e2.get())

    # 如果间隔符为下划线则替换为'-'
    if '_' in input1:
        input1 = input1.replace('_', '-')
    if '_' in input2:
        input2 = input2.replace('_', '-')

    # pod 过滤条件
    LABEL = input1  # 每次更新这个取出对应的pod
    LABEL2 = input2
    status = list_pod_status.podStatus(Token, APISERVER, namespace, LABEL, LABEL2)
    return status


# 获取已过滤后的日志
def logStr():
    input1 = str(e1.get())
    input2 = str(e2.get())
    key1 = str(e3.get())
    key2 = str(e4.get())

    # 如果间隔符为下划线则替换为'-'
    if '_' in input1:
        input1 = input1.replace('_', '-')
    if '_' in input2:
        input2 = input2.replace('_', '-')

    # pod 过滤条件
    LABEL = input1  # 每次更新这个取出对应的pod
    LABEL2 = input2
    # 日志过滤条件
    keyword = key1  # 一级筛选，日志中需过滤的关键字1
    keyword2 = key2  # 二级筛选过滤
    # 上下文行数
    scope = s.get()
    log = list_pod_log.main(Token, APISERVER, namespace, LABEL, LABEL2, keyword, keyword2, scope)
    return log


# 根据单选确定日志输出顺序
def orderClick():
    # 判断值为1或2，1正，2倒
    if v.get() == 1:
        method = 'insert'
    if v.get() == 2:
        method = '1.0'
    return method


# 点击按钮执行操作
def logClick():
    if e3.get():
        key = str(e3.get())
    if str(e1.get()):
        # 显示pod状态
        te0.tag_config('a', foreground='blue')
        te0.config(state=NORMAL)
        for p in podStasus():
            te0.insert(INSERT, p + ',', 'a')
        te0.config(state=DISABLED)
        # 显示日志内容
        methods = orderClick()
        for i in logStr():
            # print(i)
            if e3.get():
                key = str(e3.get())
                if key in i:
                    te1.tag_config('a', foreground='red')
                    te1.insert(methods, i + '\n', 'a')
                else:
                    te1.insert(methods, i + '\n')
            else:
                te1.insert(methods, i + '\n')
        logsAll = "过滤出日志共{}行 ！！！\n".format(len(logStr()))
        te1.insert(1.0, logsAll)
    else:
        te1.insert(1.0, '请输入服务过滤条件！！！')


# 清除文本框输出
def clean():
    te0.config(state=NORMAL)
    te1.delete(1.0, END)
    te0.delete(1.0, END)
    te0.config(state=DISABLED)


# 设置单选序列，，默认
v = IntVar()
v.set(1)
Radiobutton(root, text='正序', command=orderClick, variable=v, value=1).grid(row=3, column=2)
Radiobutton(root, text='倒序', command=orderClick, variable=v, value=2).grid(row=4, column=2)

# 设置单选项，默认不启用上下文
s = IntVar()
s.set(0)
Radiobutton(root, text='0行', variable=s, value=0).grid(row=1, column=3)
Radiobutton(root, text='5行', variable=s, value=5).grid(row=2, column=3)
Radiobutton(root, text='10行', variable=s, value=10).grid(row=3, column=3)

# 按钮装置
Button(root, text='查询日志（请条件确认后点击）', width=30, command=logClick, bg='CornflowerBlue').grid(row=4, column=3, sticky=W,
                                                                                          padx=10, pady=5)

Button(root, text='清空日志', width=10, command=clean).grid(row=4, column=1, sticky=W, padx=10, pady=5)

Button(root, text='退出', width=10, command=root.quit).grid(row=4, column=0, sticky=E, padx=10, pady=5)

mainloop()
