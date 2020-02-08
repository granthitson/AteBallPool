import cv2
import numpy as np
import pyautogui


img = cv2.imread('C:/Users/Grant/AppData/Local/Programs/Python/Projects/games/game76/table/pooltable1.png', 1)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

upper_whitecue = np.array([24,45,255])
lower_whitecue = np.array([21,15,0])
maskwhiteball = cv2. inRange(hsv, lower_whitecue, upper_whitecue)


upper_black = np.array([0, 0, 240])
lower_black = np.array([0, 0, 17])
maskblackball = cv2. inRange(hsv, lower_black, upper_black)

upper_yellow = np.array([31,255,255])
lower_yellow = np.array([19,150,150])
maskyellowball = cv2.inRange(hsv, lower_yellow, upper_yellow)

upper_blue = np.array([120,255,255])
lower_blue = np.array([105,30,175])
maskblueball = cv2.inRange(hsv, lower_blue, upper_blue)

upper_lightred = np.array([255,255,250])
lower_lightred = np.array([170,0,150])
masklightredball = cv2.inRange(hsv,lower_lightred, upper_lightred)

upper_purple = np.array([134,255,255])
lower_purple = np.array([130,0,120])
maskpurpleball = cv2.inRange(hsv, lower_purple, upper_purple)

upper_orange = np.array([12,255,255])
lower_orange = np.array([10,10,0])
maskorangeball = cv2.inRange(hsv,lower_orange, upper_orange)
#maskorangeball = cv2.dilate(maskorangeball,None,iterations=1)

upper_green = np.array([66,255,255])
lower_green = np.array([60,25,40])
maskgreenball = cv2.inRange(hsv, lower_green, upper_green)
#maskgreenball = cv2.dilate(maskgreenball,None,iterations=1)


upper_darkred = np.array([9,255,255])
lower_darkred = np.array([4,0,100])
maskdarkredball = cv2.inRange(hsv,lower_darkred, upper_darkred)


try:
    # cv2.imshow('white',maskwhiteball)
    # cv2.imshow('black',maskblackball)
    # cv2.imshow('blue',maskblueball)
    # cv2.imshow('lightred',masklightredball)
    cv2.imshow('darkred',maskdarkredball)
    # cv2.imshow('green',maskgreenball)
    # cv2.imshow('orange',maskorangeball)
    # cv2.imshow('yellow',maskyellowball)
    # cv2.imshow('purple',maskpurpleball)

    cv2.imshow('circle',img)
    

    while(1):
        k = cv2.waitKey(0)
        if (k == 27):
            break
except UnboundLocalError:
    pass

