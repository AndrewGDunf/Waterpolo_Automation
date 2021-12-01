# Andrew Dunford 
# November 2021

import cv2                      # import OpenCV libray 
import numpy as np              # import numpy libray and apprivate this to np
import math                     # import math function to do trigonometric calculations
import socket                   # to send data to the other script
import pickle                   # pickle will be used to structure the data sent to the other script

HEADERSIZE = 12                       #for the socket, the header is to be this size 
cap1 = cv2.VideoCapture('a100.mp4')   # import the video file of behind the goal
cap2 = cv2.VideoCapture('a00.mp4')   # import the video file of the corner of the pool 
frameTime = 10                     # time of each frame in ms, you can add logic to change this value.
hsv_min1 = (14, 100, 0)             # minimum HSV filter values for the yellow ball behind the goal
hsv_max1 = (33, 255, 255)           # maximum HSV filter values for the yellow ball corner of the pool
hsv_min2 = (14, 90, 90)               # minimum HSV filter values for the yellow ball behind the goal 
hsv_max2 = (33, 255, 255)            # maximum HSV filter values for the yellow ball corner of the pool 
# the Kernals is used to dilate and errode the mask from the HSV filter,
kernal1 = np.ones((2,2), np.uint8)  # kernal 1 is small to dilate (inlarge) the pixels of the ball 
kernal2 = np.ones((5,5), np.uint8)  # kernal 2 is large to erode (reduce) the pixels of the ball

nb1 = 1                             #initialise varriable nb1 (number pixels from camera behind goal)
ns1 = 1                             #initialise varriable nb1 (number pixels from camera side goal)
a=0

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1903))
s.listen(5)

def send(x,y,x_od,y_od,g):
    d={1: x, 2: y, 3: x_od, 4: y_od, 5: g}
    msg =pickle.dumps(d)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg
    clientsocket.send(msg)


xba = 1
yba = 1
xsa = 1
ysa = 1

def get_x_keypoints(keypoints):
    for i, keyPoint in enumerate(keypoints):
                #--- Here you can implement some tracking algorithm to filter multiple detections
                #--- We are simply getting the first result
                x = keyPoint.pt[0]
                #y = keyPoint.pt[1]
                #s = keyPoint.size
                #print ("kp %d: s = %3d   x = %3d  y= %3d"%(i, s, x, y))
                return(x)

def get_y_keypoints(keypoints):
    for i, keyPoint in enumerate(keypoints):
                #--- Here you can implement some tracking algorithm to filter multiple detections
                #--- We are simply getting the first result
                #x = keyPoint.pt[0]
                y = keyPoint.pt[1]
                #s = keyPoint.size
                #print ("kp %d: s = %3d   x = %3d  y= %3d"%(i, s, x, y))
                return(y)

def realiser(a):
    if a is None: 
        a = 0

    return(a)
        

def glt(x1,y1,x2,y2):
    if x1 > 335 and x1 < 977 and x2 > 30 and x2 < 120 and y1 > 330 and y2 > 250 and y2 < 360:
        #print("goal")
        a=1
    else:
        a=0
    return(a)


