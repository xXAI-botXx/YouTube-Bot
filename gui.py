import tkinter as tk
import main
from datetime import datetime as dt
import random
from time import time
from PIL import Image, ImageTk
import music

def rgb2hex_alt(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def rgb2hex(r, g, b):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    hex_n = format(r, 'x') + format(g, 'x') + format(b, 'x')
    return f'#{hex_n}'

def hex2rgb(x):
    x = x.replace("#", "")
    x = x.replace("0x", "")
    r = x[0:2]
    g = x[2:4]
    b = x[4:6]
    dec_n = (int(format(int(r, 16), 'd')), int(format(int(g, 16), 'd')), int(format(int(b, 16), 'd')))
    return dec_n


class Widget_With_Space(tk.Frame):
    def __init__(self, widget, text, bg, command=None, xspace=(20, 20), yspace=(20, 20), parent=None, img=None):
        super().__init__(parent)
        self.btn_color = '#A9BCF5'
        self.btn_color_2 = '#819FF7'
        self.is_hovered = False
        self.xspace = xspace
        self.yspace = yspace
        
        if command == None:    # no btn
            self.widget = widget(self, bg=bg, state="disabled")    #justify=tk.LEFT
        else:
            if img != None:
                self.widget = widget(self, text=text, bg=bg, command=command, image=img)
                self.widget.bind("<Enter>", self.on_enter)
                self.widget.bind("<Leave>", self.on_leave)
            else:
                self.widget = widget(self, text=text, bg=bg, command=command)
                self.widget.bind("<Enter>", self.on_enter)
                self.widget.bind("<Leave>", self.on_leave)
        self.widget.pack(expand=True, fill=tk.BOTH, padx=xspace, pady=yspace)

    def on_enter(self, event):
        self.is_hovered = True
        btn = event.widget
        #btn.config(bg=self.btn_color_2)
        btn.config(bg="#FA5858")

    def on_leave(self, event):
        self.is_hovered = False
        btn = event.widget
        btn.config(bg=self.btn_color)

    def write(self, txt):
        self.widget.config(state="normal")
        self.widget.delete("0.0", self.widget.index("end"))

        #splitted_txt = []
        #for x in txt.split("\n"):
        #    if len(x) < 1:
        #        continue
        #    splitted_txt += [x] 

        new_txt = ""
        for i, x in enumerate(txt.split("\n")):
            new_txt += f"{i+1}. {x}\n"

        self.widget.insert("0.0", new_txt)
        self.widget.see("end")
        self.widget.config(state="disabled")

    def out(self, txt):
        self.widget.config(state="normal")
        self.widget.delete("0.0", self.widget.index("end"))
        self.widget.insert("0.0", txt)
        self.widget.config(state="disabled")

    def set_color(self, c1:str, c2:str):
        self.btn_color = c1
        self.btn_color_2 = c2    # now geupdated
        if not self.is_hovered:
            self.widget.config(bg=c1)


class Bot_Viewer(tk.Frame):
    def __init__(self, parent, music_player):
        super().__init__(parent)
        self.music_player = music_player
        self.rows = 4
        self.columns = 3 #2
        self.control = main.Bot_System_GUI(self)
        r = random.randint(30, 255)
        g = random.randint(30, 255)
        b = random.randint(30, 255)
        self.color_factor = 10
        self.r_reduce = random.randint(-5, 5)
        self.g_reduce = random.randint(-5, 5)
        self.b_reduce = random.randint(-5, 5)
        self.btn_color = rgb2hex(r, g, b)  # random init
        self.btn_color_2 = rgb2hex(r-self.color_factor, g-self.color_factor, b-self.color_factor)
        self.should_coloring = True
        self.output = ""
        self.pause = False
        self.music_on = False
        self.history_is_shown = False
        self.buttons = []
        self.build_widgets()
        self.build_grow_factor()
        self.after(1000, self.color_update)

    def build_widgets(self):
        # -> farbe soll sich verändern, aber evtl immer nur blasse farben
        #self.label_output = Widget_With_Space(tk.Label, self.output, "#BDBDBD", xspace=(10, 10), yspace=(10, 10), parent=self)
        #self.label_output.grid(row=0, column=1, rowspan=4, sticky='NESW') #, padx=(50, 0))
        self.txt_output = Widget_With_Space(tk.Text, "", "#BDBDBD", xspace=(10, 10), yspace=(10, 10), parent=self)
        self.txt_output.grid(row=0, column=1, rowspan=4, sticky='NESW') #, padx=(50, 0))
        self.txt_output.set_color(self.btn_color, self.btn_color_2)
        # Am Anfang Bot Explaination hinzufügen
        self.output += f"Bot-System is now live ({dt.now().hour:02}:{dt.now().minute:02} Clock)"
        self.write_in_output()

        img = ImageTk.PhotoImage(Image.open("DATA/rainbow.jpg"))
        self.btn_coloring = Widget_With_Space(tk.Button, text='coloring', bg=self.btn_color, command=self.event_coloring, xspace=(10, 10), yspace=(10, 10), parent=self)#, img=img)
        self.btn_coloring.grid(row=0, column=2, sticky='NESW') 
        self.btn_coloring.set_color(self.btn_color, self.btn_color_2)
        self.buttons += [self.btn_coloring]

        #self.btn_run = tk.Button(self, text='run', bg='#FA5858', command=self.event_run)
        self.btn_run = Widget_With_Space(tk.Button, text='run', bg=self.btn_color, command=self.event_run, xspace=(10, 10), yspace=(10, 10), parent=self)
        self.btn_run.grid(row=0, column=0, sticky='NESW') 
        self.btn_run.set_color(self.btn_color, self.btn_color_2)
        self.buttons += [self.btn_run]

        self.btn_stop = Widget_With_Space(tk.Button, text='stop', bg=self.btn_color, command=self.event_stop, xspace=(10, 10), yspace=(0, 10), parent=self)
        self.btn_stop.grid(row=1, column=0, sticky='NESW')
        self.btn_stop.set_color(self.btn_color, self.btn_color_2)
        self.buttons += [self.btn_stop]

        self.btn_pause = Widget_With_Space(tk.Button, text='pause', bg=self.btn_color, command=self.event_pause, xspace=(10, 10), yspace=(0, 10), parent=self)
        self.btn_pause.grid(row=2, column=0, sticky='NESW')
        self.btn_pause.set_color(self.btn_color, self.btn_color_2)
        self.buttons += [self.btn_pause]

        self.btn_history = Widget_With_Space(tk.Button, text='history', bg=self.btn_color, command=self.event_history, xspace=(10, 10), yspace=(0, 10), parent=self)
        self.btn_history.grid(row=3, column=0, sticky='NESW')
        self.btn_history.set_color(self.btn_color, self.btn_color_2)
        self.buttons += [self.btn_history]

        self.btn_exit = Widget_With_Space(tk.Button, text='exit', bg=self.btn_color, command=self.event_exit, xspace=(10, 10), yspace=(0, 10), parent=self)
        self.btn_exit.grid(row=3, column=2, sticky='NESW')
        self.btn_exit.set_color(self.btn_color, self.btn_color_2)
        self.buttons += [self.btn_exit]

    def build_grow_factor(self):
        for r in range(self.rows):
            self.rowconfigure(r, weight=1)
        for c in range(self.columns):
            self.columnconfigure(c, weight=1)

    def event_coloring(self):
        if self.should_coloring:
            self.should_coloring = False
        else:
            self.should_coloring = True
            self.after(200, self.color_update)

    def event_run(self):
        self.control.run()
        #self.control.debug()

    def event_stop(self):
        self.control.stop()

    def event_pause(self):
        self.pause = not self.pause

    def event_history(self):
        if self.history_is_shown:
            if self.pause == True:    # for clicking in runtime
                self.pause = False
            self.write_in_output()
        else:
            if self.pause == False:
                self.pause = True
            self.history_is_shown = True
            history = self.control.get_history()
            if len(history) < 1:
                self.out("Nothing is done yet...")
            else:
                self.out(history)

    def event_exit(self):
        #exit(0)
        self.music_player.stop()
        self.control.exit()

    def key_pressed(self, key):
        input = key.char
        #...

    def write_in_output(self, txt=""):
        self.output = (self.output+"\n"+txt).strip()
        if not self.pause:
            self.history_is_shown = False
            self.txt_output.write(self.output)

    def out(self, txt):
        self.txt_output.out(txt)

    def clear_output(self):
        self.output = ""

    def color_update(self):
        if not self.should_coloring:
            return
        min_lim = 30
        max_lim = 255
        # color update
        r, g, b = hex2rgb(self.btn_color)

        r -= self.r_reduce
        if r < min_lim:
            self.r_reduce = - self.r_reduce
            r -= self.r_reduce*2
        elif r > max_lim:
            self.r_reduce = - self.r_reduce
            r -= self.r_reduce*2

        g -= self.g_reduce
        if g < min_lim:
            self.g_reduce = - self.g_reduce
            g -= self.g_reduce
        elif g > max_lim:
            self.g_reduce = - self.g_reduce
            g -= self.g_reduce

        b -= self.b_reduce
        if b < min_lim:
            self.b_reduce = - self.b_reduce
            b -= self.b_reduce
        elif b > max_lim:
            self.b_reduce = - self.b_reduce
            b -= self.b_reduce

        self.btn_color = rgb2hex(r, g, b)
        c1 = rgb2hex(r, g, b)
        # hover color update
        self.btn_color_2 = rgb2hex(r-self.color_factor, g-self.color_factor, b-self.color_factor)
        c2 = rgb2hex(r-self.color_factor, g-self.color_factor, b-self.color_factor)

        # btn update
        for btn in self.buttons:
            btn.set_color(c1, c2)
        self.txt_output.set_color(c1, c2)
        
        # repeat
        self.after(200, self.color_update)

class Intro(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.music_player = music.Music_Player()
        self.labels = []
        self.images = []
        #self.img_0 = tk.PhotoImage(file="DATA/INTRO/anzeige.jpg")
        self.img_0 = ImageTk.PhotoImage(Image.open("DATA/INTRO/anzeige.jpg"))
        self.images += [self.img_0]
        self.img_1 = ImageTk.PhotoImage(Image.open("DATA/INTRO/ueberspringen.jpg"))
        self.images += [self.img_1]
        self.img_2 = ImageTk.PhotoImage(Image.open("DATA/INTRO/werbung_ueberspringen.jpg"))
        self.images += [self.img_2]
        self.img_3 = ImageTk.PhotoImage(Image.open("DATA/INTRO/youtube_2.jpg"))
        self.images += [self.img_3]
        self.img_4 = ImageTk.PhotoImage(Image.open("DATA/INTRO/youtube.jpg"))
        self.images += [self.img_4]
        self.begin = time()
        self.music_player.play_intro()
        self.in_intro = True
        self.after(250, self.intro_update)

    def intro_update(self):
        if self.in_intro == False:
            self.at_the_end()
            return
        width = self.parent.winfo_width()
        height = self.parent.winfo_height()
        # do random stuff
        for i in range(random.randint(1, 5)):
            x = random.randint(0, width-40)
            y = random.randint(0, height-40)
            i = random.randint(0,4)
            label_img_port = tk.Label(self, image=self.images[i])
            label_img_port.place(x=x, y=y)
            self.labels += [label_img_port]
        # check time
        if time()-self.begin >= 120:
            self.at_the_end()
            return
        #repeat
        self.after(250, self.intro_update)

    def at_the_end(self):
        self.pack_forget()
        self.music_player.stop()
        self.music_player.play_and_stop("DATA/MUSIC/kluck.wav")
        viewer = Bot_Viewer(self.parent, self.music_player)
        viewer.pack(expand=True, fill=tk.BOTH)
        self.parent.bind('<Key>', viewer.key_pressed)

    def on_click(self, event):
        self.in_intro = False

def start():
    root = tk.Tk()
    root.geometry("1200x600")
    root.title("YouTube Advertising Bot")
    #root.wm_attributes('-fullscreen','true')
    #root.wm_attributes('-type', 'splash')
    #root.overrideredirect(True)
    intro = Intro(root)
    root.bind("<1>", intro.on_click)
    intro.pack(expand=True, fill=tk.BOTH)
    
    root.mainloop()


if __name__ == "__main__":
    start()

    # Testing
    #root = tk.Tk()
    #MyLabel = tk.Label(text="Moin", bg="red")#.pack(expand=True, fill=tk.BOTH)
    #MyLabelSpaced = Widget_With_Space(MyLabel, xspace=5, yspace=100, parent=root)
    #MyLabelSpaced.pack(expand=True, fill=tk.BOTH)
    #root.mainloop()
