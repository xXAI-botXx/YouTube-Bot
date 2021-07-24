# Source:
# - http://makble.com/how-to-find-window-with-wildcard-in-python-and-win32gui

import sys
import unittest

import numpy as np
 
from ctypes import *
import win32service
import win32serviceutil
import win32api
import win32event
import win32evtlogutil
import os
import win32con
 
from win32con import SWP_FRAMECHANGED 
from win32con import SWP_NOMOVE 
from win32con import SWP_NOSIZE 
from win32con import SWP_NOZORDER
from win32con import SW_HIDE
from win32con import SW_FORCEMINIMIZE
from win32con import SW_SHOWNORMAL
 
from win32con import GW_OWNER 
from win32con import GWL_STYLE 
from win32con import GWL_EXSTYLE 
 
from win32con import WM_CLOSE 
 
from win32con import WS_CAPTION 
from win32con import WS_EX_APPWINDOW 
from win32con import WS_EX_CONTROLPARENT
from win32con import WS_EX_TOOLWINDOW
from win32con import WS_EX_WINDOWEDGE
from win32con import WS_EX_LAYERED 
from win32con import LWA_ALPHA
 
import win32gui
import win32ui
import winxpgui
 
class Window_Finder():
    def __init__(self, windowname=""):
        self.windowname = windowname 
 
        self.EnumWindows = windll.user32.EnumWindows
        self.EnumWindowsProc = WINFUNCTYPE(c_bool, c_int, POINTER(c_int))
        self.GetWindowText = windll.user32.GetWindowTextW
        self.GetWindowTextLength = windll.user32.GetWindowTextLengthW
        self.IsWindowVisible = windll.user32.IsWindowVisible
        self.GetClassName = windll.user32.GetClassNameW
        self.BringWindowToTop = windll.user32.BringWindowToTop
        self.GetForegroundWindow = windll.user32.GetForegroundWindow
 
        self.titles = []

        self.EnumWindows(self.EnumWindowsProc(self.foreach_window), 0)
 
    def foreach_window(self, hwnd, lParam):
        if self.IsWindowVisible(hwnd):
            length = self.GetWindowTextLength(hwnd)
            classname = create_unicode_buffer(100 + 1)
            self.GetClassName(hwnd, classname, 100 + 1)
            buff = create_unicode_buffer(length + 1)
            self.GetWindowText(hwnd, buff, length + 1)
            self.titles.append((hwnd, buff.value, classname.value, windll.user32.IsIconic(hwnd)))
        return True
    
    def refresh_wins(self):
        del self.titles[:]
        self.EnumWindows(self.EnumWindowsProc(self.foreach_window), 0)
        return self.titles
    
    
    def find_window(self):
        newest_titles = self.refresh_wins()
        for item in newest_titles:
            if self.windowname in item[1]:
                return item[0]
        return False

    def get_windowname(self):
        newest_titles = self.refresh_wins()
        marks = self.windowname.copy()
        solve_dict = dict()
        for x in marks:
            solve_dict[x] = []
            for item in newest_titles:
                if x in item[1]:
                    solve_dict[x] += [item]
        d = dict()
        for key, values in solve_dict.items():
            for v in values:
                if d.get(v) is None:
                    d[v] = 1
                else:
                    d[v] += 1
        try:
            max_elem = max(d)    # das was am nähesten dran ist
        except ValueError:
            max_elem = None

        if max_elem is not None:
            print(f"Screen: {max_elem}")
            return max_elem[1]
        return None

    def get_windowname_alt(self):
        newest_titles = self.refresh_wins()
        for item in newest_titles:
            if self.windowname in item[1]:
                print(f"Screen: {item}")
                return item[1]
        return None

    def list_windownames(self) -> list:
        newest_titles = self.refresh_wins()
        windownames = []
        for item in newest_titles:
            windownames += [item[1]]
        return windownames


class Window_Capturer():
    def __init__(self, windowname:str):
        # find window
        if windowname != None:
            self.windowname = Window_Finder(windowname).get_windowname()
            # set window details
            self.hwnd = win32gui.FindWindow(None, self.windowname)
            if not self.hwnd:
                self.hwnd = win32gui.GetDesktopWindow()
                #raise Exception('Window not found "{windowname}"')
                print(f'Window not found "{windowname}"')
        else:
            self.windowname = None
            # set window details
            self.hwnd = win32gui.GetDesktopWindow()

        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        #self.w = 1920
        #self.h = 1020

        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels*2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set offset, so we can translate screenshot coordinates
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def set_windowname(self, name:str):
        self.windowname = Window_Finder(name).get_windowname()

    def take_screenshot(self):
        # get Image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, 0), win32con.SRCCOPY)

        # save screenshot
        #dataBitMap.SaveBitmapFile(cDC, "debug.bmp")
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Drop alpha channel
        img = img[..., :3]

        # for TypeError stable
        img = np.ascontiguousarray(img)

        return img

    def get_screen_pos(self, pos:tuple):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
 

if __name__ == "__main__": 
    w_finder = Window_Finder("Discord")
    if w_finder.find_window():
        print ("found")
    else:
        print ("not found")