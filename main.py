from os import times

import tkinter
from tkinter.constants import ANCHOR
from tkinter.font import BOLD, ITALIC
import cv2
import PIL.Image, PIL.ImageTk 
from functools import partial
import threading
import imutils
import time

stream = cv2.VideoCapture("clip.mp4")
flag = True
def play(speed):
    global flag
    print(f"Speed is : {speed}")
     
    #in reverse
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES,frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(120,25, fill="red",font="Times 20 italic bold",text="Decisoin Pending")
    flag = not flag


def pending(decision):
    #Display Pending
    frame = cv2.cvtColor(cv2.imread("pending1.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

    #Wait For 1 sec
    time.sleep(2)

    #Display Sponser
    frame = cv2.cvtColor(cv2.imread("sp1.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

    #Wait For 1 sec
    time.sleep(1)

    #OUT/NOT OUT
    if decision == 'Out':
        decisionImg ="out.jpg"
    else:
        decisionImg ="not_out.jpg"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)


def out():
    thread = threading.Thread(target=pending, args=("Out",))
    thread.daemon = 1
    thread.start()
    print("OUT!")

def not_out():
    thread = threading.Thread(target=pending, args=("Not Out",))
    thread.daemon = 1
    thread.start()
    print("NOT OUT!")

SET_WIDTH = 650
SET_HEIGHT = 368

window = tkinter.Tk()
window.title("Third Umpire Decision Review System.")
cv_img = cv2.cvtColor(cv2.imread("sp1.jpg"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0,0, ancho=tkinter.NW, image=photo)
canvas.pack()


btn = tkinter.Button(window, text="<< Previous (Fast)",width=50, command=partial (play,-25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (Slow)",width=50, command=partial (play,-2))
btn.pack()

btn = tkinter.Button(window, text=" Next (Slow) >>",width=50, command=partial (play,2))
btn.pack()

btn = tkinter.Button(window, text=" Next (Fast) >>",width=50, command=partial (play,40))
btn.pack()

btn = tkinter.Button(window, text=" Give OUT",width=50,command=out)
btn.pack()

btn = tkinter.Button(window, text=" Give NOT OUT",width=50,command=not_out)
btn.pack()
window.mainloop()