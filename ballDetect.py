import numpy as np
import cv2
import imutils
import serial,time,os


os.chdir('/home/pi/lego')
# os.chdir('F:/Users/K-GIFT/Desktop/pi+EV3/Ev3PiSoccer')
import EV3BT
BT = True
if BT:
    try:
        ev3 = serial.Serial('/dev/rfcomm0')
        # ev3 = serial.Serial('COM6')
    except Exception as e:
        print(str(e))


cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('4.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)

#param#-------------------------------------
yellow1 = (25, 60, 60) #green1(HSV)
yellow2 = (40, 255, 255) #green2(HSV)

blue1 = (50, 70, 70) #green1(HSV)
blue2 = (100, 180, 180) #green2(HSV)
#HSV H=hue S=saturation V=value or brightness, low S or V mean can't distunguish color
numOfCnt = 1 #amount of screen


def resizeH(img,high):
    h = img.shape[0]
    w = img.shape[1]
    img = cv2.resize(img,( int(high*w/h) ,high))
    return(img)

x2outL=0
while(True):
    # 0) read image, preprocess
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=100)
    original = frame.copy()
    #frame = cv2.bilateralFilter(frame, 20, 50, 100)#crucial
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray = cv2.bilateralFilter(gray, 20, 50, 100)
    #bw = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)[1]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #detect line ----------------------------------------------------------
    # 1) get green area ------------------------
    maskBall = cv2.inRange(hsv, yellow1, yellow2)
    maskBall = cv2.GaussianBlur(maskBall,(11,11),0)

    maskGoal = cv2.inRange(cv2.bitwise_not(hsv, hsv, mask=maskBall), blue1, blue2)
    maskGoal = cv2.GaussianBlur(maskGoal,(11,11),0)

    maskBall = cv2.threshold(maskBall, 100, 255, cv2.THRESH_BINARY)[1]
    maskGoal = cv2.threshold(maskGoal, 100, 255, cv2.THRESH_BINARY)[1] #threshold 100

    outputImg = maskBall
    outputImg2 = maskGoal #threshold 50

    cnts = cv2.findContours(maskBall, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #cnts = cv2.findContours(maskGoal, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)
    cntsList = []
    cntsOut = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cntsList.append([x, y, w, h])

    cntsSize = [ c[2]*c[3] for c in cntsList ]
    cntsSortedIndex = np.sort(cntsSize)[::-1]
    cntsSortedIndex = [cntsSize.index(size) for size in  cntsSortedIndex]
    #get only the i_th biggest cnts
    if len(cntsSortedIndex)>=numOfCnt:
        cntsSortedIndex = cntsSortedIndex[0:numOfCnt]
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

    cnts = cv2.findContours(maskGoal, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cntsList = []
    cntsOut = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cntsList.append([x, y, w, h])
    cntsSize = [ c[2]*c[3] for c in cntsList ]
    cntsSortedIndex = np.sort(cntsSize)[::-1]
    cntsSortedIndex = [cntsSize.index(size) for size in  cntsSortedIndex]
    if len(cntsSortedIndex)>=numOfCnt:
        cntsSortedIndex = cntsSortedIndex[0:numOfCnt]
    for i in cntsSortedIndex:
        x2, y, w2, h = cntsList[i]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    if x2!= -1:
        if w>h:
            x2out = round( (x2+w2/2)/frame.shape[1] *100)
        else:
            x2out = x2outL

    xoutL = xout
    youtL = yout
    woutL = wout
    houtL = hout
    x2outL = x2out


    text = str(xout)+' '+str(yout)+' '+str(wout)+' '+str(hout)+' '+str(ratio)

    #message = EV3BT.encodeMessage(EV3BT.MessageType.Text, 'abc', text)
    if BT:
        # message = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, 'x', xout)
        # ev3.flush()
        # ev3.write(message)
        # time.sleep(0.01)
        # message = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, 'y', yout)
        # ev3.flush()
        # ev3.write(message)
        # time.sleep(0.01)
        message = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, 'num', (xout*10000+yout*100+x2out))
        # ev3.flush()
        ev3.write(message)
        time.sleep(0.01)
        #print(EV3BT.printMessage(message))

    cv2.putText(frame,str(x2out)+' '+str(x2outL),(0,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2)
    # cv2.imshow('frame',outputImg)
    cv2.imshow('frame2',frame)
    # cv2.imshow('frame3',outputImg2)


    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
if BT:
    ev3.close()