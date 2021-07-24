from object_detection import Object_Detector
from enum import Enum
import threading

video_state = Enum("video_state", "RUNNING ADVERTISING PAUSED")
audio_state = Enum("audio_state", "MUTE_ON MUTE_OFF")

class Youtube_Bot():
    def __init__(self):
        self.video = video_state.RUNNING
        self.audio = audio_state.MUTE_OFF
        self.should_run = False
        self.run = False
        self.commands = {'run':lambda: self.run(), 'pause':lambda:self.pause()}

    def main(self):
        while True:
            user_input = input("User Input: ")

    def run(self):
        if self.run == False:
            pass
            # threads starten

    def pause(self):
        if self.run == True:
            pass
            # Object_Detector.SHOULD_RUN = False
            # sind Threads nun gewschlossen? wie kann man prüfen? schau im Buch!
            

    


    