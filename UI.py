import cv2
from SudokuProcessing import *
from tkinter import *
from PIL import Image, ImageTk
import os
dir_path=r'sudokusolver/RecordedImages'
width, height = 600, 400
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def setSudokuvalue(startsize,sizex,sizey):
        print(startsize,sizex,sizey)
def image_selected(event):
    print(event)
def callback(sv):
    print(sv)

def showhomescreen(darkmode):

    # Create an instance of TKinter Window or frame
    root = Tk()
    root.title("Sodokusolver")
    root.configure(background="#222222")
    root.bind('<Escape>', lambda e: root.quit())
    
    #Webcam image
    lmain=Label()
    lmain.grid(row=2,column=2, padx='5', pady='5', sticky='ew')
    def show_frame():
        _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(1, show_frame)
    show_frame()
    #Record Button
    recordicon=Image.open("sudokusolver/UI Elements/cameraicon.png")
    recordicon=recordicon.resize((20,20))
    recordicon=ImageTk.PhotoImage(recordicon)

    recordbutton=Button(root,image=recordicon,command= lambda:imageprocessing(cap,root),borderwidth=0)
    recordbutton.grid(row=3,column=2, padx='5', pady='5', sticky='ew')
    
    #Solution Button
    solutionicon=Image.open("sudokusolver/UI Elements/solutionicon.png")
    solutionicon=solutionicon.resize((20,20))
    solutionicon=ImageTk.PhotoImage(solutionicon)
    solutionbutton=Label(root,image=solutionicon)
    solutionbutton.grid(row=4,column=2, padx='5', pady='5', sticky='ew')
    
    #SudokuGrid
    gridFrame=Frame(root)
    gridFrame.grid(row=5,column=2, padx='5', pady='5', sticky='ew')
    x=400
    sv = StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
    sudokurange=range(x,x+420,50)
    for a in sudokurange:
        for b in sudokurange:
            button=Entry(gridFrame,textvariable=sv)
            button.grid(row=a,column=b, padx='1', pady='2', sticky='ew')
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
            Filelist.insert(a,path)
            t=t+1
    Filelist.bind('<<ListboxSelect>>', image_selected)
    Filelist.grid(row=2,column=0, padx='5', pady='5', sticky='ew')

    root.mainloop()
showhomescreen(1)
