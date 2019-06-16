"""
Just having some fun in Python.
//christianlindeneg, June, 2019//

Thanks for jams & music:
https://studiojams.com/
"""
from tkinter import Tk, Canvas, Frame, Button, Text, mainloop, INSERT, DISABLED, BOTTOM
from json import load, loads
from random import randint
from os import system

try:
    from ffpyplayer.player import MediaPlayer
    from pafy import new
    from vlc import Instance
except ImportError:
    system('python -m pip install -r requirements.txt')

class Start:
    def __init__(self):
        self.HEIGHT = 150
        self.WIDTH = 500
        self.default_C = '#060606'
        self.pick_tune()

    def read(self):
        with open('music.json') as music:
            r_music = load(music)
            str_music = loads(r_music)

        return str_music

    def ranint(self, length):
        return randint(0, length-1)

    def pick_tune(self):
        self.music = self.read()
        self.music = self.music['music']
        self.randint = self.ranint(len(self.music))
        
        if not self.music[self.randint]['mp_link'] == None:
            self.randtune_local = self.music[self.randint]['mp_link']
            self.url = self.music[self.randint]['yt_link']
            self.credit = self.music[self.randint]['uploader']

            self.metho = 'local-file'
            self.player = MediaPlayer(str(self.randtune_local))

        else:
            self.randtune_stream = self.music[self.randint]['yt_link']
            self.url = self.music[self.randint]['yt_link']
            self.credit = self.music[self.randint]['uploader']

            self.metho = 'online-stream'
            self.video = new(self.randtune_stream)
            self.quality = self.video.getbestaudio()
            self.quality_url = self.quality.url

            self.vlc_ins = Instance()
            self.players = self.vlc_ins.media_player_new()
            self.current_media = self.vlc_ins.media_new(str(self.quality.url))
            self.player = MediaPlayer(self.current_media.get_mrl())

        self.title = '%s, #%s/%s' % (self.music[self.randint]['tune'], self.randint, len(self.music))
        self.pl_str = '\n%s\n\n%s\n%s\n\nplaying from: %s' % (self.credit, self.title, self.url, self.metho)

class GuiMain(Start):
    def __init__(self, master):
        super().__init__()
        """Acts as the Main Menu"""
        self.master = master
        # Generate Canvas
        self.canvas = Canvas(self.master, bg=self.default_C, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()
        # Generate Frame
        self.main_frame = Frame(self.master, bg=self.default_C)
        self.main_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

        self.vid_frame = Frame(self.master, bg=self.default_C)
        self.vid_frame.place(relx=0, rely=0, relwidth=1, relheight=0.872)
        self.vid_text_info = Text(self.vid_frame, bg='#070707', bd=5, exportselection=0, fg='#196619', height=self.HEIGHT, width=self.WIDTH)
        self.vid_text_info.insert(INSERT, str(self.pl_str))
        self.vid_text_info.config(state=DISABLED)
        self.vid_text_info.pack()

        self.add_frame= Frame(self.master, bg='white')
        self.add_frame.place(relx=0, rely=0.85, relwidth=1, relheight=0.15)

        self.playstop_but = Button(self.add_frame, text="Start/Stop", bg='#070707', fg='#196619', command=self.toggle_pause_command)
        self.new_but = Button(self.add_frame, text="New", bg='#070707', fg='#196619', command=self.new_command)
        self.vol_up_but = Button(self.add_frame, text="Volume +", bg='#070707', fg='#196619',  command=self.vol_up_command) 
        self.vol_down_but = Button(self.add_frame, text="Volume -", bg='#070707', fg='#196619', command=self.vol_down_command)

        self.playstop_but.grid(row=0, column=1, ipadx=37)
        self.new_but.grid(row=0, column=2, ipadx=37)
        self.vol_up_but.grid(row=0, column=3, ipadx=37)
        self.vol_down_but.grid(row=0, column=4, ipadx=37)

    def update(self):
        self.new_frame = Frame(self.master, bg=self.default_C)
        self.new_frame.place(relx=0, rely=0, relwidth=1, relheight=0.8655)
        self.new_text_info = Text(self.new_frame, bg='#070707', bd=5, exportselection=0, fg='#196619', height=self.HEIGHT, width=self.WIDTH)
        self.new_text_info.insert(INSERT, str(self.pl_str))
        self.new_text_info.config(state=DISABLED)
        self.new_text_info.pack()

    def new_command(self):
        self.player.close_player()
        self.pick_tune()
        return self.update()

    def toggle_pause_command(self):
        return self.player.toggle_pause()

    def vol_down_command(self):
        return self.player.set_volume(self.player.get_volume() - 0.1)

    def vol_up_command(self):
        return self.player.set_volume(self.player.get_volume() + 0.1)

if __name__ == '__main__':
    root = Tk()
    root.title('JazzJam')
    root.iconbitmap('j_for_jazz.ico')
    initiater = GuiMain(root)
    root.resizable(False, False)
    root.mainloop()