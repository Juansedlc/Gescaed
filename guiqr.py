import tkinter as tk
from tkinter import filedialog as fd 
import customtkinter as ct
from PIL import Image , ImageTk
import pandas as pd
import utlis
import qr
ct.set_appearance_mode("dark")
ct.set_default_color_theme("green")
root = ct.CTk()
root.geometry("400x400")
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.wm_title("qrbuilder")

def callback():
    filex= fd.askopenfilename()
    xls = pd.ExcelFile(filex)
    #filename = filex.split("/")
    #filename = filename[-1]
    #filename = filename.split(".")
    #filename = filename[0]
    df = pd.read_excel(xls,sheet_name="Sheet1")
    fap = df['estu'].values.tolist()
    #sap = df['Segundo Apellido'].values.tolist()
    #fn = df['Primer Nombre'].values.tolist()
    #sn = df['Segundo Nombre'].values.tolist()
    #grado = df['Grado'].values.tolist()
    #curso = df['Grupo'].values.tolist()
    #doc = df['Numero Identificacion'].values.tolist()
    i=0
    data = []
    for x in fap:
       # if str(sn[i]) == "null":
       #     sn[i] = ""
       # if str(doc[i]) == "nan":
       #     doc[i] = "DOCUMENTO FALTANTE"
        data.append(fap[i])#+" "+sap[i]+" "+fn[i]+" "+str(sn[i]))
        i=i+1
    print(data)
    i=0
    a=0
    for x in fap:
        #qr.qrcreator(data[i],grado[i]+curso[i]+"00"+str(i))
        qr.qrcreator(data[i],"00"+str(i))
        i=i+1
        #if grado[i+1] == grado[i] and curso[i+1] == curso[i]:
        #    a= a+1
        #else:
        #    a=0


errmsg = 'Error!'

frame = ct.CTkFrame(master = root, width=600, height=600)
frame.pack(pady = 20,padx=20,fill=ct.Y, side=ct.LEFT,  expand = True)

Openbutton = ct.CTkButton(master = frame, text = "Abrir archivo" , command = callback, width = 140, height=40 )
Openbutton.pack(pady = 10,padx = 20)

cajatexto = ct.CTkTextbox(master = frame,width= 400, height=250,)
cajatexto.pack(pady = 20)

root.mainloop()