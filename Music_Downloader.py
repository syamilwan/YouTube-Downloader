from __future__ import unicode_literals
import youtube_dl
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
import subprocess
import threading

os.system("youtube-dl --rm-cache-dir")     
global directory
directory = "E:\Downloads\Musics"

def Start():
    global directory
    link=e1.get()
    print("## Starting ..")
    process.set("Starting..")
    x = threading.Thread(target= Download, args=(link,directory))
    x.start()

def Download(dlLink,directory):
    
    class MyLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)

    def my_hook(d):
        if d['status'] == 'finished':
            print('\n## Done downloading')
            process.set("Idle")
            s = done.get()
            done.set(s+"\n"+xx2)
            #test
    ydl_opts = {
        'merge_output_format': True,
        'format': 'bestaudio/best',
        'outtmpl': r"{}/{}.%(ext)s".format(directory, '%(title)s'),
        'ignoreerrors': True,
        'restrictfilenames':False,
        'forcefilename':True,
        'writethumbnail':True,
        'writesubtitles':True,
        'subtitleslangs':'en',
        'subtitlesformat':'srt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '140',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    global titl
    titl= '%(title)s'
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:    
        meta = ydl.extract_info(e1.get(), download = False)
        print('\n## Downloading ==>> ' + meta['title'])
        xx2 = ydl.prepare_filename(meta)
        process.set(meta['title'] + str(dlLink))
        ydl.download([dlLink])

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    global directory
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    directory = filename
    print('\n## ==>> Directory set to :' + filename)

def GetIPaddress():
    test = str.split(os.popen('arp -a').read())
    test2 = os.popen('arp -a').read()
    print(test)
    print(test2)

    def split(word): 
        return [char for char in word] 

    getMAC = []
    getIP = []
    c=0
    for i in test:
        y=0
        j = split(i)
        for x in j:
            if x == '-':
                y+=1
            if y==5:
                getMAC.insert(c,i)
                getIP.insert(c,test[c-1])
                break
        c+=1
    return getMAC,getIP

def send():
    test = []
    test = str.split(os.popen('adb devices').read())
    print(test)

win = tk.Tk()
folder_path = StringVar()
status = StringVar()
dlto = StringVar()
process = StringVar()
process.set("Idle")
done = StringVar()
phoneStatus = StringVar()
win.title("YouTube to Mp3")
frmMain = Frame(win)
folder_path.set("E:\Downloads\Musics")
lStatus = tk.Label(frmMain,textvariable=folder_path)
status.set("Enter Link : ")
lLink = tk.Label(frmMain,textvariable=status)
dlto.set("Download to : ")
lDload = tk.Label(frmMain,textvariable=dlto)
phoneStatus.set("Not Connected")
phoneS = tk.Label(frmMain,textvariable=phoneStatus)
dlFrame = Frame(frmMain)
lProcess = tk.Label(dlFrame,textvariable=process)
lFinish = tk.Label(dlFrame,textvariable=done)


## Entry
e1 = tk.Entry(frmMain)

## Buttons
bStart = ttk.Button(frmMain,text="Start", command = Start)
bEdit = tk.Button(frmMain,text="...", height = 0, width = 3, command = browse_button)
bSend = ttk.Button(frmMain,text="Send to Phone ", command = send)

w = ttk.Separator(frmMain)

## Main Window
lLink.grid(row=0,column=0,sticky="w")
e1.grid(row=0,column=1,sticky="ew")
bStart.grid(row=0,column=2)
lDload.grid(row=3,column=0,sticky="w")
lStatus.grid(row=3,column=1,sticky="w")
bEdit.grid(row=3,column=2)
frmMain.grid(row=0, column=0, sticky="NESW")
w.grid(row=4, columnspan=10,sticky="ew")
dlFrame.grid(row=5, column=0, sticky="NESW")
lProcess.grid(row=5, column=0)
lFinish.grid(row=6, column=0,sticky="ew")
phoneS.grid(row=7,column=1,sticky="es")
bSend.grid(row=7, column=2, sticky="es")


# Main Loop
#win.protocol('WM_DELETE_WINDOW', withdraw_window)  ## if window closes, move to tray instead of closing program
win.mainloop()
