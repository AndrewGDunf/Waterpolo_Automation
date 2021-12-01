# Andrew Dunford 
# August 2021

import cv2                      # import OpenCV libray 
import numpy as np              # import numpy libray and apprivate this to np
from time import sleep          # import sleep from the time library 

cap = cv2.VideoCapture('awl.mp4')   # import the video file 
frameTime = 25                      # time of each frame in ms, you can add logic to change this value.
hsv_min = (14, 90, 83)
hsv_max = (27, 186, 210)
#hsv_min = (14, 55, 63)              # minimum HSV filter values for the yellow ball 
#hsv_max = (27, 186, 210)            # maximum HSV filter values for the yellow ball
# the Kernals is used to dilate and errode the mask from the HSV filter,
kernal1 = np.ones((2,2), np.uint8)  # kernal 1 is small to dilate (inlarge) the pixels of the ball 
kernal2 = np.ones((5,5), np.uint8)  # kernal 2 is large to erode (reduce) the pixels of the ball

#while loop, will repeat the code inside the loop until the video ends 
while(cap.isOpened()):
    ret, frame = cap.read()                              # read the frame from the video
    sframe = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)   # option to resize the frame 
    roi = frame[100: 600, 300: 1520] #for awl.mp4        # roi is the "region of interest" that we care if the ball is in (usally the field of play)
    #roi = frame[100: 700, 100: 1180] #for BehindGoals1  # this is an option for a different video feed 
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)           # converts the colour spectrum from BGR to HSV to enable the HSV filter
    mask = cv2.inRange(hsv, hsv_min, hsv_max)            # mask looks for the HSV values in the ranges set previous
    
    cv2.imshow('frame',frame)                            # outputs the video
    cv2.imshow("HSV Mask", mask)                         # outputs the video with the HSV mask applied, the white is within the accept HSV value        
    
    """
    rows = float(frame.shape[0])   # rows = 1080         # finds the videos height (ie number of rows of pixels)
    cols = float(frame.shape[1])   # cols = 1920         # finds the videos width (ie number of colums of pixels)
    print(rows, cols)                                    # prints the rows and the cols
    """
    mask = cv2.dilate(mask, kernal1, iterations=2)       # dilate the mask using kernal1 twice
    #cv2.imshow("Dilate Mask", mask)                     # show the mask that has been dilated 
    mask = cv2.erode(mask, kernal2, iterations=1)        # erode the mask using kernal2 once 
    mask = cv2.dilate(mask, kernal1, iterations=2)       # dilate the mask using kernal1 twice, This step makes sure we dont lose too much detail of the ball for optimal tracking 
    cv2.imshow("Dilated and Erode Mask", mask)           # show the result of this dilation 

    params = cv2.SimpleBlobDetector_Params()             # use the OpenCV function SimpleBlobDetector and edit its parametres 
         
    # Change thresholds                                  # threshold does 
    params.minThreshold = 0;
    params.maxThreshold = 100;
         
    # Filter by Area.                                    # Area looks at how large the blob is and filters the detections         
    params.filterByArea = True                           # this line says that we do want to filter the blobs by their area 
    params.minArea = 100                                 # Area of  coresponds with a 
    params.maxArea = 20000      
         
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1  # why is it point 0.1 
         
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.5
         
    # Filter by Inertia
    params.filterByInertia =True
    params.minInertiaRatio = 0.5

    detector = cv2.SimpleBlobDetector_create(params)

    reversemask = 255-mask
    #cv2.imshow("Reverse Mask", reversemask)
    keypoints = detector.detect(reversemask)

    im_with_keypoints = cv2.line(roi, (400,310), (620,310), (255, 0, 0), 2)  # cross bar (x1, y1), (x2, y2)
    im_with_keypoints = cv2.line(im_with_keypoints, (400,410), (620,400), (255, 0, 0), 2) # water level of goal 
    im_with_keypoints = cv2.line(im_with_keypoints, (400,310), (400,410), (255, 0, 0), 2)  # left goal post 
    im_with_keypoints = cv2.line(im_with_keypoints, (620,310), (620,400), (255, 0, 0), 2)  # right goal post 

    for i, keyPoint in enumerate(keypoints):
                #--- Here you can implement some tracking algorithm to filter multiple detections
                #--- We are simply getting the first result
                x = keyPoint.pt[0]
                y = keyPoint.pt[1]
                s = keyPoint.size
                print ("kp %d: s = %3d   x = %3d  y= %3d"%(i, s, x, y))
                #sleep(1)
                #--- Find x and y position in camera adimensional frame
                #x, y = get_blob_relative_position(frame, keyPoint)
                #print(x, y)  
                if x > 400 and x < 620 and y > 310 and y < 410:
                    im_with_keypoints = cv2.drawKeypoints(im_with_keypoints, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                else: 
                    im_with_keypoints = cv2.drawKeypoints(im_with_keypoints, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)   
    

    #im_with_keypoints = cv2.drawKeypoints(im_with_keypoints, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow("Keypoints", im_with_keypoints)
    #print(keypoints)



    if cv2.waitKey(frameTime) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()