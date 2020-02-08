import cv2
import numpy as np


class Ball:
    def __init__(self, inputSuit, inputName, inputColor, inputTarget):
        self.center = (0, 0)
        self.offsetCenter = (0, 0)
        self.area = 0
        self.hitPoint = (0, 0)
        self.hitPointStart = (0, 0)
        self.hitPointEnd = (0, 0)
        self.angle = 0

        self.target = inputTarget
        self.suit = inputSuit
        self.color = inputColor
        self.name = inputName
        self.mask = None
        self.RGB = (255, 255, 255)
        self.pocketed = False

        self.currentHole = (0, 0)
        self.offsetCurrentHole = (0, 0)
        self.currentHoleName = ""

        self.leftMarkH = (0, 0)
        self.rightMarkH = (0, 0)
        self.holeGapSlope = 0
        self.holeGapSlopeRise = 0
        self.holeGapSlopeRun = 0
        self.innerBoundLeft = (0,0)
        self.innerBoundRight = (0,0)

        self.distanceToHole = 0
        self.slopeToHoleRise = 0
        self.slopeToHoleRun = 0
        self.slopeToHole = 0
        self.perpSlopeH = 0

        self.leftMarkB1 = (0, 0)
        self.rightMarkB1 = (0, 0)

        self.distancetoCue = 0 #
        self.slopetoCueRise = 0 #
        self.slopetoCueRun = 0 #
        self.slopetoCue = 0 #
        self.perpSlopeC = 0 #

        self.leftMarkC = (0, 0)
        self.rightMarkC = (0, 0)

        self.leftMarkB2 = (0, 0)
        self.rightMarkB2 = (0, 0)

        self.distanceToHP = 0
        self.slopeToHPRise = 0
        self.slopeToHPRun = 0
        self.slopeToHP = 0
        self.perpSlopeHP = 0

        self.slopetoDragPoint = (0, 0)
        self.deflectionPoint = (0, 0)

    def stats(self):
        print(
            "center: {},\noffsetCenter: {},\nhitpoint: {},\nstartpoint: {},\nendpoint: {},\nsuit: {},\ncolor: {},\nname: {},"
            "\ncurrenthole: {},\noffsetcurrenthole: {},\ncurrentholename: {},"
            "\n\nleftmarkH: {},\nrightMarkH: {},\nslopetoHoleRise: {},\nslopetoHoleRun: {},"
            "\nSlopetoHole: {},\nperpSlopeH: {},""\n\nleftMarkB1: {},\nrightMarkB1: {},\nleftMarkB2: {},"
            "\nrightMarkB2: {},\n\nslopetoCue: {},\nperpSlopeC: {},\nleftMarkC: {},\nrightMarkC: {},"
            "\n\ndistanceToHP: {},\nslopeToHP: {},\nperpSlopeHP: {},\nslopeToDragPoint: {}".format(
                self.center, self.offsetCenter,
                self.hitPoint, self.hitPointStart, self.hitPointEnd,
                self.suit, self.color, self.name,
                self.currentHole,
                self.offsetCurrentHole,
                self.currentHoleName,
                self.leftMarkH, self.rightMarkH,
                self.slopeToHoleRise,
                self.slopeToHoleRun,
                self.slopeToHole,
                self.perpSlopeH,
                self.leftMarkB1,
                self.rightMarkB1,
                self.leftMarkB2,
                self.rightMarkB2,
                self.slopetoCue, self.perpSlopeC,
                self.leftMarkC,
                self.rightMarkC,
                self.distanceToHP,
                self.slopeToHP,
                self.perpSlopeHP,
                self.slopetoDragPoint))

    def maskSetup(self, hsv):
        if self.color == "white":
            upper_whitecue = np.array([27, 36, 255])
            lower_whitecue = np.array([18, 0, 120])
            maskwhiteball = cv2.inRange(hsv, lower_whitecue, upper_whitecue)
            maskwhiteball = cv2.morphologyEx(maskwhiteball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            self.mask = maskwhiteball
            self.RGB = 255, 255, 255
        elif self.color == "black":
            upper_black = np.array([0, 0, 110])
            lower_black = np.array([0, 0, 30])
            maskblackball = cv2.inRange(hsv, lower_black, upper_black)
            maskblackball = cv2.morphologyEx(maskblackball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            self.mask = maskblackball
            self.RGB = 17, 17, 17
        elif self.color == "yellow":
            upper_yellow = np.array([31, 255, 255])
            lower_yellow = np.array([19, 50, 160])
            maskyellowball = cv2.inRange(hsv, lower_yellow, upper_yellow)
            maskyellowball = cv2.morphologyEx(maskyellowball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            self.mask = maskyellowball
            self.RGB = 30, 240, 247
        elif self.color == "blue":
            upper_blue = np.array([120, 220, 255])
            lower_blue = np.array([105, 50, 160])
            maskblueball = cv2.inRange(hsv, lower_blue, upper_blue)
            maskblueball = cv2.morphologyEx(maskblueball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            self.mask = maskblueball
            self.RGB = 196, 112, 58
        elif self.color == "lightred":
            upper_lightred = np.array([180, 255, 250])
            lower_lightred = np.array([170, 0, 150])
            masklightredball = cv2.inRange(hsv, lower_lightred, upper_lightred)
            masklightredball = cv2.morphologyEx(masklightredball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            self.mask = masklightredball
            self.RGB = 21, 6, 242
        elif self.color == "purple":
            upper_purple = np.array([139, 255, 255])
            lower_purple = np.array([130, 11, 70])
            maskpurpleball = cv2.inRange(hsv, lower_purple, upper_purple)
            maskpurpleball = cv2.morphologyEx(maskpurpleball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            self.mask = maskpurpleball
            self.RGB = 130, 0, 120
        elif self.color == "orange":
            upper_orange = np.array([12, 255, 255])
            lower_orange = np.array([10, 134, 0])
            maskorangeball = cv2.inRange(hsv, lower_orange, upper_orange)
            maskorangeball = cv2.morphologyEx(maskorangeball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            self.mask = maskorangeball
            self.RGB = 9, 101, 241
        elif self.color == "green":
            upper_green = np.array([70, 255, 255])
            lower_green = np.array([50, 0, 140])
            maskgreenball = cv2.inRange(hsv, lower_green, upper_green)
            maskgreenball = cv2.morphologyEx(maskgreenball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            self.mask = maskgreenball
            self.RGB = 76, 149, 62
        else:
            upper_darkred = np.array([7, 255, 255])
            lower_darkred = np.array([3, 100, 100])
            maskdarkredball = cv2.inRange(hsv, lower_darkred, upper_darkred)
            maskdarkredball = cv2.morphologyEx(maskdarkredball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            self.mask = maskdarkredball
            self.RGB = 6, 24, 102

    def isPocketed(self, min, max):
        if (self.center[0] + min) < min or (self.center[0] + min) > max:
            self.pocketed = True
        else:
            self.pocketed = False
