import cv2
import numpy as np
import time
from array import *
import pytesseract
from PIL import Image
from SudokuSolver import *
from scipy import spatial
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime

def setmatrix(root,sudokuarray):
    """Set Matrix of GUI
    :param root: Required TK Object for printing Sudokuarray
    :param sudokuarray: Required 9x9 Array
    """
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

def label_image(img,root):
    """Label image on GUI
    :param img: Required Image
    :param root: Required TK Object for printing img
    """
    if img!=[]:
        Imglbl=Label(root)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        img= cv2.resize(img,(720,480))
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        Imglbl.imgtk = imgtk
        Imglbl.configure(image=imgtk)
        Imglbl.grid(row=2,column=2, padx='5', pady='5', sticky='ew')
        time.sleep(2)

def get_contoursandcorner(origimg,img):
    """Name
    :param origimg:
    :param img:
    :return imgcont:
    :return resultarray:
    """
    kernelcl = np.ones((2,2),np.uint8)

    contoursimage=cv2.morphologyEx(img, cv2.MORPH_DILATE, kernelcl)
    contours, _ = cv2.findContours(contoursimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    corner = None
    #Selected contours
    for i in contours:
        area = cv2.contourArea(i)
        perimeter = cv2.arcLength(i, closed=True)
        approx = cv2.approxPolyDP(i, 0.01 * perimeter, closed=True)
        num_corners = len(approx)
        if num_corners == 4 and area > 1000:
            corner = i
            imgcont=cv2.drawContours(origimg, [corner], 0, (0,0,0), 6)
            for i in approx:
                imgcont=cv2.circle(imgcont,i[0], 3, (255,255,255), -1)
            #imgcont=cv2.cvtColor(imgcont, cv2.COLOR_BGR2GRAY)
            #Sort approx array
            resultarray=[[],[],[],[]]
            inputarray=[[approx[0][0][0],approx[0][0][1]],[approx[1][0][0],approx[1][0][1]],[approx[2][0][0],approx[2][0][1]],[approx[3][0][0],approx[3][0][1]]]
            imgsize=[[0,0],[origimg.shape[1],0],[0,origimg.shape[0]],[720,480]]
            tree=spatial.KDTree(inputarray)
            for x in range(0,4):
                _,result=tree.query(imgsize[x])
                resultarray[x]=inputarray[result]
                
            return imgcont,resultarray
            
    return [],[]


def imagewarping(img,cornerposition):
    """Warp Image Perspective
    :param img: Required Grayscale
    :param cornerposition: Required 2d array with four corner values [[lefttop],[leftbottom],[rightop],[rightbottom]]
    :return:
    """
    inputpts=np.array(cornerposition,dtype=np.float32)
    outputpts = np.array([[0, 0],[500, 0],[0, 500],[500, 500]],dtype=np.float32)

    PT=cv2.getPerspectiveTransform(inputpts,outputpts)
    imgwarp=cv2.warpPerspective(img,PT,(500,500),flags=cv2.INTER_LINEAR)
    return imgwarp

def imagegrid(img):
    """Subdivide Image into squares and convert image to number
    :param img: Required Grayscale Image
    :return: Grayscale Image
    """
    img_blur = cv2.GaussianBlur(img, (3,3), 1) 
    img_thresh= cv2.adaptiveThreshold(img_blur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15,4)

    kernelcl = np.ones((3,3),np.uint8)
    img_morph=cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernelcl)

    cdstP = cv2.cvtColor(img_morph, cv2.COLOR_GRAY2BGR)
    linesP = cv2.HoughLinesP(img_morph, 1, np.pi / 180, 50, None, 50, 10)
    #create new image
    blank_image = np.zeros((cdstP.shape[0],cdstP.shape[1],3), np.uint8)
    blank_image=255-blank_image
    if linesP is not None:
        for i in range(0, len(linesP)):
            #Grid wird nicht komplett ausgefüllt
            l = linesP[i][0]
            cv2.line(blank_image, (l[0], l[1]), (l[2], l[3]), (0,0,0), 3, cv2.LINE_AA)
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,0), 3, cv2.LINE_AA)
    return cdstP

def get_sudokugrid(img):
    """Image2Array
    :param img: Required Binaryimage with a 9x9 Sudokumatrix
    :return: Sudoku as array
    """
    sudoku_array=np.zeros((9,9))
    #unterteilen in quadrate
    höhe=img.shape[0]
    breite=img.shape[1]
    höhe_angepasst=np.uint16(höhe/9)
    breite_angepasst=np.uint16(breite/9)
    
    for h in range(0,9):
        linearray=np.zeros((9))
        for w in range(0,9):
            roi=img[höhe_angepasst*h:höhe_angepasst*(h+1),breite_angepasst*w:breite_angepasst*(w+1)]
            
            roi=cv2.resize(roi,(32,32),interpolation = cv2.INTER_AREA)
            #cv2.imshow('Test'+str(h)+str(w),roi)
            number=pytesseract.image_to_string(roi,config='--psm 6 -c tessedit_char_whitelist=0123456789')
            if number!='':
                linearray[w]=number[0]
            else:
                linearray[w]=0
        sudoku_array[h]=linearray
    return sudoku_array

def imagecontrast(img,inputalpha=0,inputbeta=1.1):
    """Change Imagecontract for more Contrast
    :param img: Required Grayimage
    :param inputalpha: <0 Lighter;>0 Darker
    :param inputbeta: <1 less Contrast;>1 less Contrast
    :return: customized image
    """
    img=cv2.normalize(img, None, alpha=inputalpha, beta=inputbeta, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    img= (255*img).astype(np.uint8)
    imggray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return imggray


def imageprocessing(img,root):
    """Main Process function for Image Process; Set Grid Matrix
    :param img: Image to process
    :param root: Need to show process on GUI
    """
    #Gray image
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("sudokusolver/RecordedImages/sudokuimage.png",img)
    #Preprocessing Image
    label_image(img_gray,root)
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (5,5), 1)
    img_thresh= cv2.adaptiveThreshold(img_blur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    img_contours,corner=get_contoursandcorner(img_gray,img_thresh)
    label_image(img_contours,root)

    img_roi=imagewarping(img_contours,corner)
    label_image(img_roi,root)

    img_grid=imagegrid(img_roi)
    img_grid=imagecontrast(img_grid)
    label_image(img_grid,root)

    sudokuarray=get_sudokugrid(img_grid)
    setmatrix(root,sudokuarray)



    
    
    
    
    
     