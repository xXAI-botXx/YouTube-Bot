import tkinter as tk
import main
from datetime import datetime as dt

def rgb2hex(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def rgb2hex_alt(r, g, b):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    hex_n = format(r, 'x') + format(g, 'x') + format(b, 'x')
    return f'#{hex_n}'


class Widget_With_Space(tk.Frame):
    def __init__(self, widget, text, bg, command=None, xspace=(20, 20), yspace=(20, 20), parent=None):
        super().__init__(parent)
        self.btn_color = '#A9BCF5'
        self.btn_color_2 = '#819FF7'
        
        if command == None:    # no btn
            self.widget = widget(self, bg=bg, state="disabled")    #justify=tk.LEFT
        else:
            self.widget = widget(self, text=text, bg=bg, command=command)
            self.widget.bind("<Enter>", self.on_enter)
            self.widget.bind("<Leave>", self.on_leave)
        self.widget.pack(expand=True, fill=tk.BOTH, padx=xspace, pady=yspace)

    def on_enter(self, event):
        btn = event.widget
        btn.config(bg=self.btn_color_2)

    def on_leave(self, event):
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
        


class Bot_Viewer(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.output = tk.StringVar()
        #self.output.set("Welcome to this YouTube Bot!")
        self.rows = 6
        self.columns = 2 #2
        self.control = main.Bot_System_GUI(self)
        self.btn_color = '#A9BCF5'
        self.btn_color_2 = '#819FF7'
        self.output = ""
        self.pause = False
        self.history_is_shown = False
        self.build_widgets()
        self.build_grow_factor()

    def build_widgets(self):
        # -> farbe soll sich verändern, aber evtl immer nur blasse farben
        #self.label_output = Widget_With_Space(tk.Label, self.output, "#BDBDBD", xspace=(10, 10), yspace=(10, 10), parent=self)
        #self.label_output.grid(row=0, column=1, rowspan=4, sticky='NESW') #, padx=(50, 0))
        self.txt_output = Widget_With_Space(tk.Text, "", "#BDBDBD", xspace=(10, 10), yspace=(10, 10), parent=self)
        self.txt_output.grid(row=0, column=1, rowspan=6, sticky='NESW') #, padx=(50, 0))
        # Am Anfang Bot Explaination hinzufügen
        self.output += f"Bot-System is now live ({dt.now().hour:02}:{dt.now().minute:02} Clock)"
        self.write_in_output()

        #self.btn_run = tk.Button(self, text='run', bg='#FA5858', command=self.event_run)
        self.btn_run = Widget_With_Space(tk.Button, text='run', bg=self.btn_color, command=self.event_run, xspace=(10, 10), yspace=(10, 10), parent=self)
        self.btn_run.grid(row=0, column=0, sticky='NESW') 

        self.btn_stop = Widget_With_Space(tk.Button, text='stop', bg=self.btn_color, command=self.event_stop, xspace=(10, 10), yspace=(0, 10), parent=self)
        self.btn_stop.grid(row=1, column=0, sticky='NESW')

        self.btn_debug = Widget_With_Space(tk.Button, text='debug', bg=self.btn_color, command=self.event_debug, xspace=(10, 10), yspace=(0, 10), parent=self)
        self.btn_debug.grid(row=2, column=0, sticky='NESW')

        self.btn_pause = Widget_With_Space(tk.Button, text='pause', bg=self.btn_color, command=self.event_pause, xspace=(10, 10), yspace=(0, 10), parent=self)
        self.btn_pause.grid(row=3, column=0, sticky='NESW')

        self.btn_history = Widget_With_Space(tk.Button, text='history', bg=self.btn_color, command=self.event_history, xspace=(10, 10), yspace=(0, 10), parent=self)
        self.btn_history.grid(row=4, column=0, sticky='NESW')

        self.btn_exit = Widget_With_Space(tk.Button, text='exit', bg=self.btn_color, command=self.event_exit, xspace=(10, 10), yspace=(0, 10), parent=self)
        self.btn_exit.grid(row=5, column=0, sticky='NESW')

    def build_grow_factor(self):
        for r in range(self.rows):
            self.rowconfigure(r, weight=1)
        for c in range(self.columns):
            self.columnconfigure(c, weight=1)

    def event_run(self):
        self.control.run()

    def event_stop(self):
        self.control.stop()

    def event_debug(self):
        self.control.debug()

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

def start():
    root = tk.Tk()
    root.geometry("800x400")
    root.title("YouTube Advertising Bot")
    #root.wm_attributes('-fullscreen','true')
    #root.wm_attributes('-type', 'splash')
    #root.overrideredirect(True)
    viewer = Bot_Viewer(root)
    viewer.pack(expand=True, fill=tk.BOTH)
    root.bind('<Key>', viewer.key_pressed)
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    root.title("YouTube Advertising Bot")
    #root.wm_attributes('-fullscreen','true')
    #root.wm_attributes('-type', 'splash')
    #root.overrideredirect(True)
    viewer = Bot_Viewer(root)
    viewer.pack(expand=True, fill=tk.BOTH)
    root.bind('<Key>', viewer.key_pressed)
    root.mainloop()

    # Testing
    #root = tk.Tk()
    #MyLabel = tk.Label(text="Moin", bg="red")#.pack(expand=True, fill=tk.BOTH)
    #MyLabelSpaced = Widget_With_Space(MyLabel, xspace=5, yspace=100, parent=root)
    #MyLabelSpaced.pack(expand=True, fill=tk.BOTH)
    #root.mainloop()