while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    #while loop, will repeat the code inside the loop until the video ends 
    while(cap1.isOpened()):
        
        ret1, frame1 = cap1.read()                              # read the frame from the video
        ret2, frame2 = cap2.read()                              # read the frame from the video
     
        sframe1 = cv2.resize(frame1, (0, 0), fx=0.5, fy=0.5)    # option to resize the frame 
        roi1 = sframe1[0: 575, 0: 1352] #[y1: y2, x1: x2]                        # roi is the "region of interest" that we care if the ball is in (usally the field of play)
        hsv1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2HSV)            # converts the colour spectrum from BGR to HSV to enable the HSV filter
        mask1 = cv2.inRange(hsv1, hsv_min1, hsv_max1)           # mask looks for the HSV values in the ranges set previous

        """
        sframe1 = cv2.line(sframe1, (0,0), (0,425), (255, 0, 0), 2)   #left box
        sframe1 = cv2.line(sframe1, (0,0), (960,0), (255, 0, 0), 2)   #top box
        sframe1 = cv2.line(sframe1, (960,0), (960,425), (255, 0, 0), 2)   #right box
        sframe1 = cv2.line(sframe1, (0,425), (960,425), (255, 0, 0), 2)   #bottom box 
        
        
        """
        sframe2 = cv2.resize(frame2, (0, 0), fx=0.5, fy=0.5)    # option to resize the frame 
        roi2 = sframe2[0: 700, 0: 1352] #for awl.mp4        # roi is the "region of interest" that we care if the ball is in (usally the field of play) 
        hsv2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)           # converts the colour spectrum from BGR to HSV to enable the HSV filter
        mask2 = cv2.inRange(hsv2, hsv_min2, hsv_max2)            # mask looks for the HSV values in the ranges set previous
    
        """
        sframe2 = cv2.line(sframe2, (0,0), (0,350), (255, 0, 0), 2)   #left box
        sframe2 = cv2.line(sframe2, (0,0), (960,0), (255, 0, 0), 2)   #top box
        sframe2 = cv2.line(sframe2, (960,0), (960,350), (255, 0, 0), 2)   #right box
        sframe2 = cv2.line(sframe2, (0,350), (900,350), (255, 0, 0), 2)   #bottom box 
        
        #cv2.imshow('frame1',sframe1)                            # outputs the video
        #cv2.imshow('frame2',sframe2)                            # outputs the video
        
        #cv2.imshow("HSV Mask1", mask1)                         # outputs the video with the HSV mask applied, the white is within the accept HSV value 
        #cv2.imshow("HSV Mask2", mask2)       
        
        
        rows = float(sframe1.shape[0])   # rows = 720 = ymax   # finds the videos height (ie number of rows of pixels)
        cols = float(sframe1.shape[1])   # cols = 1280 = xmax  # finds the videos width (ie number of colums of pixels)
        print(rows, cols)                                    # prints the rows and the cols
        """

        mask1 = cv2.dilate(mask1, kernal1, iterations=2)       # dilate the mask using kernal1 twice
        #cv2.imshow("Dilate Mask", mask)                     # show the mask that has been dilated 
        mask1 = cv2.erode(mask1, kernal2, iterations=1)        # erode the mask using kernal2 once 
        mask1 = cv2.dilate(mask1, kernal1, iterations=4)       # dilate the mask using kernal1 twice, This step makes sure we dont lose too much detail of the ball for optimal tracking 
        #cv2.imshow("Dilated and Erode Mask1", mask1)           # show the result of this dilation 
        
        

        mask2 = cv2.dilate(mask2, kernal1, iterations=2)       # dilate the mask using kernal1 twice
        #cv2.imshow("Dilate Mask", mask)                     # show the mask that has been dilated 
        mask2 = cv2.erode(mask2, kernal2, iterations=2)        # erode the mask using kernal2 once 
        #mask2 = cv2.erode(mask2, kernal1, iterations=1)
        mask2 = cv2.dilate(mask2, kernal1, iterations=5)       # dilate the mask using kernal1 twice, This step makes sure we dont lose too much detail of the ball for optimal tracking 
        #cv2.imshow("Dilated and Erode Mask2", mask2)           # show the result of this dilation 
        
        

        blob = cv2.SimpleBlobDetector_Params()             # use the OpenCV function SimpleBlobDetector and edit its parametres 
         
        # Change thresholds                                  # threshold does 
        blob.minThreshold = 0;
        blob.maxThreshold = 100;
             
        # Filter by Area.                                    # Area looks at how large the blob is and filters the detections         
        blob.filterByArea = True                           # this line says that we do want to filter the blobs by their area 
        blob.minArea = 20                                  # Area of  coresponds with a 
        blob.maxArea = 20000      
             
        # Filter by Circularity
        blob.filterByCircularity = True
        blob.minCircularity = 0.1  # why is it point 0.1 
             
        # Filter by Convexity
        blob.filterByConvexity = True
        blob.minConvexity = 0.1
             
        # Filter by Inertia
        blob.filterByInertia =True
        blob.minInertiaRatio = 0.5

        detector = cv2.SimpleBlobDetector_create(blob)

        
        reversemask1 = 255-mask1
        #cv2.imshow("Reverse Mask", reversemask)
        keypoints1 = detector.detect(reversemask1)
        
        
        reversemask2 = 255-mask2
        #cv2.imshow("Reverse Mask", reversemask)
        keypoints2 = detector.detect(reversemask2)
        
        """
        im_with_keypoints1 = cv2.line(roi1, (400,310), (620,310), (255, 0, 0), 2)  # cross bar (x1, y1), (x2, y2)
        im_with_keypoints1 = cv2.line(im_with_keypoints1, (400,410), (620,400), (255, 0, 0), 2) # water level of goal 
        im_with_keypoints1 = cv2.line(im_with_keypoints1, (400,310), (400,410), (255, 0, 0), 2)  # left goal post 
        im_with_keypoints1 = cv2.line(im_with_keypoints1, (620,310), (620,400), (255, 0, 0), 2)  # right goal post 
        
        
        for i, keyPoint2 in enumerate(keypoints2):
                    #--- Here you can implement some tracking algorithm to filter multiple detections
                    #--- We are simply getting the first result
                    x2 = keyPoint2.pt[0]
                    y2 = keyPoint2.pt[1]
                    s2 = keyPoint2.size
                    print ("kp %d: s = %3d   x = %3d  y= %3d"%(i, s2, x2, y2))
                    #sleep(1)
                    #--- Find x and y position in camera adimensional frame
                    #x, y = get_blob_relative_position(frame, keyPoint)
                    #print(x, y)  
                    

        for j, keyPoint1 in enumerate(keypoints1):
                    #--- Here you can implement some tracking algorithm to filter multiple detections
                    #--- We are simply getting the first result
                    x1 = keyPoint1.pt[0]
                    y1 = keyPoint1.pt[1]
                    s1 = keyPoint1.size
                    print ("kp %d: s = %3d   x = %3d  y= %3d"%(j, s1, x1, y1))
                    return(x1)
                    #sleep(1)
                    #--- Find x and y position in camera adimensional frame
                    #x, y = get_blob_relative_position(frame, keyPoint)
                    #print(x, y)  
        """
        
        xb = get_x_keypoints(keypoints1) 
        yb = get_y_keypoints(keypoints1)
        xs = get_x_keypoints(keypoints2)
        ys = get_y_keypoints(keypoints2)

        xb = realiser(xb)
        if xb > 0: 
                xba = xb
        yb = realiser(yb)
        if yb > 0: 
                yba = yb
        xs = realiser(xs)
        if xs > 0: 
                xsa = xs
        ys = realiser(ys)
        if ys > 0: 
                ysa = ys

        g = glt(xba, yba, xsa, ysa)
        
        beta = (109*(1-(xba/1352)) + 35)*0.0174533
        alpha = (174 - 78*xsa/1352)*0.0174533



        a = math.tan(alpha)
        b = math.tan(beta)
        y = 10 - (10*a)/(a-b)
        x = (10*a)/(a/b - 1)


        print(round(xba),round(xsa),  "          ", round(y,3), round(x, 3), g)

        
        
        """
        data = [x,y]
        encode = struct.pack('<2f',*data)
        print(encode)
        data1=struct.unpack('<2f', encode)
        print(data1)
        clientsocket.send(bytes(encode,"utf-8"))
        """

        x_od = x*30 + 50
        y_od = 650-(y*30)

        send(x,y,x_od,y_od,g)

        

        if xb > 0 and xs > 0:
            im_with_keypoints1 = cv2.drawKeypoints(roi1, keypoints1, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            im_with_keypoints2 = cv2.drawKeypoints(roi2, keypoints2, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        else: 
            im_with_keypoints1 = cv2.drawKeypoints(roi1, keypoints1, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            im_with_keypoints2 = cv2.drawKeypoints(roi2, keypoints2, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        
        cv2.imshow("Keypoints1", im_with_keypoints1)
        cv2.imshow("Keypoints2", im_with_keypoints2)
        """
        
        plt.title("ball tracking")
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.axis([0,750,0,900])
        plt.plot(x1a,x2a,'ro')
        plt.pause(0.05)
        plt.show()
        """


        if cv2.waitKey(frameTime) & 0xFF == ord('q'):
            break


cap1.release()
cap2.release()
cv2.destroyAllWindows()
