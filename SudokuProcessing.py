import cv2
import numpy as np
import time
import sys
import math
from array import *
import pytesseract
from PIL import Image
from SudokuSolver import *
from tkinter import *
from PIL import Image, ImageTk

def label_image(img,root):
    #label image
    lmain=Label()
    lmain.grid(row=2,column=2, padx='5', pady='5', sticky='ew')
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    time.sleep(1)

def get_contours(img):
    kernelcl = np.ones((2,2),np.uint8)

    contoursimage=cv2.morphologyEx(img, cv2.MORPH_DILATE, kernelcl)
    contours, _ = cv2.findContours(contoursimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    polygon = None
    #Selected contours
    for i in contours:
        area = cv2.contourArea(i)
        perimeter = cv2.arcLength(i, closed=True)
        approx = cv2.approxPolyDP(i, 0.01 * perimeter, closed=True)
        num_corners = len(approx)

        if num_corners == 4 and area > 1000:
            polygon = i
            break

    imgcont=cv2.drawContours(img, [polygon], 0, (0,0,0), 5)
    imgcont=cv2.cvtColor(imgcont, cv2.COLOR_BGR2GRAY)
    

def draw_corner(img):
    corners=cv2.goodFeaturesToTrack(img, maxCorners=4, qualityLevel=0.5, minDistance=150,useHarrisDetector=True,k=0.04)
    cornerpositions=[]
    #Check if 4 Corners are Selected

    #Sort cornerpositions

    x,y=corners[1].ravel()
    cornerpositions[0]=lefttop_pts=[np.uint16(x),np.uint16(y)]
    cv2.circle(img,lefttop_pts,5,(255,255,255),-1)
    x,y=corners[2].ravel()
    cornerpositions[1]=leftbottom_pts=[np.uint16(x),np.uint16(y)]
    cv2.circle(img,leftbottom_pts,5,(255,255,255),-1)
    x,y=corners[3].ravel()
    cornerpositions[2]=rightbottom_pts=[np.uint16(x),np.uint16(y)]
    cv2.circle(img,rightbottom_pts,5,(255,255,255),-1)
    x,y=corners[0].ravel()
    cornerpositions[3]=righttop_pts=[np.uint16(x),np.uint16(y)]
    cv2.circle(img,righttop_pts,5,(255,255,255),-1)
    
    return img,cornerpositions


def imagewarping(img,cornerposition):
    
    outputpts = np.array([[0, 0],[500, 500],[500, 0],[0, 500]],dtype=np.float32)

    PT=cv2.getPerspectiveTransform(cornerposition,outputpts)
    imgwarp=cv2.warpPerspective(img,PT,(500,500),flags=cv2.INTER_LINEAR)
    return imgwarp

def imagegrid(img):
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
            l = linesP[i][0]
            cv2.line(blank_image, (l[0], l[1]), (l[2], l[3]), (0,0,0), 3, cv2.LINE_AA)
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,0), 3, cv2.LINE_AA)
    return cdstP

def get(img):
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

def imagecontrast(img,inputalpha,inputbeta=1.1):
    img=cv2.normalize(img, None, alpha=inputalpha, beta=inputbeta, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    img= (255*img).astype(np.uint8)
    imggray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return imggray

def imageprocessing(cam,root):
    print("Imageprocessing")
    #Read Webcam Image
    _, frame = cam.read()
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #Preprocessing Image

    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (5,5), 1)
    img_thresh= cv2.adaptiveThreshold(img_blur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)

    
    
    
    
    
     