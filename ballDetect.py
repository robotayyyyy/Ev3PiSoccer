import numpy as np
import cv2
import imutils
import os
import matplotlib.pyplot as plt

#os.chdir('F:/Users/K-GIFT/Desktop/pi+EV3')
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('4.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)

#param#-------------------------------------
yellow1 = (20, 60, 60) #green1(HSV)
yellow2 = (40, 255, 255) #green2(HSV)
#HSV H=hue S=saturation V=value or brightness, low S or V mean can't distunguish color
numOfCnt = 1 #amount of screen


def resizeH(img,high):
    h = img.shape[0]
    w = img.shape[1]
    img = cv2.resize(img,( int(high*w/h) ,high))
    return(img)


while(True):
    # 0) read image, preprocess
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=300)
    original = frame.copy()
    #frame = cv2.bilateralFilter(frame, 20, 50, 100)#crucial
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray = cv2.bilateralFilter(gray, 20, 50, 100)
    #bw = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)[1]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #detect line ----------------------------------------------------------
    # 1) get green area ------------------------
    maskGreen = cv2.inRange(hsv, yellow1, yellow2)
    maskGreen = cv2.GaussianBlur(maskGreen,(51,51),0) #need really big kernel for bluring
    outputImg = maskGreen
    maskGreen = cv2.threshold(maskGreen, 30, 255, cv2.THRESH_BINARY)[1] #threshold 50

    cnts = cv2.findContours(maskGreen, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cntsList = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cntsList.append([x, y, w, h])

    cntsSize = [ c[2]*c[3] for c in cntsList ]
    cntsSortedIndex = np.sort(cntsSize)[::-1]
    cntsSortedIndex = [cntsSize.index(size) for size in  cntsSortedIndex]
    #get only the i_th biggest cnts
    if len(cntsSortedIndex)>=numOfCnt:
        cntsSortedIndex = cntsSortedIndex[0:numOfCnt]
    for i in cntsSortedIndex:
        x, y, w, h = cntsList[i]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),3)

    xout = round( (x+w/2)/frame.shape[1] *100)
    yout = round( (y+h/2)/frame.shape[0] *100)
    wout = round(w/frame.shape[1] *100)
    hout = round(h/frame.shape[0] *100)

    ratio = round(w/h,2)

    text = str(xout)+' '+str(yout)+' '+str(wout)+' '+str(hout)+' '+str(ratio)
    cv2.putText(frame,str(text),(0,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2)
    cv2.imshow('frame',outputImg)
    cv2.imshow('frame2',frame)


    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()