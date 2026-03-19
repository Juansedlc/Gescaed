import tkinter as tk
from tkinter import filedialog as fd 
import customtkinter as ct
from PIL import Image , ImageTk
import pandas as pd
import utlis
import OMR_Main
import reader

ct.set_appearance_mode("dark")
ct.set_default_color_theme("green")
root = ct.CTk()
root.geometry("400x400")
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.wm_title("Calificator 3000")
texto = "a"
respuestas= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1]
resname = "libro1"
pathimage = ""
def callback():
    global pathimage
    global nombreqr
    pathimage = fd.askopenfilename()
    #LabelPrincipal.configure(Image=converted_image)
    photo2 = Image.open(pathimage)
    reshaped2 = photo2.rotate(270)
    resized2 = reshaped2.resize((600,600))
    converted_image2 = ImageTk.PhotoImage(resized2)
    LabelPrincipal.configure(image=converted_image2)
    LabelPrincipal.pack_forget()    
    LabelPrincipal.pack(pady= 30, padx = 20)
    nombreqr = reader.reader(pathimage)
    cajatexto.insert(index = ct.END,text = nombreqr)
    
def tomar_respuestas():
    filex= fd.askopenfilename()
    xls = pd.ExcelFile(filex)
    print(NombreRes.get())
    if NombreRes.get() == "":
        df = pd.read_excel(xls,sheet_name="Sheet")
    if NombreRes.get() != "":
        df = pd.read_excel(xls,sheet_name=NombreRes.get())
    ans = df['respuestas'].values.tolist()
    counter = 0
    global respuestas
    respuestas = []
    while(counter < len(ans)):
        respuestas.append(ans[counter])
        counter = counter + 1
    respuestas = utlis.ansTuple(respuestas, combobox.get()) 
    
def calificar():
    respuestas2 = utlis.the120inator(respuestas)
    global grade
    grade, img = OMR_Main.califier(pathimage, respuestas2)
    grade = utlis.the120ans(combobox.get(),grade)
    cajatexto.insert(index = ct.END,text = grade)
    img2 =  ImageTk.PhotoImage(image=Image.fromarray(img))
    LabelPrincipal.configure(image=img2)
    LabelPrincipal.pack_forget()    
    LabelPrincipal.pack(pady= 30, padx = 20)

def copiar():
    grades = utlis.copyfun(grade)
    if NombreEs.get() != "":
        grades = NombreEs.get()+"\t"+grades
    if NombreEs.get() == "":
        grades = nombreqr+"\t"+grades
    utlis.copy(grades)

errmsg = 'Error!'

frame = ct.CTkFrame(master = root, width=600, height=600)
frame.pack(pady = 20,padx=20,fill=ct.Y, side=ct.LEFT,  expand = True)

frame2 = ct.CTkFrame(master = root, width=600, height=600)
frame2.pack(pady = 20,padx=20,fill=ct.Y, side = ct.RIGHT, expand = True)

frame3   = ct.CTkFrame(master = frame, width = 400, height = 150)
frame3.pack(pady = 0,padx=0,fill=ct.Y, side = ct.TOP, expand = True)

frame4   = ct.CTkFrame(master = frame, width = 400, height = 150)
frame4.pack(pady = 0,padx=0,fill=ct.Y, side = ct.TOP, expand = True)

NombreEs = ct.CTkEntry(master = frame3, placeholder_text="Nombre Estudiante")
NombreEs.pack(pady = 20,padx = 25, side = ct.RIGHT)

NombreRes = ct.CTkEntry(master = frame4, placeholder_text="Nombre hoja res")
NombreRes.pack(pady = 20,padx = 20, side = ct.RIGHT)

ans = ["120","110","102","100", "95","90","80", "79","60","50","56","70","30","40"]
combobox = ct.CTkComboBox(master = frame3, values=ans, state="normal", corner_radius=5)
combobox.pack(pady = 20,padx = 20 ,   side = ct.LEFT)

Openbutton = ct.CTkButton(master = frame, text = "Abrir archivo" , command = callback, width = 140, height=40 )
Openbutton.pack(pady = 10,padx = 20)

RespuestasButton = ct.CTkButton(master = frame4, text = "Seleccionar Respuestas" , command = tomar_respuestas, width = 140, height=40 )
RespuestasButton.pack(pady = 20,padx = 20)

CalificarButton = ct.CTkButton(master = frame, text = "Calificar Prueba" , command = calificar, width = 140, height=40 )
CalificarButton.pack(pady = 10,padx = 20)

cajatexto = ct.CTkTextbox(master = frame,width= 400, height=250,)
cajatexto.pack(pady = 20)

photo = Image.open("copy.png")
reshaped = photo.rotate(270)
resized = photo.resize((20,20))


converted_image = ImageTk.PhotoImage(resized)
CopyButton = ct.CTkButton(master = frame, image=converted_image , text = "Copiar" ,command = copiar, width = 190, height=40 )
CopyButton.pack(pady = 20)

photo2 = Image.open("prueba 3.jpg")
reshaped2 = photo2.rotate(270)
resized2 = reshaped2.resize((600,600))
converted_image2 = ImageTk.PhotoImage(resized2)
LabelPrincipal = ct.CTkLabel(master = frame2, image=converted_image2)
LabelPrincipal.pack(pady= 30, padx = 20)
root.mainloop()