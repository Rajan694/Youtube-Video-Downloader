from io import BytesIO
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from urllib.request import urlopen
from PIL import Image, ImageTk
from pytube import YouTube
import os
import sys


def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


root = Tk()
root.geometry("610x500")
root.resizable(False, False)
root.title("Yt Video Downloader")
raj=resource_path("yt.ico")
root.iconbitmap(raj)
root.configure(bg="#000")

ans = ""
raj1=resource_path("yt.jpg")
photo = Image.open(raj1)
photo.resize((122, 33))
heading = ImageTk.PhotoImage(photo)
audio = False
video = False
click = ""


def sele():
    global ans
    pa = filedialog.askdirectory()
    ans += pa
    pathn.config(text=ans)
    btn2.grid(row=3, column=1)
    btn3.grid(row=3, column=2)


def vid():
    global click
    click = "Get Video"
    getn()


def aud():
    global click
    click = "Get Audio"
    getn()


def getn():
    global audio, video, clicked, dropdown, yt, click, image1
    clicked = StringVar()
    yt = YouTube(linkn.get())
    title.config(text=f"{yt.title[:30]}...")
    channel.config(text=f"{yt.author}")
    view.config(text="{:,}".format(yt.views))
    Length = yt.length
    if Length > 60 and Length < 3600:
        minute = Length // 60
        second = Length % 60
        length.config(text=f"{minute} minutes {second} seconds")
    elif Length >= 3600:
        hour = (Length // 60) // 60
        minute = (Length // 60) % 60
        second = Length % 60
        length.config(text=f"{hour} hour {minute} minutes {second} seconds")
    elif Length < 60:
        length.config(text=f"{Length} seconds")
    u = urlopen(yt.thumbnail_url).read()
    im = Image.open(BytesIO(u))
    resize = im.resize((150, 150))
    image1 = ImageTk.PhotoImage(resize)
    img = Label(root, image=image1)

    if click == "Get Video":
        video = True
        audio = False

        resolution = [stream.resolution for stream in yt.streams.filter(mime_type="video/mp4", progressive=True)]
        clicked.set("Select Resolution")
        dropdown = OptionMenu(root, clicked, *resolution)
        dropdown.grid(row=9, column=1)
        format.config(text="Video(mp4)")

    if click == "Get Audio":
        try:
            dropdown.grid_forget()
        except Exception as e:
            pass
        audio = True
        video = False
        format.config(text="Audio(mp3)")

    titl.grid(row=4, column=0, sticky="e")
    lengt.grid(row=6, column=0, sticky="e")
    channe.grid(row=5, column=0, sticky="e")
    vie.grid(row=7, column=0, sticky="e")
    forma.grid(row=8, column=0, sticky="e")
    title.grid(row=4, column=1, sticky="w", columnspan=2)
    length.grid(row=6, column=1, sticky="w")
    channel.grid(row=5, column=1, sticky="w", columnspan=2)
    view.grid(row=7, column=1, sticky="w")
    img.grid(row=5, column=2, rowspan=4, sticky="w")
    format.grid(row=8, column=1, sticky="w")
    down.grid(row=10, column=1)


def download():
    global video, audio, ans, yt, dropdown, clicked
    tit = yt.title[:20]
    if video == True:
        try:
            file = yt.streams.filter(res=clicked.get()).first()
            size = file.filesize
            a = messagebox.askyesno("Do You Want To Download", f"File Size: {round(size * 0.000001, 2)} MegaBytes")
            if a == True:
                dowtext.grid(row=10, column=0)
                file.download(filename=tit + ".mp4", output_path=ans)

                messagebox.showinfo("Alert!!!", "Done!!!")
                dowtext.grid_forget()
            if a == False:
                dropdown.grid(row=9, column=1)

        except Exception as e:
            dropdown.grid(row=9, column=1)
            messagebox.showerror("Error", "Error Raised Due To!\n>UnSelected Resolution  \n>Your Internet Connectivity")

    if audio == True:
        try:
            file = yt.streams.filter(only_audio=True).first()
            size = file.filesize
            get = messagebox.askyesno("Do You Want To Download", f"File Size: {round(size * 0.000001, 2)} MegaBytes")

            if get == True:
                dowtext.grid(row=10, column=0)
                file.download(filename=tit + ".mp3", output_path=ans)

                messagebox.showinfo("Download", "Done!!!")
                dowtext.grid_forget()
            
            if get == False:
                messagebox.showinfo("Download it", "Choose one")

        except Exception as e:
            messagebox.showerror("Error ", "Error Raised Due To!\n\n>Your Internet Connectivity")


head = Label(root, image=heading).grid(row=0, column=0)

link = Label(root, text="Enter download link :-", bg="#000", fg="orange", pady="10", font=('Georgia bold', 12)).grid(
    row=1, column=0, sticky="w")
linkn = Entry(root, width=40, font=('Arial', 12))
linkn.grid(row=1, column=1, columnspan=2, sticky="w")

path = Label(root, text="Select Path For Download :-", pady="10", bg="#000", fg="orange",
             font=('Georgia bold', 12)).grid(row=2, column=0, sticky="w")
pathn = Label(root, text="", bg="#000", fg="white", pady="10", font=("Arial bold", 12))
pathn.grid(row=2, column=1, columnspan=2, sticky="w")

btn1 = Button(root, text="Select Path", bg='Grey', font=('Tahoma bold', 12), fg='#fff', command=sele)
btn1.grid(row=3, column=0)
btn2 = Button(root, text="Get Audio", bg='Grey', font=('Tahoma bold', 12), fg='#fff', command=aud)
btn3 = Button(root, text="Get Video", bg='Grey', font=('Tahoma bold', 12), fg='#fff', command=vid)

titl = Label(root, text="Title :-", bg="#000", fg="yellow", pady="10", font=("Arial bold", 12))
title = Label(root, text="", bg="#000", fg="white", pady="10", font=("Arial bold", 12))

lengt = Label(root, text="Length :-", bg="#000", fg="yellow", pady="10", font=("Arial bold", 12))
length = Label(root, text="", bg="#000", fg="white", pady="10", font=("Arial bold", 12))

channe = Label(root, text="Channel :-", bg="#000", fg="yellow", pady="10", font=("Arial bold", 12))
channel = Label(root, text="", bg="#000", fg="white", pady="10", font=("Arial bold", 12))

vie = Label(root, text="Views :-", bg="#000", fg="yellow", pady="10", font=("Arial bold", 12))
view = Label(root, text="", bg="#000", fg="white", pady="10", font=("Arial bold", 12))

forma = Label(root, text="File :-", bg="#000", fg="yellow", pady="10", font=("Arial bold", 12))
format = Label(root, text="", bg="#000", fg="white", pady="10", font=("Arial Bold", 12))

down = Button(root, text="Download", bg="red", font=('Arial bold', 12), command=download)
dowtext= Label(root, text="Downloading...", bg="#000", fg="white", font=("Arial Bold", 12))

root.mainloop()
