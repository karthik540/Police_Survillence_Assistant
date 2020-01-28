import cv2
import numpy as np
import time

cap = cv2.VideoCapture("http://192.168.43.102:4747/mjpegfeed")

while(True):
    last_time = time.time()
    ret , frame = cap.read()
    #   RGB -> Grey Conversion (Optional)
    #gray_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('Grey SelfCam' , frame)
    print("FPS: {}".format(1/(time.time() - last_time)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 