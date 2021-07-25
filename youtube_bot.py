from object_detection import Object_Detector
from enum import Enum
from time import sleep
import pyautogui as pag


class Mute_Bot():
    def __init__(self, target_path: str, target_2_path:str, target_3_path:str, target_4_path:str):
        self.anzeige_detector = Object_Detector(target_path, equality=0.7)
        self.mute_on_detector = Object_Detector(target_2_path, equality=0.9)
        self.mute_off_detector = Object_Detector(target_3_path, equality=0.9)
        self.play_detector = Object_Detector(target_4_path, equality=0.6)
        self.in_advertising = False

    def run(self):
        anzeige_appear = self.anzeige_detector.detect()
        if anzeige_appear and self.in_advertising:
            pass
        elif anzeige_appear and not self.in_advertising:
            old_pos = pag.position()
            self.anzeige_detector.find_and_move()
            self.in_advertising = True
            self.mute_on()
            pag.moveTo(old_pos)
        elif not anzeige_appear and self.in_advertising:
            self.in_advertising = False
            self.mute_off()

    def run_debug(self):
        print("\nXXX Detection XXX -> Mute_Bot")
        print(f"        Anzeige: {self.anzeige_detector.detect()}")
        print(f"        Mute_On: {self.mute_on_detector.detect()}")
        print(f"        Mute_Off:{self.mute_off_detector.detect()}\n")
        anzeige_appear = self.anzeige_detector.detect()
        if anzeige_appear and self.in_advertising:
            print("\n#Mute-Bot: You are in advertising and i should have done my job.")
        elif anzeige_appear and not self.in_advertising:
            old_pos = pag.position()
            self.anzeige_detector.find_and_move()
            self.in_advertising = True
            self.mute_on()
            pag.moveTo(old_pos)
            print("#Mute-Bot: You are in advertising and i turned off the sound.")
        elif not anzeige_appear and self.in_advertising:
            self.in_advertising = False
            self.mute_off()
            print("#Mute-Bot: You are out of advertising and i turned on the sound.")
        else:
            print("#Mute-Bot: No Advertising no problems...")

    def mute_on(self):
        if not self.mute_on_detector.detect():
            self.mute_off_detector.find_and_click()

    def mute_off(self):
        if not self.mute_off_detector.detect():
            self.mute_on_detector.find_and_click()


class Advertising_Skip_Bot():
    def __init__(self, target_path:str, target_2_path:str):
        self.advertising_skip_detector = Object_Detector(target_path, equality=0.6) 
        self.skip_detector = Object_Detector(target_2_path, equality=0.6)

    def run(self):
        self.advertising_skip_detector.detect()
        self.skip_detector.detect()
        self.advertising_skip_detector.find_and_click()
        self.skip_detector.find_and_click()

    def run_debug(self):
        print("\nXXX Detection XXX -> Advertising_Skip_Bot")
        print(f"        Advertising-Skip: {self.advertising_skip_detector.detect()}")
        print(f"        Skip:             {self.skip_detector.detect()}")
        self.advertising_skip_detector.find_and_click()
        self.skip_detector.find_and_click()


class Advertising_Banner_Bot():
    def __init__(self, target_path:str, target_2_path:str):
        self.advertising_banner_black_detector = Object_Detector(target_path, equality=0.75)
        self.advertising_banner_white_detector = Object_Detector(target_2_path, equality=0.75)

    def run(self):
        self.advertising_banner_black_detector.find_and_click()
        self.advertising_banner_white_detector.find_and_click()

    def run_debug(self):
        print("\nXXX Detection XXX -> Advertising_Banner_Bot")
        print(f"        Advertising-black-Skip: {self.advertising_banner_black_detector.detect()}")
        print(f"        Advertising-white-Skip: {self.advertising_banner_white_detector.detect()}")
        self.advertising_banner_black_detector.find_and_click()
        self.advertising_banner_white_detector.find_and_click()


class Youtube_Bot():
    def __init__(self, debug_mode):
        self.advertising_skip_bot = Advertising_Skip_Bot("DATA/werbung_ueberspringen.jpg", "DATA/ueberspringen.jpg")
        self.mute_bot = Mute_Bot("DATA/anzeige.jpg", "DATA/mute_on.jpg", "DATA/mute_off.jpg", "DATA/play.jpg")
        self.advertising_banner_bot = Advertising_Banner_Bot("DATA/werbe_banner_i_x_schwarz.jpg", "DATA/werbe_banner_i_x_weis.jpg")
        self.youtube_logo_black_bot = Object_Detector("DATA/youtube.jpg", equality=0.5)
        self.youtube_logo_white_bot = Object_Detector("DATA/youtube_2.jpg", equality=0.5)
        self.debug_mode = debug_mode

    def run(self):
        while Object_Detector.SHOULD_RUN:
            
            if self.debug_mode:
                if self.youtube_logo_black_bot.detect() or self.youtube_logo_white_bot.detect():
                    self.advertising_skip_bot.run_debug()
                    self.mute_bot.run_debug()
                    self.advertising_banner_bot.run_debug()
                    sleep(1)    # FIXME -> mit FPS
                else:
                    print("YouTube not detected...")
            else:
                if self.youtube_logo_bot.detect():
                    self.advertising_skip_bot.run()
                    self.mute_bot.run()
                    self.advertising_banner_bot.run()
                    sleep(1)    # FIXME -> mit FPS
