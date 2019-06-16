"""
Just having some fun in Python.
//christianlindeneg, June, 2019//

Thanks for jams & music:
https://studiojams.com/
"""
from tkinter import Tk, Canvas, Frame, Button, Text, mainloop, INSERT, DISABLED, BOTTOM
from json import load, loads
from random import randint
from time import sleep
from zipfile import ZipFile
from os import remove, system

try:
    from ffpyplayer.player import MediaPlayer
    from pafy import new
    from vlc import Instance
    from google_drive_downloader import GoogleDriveDownloader as gdd
except ImportError:
    system('python -m pip install -r requirements.txt')

class Start:
    def __init__(self, master):
        self.master = master
        self.HEIGHT = 150
        self.WIDTH = 500
        self.default_C = '#060606'
        self.read()

    def read(self):
        try:
            with open('m/music.json') as music:
                r_music = load(music)
                self.str_music = loads(r_music)
                self.pick_tune()
        except FileNotFoundError:
            try:
                with ZipFile("m.zip","r") as zip_ref:
                    zip_ref.extractall()

                remove("m.zip")
                with open('m/music.json') as music:
                    r_music = load(music)
                    self.str_music = loads(r_music)
                    self.pick_tune()

            except FileNotFoundError:
                self.temp_ui()
                try:
                    if input() == None: # if this is not here, the temp_ui wont show for some reason
                        exit()
                    else:
                        exit()
                except AttributeError:
                    print('\nSomething went wrong..')
                    exit()

    def downloader(self):
        gdd.download_file_from_google_drive(file_id='1n5o3FiGzPdHSfM6JDBN8IqCXxb8JaVET', dest_path='./m.zip')
        with ZipFile("m.zip","r") as zip_ref:
            zip_ref.extractall()
        remove("m.zip")
        
        with open('m/music.json') as music:
            r_music = load(music)
            self.str_music = loads(r_music)
        
        sleep(0.5)
        self.temp_frame2.destroy()
        self.text_info2.destroy()
        self.temp_frame.destroy()
        self.text_info.destroy()
        self.canvas.destroy()
        self.temp_main_frame.destroy()
        sleep(0.5)
        self.pick_tune()
        self.maingui()

    def ranint(self, length):
        return randint(0, length-1)

    def pick_tune(self):
        self.music = self.str_music['music']
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
        super().__init__(master)

    def maingui(self):
        self.canvas = Canvas(self.master, bg=self.default_C, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()
        # Generate Frame
        self.main_frame = Frame(self.master, bg=self.default_C)
        self.main_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

        self.vid_frame = Frame(self.master, bg=self.default_C)
        self.vid_frame.place(relx=0, rely=0, relwidth=1, relheight=0.872)
        self.vid_text_info = Text(self.vid_frame, bg='#070707', bd=5, exportselection=0, fg='#196619', height=self.HEIGHT, width=self.WIDTH)
        try:       
            self.vid_text_info.insert(INSERT, str(self.pl_str))
        except AttributeError:
            self.vid_text_info.insert(INSERT, '\nError reading name of tune.\n\nTry clicking "New"..')
        self.vid_text_info.config(state=DISABLED)
        self.vid_text_info.pack()

        self.add_frame= Frame(self.master)
        self.add_frame.place(relx=0, rely=0.85, relwidth=1, relheight=0.15)

        self.playstop_but = Button(self.add_frame, text="Start/Stop", bg='#070707', fg='#196619', command=self.toggle_pause_command)
        self.new_but = Button(self.add_frame, text="New", bg='#070707', fg='#196619', command=self.new_command)
        self.vol_up_but = Button(self.add_frame, text="Volume +", bg='#070707', fg='#196619',  command=self.vol_up_command) 
        self.vol_down_but = Button(self.add_frame, text="Volume -", bg='#070707', fg='#196619', command=self.vol_down_command)
        self.exit_but = Button(self.add_frame, text="Quit", bg='#070707', fg='#196619', command=self.temp_abort)

        self.playstop_but.grid(row=0, column=1, ipadx=25)
        self.new_but.grid(row=0, column=2, ipadx=25)
        self.vol_up_but.grid(row=0, column=3, ipadx=25)
        self.vol_down_but.grid(row=0, column=4, ipadx=25)
        self.exit_but.grid(row=0, column=5, ipadx=25)

    def update(self):
        self.new_frame = Frame(self.master, bg=self.default_C)
        self.new_frame.place(relx=0, rely=0, relwidth=1, relheight=0.8655)
        self.new_text_info = Text(self.new_frame, bg='#070707', bd=5, exportselection=0, fg='#196619', height=self.HEIGHT, width=self.WIDTH)
        self.new_text_info.insert(INSERT, str(self.pl_str))
        self.new_text_info.config(state=DISABLED)
        self.new_text_info.pack()

    def temp_ui(self):
        self.canvas = Canvas(self.master, bg=self.default_C, height=150, width=350)
        self.canvas.pack()
        # Generate Frame
        self.temp_main_frame = Frame(self.master, bg=self.default_C)
        self.temp_main_frame.place(relx=1, rely=1, relwidth=1, relheight=1)

        self.temp_frame = Frame(self.master, bg=self.default_C)
        self.temp_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.text_info = Text(self.temp_frame, bg='#070707', bd=5, exportselection=0, fg='#196619', height=self.HEIGHT, width=self.WIDTH)
        self.text_info.insert(INSERT, '\nYou need local files to start.\n\nContinue with download of ~200MB?\n\n(alternatively, use online-version)')
        self.text_info.config(state=DISABLED)
        self.text_info.pack()

        add_t_frame= Frame(self.master)
        add_t_frame.place(relx=0, rely=0.85, relwidth=1, relheight=0.15)
        
        self.choice_yes = Button(add_t_frame, text="Download", bg='#373737', fg='#196619', command=self.temp_con)
        self.choice_no = Button(add_t_frame, text="Abort", bg='#373737', fg='#196619', command=self.temp_abort)

        self.choice_yes.grid(row=0, column=1, ipadx=64)
        self.choice_no.grid(row=0, column=2, ipadx=64)

    def temp_con(self):
        self.choice_yes.destroy()
        self.choice_no.destroy()
        self.temp_frame2 = Frame(self.master, bg=self.default_C)
        self.temp_frame2.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.text_info2 = Text(self.temp_frame2, bg='#070707', bd=5, exportselection=0, fg='#196619', height=self.HEIGHT, width=self.WIDTH)
        self.text_info2.insert(INSERT, '\nDownloading ZIP. ~200MB.\n\nPlease Wait.\n\nIt can take a few minutes..')
        self.text_info2.config(state=DISABLED)
        self.text_info2.pack()
        self.text_info2.update()

        sleep(0.5)
        self.downloader()

    def temp_abort(self):
        return exit()

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
    root.resizable(False, False)
    initiater = GuiMain(root)
    initiater.maingui()
    root.mainloop()