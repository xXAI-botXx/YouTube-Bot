# Source:
# - https://www.youtube.com/watch?v=7k4j-uL8WSQ

import cv2 as cv    # pip install opencv-python
import pyautogui as pag
from PIL import ImageGrab, Image    # pip install pillow
import win32gui    # pip install pywin32
import numpy as np
from time import time
#import os

import window_capture as wr

class Object_Detector():
    def __init__(self, windowname:str, target_path:str, full_mode=True):
        if full_mode == False:
            self.windowname = windowname
            self.window_capturer = wr.Window_Capturer(windowname)
        else:
            self.windowname = None
            self.window_capturer = wr.Window_Capturer(windowname)
        self.target_path = target_path
        self.full_mode = full_mode

    def change_target(self, windowname:str):
        self.window_capturer.set_windowname(windowname)

    def window_capture(self):
        return self.window_capturer.take_screenshot()

    def detect(self):
        while True:
            loop_begin = time()
            #screenshot = pag.screenshot()
            #screenshot = ImageGrab.grab()
            cv_img = self.window_capture()
            #cv_img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
            cv.imshow('Object-Detector', cv_img)
            #self.find_click_pos(self.target_path, haystack_img=cv_img, threshold=0.6, debug_mode='rectangles')

            try:
                print(f"FPS {1 / (time()-loop_begin)}")
            except ZeroDivisionError:
                print("FPS 0")

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

        print("I'm finish!")

    def find_click_pos(self, needle_img_path, haystack_img, threshold=0.5, debug_mode=None):
        if not needle_img_path.endswith(".jpg"):  
            img = Image.open(needle_img_path).convert('RGB')
            needle_img_path = ".".join(needle_img_path.split(".")[:-1])+".jpg"
            img.save(needle_img_path)

        needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
        #if(needle_img is not None):
        #    cv.cvtColor(needle_img, cv.COLOR_BGR2GRAY)

        needle_w = needle_img.shape[1]
        needle_h = needle_img.shape[0]

        method = cv.TM_CCOEFF_NORMED
        result = cv.matchTemplate(haystack_img, needle_img, method)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []
        for location in locations:
            rect = [int(location[0]), int(location[1]), needle_w, needle_h]
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

# Testing
if __name__ == "__main__":
    #list(map(lambda x: print(x) if len(x) > 0 else True, wr.Window_Finder().list_windownames()))
    Object_Detector([""], "DATA/test_target.png", full_mode=True).detect()
