import cv2
import numpy as np

vcap = cv2.VideoCapture('http://mypi:8080/?action=stream')
#if not vcap.isOpened():
#    print "File Cannot be Opened"
i = 1
path = "D:/catkin_ws/src/laser_scanner_tfmini/images/"
while(True):
    # Capture frame-by-frame
    ret, frame = vcap.read()
    #print cap.isOpened(), ret
    if frame is not None:
        # Display the resulting frame
       

        cv2.imshow('frame',frame)
        
       
        # Press q to close the video windows before it ends if you want
        if cv2.waitKey(22) & 0xFF == ord('q'):
            break
    else:
        print("Frame is None")
        break

# When everything done, release the capture
vcap.release()
cv2.destroyAllWindows()


