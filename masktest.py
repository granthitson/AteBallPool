import cv2
import numpy as np
import pyautogui


img = cv2.imread(r'C:\Users\Grant\AppData\Local\Programs\Python\Projects\games\game50\table\pooltable1.png',)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

upper_whitecue = np.array([180,50,255])
lower_whitecue = np.array([0,10,80])
maskwhiteball = cv2. inRange(hsv, lower_whitecue, upper_whitecue)


upper_black = np.array([50,225,50])
lower_black = np.array([10,0,0])
maskblackball = cv2. inRange(hsv, lower_black, upper_black)

upper_yellow = np.array([25,255,255])
lower_yellow = np.array([23,150,100])
maskyellowball = cv2.inRange(hsv, lower_yellow, upper_yellow)
maskyellowball = cv2.dilate(maskyellowball,None,iterations=1)

upper_blue = np.array([135,255,255])
lower_blue = np.array([112,70,100])
maskblueball = cv2.inRange(hsv, lower_blue, upper_blue)

upper_lightred = np.array([4,255,250])
lower_lightred = np.array([0,105,150])
masklightredball = cv2.inRange(hsv,lower_lightred, upper_lightred)

upper_purple = np.array([160,255,255])
lower_purple = np.array([135,50,70])
maskpurpleball = cv2.inRange(hsv, lower_purple, upper_purple)

upper_orange = np.array([19,255,255])
lower_orange = np.array([11,150,170])
maskorangeball = cv2.inRange(hsv,lower_orange, upper_orange)

upper_green = np.array([60,255,255])
lower_green = np.array([53,70,50])
maskgreenball = cv2.inRange(hsv, lower_green, upper_green)
#maskgreenball = cv2.dilate(maskgreenball,None,iterations=1)


upper_darkred = np.array([4,255,180])
lower_darkred = np.array([3,50,50])
maskdarkredball = cv2.inRange(hsv,lower_darkred, upper_darkred)


try:
    cv2.imshow('white',maskwhiteball)
    cv2.imshow('black',maskblackball)
    cv2.imshow('blue',maskblueball)
    cv2.imshow('lightred',masklightredball)
    cv2.imshow('darkred',maskdarkredball)
    cv2.imshow('green',maskgreenball)
    cv2.imshow('orange',maskorangeball)
    cv2.imshow('yellow',maskyellowball)
    cv2.imshow('purple',maskpurpleball)

    cv2.imshow('circle',img)
    

    while(1):
        k = cv2.waitKey(0)
        if (k == 27):
            break
except UnboundLocalError:
    pass

