import cv2
import numpy as np

def nothing(x):
    pass
frameTime = 25 # time of each frame in ms, you can add logic to change this value.

cv2.namedWindow("Tracking1")
cv2.createTrackbar("LH", "Tracking1", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking1", 0, 255, nothing)
cv2.createTrackbar("LV", "Tracking1", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking1", 255, 255, nothing)
cv2.createTrackbar("US", "Tracking1", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking1", 255, 255, nothing)

#kernal1 = np.ones((2,2), np.uint8)

while True:
    frame = cv2.imread('balls.jpg')
    frame =cv2.rotate(frame, rotateCode=2)
    #frame = cv2.imread('ball_stairs3.png')
    sframe = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    #sframe = cv2.resize(frame, (0, 0), fx=1.5, fy=1.5)

    hsv = cv2.cvtColor(sframe, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("LH", "Tracking1")
    l_s = cv2.getTrackbarPos("LS", "Tracking1")
    l_v = cv2.getTrackbarPos("LV", "Tracking1")

    u_h = cv2.getTrackbarPos("UH", "Tracking1")
    u_s = cv2.getTrackbarPos("US", "Tracking1")
    u_v = cv2.getTrackbarPos("UV", "Tracking1")

    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, l_b, u_b)
    #mask = cv2.dilate(mask, kernal1, iterations=2)
    #cv2.imshow("Dilate Mask", mask)

    res = cv2.bitwise_and(sframe, sframe, mask=mask)

    #cv2.imshow("frame", sframe)
    #cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    if cv2.waitKey(frameTime) & 0xFF == ord('q'):
        break
#cap.release()
cv2.destroyAllWindows()