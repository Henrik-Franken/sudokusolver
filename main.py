import cv2
import numpy as np
from SudokuProcessing import *
from SudokuSolver import *
from tkinter import *
from PIL import Image, ImageTk
import os
import threading
Filelist=0
rows=0
sudokuarray=np.ones((9,9),dtype=str)
root=0
live=True
listimage=[]
dir_path=r'sudokusolver/RecordedImages'
width, height = 600, 400
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
pytesseract.pytesseract.tesseract_cmd=r'C:\Users\Frank\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'



def solvesudoku():
    """Solve Sudoku of GUI Matrix"""
    global sudokuarray
    sudokuarray=sudokuarray.astype('float32')
    getmatrix()
    try:
        result=solve_sudoku(sudokuarray)
        sudokuarray=result
        setmatrix()
    except:
        Imglbl=Label(root,text="The Sodoku can not be recognized. Please try again")
        Imglbl.grid(row=4,column=2, padx='5', pady='5', sticky='ew')
        time.sleep(3)
        #Old
    

def imageprocess():
    """Start Imageprocess in a new Thread for no freezing GUI"""
    global live
    global sudokuarray
    global listimage
    live=False
    img=0
    if not len(listimage):
        _, img = cap.read()
    else:
        img=listimage
        try:
            result=threading.Thread(target=imageprocessing,args=(img,root))
            result.start()
    
        except:
            Imglbl=Label(root,text="The Sodoku can not be recognized. Please try again")
            Imglbl.grid(row=4,column=2, padx='5', pady='5', sticky='ew')
            time.sleep(1)
            live=True
    
def setmatrix():
    """Set Gridmatrix of GUI by using GUI Variable root"""
    global sudokuarray

    entry='!entry'
    t=1
    for x in sudokuarray:
        for y in x:
            if t==1:
                entrytmp=entry
            else:
                entrytmp=entry+str(t)
            root.children['!frame'].children[entrytmp].delete(0,END)
            root.children['!frame'].children[entrytmp].insert(0,int(y))
            t=t+1

def getmatrix():
    """Get Gridmatrix of GUI by using Sudokumatrix Variable rows"""
    global sudokuarray
    global rows
    global dir_path
    entry='!entry'
    for x in range(0,9):
        for y in range(0,9):
            sudokuarray[x][y]=int(rows[x][y].get())
    


def image_selected(event):
    """Override Webcamimage with selected image of Listbox
    :param event: not used because of no information
    """
    global Filelist
    global live
    global listimage
    live=False
    if Filelist.curselection()!=():
        filename=Filelist.get(Filelist.curselection()[0])
        path=dir_path+'/'+filename
        img=cv2.imread(path,0)
        wbimage=Label(root)
        wbimage.grid(row=2,column=2, padx='5', pady='5', sticky='ew')
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        cv2image= cv2.resize(cv2image,(720,480))
        listimage=cv2image
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        wbimage.imgtk = imgtk
        wbimage.configure(image=imgtk)


def showhomescreen():
    """Main-Function for Creating Grid an initiale Global Variables"""
    global Filelist
    global rows
    global sudokuarray
    global root
    global live
    live=True
    # Create an instance of TKinter Window or frame
    root = Tk()
    root.title("Sodokusolver")
    #root.configure(background="#222222")
    root.bind('<Escape>', lambda e: root.quit())
    root.focus()
    
    #Webcam image
    wbimage=Label(root)
    wbimage.grid(row=2,column=2, padx='5', pady='5', sticky='ew')
    def show_frame():
        if live:
            _, frame = cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            cv2image= cv2.resize(cv2image,(720,480))
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            wbimage.imgtk = imgtk
            wbimage.configure(image=imgtk)
            wbimage.after(1, show_frame)
    show_frame()
    #Record Button
    recordicon=Image.open("sudokusolver/UI Elements/cameraicon.png")
    recordicon=recordicon.resize((20,20))
    recordicon=ImageTk.PhotoImage(recordicon)

    recordbutton=Button(root,image=recordicon,command= imageprocess,borderwidth=0)
    recordbutton.grid(row=3,column=2, padx='5', pady='5', sticky='ew')
    
    #Solution Button
    solutionicon=Image.open("sudokusolver/UI Elements/solutionicon.png")
    solutionicon=solutionicon.resize((20,20))
    solutionicon=ImageTk.PhotoImage(solutionicon)
    solutionbutton=Button(root,image=solutionicon,command=solvesudoku)
    solutionbutton.grid(row=4,column=2, padx='5', pady='5', sticky='ew')
    
    #SudokuGrid
    gridFrame=Frame(root)
    gridFrame.grid(row=5,column=2, padx='5', pady='5', sticky='ew')
    
    rows = []
    for i in range(9):
        cols = []
        for j in range(9):
            e = Entry(gridFrame,width=5,bd=7,)
            e.grid(row=i, column=j, sticky=NSEW)
            cols.append(e)
        rows.append(cols)

    #Welcome Label
    welcomelbl=Label(text="Welcome")
    welcomelbl2=Label(text="Please show your Sudoku and take a picture")
    welcomelbl.grid(row=0,column=2, padx='5', pady='5', sticky='ew')
    welcomelbl2.grid(row=1,column=2, padx='5', pady='5', sticky='ew')
    
    #Program Icon
    frame=Frame(root)
    frame.grid(row=0,column=0, padx='5', pady='5', sticky='ew')
    programicon=ImageTk.PhotoImage(Image.open("sudokusolver/UI Elements/sudokuicon.png").resize((30,30)))
    programiconlbl=Label(root,image=programicon)
    programiconlbl.grid(row=0,column=0, padx='5', pady='5', sticky='ew')
    
    #Programm Label
    programlbl=Label(text="Sudokusolver")
    programlbl.grid(row=0,column=1, padx='5', pady='5', sticky='ew')
    
    #List Record
    recordlistlbl=Label(text="Already recorded")
    recordlistlbl.grid(row=1,column=0, padx='5', pady='5', sticky='ew')
    #List Files
    Filelist=Listbox(root)
    t=0
    for path in os.listdir(dir_path):
    # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            Filelist.insert(0,path)
            t=t+1
    Filelist.bind('<<ListboxSelect>>', image_selected)
    Filelist.grid(row=2,column=0, padx='5', pady='5', sticky='ew')

    root.mainloop()
showhomescreen()
