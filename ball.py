import cv2
import numpy as np


class Ball:
    def __init__(self, inputSuit, inputName, inputColor):
        self.center = (0, 0)
        self.area = 0
        self.hitPoint = (0, 0)
        self.dragPoint = (0, 0)

        self.suit = inputSuit
        self.color = inputColor
        self.name = inputName
        self.mask = None
        self.RGB = (255, 255, 255)

        self.currentHole = (0, 0)
        self.currentHoleName = ""
        self.leftMarkH = (0, 0)
        self.rightMarkH = (0, 0)

        self.distanceToHole = 0
        self.slopeToHoleRise = 0
        self.slopeToHoleRun = 0
        self.slopeToHole = 0
        self.perpSlopeH = 0

        self.leftMarkB1 = (0, 0)
        self.rightMarkB1 = (0, 0)

        self.leftMarkSlopeH = 0
        self.rightMarkSlopeH = 0

        self.leftMarkB2 = (0, 0)
        self.rightMarkB2 = (0, 0)

        self.distancetoCue = 0
        self.slopetoCue = 0
        self.perpSlopeC = 0
        self.leftMarkC = 0
        self.rightMarkC = 0

        self.leftMarkSlopeC = 0
        self.rightMarkSlopeC = 0

        self.slopetoDragPoint = 0

    def stats(self):
        print("{},\n{},\n{},\n{},\n{},\n".format(self.center, self.suit, self.color, self.name, self.mask))

    def maskSetup(self, hsv):
        if self.color == "white":
            upper_whitecue = np.array([180, 40, 255])
            lower_whitecue = np.array([0, 10, 200])
            maskwhiteball = cv2.inRange(hsv, lower_whitecue, upper_whitecue)
            maskwhiteball = cv2.morphologyEx(maskwhiteball, cv2.MORPH_OPEN, np.ones((1, 2), np.uint8))
            self.mask = maskwhiteball
            self.RGB = 255, 255, 255
        elif self.color == "black":
            upper_black = np.array([0, 0, 240])
            lower_black = np.array([0, 0, 17])
            maskblackball = cv2.inRange(hsv, lower_black, upper_black)
            maskblackball = cv2.erode(maskblackball, None, iterations=3)
            maskblackball = cv2.dilate(maskblackball, None, iterations=4)
            self.mask = maskblackball
            self.RGB = 17, 17, 17
        elif self.color == "yellow":
            upper_yellow = np.array([25, 255, 255])
            lower_yellow = np.array([19, 100, 235])
            maskyellowball = cv2.inRange(hsv, lower_yellow, upper_yellow)
            maskyellowball = cv2.dilate(maskyellowball, None, iterations=1)
            self.mask = maskyellowball
            self.RGB = 30, 240, 247
        elif self.color == "blue":
            upper_blue = np.array([120, 255, 255])
            lower_blue = np.array([70, 0, 150])
            maskblueball = cv2.inRange(hsv, lower_blue, upper_blue)
            self.mask = maskblueball
            self.RGB = 196, 112, 58
        elif self.color == "lightred":
            upper_lightred = np.array([255, 255, 250])
            lower_lightred = np.array([175, 0, 0])
            masklightredball = cv2.inRange(hsv, lower_lightred, upper_lightred)
            self.mask = masklightredball
            self.RGB = 21, 6, 242
        elif self.color == "purple":
            upper_purple = np.array([140, 255, 255])
            lower_purple = np.array([120, 0, 135])
            maskpurpleball = cv2.inRange(hsv, lower_purple, upper_purple)
            self.mask = maskpurpleball
            self.RGB = 127, 0, 225
        elif self.color == "orange":
            upper_orange = np.array([19, 255, 255])
            lower_orange = np.array([11, 0, 170])
            maskorangeball = cv2.inRange(hsv, lower_orange, upper_orange)
            self.mask = maskorangeball
            self.RGB = 9, 101, 241
        elif self.color == "green":
            upper_green = np.array([70, 255, 255])
            lower_green = np.array([50, 70, 50])
            maskgreenball = cv2.inRange(hsv, lower_green, upper_green)
            self.mask = maskgreenball
            self.RGB = 76, 149, 62
        else:
            upper_darkred = np.array([8, 255, 255])
            lower_darkred = np.array([3, 0, 0])
            maskdarkredball = cv2.inRange(hsv, lower_darkred, upper_darkred)
            self.mask = maskdarkredball
            self.RGB = 6, 24, 102