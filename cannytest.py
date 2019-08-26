import cv2
import numpy as np
import imutils
import math
import os
import time
import pyautogui

def surprise():
    
    img1 = cv2.imread('pooltable3.png',1)
    hsv2 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    test1 = np.array([70, 0, 0])
    test2 = np.array([105, 255, 255])
    testmask = cv2.inRange(hsv2, test1, test2)
   
    testmask = cv2.bitwise_not(testmask)
    testmask = cv2.bitwise_and(img1,img1, mask=testmask)
    cv2.imwrite('temp.png', testmask)

    img = cv2.imread('temp.png',0)
    img4 = cv2.imread('temp.png',1)

    hsv1 = cv2.cvtColor(img4, cv2.COLOR_BGR2HSV)

    alist = masks(hsv1)
    rect = None

    for n, b in alist:
        contours = cv2.findContours(b.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if imutils.is_cv2() else contours[1]
        contours = sorted(contours, key=cv2.contourArea)
        if n == 'cueball' or n == 'eightball':
            contours = contours[len(contours)-1:len(contours)]
        else:
            contours = contours[len(contours)-2:len(contours)]

        ball_1 = None
        ball_2 = None
        for c in contours:
            carea = cv2.contourArea(c)
            if carea > 15:
                (x,y),radius = cv2.minEnclosingCircle(c)
                center = (int(x),int(y))
                b = cv2.circle(b,center,10,(170,0,255),1)
                if ball_1 is None:
                    ball_1 = (center[0],center[1],carea)
                else:
                    ball_2 = (center[0],center[1],carea)
            else:
                continue
            
        img = cv2.medianBlur(img,3)
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,.5,13,
                                param1=75,param2=9.75,minRadius=15,maxRadius=20)
        circles = np.uint16(np.around(circles))

        suit = 'nosuit'
        for i in circles[0,:]:
            if ball_1 is not None:
                if math.fabs(i[0] - ball_1[0]) < 6 and math.fabs(i[1] - ball_1[1]) < 6:
                    print("6 - ", (ball_1[0],ball_1[1]),(i[0],i[1]))
                    ball_1 = (i[0],i[1],ball_1[2])
            if ball_2 is not None:
                if math.fabs(i[0] - ball_2[0]) < 6 and math.fabs(i[1] - ball_2[1]) < 6:
                    print("7 - ", (ball_2[0],ball_2[1]),(i[0],i[1]))
                    ball_2 = (i[0],i[1],ball_2[2])
            
        if n == 'cueball' or n == 'eightball':
            print('ball_1 is cueball or eightball. {}'.format((ball_1[0],ball_1[1])))
            cv2.circle(img1, (ball_1[0],ball_1[1]), 10, (255,255,255), 1)
        else:
            if ball_1[2] > ball_2[2]:
                print('ball_1 is solid. {} {}'.format(n,(ball_1[0],ball_1[1])))
                cv2.circle(img1, (ball_1[0],ball_1[1]), 10, (255,255,255), 1)
                print('ball_2 is stripe. {} {}'.format(n,(ball_2[0],ball_2[1])))
                cv2.circle(img1, (ball_2[0],ball_2[1]), 10, (255,255,255), 1)
            else:
                print('ball_1 is stripe. {} {}'.format(n,(ball_1[0],ball_1[1])))
                cv2.circle(img1, (ball_1[0],ball_1[1]), 10, (255,255,255), 1)
                print('ball_2 is solid. {} {}'.format(n,(ball_2[0],ball_2[1])))
                cv2.circle(img1, (ball_2[0],ball_2[1]), 10, (255,255,255), 1)

        
        cv2.imshow('img1',img1)
        cv2.imshow('img4',b)
        cv2.imshow('img5',testmask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
                    

def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, (255,255,255))
    masked = cv2.bitwise_and(img, mask)
    return masked

def stringToColor(color):  # takes the list of colors and based on name, returns a rgb color value
    '''

    :param color:
    :return:
    '''
    if color == 'cueball':
        return 255, 255, 255
    elif color == 'eightball':
        return 17, 17, 17
    elif color == 'blueball':
        return 196, 112, 58
    elif color == 'lightredball':
        return 21, 6, 242
    elif color == 'darkredball':
        return 6, 24, 102
    elif color == 'greenball':
        return 76, 149, 62
    elif color == 'orangeball':
        return 9, 101, 241
    elif color == 'yellowball':
        return 33, 171, 235
    elif color == 'purpleball':
        return 148, 38, 87
    else:
        return 127, 0, 225

def masks(hsv):
    alist = []
    upper_whitecue = np.array([180, 40, 255])
    lower_whitecue = np.array([0, 10, 200])
    maskwhiteball = cv2.inRange(hsv, lower_whitecue, upper_whitecue)
    maskwhiteball = cv2.morphologyEx(maskwhiteball, cv2.MORPH_OPEN, np.ones((1,2),np.uint8))
    alist.append(('cueball',maskwhiteball))

    upper_black = np.array([0, 0, 255])
    lower_black = np.array([0, 0, 17])
    maskblackball = cv2.inRange(hsv, lower_black, upper_black)
    maskblackball = cv2.erode(maskblackball, None, iterations=3)
    maskblackball = cv2.dilate(maskblackball, None, iterations=4)
    alist.append(('eightball',maskblackball))

    upper_yellow = np.array([25, 255, 255])
    lower_yellow = np.array([19, 100, 235])
    maskyellowball = cv2.inRange(hsv, lower_yellow, upper_yellow)
    maskyellowball = cv2.dilate(maskyellowball, None, iterations=1)
    alist.append(('yellowball',maskyellowball))

    upper_blue = np.array([120, 255, 255])
    lower_blue = np.array([70, 0, 150])
    maskblueball = cv2.inRange(hsv, lower_blue, upper_blue)
    alist.append(('blueball',maskblueball))

    upper_lightred = np.array([255, 255, 250])
    lower_lightred = np.array([175, 0, 0])
    masklightredball = cv2.inRange(hsv, lower_lightred, upper_lightred)
    alist.append(('lightredball',masklightredball))

    upper_purple = np.array([140, 255, 255])
    lower_purple = np.array([120, 0, 135])
    maskpurpleball = cv2.inRange(hsv, lower_purple, upper_purple)
    alist.append(('purpleball',maskpurpleball))

    upper_orange = np.array([19, 255, 255])
    lower_orange = np.array([11, 0, 170])
    maskorangeball = cv2.inRange(hsv, lower_orange, upper_orange)
    alist.append(('orangeball',maskorangeball))

    upper_green = np.array([70, 255, 255])
    lower_green = np.array([50, 70, 50])
    maskgreenball = cv2.inRange(hsv, lower_green, upper_green)
    alist.append(('greenball',maskgreenball))

    upper_darkred = np.array([8, 255, 255])
    lower_darkred = np.array([3, 0, 0])
    maskdarkredball = cv2.inRange(hsv, lower_darkred, upper_darkred)
    alist.append(('darkredball',maskdarkredball))

    
    return alist

def main():
    surprise()
    

if __name__ == '__main__':
    main()
