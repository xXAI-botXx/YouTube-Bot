from object_detection import Object_Detector
from youtube_bot import Youtube_Bot
import threading
import keyboard

class Bot_System(object):
    def __init__(self):
        self.bot = Youtube_Bot(debug_mode=False)
        self.should_run = False
        self.is_running = False
        self.t = None
        self.debug_mode = False
        self.commands = {'run':lambda: self.run(), 'stop':lambda:self.stop(), 'exit':lambda:self.exit(), 'state':lambda:self.state(), 'debug':lambda:self.debug(), 'help':lambda:self.help()}

    def main(self):
        while True:
            user_input = input("User Input: ")
            try:
                self.commands[user_input.replace(" ", "")]()
            except KeyError:
                print(f"----> There is not Keyword '{user_input}'")
                print(f"----> Type 'help' for more informations!")

    def run(self):
        if self.is_running == False:
            self.is_running = True
            self.should_run = True
            self.t = threading.Thread(target=lambda: self.bot.run())
            if self.debug_mode:    # to get out
                print("----> Bot is now running")
                print(self.bot.debug_mode)
                self.t.start()
                keyboard.wait("q")
                #self.exit()
                self.stop()
            else:
                self.t.start()
            print("----> Bot is now running")
        else:
            print("----> Bot still running")

    def stop(self):
        if self.is_running == True:
            self.is_running = False
            self.should_run = True
            Object_Detector.SHOULD_RUN = False    # should stop bzw. kill the threads
            self.t.join()
            # sind Threads nun gewschlossen? wie kann man prüfen? schau im Buch!
            #print(self.t.is_alive())
            print("----> Bot is stopped")
        else:
            print("----> Bot is still stopped")

    def exit(self):
        if self.t != None:
            if self.t.is_alive():
                self.stop()
        print("----> System shut down...")
        exit(0)

    def state(self):
        if self.is_running:
            print("----> The Bot is running!")
        else:
            print("----> The Bot don't runs...")

    def getState(self) -> bool:
        if self.is_running:
            return True
        else:
            return False

    def debug(self):
        if self.debug_mode:
            self.debug_mode = False
            if self.getState():
                self.stop()
                self.bot = Youtube_Bot(debug_mode=False) 
                self.t = threading.Thread(target=lambda: self.bot.run())
                print("----> Debug-Mode deactivated")
                self.run()
            else:
                self.bot = Youtube_Bot(debug_mode=False) 
                self.t = threading.Thread(target=lambda: self.bot.run())
                print("----> Debug-Mode deactivated")
        else:
            self.debug_mode = True
            if self.getState():
                self.stop()
                self.bot = Youtube_Bot(debug_mode=True)
                self.t = threading.Thread(target=lambda: self.bot.run())
                print("----> Debug-Mode activated    -> press q to get out")
                self.run()
            else:
                self.bot = Youtube_Bot(debug_mode=True)
                self.t = threading.Thread(target=lambda: self.bot.run())
                print("----> Debug-Mode activated    -> press q to get out")

    def help(self):
        txt = "----> Welcome to this Bot Application. The Bot should help you with you YouTube Advertising."
        txt += "\n----> Currently the Application is for german version of YouTube!"
        txt += "\n----> There are follow key-words:"
        txt += "\n        - 'run'"
        txt += "\n        - 'stop'"
        txt += "\n        - 'debug'  -> press q to get out"
        txt += "\n        - 'exit'"
        txt += "\n        - 'state'"

if __name__ == "__main__":
    #keyboard.on_press_key("q", lambda _:exit)
    Bot_System().main()