from object_detection import Object_Detector
from time import sleep
import pyautogui as pag

class Mute_Bot():
    def __init__(self, target_path: str, target_2_path:str, target_3_path:str, target_4_path:str, viewer):
        self.anzeige_detector = Object_Detector(target_path, equality=0.7)
        self.mute_on_detector = Object_Detector(target_2_path, equality=0.9)
        self.mute_off_detector = Object_Detector(target_3_path, equality=0.9)
        self.play_detector = Object_Detector(target_4_path, equality=0.6)
        self.in_advertising = False
        self.viewer = viewer

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
        self.print_out("\nXXX Detection XXX -> Mute_Bot")
        self.print_out(f"        Anzeige: {self.anzeige_detector.detect()}")
        self.print_out(f"        Mute_On: {self.mute_on_detector.detect()}")
        self.print_out(f"        Mute_Off:{self.mute_off_detector.detect()}\n")
        anzeige_appear = self.anzeige_detector.detect()
        if anzeige_appear and self.in_advertising:
            self.print_out("\n#Mute-Bot: You are in advertising and i should have done my job.")
        elif anzeige_appear and not self.in_advertising:
            old_pos = pag.position()
            self.anzeige_detector.find_and_move()
            self.in_advertising = True
            self.mute_on()
            pag.moveTo(old_pos)
            self.print_out("#Mute-Bot: You are in advertising and i turned off the sound.")
        elif not anzeige_appear and self.in_advertising:
            self.in_advertising = False
            self.mute_off()
            self.print_out("#Mute-Bot: You are out of advertising and i turned on the sound.")
        else:
            self.print_out("#Mute-Bot: No Advertising no problems...")

    def mute_on(self):
        if not self.mute_on_detector.detect():
            self.mute_off_detector.find_and_click()

    def mute_off(self):
        if not self.mute_off_detector.detect():
            self.mute_on_detector.find_and_click()

    def print_out(self, txt):
        if self.viewer == None:
            print(txt)
        else:
            #self.output_var.set(self.output_var.get()+"\n"+txt)
            self.viewer.write_in_output(txt)


class Advertising_Skip_Bot():
    def __init__(self, target_path:str, target_2_path:str, viewer):
        self.advertising_skip_detector = Object_Detector(target_path, equality=0.6) 
        self.skip_detector = Object_Detector(target_2_path, equality=0.6)
        self.viewer = viewer

    def run(self):
        self.advertising_skip_detector.detect()
        self.skip_detector.detect()
        self.advertising_skip_detector.find_and_click()
        self.skip_detector.find_and_click()

    def run_debug(self):
        self.print_out("\nXXX Detection XXX -> Advertising_Skip_Bot")
        self.print_out(f"        Advertising-Skip: {self.advertising_skip_detector.detect()}")
        self.print_out(f"        Skip:             {self.skip_detector.detect()}")
        self.advertising_skip_detector.find_and_click()
        self.skip_detector.find_and_click()

    def print_out(self, txt):
        if self.viewer == None:
            print(txt)
        else:
            #self.output_var.set(self.output_var.get()+"\n"+txt)
            self.viewer.write_in_output(txt)


class Advertising_Banner_Bot():
    def __init__(self, target_path:str, target_2_path:str, viewer):
        self.advertising_banner_black_detector = Object_Detector(target_path, equality=0.75)
        self.advertising_banner_white_detector = Object_Detector(target_2_path, equality=0.75)
        self.viewer = viewer

    def run(self):
        self.advertising_banner_black_detector.find_and_click()
        self.advertising_banner_white_detector.find_and_click()

    def run_debug(self):
        self.print_out("\nXXX Detection XXX -> Advertising_Banner_Bot")
        self.print_out(f"        Advertising-black-Skip: {self.advertising_banner_black_detector.detect()}")
        self.print_out(f"        Advertising-white-Skip: {self.advertising_banner_white_detector.detect()}")
        self.advertising_banner_black_detector.find_and_click()
        self.advertising_banner_white_detector.find_and_click()

    def print_out(self, txt):
        if self.viewer == None:
            print(txt)
        else:
            #self.output_var.set(self.output_var.get()+"\n"+txt)
            self.viewer.write_in_output(txt)


class Youtube_Bot():
    def __init__(self, debug_mode, viewer=None):
        self.advertising_skip_bot = Advertising_Skip_Bot("DATA/werbung_ueberspringen.jpg", "DATA/ueberspringen.jpg", viewer)
        self.mute_bot = Mute_Bot("DATA/anzeige.jpg", "DATA/mute_on.jpg", "DATA/mute_off.jpg", "DATA/play.jpg", viewer)
        self.advertising_banner_bot = Advertising_Banner_Bot("DATA/werbe_banner_i_x_schwarz.jpg", "DATA/werbe_banner_i_x_weis.jpg", viewer)
        self.youtube_logo_black_bot = Object_Detector("DATA/youtube.jpg", equality=0.5)
        self.youtube_logo_white_bot = Object_Detector("DATA/youtube_2.jpg", equality=0.5)
        self.debug_mode = debug_mode
        self.viewer = viewer

    def run(self):
        while Object_Detector.SHOULD_RUN:
            
            if self.debug_mode:
                if self.youtube_logo_black_bot.detect() or self.youtube_logo_white_bot.detect():
                    self.print_out("YouTube detected...checking process:")
                    self.advertising_skip_bot.run_debug()
                    self.mute_bot.run_debug()
                    self.advertising_banner_bot.run_debug()
                    #sleep(1)    # FIXME -> mit FPS
                else:
                    self.print_out("YouTube not detected...")
            else:
                if self.youtube_logo_black_bot.detect() or self.youtube_logo_white_bot.detect():
                    self.advertising_skip_bot.run()
                    self.mute_bot.run()
                    self.advertising_banner_bot.run()
                    #sleep(1)    # FIXME -> mit FPS

    def print_out(self, txt):
        if self.viewer == None:
            print(txt)
        else:
            #self.output_var.set(self.output_var.get()+"\n"+txt)
            self.viewer.write_in_output(txt)
