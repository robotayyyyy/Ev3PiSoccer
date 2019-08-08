import numpy as np
import cv2
import imutils
import serial,time,os

#for running script via IDE
os.chdir('/home/pi/lego')
# os.chdir('F:/Users/K-GIFT/Desktop/pi+EV3/Ev3PiSoccer')
import EV3BT
BT = True # True for sending data via bluetooth
if BT:
    try:
        ev3 = serial.Serial('/dev/rfcomm0')#for pi
        # ev3 = serial.Serial('COM6')#for windows
    except Exception as e:
        print(str(e))

cap = cv2.VideoCapture(0) #read from webcam
#cap = cv2.VideoCapture('4.mp4') #read videos from file, for debugging

#param#-------------------------------------
yellow1 = (25, 60, 60) #yellow1(HSV)
yellow2 = (40, 255, 255) #yellow2(HSV)

green1 = (50, 70, 70) #green1(HSV)
green2 = (100, 180, 180) #green2(HSV)
#HSV H=hue S=saturation V=value or brightness, low S or V mean can't distunguish color
numOfCnt = 1 #amount of interested objects, based on its size

def resizeH(img,high):
    h = img.shape[0]
    w = img.shape[1]
    img = cv2.resize(img,( int(high*w/h) ,high))
    return(img)

x2outL=0
while(True):
    # I don't know what I did but it works!
    x=0
    y=0
    w=-1
    h=-1
    x2=0
    w2=-1
    ratio = round(w/h,2)
    xout = 0
    yout = 0
    wout = -1
    hout = -1
    x2out = 0

    ret, frame = cap.read()# read image
    frame = imutils.resize(frame, width=100)#resize
    # original = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 1) get interested area ------------------------
    maskBall = cv2.inRange(hsv, yellow1, yellow2)
    maskBall = cv2.GaussianBlur(maskBall,(11,11),0)
    maskBall = cv2.threshold(maskBall, 100, 255, cv2.THRESH_BINARY)[1] #threshold 100

    maskGoal = cv2.inRange(cv2.bitwise_not(hsv, hsv, mask=maskBall), green1, green2)
    maskGoal = cv2.GaussianBlur(maskGoal,(11,11),0)
    maskGoal = cv2.threshold(maskGoal, 100, 255, cv2.THRESH_BINARY)[1] #threshold 100

    #for debugging
    # outputImg = maskBall
    # outputImg2 = maskGoal

    # 2) grab contours of the ball
    cnts = cv2.findContours(maskBall, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cntsList = []
    cntsOut = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cntsList.append([x, y, w, h])
    # sort by its size
    cntsSize = [ c[2]*c[3] for c in cntsList ]
    cntsSortedIndex = np.sort(cntsSize)[::-1] # [::-1] = desc
    cntsSortedIndex = [cntsSize.index(size) for size in  cntsSortedIndex]
    #get only the i_th biggest cnts
    if len(cntsSortedIndex)>=numOfCnt:
        cntsSortedIndex = cntsSortedIndex[0:numOfCnt]

    for i in cntsSortedIndex:
        x, y, w, h = cntsList[i]
        # cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),3)

    if x!= -1:
        if 0.8 < ratio and ratio < 1.2 :
            xout = round( (x+w/2)/frame.shape[1] *100)
            yout = round( (y+h/2)/frame.shape[0] *100)
            wout = round(w/frame.shape[1] *100)
            hout = round(h/frame.shape[0] *100)
        else:#return last value
            xout = xoutL
            yout = youtL
            wout = woutL
            hout = houtL

    # 3) grab contours of the goal
    cnts = cv2.findContours(maskGoal, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cntsList = []
    cntsOut = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cntsList.append([x, y, w, h])
    # sort by its size
    cntsSize = [ c[2]*c[3] for c in cntsList ]
    cntsSortedIndex = np.sort(cntsSize)[::-1]
    cntsSortedIndex = [cntsSize.index(size) for size in  cntsSortedIndex]
    #get only the i_th biggest cnts
    if len(cntsSortedIndex)>=numOfCnt:
        cntsSortedIndex = cntsSortedIndex[0:numOfCnt]
    for i in cntsSortedIndex:
        x2, y, w2, h = cntsList[i]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    if x2!= -1:
        if w2>h:
            x2out = round( (x2+w2/2)/frame.shape[1] *100)
        else:#return last value
            x2out = x2outL

    xoutL = xout
    youtL = yout
    woutL = wout
    houtL = hout
    x2outL = x2out

    #message = EV3BT.encodeMessage(EV3BT.MessageType.Text, 'abc', text)
    if BT:
        ## old method, sending 3 messages. I suspected it caused runtime error
        # message = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, 'x', xout)
        # ev3.flush()
        # ev3.write(message)
        # time.sleep(0.01)
        # message = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, 'y', yout)
        # ev3.flush()
        # ev3.write(message)
        # time.sleep(0.01)

        ## current method pack all number to the one
        message = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, 'num', (xout*10000+yout*100+x2out))
        # ev3.flush()
        ev3.write(message)
        time.sleep(0.01)
        #print(EV3BT.printMessage(message))

    # display section
    text = str(xout)+' '+str(yout)+' '+str(wout)+' '+str(hout)+' '+str(ratio)
    cv2.putText(frame,str(x2out)+' '+str(x2outL),(0,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2)
    cv2.imshow('frame',frame)
    # cv2.imshow('ball',outputImg)
    # cv2.imshow('goal',outputImg2)

    if cv2.waitKey(1) & 0xFF == ord(' '):#press spacebar to exit
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
if BT:
    ev3.close()