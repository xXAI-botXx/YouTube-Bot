# Source:
# - https://www.youtube.com/watch?v=7k4j-uL8WSQ

import ctypes
import cv2 as cv    # pip install opencv-python
import pyautogui as pag
from PIL import ImageGrab, Image    # pip install pillow
from functools import partial
import win32gui    # pip install pywin32
#from pywinauto import mouse
import pywinauto
import numpy as np
from time import time
#import os

class Object_Detector():

    MOUSE_LEFTDOWN = 0x0002     # left button down 
    MOUSE_LEFTUP = 0x0004       # left button up 
    MOUSE_RIGHTDOWN = 0x0008    # right button down 
    MOUSE_RIGHTUP = 0x0010      # right button up 
    MOUSE_MIDDLEDOWN = 0x0020   # middle button down 
    MOUSE_MIDDLEUP = 0x0040     # middle button up 

    SHOULD_RUN = True

    def __init__(self, target_path:str):
        self.target_path = target_path
        self.cool_down = [None, 5]    # start, limit

        # init target
        if not self.target_path.endswith(".jpg"):  
            img = Image.open(self.target_path).convert('RGB')
            needle_img_path = ".".join(self.target_path.split(".")[:-1])+".jpg"
            img.save(needle_img_path)

        self.target_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
        #if(needle_img is not None):
        #    cv.cvtColor(needle_img, cv.COLOR_BGR2GRAY)

        self.target_w = self.target_img.shape[1]
        self.target_h = self.target_img.shape[0]

        self.method = cv.TM_CCOEFF_NORMED

    def work(self):
        loop_begin = time()
        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
        #screenshot = pag.screenshot()
        screenshot = ImageGrab.grab()
        #cv_img = self.window_capture()
        cv_img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
        #cv.imshow('Object-Detector', cv_img)
        point = self.find_click_pos(haystack_img=cv_img, threshold=0.7, debug_mode=None)
        self.click(point)
        #print(pag.position())

        try:
            pass
            #print(f"FPS {1 / (time()-loop_begin)}")
        except ZeroDivisionError:
            print("FPS 0")

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()

    def detect(self):
        while Object_Detector.SHOULD_RUN:
            loop_begin = time()
            ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
            #screenshot = pag.screenshot()
            screenshot = ImageGrab.grab()
            #cv_img = self.window_capture()
            cv_img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
            #cv.imshow('Object-Detector', cv_img)
            point = self.find_click_pos(haystack_img=cv_img, threshold=0.7, debug_mode=None)
            self.click(point)
            #print(pag.position())

            try:
                pass
                #print(f"FPS {1 / (time()-loop_begin)}")
            except ZeroDivisionError:
                print("FPS 0")

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break
        cv.destroyAllWindows()

        print("I'm finish!")

    def find_click_pos(self, haystack_img, threshold=0.5, debug_mode=None):
        result = cv.matchTemplate(haystack_img, self.target_img, self.method)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []
        for location in locations:
            rect = [int(location[0]), int(location[1]), self.target_w, self.target_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        points = []
        if len(rectangles):
            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            for (x, y, w, h) in rectangles:
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                points.append((center_x, center_y))

                if debug_mode == 'rectangles':
                    # Determine the box position
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    # Draw the box
                    cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                                lineType=line_type, thickness=2)
                elif debug_mode == 'points':
                    # Draw the center point
                    cv.drawMarker(haystack_img, (center_x, center_y), 
                                color=marker_color, markerType=marker_type, 
                                markerSize=40, thickness=2)

        if debug_mode:
            cv.imshow('Matches', haystack_img)
            #cv.waitKey()
            #cv.imwrite('result_click_point.jpg', haystack_img)

        return points

    def click(self, point):    # [(1853, 146), (3743, 547)]    Point(x=-61, y=144)
        if len(point) >= 1:
            # libs for clicking = pyautogui, pywinauto, ctypes.windll
            old_pos = pag.position()
            # img started by 0 and pos does not
            x_scale = 1920
            p1 = point[0][0] - x_scale
            p2 = point[0][1]
        
            if self.cool_down[0] == None:
                self.cool_down[0] = time()
                #print(point)
                #pywinauto.mouse.move(coords=(p1, p2))
                #ctypes.windll.user32.SetCursorPos(p1, p2)
                #ctypes.windll.user32.mouse_event(Object_Detector.MOUSE_LEFTDOWN)
                #ctypes.windll.user32.mouse_event(Object_Detector.MOUSE_LEFTUP)
                pag.moveTo(p1, p2)
                pag.click(p1, p2)    # auto move
            elif time() - self.cool_down[0] > self.cool_down[1]:
                self.cool_down[0] = None
                pag.moveTo(p1, p2)
                pag.click(p1, p2)
            pag.moveTo(old_pos)

# Testing
if __name__ == "__main__":
    #list(map(lambda x: print(x) if len(x) > 0 else True, wr.Window_Finder().list_windownames()))
    Object_Detector("DATA/test_target.png").detect()
