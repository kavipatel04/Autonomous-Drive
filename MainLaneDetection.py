import cv2
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time

steerRightSetting = 0
steerLeftSetting = 0
dutyCycle = 0
rightYCoord = -10000
leftError = -10000
rightError = -10000
car_cascade = cv2.CascadeClassifier('cars.xml') 
#processorLogic = 0

def edgeDetection(img):
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(img, low_threshold, high_threshold)
    return edges



def filter_colors_hsv(img):
    """
    Convert image to HSV color space and suppress any colors
    outside of the defined color ranges
    """
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    yellow_dark = np.array([15, 127, 127], dtype=np.uint8)
    yellow_light = np.array([25, 255, 255], dtype=np.uint8)
    yellow_range = cv2.inRange(img, yellow_dark, yellow_light)

    white_dark = np.array([0, 0, 200], dtype=np.uint8)
    white_light = np.array([255, 30, 255], dtype=np.uint8)
    white_range = cv2.inRange(img, white_dark, white_light)
    yellows_or_whites = yellow_range | white_range
    img = cv2.bitwise_and(img, img, mask=yellows_or_whites)
    return img

def getTheLines(img, edges):
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)
    return lines


def drawLines(lines, line_image):
    for line in lines:
        for x1,y1,x2,y2 in line:
            #220 x 950X
            if x1 > 100 and x1 < 700:
                if y1 > 225:
                    cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

def runLineLogic(lines, center_coordinates, img):
    global rightError
    global leftError
    global rightYCoord
    averageRightCounter = 0
    rightXCoord = 0
    rightYCoord = 0
    averageLeftCounter = 0
    leftXCoord = 0
    leftYCoord = 0
    for line in lines:
        for x1,y1,x2,y2 in line:
            #220 x 950X
            if x1 > 220 and x1 < 500:
                if y1 > 500:
                    rightXCoord += x1
                    rightYCoord += y1
                    averageRightCounter += 1
            elif x1 > 500 and x1 < 900:
                if y1 > 500:
                    leftXCoord += x1
                    leftYCoord += y1
                    averageLeftCounter += 1
    if averageRightCounter > 0:
        rightXCoord = rightXCoord/averageRightCounter
        rightYCoord = rightYCoord/averageRightCounter
        drawCircle(img, (int(rightXCoord), int(rightYCoord)))
        rightError = rightXCoord
    if averageLeftCounter > 0:
        leftXCoord = leftXCoord/averageLeftCounter
        leftYCoord = leftYCoord/averageLeftCounter
        drawCircle(img, (int(leftXCoord), int(rightYCoord)))
        leftError = leftXCoord

    

def runSteeringLogic(xCenter, yCenter, img):
    global rightError
    global leftError  
    global rightYCoord
    global steerLeftSetting
    global steerRightSetting
    global dutyCycle

    rightError = xCenter - rightError
    leftError = leftError - xCenter
    if rightYCoord > 450 and rightYCoord < 550: 
        if rightError > 310:
            writeText(img, (50, 50), 'Steer Left')
            steerLeftSetting += 1
            steerRightSetting = 0
        elif rightError < 210:
            writeText(img, (50, 50), 'Steer Right')
            steerRightSetting += 1
            steerLeftSetting = 0
        else:
            writeText(img, (50, 50), 'GOOD DRIVING')
            steerRightSetting = 0
            steerLeftSetting = 0
    elif rightYCoord > 600:
        if rightError > 380:
            writeText(img, (50, 50), 'Steer Left')
            steerLeftSetting += 1
            steerRightSetting = 0
        elif rightError < 230:
            writeText(img, (50, 50), 'Steer Right')
            steerRightSetting += 1
            steerLeftSetting = 0
        else:
            writeText(img, (50, 50), 'GOOD DRIVING')
            steerRightSetting = 0
            steerLeftSetting = 0
    #writeText(img, (400, 50), str(rightError))
    if steerRightSetting > 0:
        dutyCycle = (steerRightSetting**3) + 20
    elif steerLeftSetting > 0:
        dutyCycle = (steerLeftSetting**3) + 20
    else:
        dutyCycle = 0
    #writeText(img, (1000, 50), str(dutyCycle))

def drawScale(error, img):
    coord = (500, 200)
    y1, y2 = 70, 100
    x1 = 600 + ((error -260)/5)
    x1 = int(x1)
    x2 = x1
    cv2.line(img, (x1,y1), (x2, y2), (0, 0, 255), 2)
    cv2.line(img, (600, y1), (600, y2), (0, 255, 0), 2)

def findAndDrawCar(frames, drawImg):
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY) 
    # Detects cars of different sizes in the input image 
    cars = car_cascade.detectMultiScale(gray, 1.1, 1) 
    # To draw a rectangle in each cars 
    for (x,y,w,h) in cars: 
        area = w*h
        if area > 50:
            cv2.rectangle(drawImg,(x,y),(x+w,y+h),(0,0,255),2) 

def writeText(img, org, text):
    font = cv2.FONT_HERSHEY_SIMPLEX  
    fontScale = 1
    color = (255, 0, 0)  
    thickness = 2
    cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA)

def drawCircle(img, coordinates):
    #center_coordinates = (630, 500)
    radius = 20
    color = (0, 0, 255)
    thickness = 2
    cv2.circle(img, coordinates, radius, color, thickness)

def computeRunTime(label, start, end):
    final = end - start
    print("It took " + str(label) + " , " + str(final))


cap = cv2.VideoCapture('TrimmedVid.mp4')


while True:
    start2 = time.time()
    start = time.time() #del
    ret, mimg = cap.read()
    pimg = mimg.copy()
    end = time.time() #del
    computeRunTime("img copy", start, end) #del

    start = time.time() #del
    pimg = filter_colors_hsv(pimg)
    edges = edgeDetection(pimg)
    end = time.time() #del
    computeRunTime("img process", start, end) #del
    
    start = time.time()
    lines = getTheLines(pimg, edges)
    drawLines(lines, pimg)
    end = time.time()
    computeRunTime("line processing", start, end)

    start = time.time()
    drawCircle(pimg, (615, 500))
    runLineLogic(lines, (615, 500), pimg)
    runSteeringLogic(615, 500, pimg)
    end = time.time()
    computeRunTime("steering logic", start, end)
    #findAndDrawCar(mimg, mimg)
    #drawScale(rightError, pimg)
    #plt.imshow(pimg)
    #plt.show()
    start = time.time()
    cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
    #time.sleep(0.1)
    end2 = time.time()
    writeText(pimg, (700, 50), "FPS: " + str(round(1/(end2-start2), 2)))
    cv2.imshow('Frame', pimg)
    cv2.imshow('Original', mimg)
    end = time.time()
    computeRunTime("img display", start, end)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()