# Source:
# - https://www.youtube.com/watch?v=7k4j-uL8WSQ

import cv2 as cv    # pip install opencv-python
import pyautogui as pag
from PIL import ImageGrab, Image    # pip install pillow
from functools import partial
import numpy as np

class Object_Detector():

    SHOULD_RUN = True

    def __init__(self, target_path:str, equality=0.7):
        self.target_path = target_path
        self.equality = equality

        # init target
        if not self.target_path.endswith(".jpg"):  
            img = Image.open(self.target_path).convert('RGB')
            needle_img_path = ".".join(self.target_path.split(".")[:-1])+".jpg"
            img.save(needle_img_path)
        else:
            needle_img_path = target_path

        self.target_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

        self.target_w = self.target_img.shape[1]
        self.target_h = self.target_img.shape[0]

        self.method = cv.TM_CCOEFF_NORMED

    def detect(self) -> bool:
        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
        screenshot = ImageGrab.grab()
        cv_img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
        point = self.find_click_pos(haystack_img=cv_img, debug_mode=None)
        if len(point) > 0:
            return True
        else:
            return False

    def find_click_pos(self, haystack_img, debug_mode=None):
        threshold = self.equality
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

        return points

    def click(self, point):
        try:
            if len(point) > 0:
                if len(point[0]) >= 2:
                    # libs for clicking = pyautogui, pywinauto, ctypes.windll
                    old_pos = pag.position()
                    # img started by 0 and pos does not
                    x_scale = 1920
                    p1 = point[0][0] - x_scale
                    p2 = point[0][1]
                    pag.moveTo(p1, p2)
                    pag.click(p1, p2)
                    pag.moveTo(old_pos)
        except IndexError:
            print("Error: no point to click")

    def find_and_click(self):
        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
        # libs for screenshoting: pyautogui, PIL, win32
        screenshot = ImageGrab.grab()
        cv_img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
        point = self.find_click_pos(haystack_img=cv_img, debug_mode=None)
        self.click(point)

    def find_and_move(self):
        ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
        screenshot = ImageGrab.grab()
        cv_img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
        point = self.find_click_pos(haystack_img=cv_img, debug_mode=None)
        try:
            if len(point) > 0:
                if len(point[0]) >= 2:
                    x_scale = 1920
                    p1 = point[0][0] - x_scale
                    p2 = point[0][1]
                    pag.moveTo(p1, p2)
        except IndexError:
            print("Error: no point to click")

# Testing
if __name__ == "__main__":
    Object_Detector("DATA/test_target.png").detect()
