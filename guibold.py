import tkinter as tk
from tkinter import filedialog as fd 
import customtkinter as ct
from PIL import Image , ImageTk
import pandas as pd
import wordrbold 
ct.set_appearance_mode("dark")
ct.set_default_color_theme("green")
root = ct.CTk()
root.geometry("400x400")
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.wm_title("qrbuilder")

def callback():
    filex= fd.askopenfilename()
    data = wordrbold.reader(filex)
    wordrbold.writerbold(data,"demo")

errmsg = 'Error!'

frame = ct.CTkFrame(master = root, width=600, height=600)
frame.pack(pady = 20,padx=20,fill=ct.Y, side=ct.LEFT,  expand = True)

Openbutton = ct.CTkButton(master = frame, text = "Abrir archivo" , command = callback, width = 140, height=40 )
Openbutton.pack(pady = 10,padx = 20)

cajatexto = ct.CTkTextbox(master = frame,width= 400, height=250,)
cajatexto.pack(pady = 20)

root.mainloop()