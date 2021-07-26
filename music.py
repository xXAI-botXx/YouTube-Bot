import winsound
import threading
import random
import time
import wave
import contextlib
#import queue

class Timer():

    SHOULD_RUN = False

    def __init__(self):
        pass

    def start(self, time, func):
        self.time = time
        self.func = func
        Timer.SHOULD_RUN = True
        t = threading.Thread(target=lambda:self.run())
        t.start()

    def run(self):
        self.begin = time.time()
        i = 0
        while time.time()-self.begin < self.time:
            if Timer.SHOULD_RUN == False:
                break
            i += 1
        if Timer.SHOULD_RUN:
            self.func()

    def stop(self):
        Timer.SHOULD_RUN = False

class Music_Player():
    def __init__(self):
        self.timer = Timer()
        self.song = None
        self.songs = ["DATA/MUSIC/song_1.wav", "DATA/MUSIC/song_2.wav", "DATA/MUSIC/song_3.wav"]
        self.last_song = ""
        self.is_playing = False
        self.play_thread = None
        self.in_song = True

    def play_intro(self):
        self.is_playing = True
        self.in_song = True
        # find a song
        self.song = self.songs[1]
        self.last_song = self.song
        #get duration
        with contextlib. closing(wave. open(self.song,'r')) as f:
            frames = f. getnframes()
            rate = f. getframerate()
        duration = frames / float(rate)

        # play and start a Timer
        self.timer.start(duration, lambda:self.play())
        winsound.PlaySound(self.song, winsound.SND_ASYNC)

    def play(self):
        self.stop()   # stay safe
        self.is_playing = True
        self.in_song = True
        # find a song
        self.song = random.choice(self.songs)
        while self.song == self.last_song:
            self.song = random.choice(self.songs)
        self.last_song = self.song
        #get duration
        with contextlib. closing(wave. open(self.song,'r')) as f:
            frames = f. getnframes()
            rate = f. getframerate()
        duration = frames / float(rate)

        # play and start a Timer
        self.timer.start(duration, lambda:self.play())
        winsound.PlaySound(self.song, winsound.SND_ASYNC)

    def play_and_stop(self, path):
        self.stop()   # stay safe
        self.is_playing = True
        self.in_song = True
        # find a song
        self.song = path
        self.last_song = path
        #get duration
        with contextlib. closing(wave. open(self.song,'r')) as f:
            frames = f. getnframes()
            rate = f. getframerate()
        duration = frames / float(rate)

        # play and start a Timer
        self.timer.start(duration, lambda:self.stop())
        winsound.PlaySound(self.song, winsound.SND_ASYNC)

    def stop(self):
        self.is_playing = False
        winsound.PlaySound(None, winsound.SND_PURGE)
        self.timer.stop()

    def thread_function(self):
        while self.is_playing:
            if not self.in_song:
                self.in_song = True
                self.song = random.choice(self.songs)
                while self.song == self.last_song:
                    self.song = random.choice(self.songs)
                #winsound.PlaySound(self.song, winsound.SND_FILENAME)
                winsound.PlaySound(self.song, winsound.SND_ASYNC)

    