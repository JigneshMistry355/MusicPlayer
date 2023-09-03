import os
import pickle
import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer
from playsound import playsound
from tkinter import Scale
from mutagen.mp3 import MP3
import time


class Player(tk.Tk):
    def __init__(self):
        super().__init__()

        mixer.init()
        self.title("Music Player")
        self.geometry("600x300")

        # Menu
        self.createMenu()

        self.label = ttk.Label(self, text='List',font=('gabriola', 25))
        self.label.pack()

        self.createButton()
        self.create_listbox()

        self.progress_bar = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='determinate'
        )
        self.progress_bar.pack(side=tk.BOTTOM, fill='x', padx=10, pady=5)
        self.playBackPaused = False

        self.updateProgressBar()

    def updateProgressBar(self):
        if mixer.music.get_busy():
            self.currentPosition = mixer.music.get_pos()/1000
            self.songLength = self.getSongLength(self.currentMusic)
            self.progressPercentage = (self.currentPosition/self.songLength) * 100
            self.progress_bar['value'] = self.progressPercentage
            self.after(1000, self.updateProgressBar)

    def getSongLength(self, music_path):
        self.audio = MP3(music_path)
        return self.audio.info.length

    def togglePlayPause(self):
        if not self.playBackPaused:
            self.playMusic()
            self.playBackPaused = True
        else:
            self.resumeMusic()
            self.playBackPaused = False
    def playMusic(self):
        self.currentMusic = self.listbox.get(tk.ACTIVE)
        mixer.music.load(self.currentMusic)
        mixer.music.play()
        self.playButton.configure(image=self.pauseImage, command=self.pauseMusic)

    def pauseMusic(self):
        mixer.music.pause()
        self.playButton.configure(image=self.playImage, command=self.resumeMusic)

    def resumeMusic(self):
        mixer.music.unpause()
        self.playButton.configure(image=self.pauseImage, command=self.pauseMusic)

    def playSelectedSong(self, event):
        self.currentMusic = self.listbox.get(tk.ACTIVE)
        self.playMusic()

    def create_listbox(self):
        self.listbox = tk.Listbox(
            self,
            height=10,
            width=150,
            justify='left',
            font=('gabriola', 15),
            bd=0
        )
        self.listbox.pack(side='top', fill=tkinter.BOTH, padx=10)
        self.listbox.bind('<<ListboxSelect>>', self.playSelectedSong)

    def createMenu(self):
        self.myMenu = tk.Menu(self)
        self.config(menu=self.myMenu)
        self.addSongs = tk.Menu(self.myMenu, tearoff=0) # tearoff removes dotted lines in menu
        self.myMenu.add_cascade(label='Menu', menu=self.addSongs)
        self.addSongs.add_command(label='Add Songs', command=self.addsongs)

    def addsongs(self):
        self.path = filedialog.askdirectory()
        if self.path:
            os.chdir(self.path)
            self.songs = os.listdir(self.path)

            for song in self.songs:
                if song.endswith('.mp3'):
                    self.listbox.insert(tk.END, song)

    def createButton(self):
        self.newPauseImage = PhotoImage(file='black pause.png')
        self.pauseImage = self.newPauseImage.subsample(10, 10)
        self.newPlayImage = PhotoImage(file='black play.png')
        self.playImage = self.newPlayImage.subsample(10, 10)
        self.playButton = tk.Button(
            self,
            image=self.playImage,
            command=self.togglePlayPause,
            bd=0
        )
        self.playButton.pack(side=tk.BOTTOM, pady=10)


pl = Player()
pl.mainloop()

