import cv2
import numpy as np
import time
import sys
import math
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd=r'C:\Users\Frank\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
img=cv2.imread("opencv_frame_0.png")
x=0
#Preprocess
while True:

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (5,5), 1) 
    img_thresh= cv2.adaptiveThreshold(img_blur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    imginvert=255-img_thresh

    kernelcl = np.ones((2,2),np.uint8)

    contoursimage=cv2.morphologyEx(imginvert, cv2.MORPH_DILATE, kernelcl)

    contours, hierarchy = cv2.findContours(contoursimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

    imgcont=cv2.drawContours(img, [polygon], 0, (0,255,255), 3)

    imgcont=cv2.cvtColor(imgcont, cv2.COLOR_BGR2GRAY)
    corners=cv2.goodFeaturesToTrack(imgcont, maxCorners=4, qualityLevel=0.5, minDistance=150)

    x,y=corners[0].ravel()
    lefttop_pts=[np.uint16(x),np.uint16(y)]
    cv2.circle(imgcont,lefttop_pts,5,(0,0,0),-1)
    x,y=corners[1].ravel()
    leftbottom_pts=[np.uint16(x),np.uint16(y)]
    cv2.circle(imgcont,leftbottom_pts,5,(0,0,0),-1)
    x,y=corners[2].ravel()
    rightbottom_pts=[np.uint16(x),np.uint16(y)]
    cv2.circle(imgcont,rightbottom_pts,5,(0,0,0),-1)
    x,y=corners[3].ravel()
    righttop_pts=[np.uint16(x),np.uint16(y)]
    cv2.circle(imgcont,righttop_pts,5,(0,255,255),-1)


    inputpts = np.array([lefttop_pts, rightbottom_pts, righttop_pts, leftbottom_pts],dtype=np.float32)
    outputpts = np.array([[0, 0],[500, 500],[500, 0],[0, 500]],dtype=np.float32)

    
    M=cv2.getPerspectiveTransform(inputpts,outputpts)
    imgwarp=cv2.warpPerspective(img,M,(500,500),flags=cv2.INTER_LINEAR)
    
    imgwarpgray=cv2.cvtColor(imgwarp, cv2.COLOR_BGR2GRAY)
    imgwarp_blur = cv2.GaussianBlur(imgwarpgray, (3,3), 1) 
    imgwarp_thresh= cv2.adaptiveThreshold(imgwarp_blur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,17,2)
    imgwarpinvert=255-imgwarp_thresh
    imagewarpmorph=imgwarpinvert

    kernelcl = np.ones((3,3),np.uint8)
    imagewarpmorph=cv2.morphologyEx(imgwarpinvert, cv2.MORPH_CLOSE, kernelcl)
    imagewarpmorph=cv2.morphologyEx(imagewarpmorph, cv2.MORPH_OPEN, kernelcl)

    cdstP = cv2.cvtColor(imagewarpmorph, cv2.COLOR_GRAY2BGR)
    linesP = cv2.HoughLinesP(imagewarpmorph, 1, np.pi / 180, 50, None, 50, 10)
    #create new image
    blank_image = np.zeros((cdstP.shape[0],cdstP.shape[1],3), np.uint8)
    blank_image=255-blank_image
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(blank_image, (l[0], l[1]), (l[2], l[3]), (0,0,0), 3, cv2.LINE_AA)
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,0), 3, cv2.LINE_AA)
    #unterteilen in quadrate
    höhe=cdstP.shape[0]
    breite=cdstP.shape[1]
    höhe_angepasst=np.uint16(höhe/9)
    breite_angepasst=np.uint16(breite/9)
    tl_pts=[0,0]
    br_pts=[höhe_angepasst,breite_angepasst]
    
    
    print(höhe_angepasst*breite_angepasst)
    tst=0
    for h in range(0,8):
        for w in range(0,8):
                roi=cdstP[höhe_angepasst*h:höhe_angepasst*(h+1),breite_angepasst*w:breite_angepasst*(w+1)]
                if np.count_nonzero(roi)/(höhe_angepasst*breite_angepasst)>0.09:
                    roi = cv2.rotate(roi, cv2.ROTATE_90_CLOCKWISE)
                    roi=cv2.resize(roi,(32,32),interpolation = cv2.INTER_AREA)
                    #cv2.imshow('Test'+str(h)+str(w),roi)
                    number=pytesseract.image_to_string(roi, lang='eng',config='--psm 6 -c tessedit_char_whitelist=0123456789')
                    if number!='':
                        print(number)
                else:
                    print(0)
    #15:26
    #print(np.count_nonzero(roi))
    #print(np.count_nonzero(roi)/(höhe_angepasst*breite_angepasst))
    cv2.imshow('Test8',blank_image)
    cv2.imshow('Test7',cdstP)
    cv2.imshow('Test6',imagewarpmorph)
    cv2.imshow('Test5',imgwarpgray)
    cv2.imshow('Test4',imgcont)


    k = cv2.waitKey(0)

    if k%256 == 27:
        # ESC pressed
        print("Close Application")
        break
        