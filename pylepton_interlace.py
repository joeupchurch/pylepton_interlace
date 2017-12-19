import time
import picamera
import numpy as np
import cv2
import traceback
import imutils
from imutils.video.pivideostream import PiVideoStream
from pylepton import Lepton

min_temp = np.float(8000)
max_temp = np.float(8600)

# Set defaults - Need to change in pivideostream as well
width = 320
height = 240

# Derived analytically for height of 30 inches
cfov_h = 62.2
cfov_v = 48.8
lfov_h = 51
lfov_v = 38


# start video stream and warm-up
##PiVideoStream(resolution=(width,height))
vs = PiVideoStream().start()
time.sleep(2.0)

try:
    with Lepton("/dev/spidev0.0") as l:
        last_nr = 0
        while True:
            
            lep,nr = l.capture()
            lep = lep.astype(np.float, copy=False)

            if nr == last_nr:
                # no need to redo this frame
                continue
            last_nr = nr
            
            img = vs.read()
##            imgRot = imutils.rotate(img, angle=270)
            img = np.rot90(img,k=2)
            img = img[int(height*(cfov_v-lfov_v)/(2*cfov_v)):int(height*(1-(cfov_v-lfov_v)/(2*cfov_v))),\
                      int(width*(cfov_h-lfov_h)/(2*cfov_h)):int(width*(1-(cfov_h-lfov_h)/(2*cfov_h))),:]
##            new_width = img.shape[0]
##            new_height = img.shape[1]
            img = cv2.resize(img, (width,height), interpolation = cv2.INTER_CUBIC)
            
            lep = np.matrix(lep)
            lep = lep*255/(max_temp-min_temp) - 255*min_temp/(max_temp-min_temp)
            lep[lep<0] = 0
            lep[lep>255] = 0
            lep = lep.astype(np.uint8, copy=False)
##            lep = np.rot90(lep)
                
            dst = cv2.resize(lep, (width,height), interpolation = cv2.INTER_CUBIC)

##            ret,mask = cv2.threshold(dst, 50, 255, cv2.THRESH_BINARY)
##            img = cv2.bitwise_and(img,img, mask=mask)

            cv2.namedWindow("Image")
            cv2.imshow("Image",img)               
            cv2.namedWindow("FLIR")
            cv2.imshow("FLIR",dst)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                cv2.destroyAllWindows()
                vs.stop()
                break

except Exception:
    vs.stop()
    traceback.print_exc()
