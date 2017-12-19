import time
import numpy as np
import cv2
import traceback
from pylepton import Lepton

##lepton_buf = np.zeros((60, 80,1), dtype=np.int16)
##last_buf = np.zeros((60, 80,1))

# 7649 is min of 59F clafoutis
# 7900 is min for a cold hand ~72F
# 8400 is max of inside of mouth ~95.1F

min_temp = np.float(8000)
max_temp = np.float(8600)

frame_num = 0
##saved_frames_long = 1
##saved_frames_short = 1
##buffer = np.zeros((60,80,1), dtype=np.int16)

##erodeSize = 2
##dilateSize = 3
##mask_thresh = 75
##edges_thresh = 100

try:
    time.sleep(0.2) # give the overlay buffers a chance to initialize
    with Lepton("/dev/spidev0.0") as l:
        last_nr = 0
        while True:
            a,nr = l.capture()
            a = a.astype(np.float, copy=False)

            if nr == last_nr:
                # no need to redo this frame
##                frame_num+=1
                continue
##            elif frame_num>10:
##                buffer = np.append(buffer,a,axis=2)
##                buffer = buffer[:,:,-1:]
                
##                mean_buffer_long = np.mean(buffer,axis=2,dtype=np.uint16)
##                mean_buffer_short = np.array(np.mean(buffer[:,:,-saved_frames_short:],axis=2,dtype=np.uint16))
##                
##                diff_buf = np.subtract(mean_buffer_short,mean_buffer_long)
##                diff_buf = diff_buf-np.amin(diff_buf)
            a = np.matrix(a)
            a = a*255/(max_temp-min_temp) - 255*min_temp/(max_temp-min_temp)
            a[a<0] = 0
            a[a>255] = 0
            a = a.astype(np.uint8, copy=False)
                
##                cv2.normalize(diff_buf, diff_buf, 0, 255, cv2.NORM_MINMAX)

                
##                blurredBrightness = cv2.GaussianBlur(diff_buf,(3,3),0)
##                _,mask_upper = cv2.threshold(blurredBrightness,0,255,cv2.THRESH_BINARY)
##                img = cv2.bitwise_and(blurredBrightness,blurredBrightness,mask = mask_upper)
##                _,mask_lower = cv2.threshold(img,240,255,cv2.THRESH_BINARY_INV)
##                eroded = cv2.erode(mask_lower, np.ones((erodeSize, erodeSize)))
##                mask_temp = cv2.dilate(eroded, np.ones((dilateSize, dilateSize)))
                
##                edges = cv2.Canny(a,edges_thresh,edges_thresh*2)
                
##                img = cv2.bitwise_and(diff_buf,diff_buf,mask = mask_temp)

            dst = cv2.resize(a, (640,480), interpolation = cv2.INTER_CUBIC)
            cv2.namedWindow("Image")
            cv2.imshow("Image",dst)               
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                cv2.destroyAllWindows()
                break
                
            last_nr = nr
##            last_buf = a
##            frame_num+=1

except Exception:
    traceback.print_exc()
