from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

fileName = 'D:/out1.mp4'
fps = 100

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

vs = VideoStream(0).start()
time.sleep(2.0)
writer = None



# record video
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=300)
    h = frame.shape[0]
    w = frame.shape[1]
    if writer is None:
        writer = cv2.VideoWriter(fileName,fourcc, fps, (w,h) )

    writer.write(frame)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break


cv2.destroyAllWindows()
vs.stop()
writer.release()