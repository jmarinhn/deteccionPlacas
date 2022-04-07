from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils

def salir():
    window.destroy()
    

def iniciar():
    global cap
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    visualizar()

def limpiar():
    labelvideo.image = ""
    lblvacio.configure(text="")
    cap.release()

def visualizar():
    global cap
    ret, frame = cap.read()
    if ret == True:
        frame = imutils.resize(frame,width=640)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(im)
        labelvideo.configure(image=img)
        labelvideo.image = img
        labelvideo.after(10,visualizar)
    else:
        labelvideo.image = ""
        lblvacio.configure(text="")
        cap.release()

cap = None
window = Tk()
window.title("REAL-TIME OCR")
titulo = Label(window, text="REAL-TIME OCR",font=("Arial",24))
titulo.grid(column=0,row=0,columnspan=1)
btn = Button(window,text="START",font=("Arial",12),background="gray",fg="white", command=iniciar)
btn2 = Button(window,text="STOP",font=("Arial",12),background="orange",fg="white", command=limpiar)
btn3 = Button(window,text="EXIT",font=("Arial",12),background="red",fg="white",command=salir)
labelvideo = Label(window)
labelvideo.grid(column=0,row=1,columnspan=2,pady=10)
btn.grid(column=0,row=2)
btn2.grid(column=1,row=2)
btn3.grid(column=2,row=2)
lblvacio = Label(window,text="",width=20)
lblvacio.grid(column=4,row=0)
window.mainloop()