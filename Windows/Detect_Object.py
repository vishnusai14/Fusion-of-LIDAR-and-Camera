import cv2
import numpy as np
vcap = cv2.VideoCapture("http://mypi:8080/?action=stream")

while True:
    ret, frame = vcap.read()
    print(frame)
    if frame is not None:

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Gray Frame", gray_frame)
        thresh_frame = cv2.threshold(gray_frame, 25, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow("Thresholded Frame", thresh_frame)
        kernel = np.ones((5, 5), np.uint8)
        thresh_frame = cv2.morphologyEx(thresh_frame, cv2.MORPH_OPEN, kernel)
        cnts = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        blank_image = np.ones((450, 600, 3), np.uint8)

        # Set the minimum area for a contour
        min_area = 5000

        # Draw the contours on the original image and the blank image
        for c in cnts:
            area = cv2.contourArea(c)
            if area > min_area:
                cv2.drawContours(frame, [c], 0, (36, 255, 12), 2)
                cv2.drawContours(blank_image, [c], 0, (255, 255, 255), 2)
        cv2.imshow("Original Frame", frame)
        cv2.imshow("Contours", blank_image)
        if cv2.waitKey(22) & 0xFF == ord('q'):
            break
    else:
        break
vcap.release()
cv2.waitKey(0)
