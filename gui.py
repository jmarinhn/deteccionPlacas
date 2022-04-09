from tkinter import * 
import tkinter.font as tkFont
import os
def salir():
    window.destroy()
    
def iniciar():
    os.system("python3 deteccionPlacas.py --east frozen_east_text_detection.pb")
    

window = Tk()
window.title("Detector de Placas en Tiempo Real")

#setting window size
width=600
height=500
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
window.geometry(alignstr)
window.resizable(width=False, height=False)

titulo=Label(window)
ft = tkFont.Font(family='Arial',size=20)
titulo["font"] = ft
titulo["fg"] = "#ffffff"
titulo["justify"] = "center"
titulo["text"] = "Detector de Placas"
titulo.place(x=160,y=50,width=292,height=32)

subtitulo=Label(window)
ft = tkFont.Font(family='Arial',size=15)
subtitulo["font"] = ft
subtitulo["fg"] = "#ffffff"
subtitulo["justify"] = "center"
subtitulo["text"] = "Proyecto Final de TI-209"
subtitulo.place(x=160,y=80,width=292,height=32)

btn = Button(window,text="Iniciar deteccion",font=("Arial",12),background="gray",fg="black", command=iniciar,)
btn2 = Button(window,text="Salir",font=("Arial",12),background="red",fg="black",command=salir)

btn.place(x=230,y=180,width=144,height=30)
btn2.place(x=263,y=260,width=70,height=25)

integrantes = ('Grupo #1', 'Josue Marin', 'Jeffrey Herrera', 'Sergio Benitez')
integrantes_var = StringVar(value=integrantes)

listbox = Listbox(
    window,
    listvariable=integrantes_var,
    height=6,
    justify="center",
    selectmode='extended')

listbox.grid(
    column=0,
    row=0,
    sticky='nwes'
)

listbox.place(x=0,y=420,width=600,height=80)


window.mainloop()

