import pickle
import datetime
from pykeyboard import PyKeyboard
from keyboard_input import *
import asyncio
import time
import tkinter
from tkinter import ttk


def run_script(keyboard, frame_time, beatmap, delay_time_ms, hwnd):
    w = WindowMgr()
    w.set_handle(hwnd)
    w.set_foreground()
    with open(beatmap, "rb") as f:
        action_list = pickle.load(f)

    with open(frame_time, "rb") as f:
        frame_time_list = pickle.load(f)
    start_time = datetime.datetime.now()

    frame_time = frame_time_list[0]
    print(frame_time)
    action = action_list[0]
    frame_count = 0
    retry_button(keyboard)
    print("start_perform")
    while True:

        current_time = datetime.datetime.now()
        consumed_time = (current_time.timestamp() - start_time.timestamp()) * 1000 - delay_time_ms
        if consumed_time > frame_time:
            if action[0] == 1 and action[1] == 1:
                both_tap(keyboard)
            elif action[0] == 4 and action[1] == 4:
                both_hold(keyboard)
            elif action[0] == 5 and action[1] == 5:
                both_endhold(keyboard)
            else:
                if action[0] == 1:
                    left_tap(keyboard)
                if action[0] == 3:
                    left_slide(keyboard)
                if action[0] == 4:
                    left_hold(keyboard)
                if action[0] == 5:
                    left_endhold(keyboard)
                if action[1] == 1:
                    right_tap(keyboard)
                if action[1] == 3:
                    right_slide(keyboard)
                if action[1] == 4:
                    right_hold(keyboard)
                if action[1] == 5:
                    right_endhold(keyboard)
            frame_count = frame_count + 1
            if frame_count == len(action_list):
                break
            frame_time = frame_time_list[frame_count]
            action = action_list[frame_count]
    print("finish")


def run_vh(keyboard, frametime, beatmap, delay_str, hwnd):
    delay_time_ms=int(delay_str.get())
    print("running veryhard script")
    print(delay_time_ms)
    run_script(keyboard, frametime, beatmap, delay_time_ms, hwnd)


def run_sp(keyboard, frametime, beatmap, delay_str, hwnd):
    delay_time_ms = int(delay_str.get())
    print("running special script")
    print(delay_time_ms)
    run_script(keyboard, frametime, beatmap, delay_time_ms, hwnd)


def choose(event):
    global hwnd
    hwnd_idx = combobox.current()
    hwnd = hwnd_list[hwnd_idx]
    print(hwnd)
    print(title_list[hwnd_idx])


hwnd_title = {}


def get_all_hwnd(hwnd, mouse):
    if (win32gui.IsWindow(hwnd)
            and win32gui.IsWindowEnabled(hwnd)
            and win32gui.IsWindowVisible(hwnd)):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)

hwnd_list = []
title_list = []
for h, t in hwnd_title.items():
    if t:
        # print(h, t)
        hwnd_list.append(h)
        title_list.append(t)

hwnd = hwnd_list[0]

sp_beatmap = "sp_beatmap_fix.pkl"
sp_frametime = "sp_frame_time.pkl"
sp_delay_time_ms = 5475
vh_delay_time_ms = 6100
vh_beatmap = "vh_beatmap.pkl"
vh_frametime = "vh_frame_time.pkl"

keyboard = PyKeyboard()

# w=WindowMgr()
# # w.find_window_wildcard("夜神")
# w.set_handle(463862)
# w.set_foreground()
# print("success")
# print(w._)
#
#
win = tkinter.Tk()
win.title("爱丽丝！我不想打音游辣！！！")
win.geometry("400x300")

btn_sp = tkinter.Button(win, text="special", font=(None, 24),
                        command=lambda: run_sp(keyboard, sp_frametime, sp_beatmap, sp_delay_str, hwnd))
btn_vh = tkinter.Button(win, text="veryhard", font=(None, 24),
                        command=lambda: run_vh(keyboard, vh_frametime, vh_beatmap, vh_delay_str, hwnd))  #

vh_delay_str=tkinter.StringVar()
vh_delay_str.set(str(vh_delay_time_ms))
sp_delay_str=tkinter.StringVar()
sp_delay_str.set(str(sp_delay_time_ms))
vh_delay_entry=tkinter.Entry(win,textvariable=vh_delay_str)
sp_delay_entry=tkinter.Entry(win,textvariable=sp_delay_str)
vh_delay_text = tkinter.StringVar()
vh_delay_text.set("veryhard延迟(ms)")
lab_vh = tkinter.Label(win, textvariable=vh_delay_text, font=(None, 12))
sp_delay_text = tkinter.StringVar()
sp_delay_text.set("special延迟(ms)")
lab_sp = tkinter.Label(win, textvariable=sp_delay_text, font=(None, 12))












description = tkinter.StringVar()
description.set("选择模拟器窗口,然后点击按钮")
lab = tkinter.Label(win, textvariable=description, font=(None, 12))
chosen_window = tkinter.StringVar()
chosen_window.set(title_list[0])
combobox = ttk.Combobox(
    master=win,
    height=10,
    width=20,
    state='readonly',
    cursor='arrow',
    font=("", 16),
    textvariable=chosen_window,
    values=title_list
)
combobox.bind("<<ComboboxSelected>>", choose)
lab.pack()
combobox.pack()
lab_vh.pack()
vh_delay_entry.pack()
btn_vh.pack()
lab_sp.pack()
sp_delay_entry.pack()
btn_sp.pack()

win.mainloop()
