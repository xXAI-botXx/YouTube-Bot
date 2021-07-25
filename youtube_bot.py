from object_detection import Object_Detector
from enum import Enum
from time import sleep
import win32gui
import pyautogui as pag

video_state = Enum("video_state", "RUNNING ADVERTISING PAUSED")
audio_state = Enum("audio_state", "MUTE_ON MUTE_OFF")

class Mute_Bot():
    def __init__(self, target_path: str, target_2_path:str, target_3_path:str, target_4_path:str):
        self.anzeige_detector = Object_Detector(target_path, equality=0.85)
        self.mute_on_detector = Object_Detector(target_2_path, equality=0.9)
        self.mute_off_detector = Object_Detector(target_3_path, equality=0.9)
        self.play_detector = Object_Detector(target_4_path, equality=0.6)
        self.in_advertising = False

    def run(self):
        anzeige_appear = self.anzeige_detector.detect()
        if anzeige_appear and self.in_advertising:
            pass
        elif anzeige_appear and not self.in_advertising:
            self.in_advertising = True
            self.mute_on()
        elif not anzeige_appear and self.in_advertising:
            self.in_advertising = False
            self.mute_off()

    def run_debug(self):
        print("XXX Detection XXX ")
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

class Youtube_Bot():
    def __init__(self, debug_mode):
        self.video = video_state.RUNNING
        self.audio = audio_state.MUTE_OFF
        self.mute_bot = Mute_Bot("DATA/anzeige.png", "DATA/mute_on.png", "DATA/mute_off.png", "DATA/play.png")
        self.youtube_logo_bot = Object_Detector("DATA/youtube.png")
        self.debug_mode = debug_mode

    def run(self):
        while Object_Detector.SHOULD_RUN:
            
            if self.debug_mode:
                if self.youtube_logo_bot.detect():
                    print(win32gui.GetCursorPos())
                    print(win32gui.GetCursorInfo())
                    self.mute_bot.run_debug()
                    sleep(1)    # FIXME -> mit FPS
                else:
                    print("YouTube not detected...")
            else:
                if self.youtube_logo_bot.detect():
                    self.mute_bot.run()
                    sleep(1)    # FIXME -> mit FPS


    
            

    


    