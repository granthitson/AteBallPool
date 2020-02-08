import math
import os
import random
import time

import cv2
import imutils
import numpy as np
import pyautogui

import ball
import utils
import constants


class Round:

    def __init__(self, inputTurn, inputGameNum, inputPoolRegion, inputGameWindow, holeList):
        self.ballList = []
        self.suit = None

        self.turnNum = inputTurn
        self.gameNum = inputGameNum
        self.holeLocation = holeList
        self.poolRegion = inputPoolRegion
        self.gameWindow = inputGameWindow
        self.imgPath = "/games/game" + self.gameNum + "/table/pooltable" + str(self.turnNum) + ".png"
        self.roundImage = None

        self.sunkBalls = None
        self.chosenBall = None
        self.cueball = (0, 0)
        self.offsetCueball = (0, 0)
        self.offset = (516, 315)

        constants.debug = True

    def start(self):
        cwd = os.getcwd()
        self.imgPath = cwd + self.imgPath

        self.moveMouseOut()

        print("Turn #" + str(self.turnNum))

        self.ballCheck()
        self.outlineBall()

        cfb = self.checkForBreak()
        if cfb is False:
            qDS = self.queryDirectShot()
            if qDS is True:
                self.hitBall(self.chosenBall)
            else:
                #self.queryReboundedShot()
                print("Unable to query ball.")
                return False

        return True

    def checkForBreak(self):
        """
        Determines if bot needs to break balls. If the bot doesn't currently have a suit assigned, it checks if the centers
        of all pool balls other than the cueball are within a certain area.
        :return: True/False depending on if bot needs to break.
        """
        breakRack = True
        if self.suit == "nosuit":
            print("No suit assigned.")

            for b in self.ballList:
                if b.name == "cueball":
                    continue
                elif 691 > b.center[0] > 489 and 242 > b.center[1] > 120:
                    continue
                else:
                    breakRack = False
                    break
        else:
            print("Assigned suit: {}".format(self.suit))
            breakRack = False

        if breakRack is True:
            print("Breaking.")
            randNum = 3#random.randint(0, 10)
            if randNum < 5:
                pyautogui.moveTo((self.cueball[0] + self.offset[0]) + 175, (self.cueball[1] + self.offset[1]))
                pyautogui.dragTo((self.cueball[0] + self.offset[0])- 50, (self.cueball[1] + self.offset[1]), button="left",
                                 duration=1)
            else:
                print("Randomized Break.")
                x, y = self.offsetCueball[0] + random.randrange(-100, 0), self.cueball[1] - random.randrange(-100, 100)
                pyautogui.moveTo(self.offsetCueball)
                pyautogui.dragTo((x + 658, y + 297), button="left")
                self.cueball = x, y

                return False

        else:
            return False

    def ballCheck(self):
        """
        Checks which pool balls the bot needs to target. In the beginning of a game when no suit is assigned, bot will target
        balls that come first in dictionary.

        Needs to be reworked to target based on a variety of different variables, not just what comes first.
        :return: None - Appends balls to an existing list,
        """
        solids = {constants.img_1ball: "yellow", constants.img_2ball: "blue",
                  constants.img_3ball: "lightred", constants.img_4ball: "purple",
                  constants.img_5ball: "orange", constants.img_6ball: "green",
                  constants.img_7ball: "darkred"}

        solidsDark = {constants.img_1ballDark: "yellow", constants.img_2ballDark: "blue",
                      constants.img_3ballDark: "lightred", constants.img_4ballDark: "purple",
                      constants.img_5ballDark: "orange", constants.img_6ballDark: "green",
                      constants.img_7ballDark: "darkred"}

        stripes = {constants.img_9ball: "yellow", constants.img_10ball: "blue",
                   constants.img_11ball: "lightred", constants.img_12ball: "purple",
                   constants.img_13ball: "orange", constants.img_14ball: "green",
                   constants.img_15ball: "darkred"}

        stripesDark = {constants.img_9ballDark: "yellow", constants.img_10ballDark: "blue",
                       constants.img_11ballDark: "lightred", constants.img_12ballDark: "purple",
                       constants.img_13ballDark: "orange", constants.img_14ballDark: "green",
                       constants.img_15ballDark: "darkred"}

        pyautogui.moveTo(1186, 386)

        while True:
            pos = pyautogui.locateOnScreen(utils.imagePath(constants.img_ballPic1), region=self.gameWindow,
                                           confidence=.99)
            if pos is not None:
                topRX = pos[0] + pos[2]
                topRY = pos[1]
                reg = (topRX - 227, topRY, 227, 80)
                reg2 = (reg[0] + 470, reg[1], reg[2], reg[3])
                break

        self.ballList.append(ball.Ball("nosuit", "cueball", "white", False))
        self.ballList.append(ball.Ball("nosuit", "eightball", "black", False))

        # find targeted suit - add balls to list to find center
        for k, v in solids.items():
            pos = utils.imageSearch(k, reg, confidence=.90)
            if pos is not None:
                self.suit = "solid"
                b = ball.Ball("solid", k.replace(".png", ""), v, True)
                self.ballList.append(b)

        for k, v in stripes.items():
            pos = utils.imageSearch(k, reg, confidence=.90)
            if pos is not None:
                self.suit = "stripe"
                b = ball.Ball("stripe", k.replace(".png", ""), v, True)
                self.ballList.append(b)

        # find non targeted suit - still add balls to list to find center
        for k, v in solidsDark.items():
            pos = utils.imageSearch(k, reg2, confidence=.90)
            if pos is not None:
                b = ball.Ball("solid", k.replace("Dark.png", ""), v, False)
                self.ballList.append(b)

                if self.suit is None:
                    self.suit = "stripe"

        for k, v in stripesDark.items():
            pos = utils.imageSearch(k, reg2, confidence=.90)
            if pos is not None:
                b = ball.Ball("stripe", k.replace("Dark.png", ""), v, False)
                self.ballList.append(b)

                if self.suit is None:
                    self.suit = "solid"

        # no suit
        if len(self.ballList) == 2:
            self.suit = "nosuit"
            for k, v in solids.items():
                b = ball.Ball("solid", k.replace(".png", ""), v, True)
                self.ballList.append(b)

            for k, v in stripes.items():
                b = ball.Ball("stripe", k.replace(".png", ""), v, True)
                self.ballList.append(b)

    def outlineBall(self):
        """
        Outlines pool balls using Hough Circles and Contours. Hough Circles, while sometimes inaccurate, find the center
        of each ball on the screen more accurately than contours. This includes extraneous/uneeded circles found.

        Then, for each ball in ballList, contours are found using each balls' specific mask. Depending on the color/type
        of ball (cueball/eightball/playballs), the list of contours found is limited to the two largest. Certain circumstances
        allow for more than two, such as a split contour.

        Typically, for each of balls, assuming there is still two contours of a specific color (which means that
        there are both a solid and striped colored ball on the table), each contour is investigated. As long as the contour
        has not already been used, and is within a certain area/radius, information is collected in regard to the pool ball;
        the information includes area of the ball's colored mask, area of white contours in a region of interest around
        the center, and a number of total contours within said region of interest (a count of more than two white contours
        usually means a striped ball is present). The contour in question is then matched to the closest point identified
        by the Hough Circles.

        Depending on how many contours are being investigated, the information collected on them are assigned to variables,
        ball_1 if there is one contour, ball_2 if there is two. Then, in order to differentiate between two contours of
        the same color, a confidence level is generated based on the information collected from each ball. The confidence level
        is only generated on ball_1; if the confidence level is < 0, the ball is striped, > 0 is solid.

        The correct center point is then assigned to ball.

        :return: None - only updates paramters in each ball
        """
        utils.debugPrint("Outlining pool balls...")
        self.roundImage = cv2.imread(self.imgPath, 1)

        roundImageCopy = self.roundImage.copy()
        hsvRndImg = cv2.cvtColor(roundImageCopy, cv2.COLOR_BGR2HSV)

        # image of area where sunk balls go
        pyautogui.screenshot("games/game{}/temp1.png".format(self.gameNum),
                             region=(self.poolRegion[0] + 725, self.poolRegion[1] + 40, 50, self.poolRegion[3]))
        self.sunkBalls = cv2.imread("games/game{}/temp1.png".format(self.gameNum), 1)
        hsvSunkBall = cv2.cvtColor(self.sunkBalls, cv2.COLOR_BGR2HSV)

        # white mask of all balls (except cue)
        upper_white = np.array([0, 255, 255])
        lower_white = np.array([0, 0, 125])
        maskwhite = cv2.inRange(hsvRndImg, lower_white, upper_white)
        maskwhiteSunk = cv2.inRange(hsvSunkBall, lower_white, upper_white)

        # mask for table color - table color masked out for visibility
        blueTableLow = np.array([90, 80, 0])
        blueTableHigh = np.array([106, 255, 255])
        blackTableLow = np.array([0, 0, 35])
        blackTableHigh = np.array([180, 255, 255])
        tableInvertMask = cv2.inRange(hsvRndImg, blueTableLow, blueTableHigh)
        tableInvertMask = cv2.bitwise_not(tableInvertMask)
        holeInvertMask = cv2.inRange(hsvRndImg, blackTableLow, blackTableHigh)
        tableInvertMask = cv2.bitwise_and(tableInvertMask, holeInvertMask)
        tableInvertMask = cv2.bitwise_and(roundImageCopy, roundImageCopy, mask=tableInvertMask)
        cv2.imwrite("games/game{}/temp.png".format(self.gameNum), tableInvertMask)

        tableMaskedOut = cv2.imread("games/game{}/temp.png".format(self.gameNum), 1)
        tableMaskedOutBW = cv2.imread("games/game{}/temp.png".format(self.gameNum), 0)
        hsvTableMaskedOut = cv2.cvtColor(tableMaskedOut, cv2.COLOR_BGR2HSV)

        # Hough Circles for identifying ball locations more accurated than contours
        circles = cv2.HoughCircles(tableMaskedOutBW, cv2.HOUGH_GRADIENT, 1, 17,
                                   param1=20, param2=9, minRadius=9, maxRadius=11)
        circles = np.uint16(np.around(circles))
        pointList = []
        for i in circles[0, :]:
            cv2.circle(roundImageCopy, (i[0], i[1]), i[2], (0, 0, 0), 2)
            pointList.append((i[0], i[1]))

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.imwrite("games/game{}/{}.png".format(self.gameNum, "hough"), roundImageCopy)

        # outline each ball - find based on each color mask
        ignore = []
        for b in self.ballList:
            #print("Determining position of {} {} {}.".format(b.name, b.suit, b.color))
            b.maskSetup(hsvTableMaskedOut) # prepare each ball's mask based on its color

            contours = self.contourSetup(b.mask, True)  # list of contours found

            if b.name == "cueball" or b.name == "eightball":
                contours = contours[len(contours) - 1:len(contours)] # limits contours to single largest contour
            else:
                contoursTemp = contours[len(contours) - 2:len(contours)] # limits contorus to two largest contours

                for k, c in enumerate(contoursTemp):
                    carea = cv2.contourArea(c)
                    (x, y), radius = cv2.minEnclosingCircle(c)
                    if radius > 25: # in some cases, a message pops up on screen - replaces it
                        contoursTemp[k] = contours[len(contours) - 3]
                    else:
                        if carea > 0 and carea < 80: # if a contour that should be together is split, it will result in two smaller contours
                            b.mask = cv2.morphologyEx(b.mask, cv2.MORPH_CLOSE, np.ones((8, 8), np.uint8))
                            contoursTemp = self.contourSetup(b.mask, True)

                contours = contoursTemp

            ball_1 = None
            ball_2 = None
            large = False
            # find center based on color
            for c in contours:
                carea = cv2.contourArea(c)
                (x, y), radius = cv2.minEnclosingCircle(c)
                center = self.roundTuple((x,y))
                if center not in ignore:
                    if carea > 25:
                        if radius < 13:
                            roiMask = self.roi(maskwhite, center, 10)
                            contours1 = self.contourSetup(roiMask, False)
                            whiteArea, whiteCount = self.whiteMaskedArea(contours1, True, 0)

                            cv2.imwrite("games/game{}/{}white.png".format(self.gameNum, b.name), roiMask)

                            closest = (0, 1000)
                            closest = self.matchHoughCircleToMask(pointList, center, closest, 10)
                            if closest[1] == 1000:
                                continue
                            else:
                                if ball_1 is None:
                                    ball_1 = (pointList[closest[0]][0], pointList[closest[0]][1], carea, whiteArea, whiteCount, center)
                                else:
                                    ball_2 = (pointList[closest[0]][0], pointList[closest[0]][1], carea, whiteArea, whiteCount, center)

                                pointList.pop(closest[0])
                        else:
                            large = True
                            pointListCopy = pointList.copy()

                            closest = (0, 1000)
                            closest = self.matchHoughCircleToMask(pointListCopy, center, closest, 15)
                            point1 = pointListCopy.pop(closest[0])

                            closest1 = (0, 1000)
                            closest1 = self.matchHoughCircleToMask(pointListCopy, center, closest1, 15)
                            point2 = pointListCopy.pop(closest1[0])
                            if closest[1] == 1000 and closest1[1] == 1000:
                                continue
                            else:
                                points = [point1, point2]
                                for p in points:
                                    roiMask = self.roi(b.mask, p, 10)
                                    contours = self.contourSetup(roiMask, False)
                                    for c in contours:
                                        carea = cv2.contourArea(c)
                                        (x, y), radius = cv2.minEnclosingCircle(c)
                                        center = self.roundTuple((x,y))
                                        if carea > 30:
                                            roiMask = self.roi(maskwhite, p, 10)
                                            contours = self.contourSetup(roiMask, False)
                                            whiteArea, whiteCount = self.whiteMaskedArea(contours, True, 0)

                                            if ball_1 is None:
                                                ball_1 = (
                                                    pointList[closest[0]][0], pointList[closest[0]][1], carea,
                                                    whiteArea,
                                                    whiteCount,
                                                    center)

                                                pointList.pop(pointList.index(p))
                                            else:
                                                ball_2 = (
                                                    pointList[closest1[0]][0], pointList[closest1[0]][1], carea,
                                                    whiteArea,
                                                    whiteCount,
                                                    center)

                                                pointList.pop(pointList.index(p))

            if b.name == "cueball":
                if ball_1 is None:
                    ball_1 = self.backUpCenter(contours, maskwhite)
                    b.center = (ball_1[0], ball_1[1])
                else:
                    b.center = (ball_1[0], ball_1[1])

                self.cueball = b.center
                self.offsetCueball = (self.cueball[0] + self.offset[0], self.cueball[1] + self.offset[1])
                #print("ball_1 is cueball. {}. \n".format((ball_1[0], ball_1[1])))
                self.drawStripe(b.center, b.RGB)
            elif b.name == "eightball":
                if ball_1 is None:
                    ball_1 = self.backUpCenter(contours, maskwhite)
                    b.center = (ball_1[0], ball_1[1])
                else:
                    b.center = (ball_1[0], ball_1[1])

                b.offsetCenter = (b.center[0] + self.offset[0], b.center[1] + self.offset[1])
                #print("ball_1 is eightball. {}. \n".format((ball_1[0], ball_1[1])))
                self.drawStripe(b.center, b.RGB)
            else:
                if ball_2 is None:
                    count = 0
                    for c in contours:
                        area = cv2.contourArea(c)
                        if area > 30:
                            count += 1

                    if count == 1:
                        for b1 in self.ballList:
                            b.maskSetup(hsvSunkBall)
                            if b.color == b1.color and b.suit == b1.suit:
                                contours = self.contourSetup(b1.mask.copy(), True)
                                contours = contours[len(contours) - 2:len(contours)]

                                for c in contours:
                                    carea = cv2.contourArea(c)
                                    (x, y), radius = cv2.minEnclosingCircle(c)
                                    center = self.roundTuple((x,y))
                                    if center not in ignore:
                                        if carea > 15:
                                            roiMask1 = self.roi(maskwhiteSunk, center, 10)
                                            contours1 = self.contourSetup(roiMask1, False)

                                            whiteArea, whiteCount = self.whiteMaskedArea(contours1, True, 0)
                                            if ball_1 is None:
                                                ball_1 = (center[0] + 725, center[1] + 40, carea, whiteArea, whiteCount, center)
                                            else:
                                                ball_2 = (center[0] + 725, center[1] + 40, carea, whiteArea, whiteCount, center)


                if ball_2 is None:
                    if ball_1 is not None:
                        if b.suit == "solid":
                            b.center = (ball_1[0], ball_1[1])
                            b.offsetCenter = (b.center[0] + self.offset[0], b.center[1] + self.offset[1])
                            # print(
                            #     "ball_1 is solid. {} - {} -- {} \n".format((ball_1[0], ball_1[1]),
                            #                                                        ball_1[2], ball_1[3]))
                            self.drawSolid(b.center, b.RGB)
                        elif b.suit == "stripe":
                            b.center = (ball_1[0], ball_1[1])
                            b.offsetCenter = (b.center[0] + self.offset[0], b.center[1] + self.offset[1])
                            # print(
                            #     "ball_1 is stripe. {} - {} -- {} \n".format((ball_1[0], ball_1[1]),
                            #                                                         ball_1[2], ball_1[3]))
                            self.drawStripe(b.center, b.RGB)

                        ignore.append(ball_1[5])
                    else:
                        continue
                else:
                    confidence = self.suitConfidence(ball_1, ball_2)

                    if confidence > 0:
                        if b.suit == "solid":
                            b.center = (ball_1[0], ball_1[1])
                            b.offsetCenter = (b.center[0] + self.offset[0], b.center[1] + self.offset[1])
                            # print(
                            #     "ball_1 is solid. {} - {} -- {}".format((ball_1[0], ball_1[1]), ball_1[2],
                            #                                                  ball_1[3]))
                            self.drawSolid(b.center, b.RGB)
                            if large is False:
                                ignore.append(ball_1[5])
                                pointList.append((ball_2[0], ball_2[1]))
                            else:
                                pointList.append((ball_1[0], ball_1[1]))
                                pointList.append((ball_2[0], ball_2[1]))
                        elif b.suit == "stripe":
                            b.center = (ball_2[0], ball_2[1])
                            b.offsetCenter = (b.center[0] + self.offset[0], b.center[1] + self.offset[1])
                            # print(
                            #     "ball_2 is stripe. {} - {} -- {}".format((ball_2[0], ball_2[1]), ball_2[2],
                            #                                                   ball_2[3]))
                            self.drawStripe(b.center, b.RGB)
                            if large is False:
                                ignore.append(ball_2[5])
                                pointList.append((ball_1[0], ball_1[1]))
                            else:
                                pointList.append((ball_1[0], ball_1[1]))
                                pointList.append((ball_2[0], ball_2[1]))
                    elif confidence < 0:
                        if b.suit == "stripe":
                            b.center = (ball_1[0], ball_1[1])
                            b.offsetCenter = (b.center[0] + self.offset[0], b.center[1] + self.offset[1])
                            # print("ball_1 is stripe. {} - {} -- {}".format((ball_1[0], ball_1[1]), ball_1[2],
                            #                                                     ball_1[3]))
                            self.drawStripe(b.center, b.RGB)
                            if large is False:
                                ignore.append(ball_1[5])
                                pointList.append((ball_2[0], ball_2[1]))
                            else:
                                pointList.append((ball_1[0], ball_1[1]))
                                pointList.append((ball_2[0], ball_2[1]))
                        elif b.suit == "solid":
                            b.center = (ball_2[0], ball_2[1])
                            b.offsetCenter = (b.center[0] + self.offset[0], b.center[1] + self.offset[1])
                            # print("ball_2 is solid. {} - {} -- {}".format((ball_2[0], ball_2[1]), ball_2[2],
                            #                                                    ball_2[3]))
                            self.drawSolid(b.center, b.RGB)
                            if large is False:
                                ignore.append(ball_2[5])
                                pointList.append((ball_1[0], ball_1[1]))
                            else:
                                pointList.append((ball_1[0], ball_1[1]))
                                pointList.append((ball_2[0], ball_2[1]))
                    else:
                        # random chance at this point
                        #print("confidence is 0")
                        if b.suit == "solid":
                            b.center = (ball_1[0], ball_1[1])
                            b.offsetCenter = (b.center[0] + self.offset[0], b.center[1] + self.offset[1])
                            print("ball_1 is solid. {} - {} -- {}".format((ball_1[0], ball_1[1]), ball_1[2],ball_1[3]))
                            self.drawSolid(b.center, b.RGB)
                            if large is False:
                                ignore.append(ball_1[5])
                                pointList.append((ball_2[0], ball_2[1]))
                            else:
                                pointList.append((ball_1[0], ball_1[1]))
                                pointList.append((ball_2[0], ball_2[1]))
                        elif b.suit == "stripe":
                            b.center = (ball_2[0], ball_2[1])
                            b.offsetCenter = (b.center[0] + self.offset[0], b.center[1] + self.offset[1])
                            #print("ball_2 is stripe. {} - {} -- {}".format((ball_2[0], ball_2[1]), ball_2[2],ball_2[3]))
                            self.drawStripe(b.center, b.RGB)
                            if large is False:
                                ignore.append(ball_2[5])
                                pointList.append((ball_1[0], ball_1[1]))
                            else:
                                pointList.append((ball_1[0], ball_1[1]))
                                pointList.append((ball_2[0], ball_2[1]))

            if b.center[0] > self.poolRegion[2]:
                b.pocketed = True

        self.savePic()

    def suitConfidence(self, ball_1, ball_2):
        """
        Finds the confidence level of ball_1. Compares area of each color contour, area of each white color contour, and
        the number of white contours found within a region of interest.

        Ranges from -1 to 1. -1 being striped, 0 being uncertain, and 1 being solid.

        Confidence is added and subtracted based on typical differences in each suit. Solid balls will typically have a
        colored area of greater than 200, around 240+. The area of the white area will be around 50ish. The count will be
        either 1 or 0, though in some cases it can be two.

        The number of white contours can be a big difference maker in balls that have very similar colored areas and white
        areas. Thus, if confidence is low (between -.1 and .1), confidence given is more generous than if the bot is already
        more certain which ball is solid/striped.

        The areas of colored area and white area can result in misidentification. Sometimes a striped ball will have a
        larger colored area and smaller white area. However, if this striped ball has two white areas, and the solid ball
        only has 1/0,  the confidence that is given is multiplied by the ratio of the colored area to the white area in
        order to combat misidentification. In the cases where the "bot" is completely accurate in its assessment, multiplying
        by the color ratio, will only emphasize its decision even more, although it's capped at -1 and 1.

        :param ball_1: ball_1 from ballOutline
        :param ball_2: ball_2 from ballOutline
        :return: float - -1 to 1 - confidence level of ball_1
        """
        confidence = 0.0 #-1 to 1: -1 being striped - 1 being solid

        area1 = ball_1[2]
        whiteArea1 = ball_1[3]
        whiteCount1 = ball_1[4]
        if ball_1[3] == 0:
            colorRatio1 = 9999
        else:
            colorRatio1 = ball_1[2] / ball_1[3]

        area2 = ball_2[2]
        whiteArea2 = ball_2[3]
        whiteCount2 = ball_2[4]
        if ball_2[3] == 0:
            colorRatio2 = 9999
        else:
            colorRatio2 = ball_2[2] / ball_2[3]

        aDifference = area1-area2
        if aDifference >= 50:
            confidence += 0.25
        else:
            if aDifference > 0:
                confidence += (aDifference/50) * 0.25
            else:
                if aDifference <= -50:
                    confidence = -0.25
                else:
                    confidence += math.fabs(aDifference/50) * -0.25

        whiteDifference = whiteArea1 - whiteArea2
        if whiteDifference >= 50:
            confidence += -0.25
        else:
            if whiteDifference > 0:
                confidence += (whiteDifference/50) * -0.25
            else:
                if whiteDifference <= -50:
                    confidence += 0.25
                else:
                    confidence += math.fabs(whiteDifference/50) * 0.25

        whiteRatio = (min(whiteArea1, whiteArea2) / max(whiteArea1, whiteArea2))

        if whiteCount1 > whiteCount2:
            if 0.10 > confidence > -0.10:
                confidence += -0.5
            else:
                if confidence == -0.50:
                    confidence += (math.fabs(whiteDifference/ 100)* colorRatio2 * whiteRatio) * -0.25
                else:
                    confidence += (math.fabs(whiteDifference / 100)* colorRatio2 * whiteRatio) * -0.5
        elif whiteCount1 < whiteCount2:
            if 0.10 > confidence > -0.10:
                confidence += 0.5
            else:
                if math.fabs(confidence) > 0.45:
                    confidence += (math.fabs(whiteDifference / 100)* colorRatio1 * whiteRatio) * 0.25
                else:
                    confidence += (math.fabs(whiteDifference / 100) * colorRatio1 * whiteRatio) * 0.5

        if confidence > 1:
            confidence = 1
        elif confidence < -1:
            confidence = -1

        print("confidence value: {}".format(confidence))
        print(ball_1, ball_2)

        return confidence

    def contourSetup(self, mask, sort=True):
        """
        Allows for creation of list of contours without repeating constantly. Can return unsorted list or sorted list.

        :param mask: numpy array of mask
        :param sort: boolean - True to return sorted list - default is sorted list
        :return: sorted/unsorted list
        """
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if imutils.is_cv2() else contours[1]

        if sort is True:
            contours = sorted(contours, key=cv2.contourArea)

        return contours

    def roi(self, img, center, radius):
        """
        Creates a mask around region of interest.

        :param img: image to combine mask with
        :param center: tuple of point to center region around
        :param radius: how far around the point the region should go
        :return: mask with only region of interest
        """
        mask = np.zeros_like(img)
        cv2.circle(mask, center, radius, (255, 255, 255), -1)
        masked = cv2.bitwise_and(img, mask)
        return masked

    def whiteMaskedArea(self, contours, count, min):
        """
        Adds up total area of white mask areas and adds up the count of how many contours there are above a minimum.

        :param contours:
        :param count:
        :param min:
        :return:
        """
        whiteArea = 0
        whiteCount = 0
        for c in contours:
            carea = cv2.contourArea(c)
            whiteCount += 1
            if carea > min:
                whiteArea += carea

        if count is True:
            return whiteArea, whiteCount
        else:
            return whiteArea

    def matchHoughCircleToMask(self, pointList, center, closest, max):
        for k2, p in enumerate(pointList):
            dist = math.sqrt((p[0] - center[0]) ** 2 + (p[1] - center[1]) ** 2)

            if dist < max and dist < closest[1]:
                closest = (k2, dist)

        return closest

    def backUpCenter(self, contours, maskwhite):
        ball_1 = (0, 0, 0, 0, 0, 0)
        for c in contours:
            carea = cv2.contourArea(c)
            (x, y), radius = cv2.minEnclosingCircle(c)
            if carea > 30 and carea > ball_1[2]:
                center = self.roundTuple((x,y))

                roiMask1 = self.roi(maskwhite, center, 10)
                contours1 = cv2.findContours(roiMask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours1 = contours1[0] if imutils.is_cv2() else contours1[1]

                whiteArea = 0
                whiteCount = 0
                for c1 in contours1:
                    c1area = cv2.contourArea(c1)
                    whiteCount += 1
                    if c1area > 0:
                        whiteArea += c1area

                ball_1 = (center[0], center[1], carea, whiteArea, whiteCount, center)

        return ball_1

    def drawStripe(self, center, colorRGB):
        cv2.circle(self.roundImage, self.tupleToInt(center), 9, colorRGB, 2)
        cv2.circle(self.roundImage, self.tupleToInt(center), 10, (0, 0, 0), 1)
        cv2.line(self.roundImage, self.tupleToInt((center[0], center[1] + 10)), self.tupleToInt((center[0], center[1] - 10)), (0, 0, 0))
        cv2.line(self.roundImage, self.tupleToInt((center[0] - 10, center[1])), self.tupleToInt((center[0] + 10, center[1])), (0, 0, 0))

    def drawSolid(self, center, colorRGB):
        cv2.circle(self.roundImage, self.tupleToInt((center[0], center[1])), 10, colorRGB, -1)
        cv2.circle(self.roundImage, self.tupleToInt((center[0], center[1])), 10, (0, 0, 0), 1)
        cv2.line(self.roundImage, self.tupleToInt((center[0], center[1] + 10)), self.tupleToInt((center[0], center[1] - 10)), (255, 255, 255))
        cv2.line(self.roundImage, self.tupleToInt((center[0] - 10, center[1])), self.tupleToInt((center[0] + 10, center[1])), (255, 255, 255))

    def savePic(self):
        imgpath = "games/game" + self.gameNum + "/outlined"
        imgname = "pooltable" + str(self.turnNum) + ".png"
        cv2.imwrite(os.path.join(imgpath, imgname), self.roundImage)

    ##############################################################################################################

    def queryDirectShot(self):
        for b in self.ballList:
            if b.name == "cueball":
                if b.center == (0, 0):
                    print("Position of cueball unknown.")
                    return False
                else:
                    continue
            elif b.name == "eightball":
                if b.center == (0, 0):
                    print("Position of eightball unknown.")
                    break
                else:
                    count = 0
                    for b2 in self.ballList:
                        if b2.target is True:
                            count += 1

                    if count == 0:
                        b.target = True
                    else:
                        continue

            if b.center == (0, 0):
                print("Position of {} unknown.".format(b.name))
                continue
            else:
                print(b.name)
                if b.target is True and b.pocketed is False:
                    utils.debugPrint("\nQuerying {}..".format(b.name))
                    for name, coord in self.holeLocation.items():
                        b.offsetCurrentHole = coord[0], coord[1]
                        b.currentHole = (
                            b.offsetCurrentHole[0] - self.offset[0], b.offsetCurrentHole[1] - self.offset[1])
                        b.currentHoleName = name

                        holeParams = self.setupHoleParamaters(b)
                        if holeParams is False:
                            print("Hole Param failed.")
                            continue

                        eligible = self.holeEligibility(b)
                        if eligible is False:
                            print("Eligible failed.")
                            continue

                        print("Targeting: {}".format(name))
                        bp = self.setupBallParams(b)
                        if bp is False:
                            print("Ball Param failed.")
                            continue

                        clearpathBall = self.checkPathofBall(b)
                        if clearpathBall is False:
                            print("Path from Ball to Hole not clear.")
                            continue

                        hitp = self.setupHitParams(b)
                        cp = self.setupCueParams(b)
                        if hitp is False or cp is False:
                            print("Hit Param and Cue Param failed.")
                            continue

                        clearpathCue = self.checkPathofCue(b)
                        if clearpathCue is False:
                            print("Path from Cue to Ball not clear.")
                            continue

                        b.angle = self.findAngle(b.currentHole, b.hitPoint, self.cueball)
                        print("angle: {}".format(round(b.angle)))
                        if b.angle < 125:
                            print("Angle failed.")
                            continue

                        self.openCVDrawHoles(b)
                        self.openCVDraw(b)
                        self.savePic()
                        self.chosenBall = b

                        cv2.imshow('round', self.roundImage)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
                else:
                    #utils.debugPrint("Not a target.")
                    continue

    def queryReboundedShot(self, ball):
        pass

    def holeEligibility(self, ball):
        #utils.debugPrint("Determining if pocket is viable target.")
        angle = self.findAngle(self.cueball, ball.center, ball.currentHole)
        print("Hole Eligibility: {} degrees - {}".format(angle, ball.currentHoleName))
        if angle < 125:
            return False
        else:
            return True

    def setupHoleParamaters(self, ball):
        if ball.currentHoleName == "trh.png":
            ball.leftMarkH = ball.currentHole[0] - 32, ball.currentHole[1] + 7
            ball.rightMarkH = ball.currentHole[0] - 9, ball.currentHole[1] + 30
        elif ball.currentHoleName == "tmh.png":
            ball.leftMarkH = ball.currentHole[0] - 20, ball.currentHole[1] + 9
            ball.rightMarkH = ball.currentHole[0] + 20, ball.currentHole[1] + 9
        elif ball.currentHoleName == "tlh.png":
            ball.leftMarkH = ball.currentHole[0] + 9, ball.currentHole[1] + 30
            ball.rightMarkH = ball.currentHole[0] + 32, ball.currentHole[1] + 7
        elif ball.currentHoleName == "blh.png":
            ball.leftMarkH = ball.currentHole[0] + 32, ball.currentHole[1] - 9
            ball.rightMarkH = ball.currentHole[0] + 9, ball.currentHole[1] - 32
        elif ball.currentHoleName == "bmh.png":
            ball.leftMarkH = ball.currentHole[0] + 20, ball.currentHole[1] - 9
            ball.rightMarkH = ball.currentHole[0] - 20, ball.currentHole[1] - 9
        else:
            ball.leftMarkH = ball.currentHole[0] - 9, ball.currentHole[1] - 32
            ball.rightMarkH = ball.currentHole[0] - 32, ball.currentHole[1] - 9

        ball.currentHole = self.averagePoint(ball.leftMarkH, ball.rightMarkH)

        ball.distanceToHole = self.measureDistance(ball.center, ball.currentHole)
        ball.slopeToHoleRise, ball.slopeToHoleRun, ball.slopeToHole = self.findRiseRunSlope(ball.currentHole, ball.center)
        ball.perpSlopeH = (-1 / ball.slopeToHole)

        ball.holeGapSlopeRise, ball.holeGapSlopeRun, ball.holeGapSlope = self.findRiseRunSlope(ball.leftMarkH,
                                                                                               ball.rightMarkH)
        if "t" in ball.currentHoleName:
            ball.innerBoundLeft, ball.innerBoundRight = self.findPointsAlongSlope(ball.leftMarkH, ball.rightMarkH,
                                                                                    ball.holeGapSlope)
        else:
            ball.innerBoundLeft, ball.innerBoundRight = self.findPointsAlongSlope(ball.leftMarkH, ball.rightMarkH,
                                                                                  ball.holeGapSlope, True)

    def setupBallParams(self,ball):
        # creates points to the left and right of ball relative to the slope to the hole

        if ball.slopeToHoleRise < 0:
            if ball.slopeToHoleRun < 0:
                ball.leftMarkB1 = (ball.center[0] - (10 * math.sqrt(1 / (1 + ball.perpSlopeH ** 2)))), (
                            ball.center[1] - ((ball.perpSlopeH * 10) * math.sqrt(1 / (1 + ball.perpSlopeH ** 2))))
                ball.rightMarkB1 = (ball.center[0] + (10 * math.sqrt(1 / (1 + ball.perpSlopeH ** 2)))), (
                            ball.center[1] + ((ball.perpSlopeH * 10) * math.sqrt(1 / (1 + ball.perpSlopeH ** 2))))
            else:
                ball.leftMarkB1 = (ball.center[0] - (10 * math.sqrt(1 / (1 + ball.perpSlopeH ** 2)))), (
                        ball.center[1] - ((ball.perpSlopeH * 10) * math.sqrt(1 / (1 + ball.perpSlopeH ** 2))))
                ball.rightMarkB1 = (ball.center[0] + (10 * math.sqrt(1 / (1 + ball.perpSlopeH ** 2)))), (
                        ball.center[1] + ((ball.perpSlopeH * 10) * math.sqrt(1 / (1 + ball.perpSlopeH ** 2))))
        else:
            if ball.slopeToHoleRun < 0:
                ball.leftMarkB1 = (ball.center[0] + (10 * math.sqrt(1 / (1 + ball.perpSlopeH ** 2)))), (
                            ball.center[1] + ((ball.perpSlopeH * 10) * math.sqrt(1 / (1 + ball.perpSlopeH ** 2))))
                ball.rightMarkB1 = (ball.center[0] - (10 * math.sqrt(1 / (1 + ball.perpSlopeH ** 2)))), (
                            ball.center[1] - ((ball.perpSlopeH * 10) * math.sqrt(1 / (1 + ball.perpSlopeH ** 2))))
            else:
                ball.leftMarkB1 = (ball.center[0] + (10 * math.sqrt(1 / (1 + ball.perpSlopeH ** 2)))), (
                        ball.center[1] + ((ball.perpSlopeH * 10) * math.sqrt(1 / (1 + ball.perpSlopeH ** 2))))
                ball.rightMarkB1 = (ball.center[0] - (10 * math.sqrt(1 / (1 + ball.perpSlopeH ** 2)))), (
                        ball.center[1] - ((ball.perpSlopeH * 10) * math.sqrt(1 / (1 + ball.perpSlopeH ** 2))))

        if ball.slopeToHoleRise < 0:
            if ball.slopeToHoleRun > 0:
                x = (ball.center[0] - (20 * math.sqrt(1 / (1 + ball.slopeToHole ** 2))))
                y = (ball.center[1] - (
                        (ball.slopeToHole * 20) * math.sqrt(1 / (1 + ball.slopeToHole ** 2))))
            else:
                x = (ball.center[0] + (20 * math.sqrt(1 / (1 + ball.slopeToHole ** 2))))
                y = (ball.center[1] + (
                        (ball.slopeToHole * 20) * math.sqrt(1 / (1 + ball.slopeToHole ** 2))))

            ball.hitPoint = self.roundTuple((x, y))
        else:
            if ball.slopeToHoleRun < 0:
                x = (ball.center[0] + (20 * math.sqrt(1 / (1 + ball.slopeToHole ** 2))))
                y = (ball.center[1] + (
                        (ball.slopeToHole * 20) * math.sqrt(1 / (1 + ball.slopeToHole ** 2))))
            else:
                x = (ball.center[0] - (20 * math.sqrt(1 / (1 + ball.slopeToHole ** 2))))
                y = (ball.center[1] - (
                        (ball.slopeToHole * 20) * math.sqrt(1 / (1 + ball.slopeToHole ** 2))))

            ball.hitPoint = self.tupleToInt((x, y))

        return True

    def setupHitParams(self, ball):
        ball.distanceToHP = self.measureDistance(ball.hitPoint, self.cueball)
        ball.slopeToHPRise, ball.slopeToHPRun, ball.slopeToHP = self.findRiseRunSlope(self.cueball, ball.hitPoint)
        if ball.slopeToHP != 0:
            ball.perpSlopeHP = (-1 / ball.slopeToHP)
        else:
            ball.perpSlopeHP = 0

        if ball.slopeToHole < 0:
            if ball.slopeToHP < 0:
                #print("hp1")
                ball.leftMarkB2 = (ball.hitPoint[0] - (
                        10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (ball.hitPoint[1] - (
                        (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
                ball.rightMarkB2 = (ball.hitPoint[0] + (
                        10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (ball.hitPoint[1] + (
                        (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
            else:
                #print("hp2")
                ball.leftMarkB2 = (ball.hitPoint[0] + (
                        10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (ball.hitPoint[1] + (
                        (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
                ball.rightMarkB2 = (ball.hitPoint[0] - (
                        10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (ball.hitPoint[1] - (
                        (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
        elif ball.slopeToHole > 0:
            if ball.slopeToHP < 0:
                #print("hp3")
                ball.leftMarkB2 = (ball.hitPoint[0] - (
                        10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (ball.hitPoint[1] - (
                        (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
                ball.rightMarkB2 = (ball.hitPoint[0] + (
                        10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (ball.hitPoint[1] + (
                        (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
            else:
                #print("hp4")
                ball.leftMarkB2 = (ball.hitPoint[0] + (
                        10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (ball.hitPoint[1] + (
                        (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
                ball.rightMarkB2 = (ball.hitPoint[0] - (
                        10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (ball.hitPoint[1] - (
                        (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))

        return True

    def setupCueParams(self, ball):
        # creates point to left and right of center of cue to check to see if any
        # ball falls in area between cue and ball
        ball.distancetoCue = self.measureDistance(self.cueball, ball.center)
        ball.slopetoCueRun, ball.slopetoCueRise, ball.slopetoCue = self.findRiseRunSlope(self.cueball,ball.center)
        ball.perpSlopeC = (-1 / ball.slopetoCue)

        if ball.slopeToHP < 0:
            #print("c1")
            ball.leftMarkC = (self.cueball[0] - (10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (
                    self.cueball[1] - (
                (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
            ball.rightMarkC = (self.cueball[0] + (10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (
                    self.cueball[1] + (
                (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
            if ball.slopeToHPRise < 0:
                print(1)
                ball.hitPointStart = ((ball.hitPoint[0] - (
                        20 * math.sqrt(1 / (1 + ball.slopeToHP ** 2)))), (ball.hitPoint[1] - (
                        (ball.slopeToHP * 20) * math.sqrt(1 / (1 + ball.slopeToHP ** 2)))))
            else:
                print(2)
                ball.hitPointStart = ((ball.hitPoint[0] + (
                        20 * math.sqrt(1 / (1 + ball.slopeToHP ** 2)))), (ball.hitPoint[1] + (
                        (ball.slopeToHP * 20) * math.sqrt(1 / (1 + ball.slopeToHP ** 2)))))
        elif ball.slopeToHP > 0:
            #print("c2")
            ball.leftMarkC = (self.cueball[0] + (
                    10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (self.cueball[1] + (
                    (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
            ball.rightMarkC = (self.cueball[0] - (
                    10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (self.cueball[1] - (
                    (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
            if ball.slopeToHPRise < 0:
                print(3)
                ball.hitPointStart = ((ball.hitPoint[0] + (
                        20 * math.sqrt(1 / (1 + ball.slopeToHP ** 2)))), (ball.hitPoint[1] + (
                        (ball.slopeToHP * 20) * math.sqrt(1 / (1 + ball.slopeToHP ** 2)))))
            else:
                print(4)
                ball.hitPointStart = ((ball.hitPoint[0] - (
                        20 * math.sqrt(1 / (1 + ball.slopeToHP ** 2)))), (ball.hitPoint[1] - (
                        (ball.slopeToHP * 20) * math.sqrt(1 / (1 + ball.slopeToHP ** 2)))))
        else:
            ball.leftMarkC = (self.cueball[0] + (
                    10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (self.cueball[1] + (
                    (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
            ball.rightMarkC = (self.cueball[0] - (
                    10 * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2)))), (self.cueball[1] - (
                    (ball.perpSlopeHP * 10) * math.sqrt(1 / (1 + ball.perpSlopeHP ** 2))))
            if ball.slopeToHPRise == 0:
                print(5)
                if ball.slopeToHPRun > 0:
                    ball.hitPointStart = (ball.hitPoint[0] + 20, ball.hitPoint[1])
                else:
                    ball.hitPointStart = (ball.hitPoint[0] - 20, ball.hitPoint[1])
            else:
                print(6)
                if ball.slopeToHPRise > 0:
                    ball.hitPointStart = (ball.hitPoint[0], ball.hitPoint[1] + 20)
                else:
                    ball.hitPointStart = (ball.hitPoint[0], ball.hitPoint[1] - 20)


        return True

    def roundTuple(self, tuple):
        return (round(tuple[0]),round(tuple[1]))

    def tupleToInt(self, tuple):
        return (int(tuple[0]),int(tuple[1]))

    def averagePoint(self, p1, p2):
        return ((p1[0] + p2[0])/2,(p1[1] + p2[1])/2)

    def findRiseRunSlope(self, p1, p2):
        rise = float(p1[1]) - float(p2[1])
        run = float(p1[0]) - float(p2[0])
        if run != 0:
            slope = rise / run
        else:
            slope = 0

        return rise, run, slope

    def findPointsAlongSlope(self, p1, p2, slope, invert=False):
        if invert is False:
            left = (p1[0] + (10 * math.sqrt(1 / (1 + slope ** 2)))), (p1[1] + ((slope * 10) * math.sqrt(1 / (1 + slope ** 2))))
            right = (p2[0] - (10 * math.sqrt(1 / (1 + slope ** 2)))), (p2[1] - ((slope * 10) * math.sqrt(1 / (1 + slope ** 2))))
        else:
            left = (p1[0] - (10 * math.sqrt(1 / (1 + slope ** 2)))), (p1[1] - ((slope * 10) * math.sqrt(1 / (1 + slope ** 2))))
            right = (p2[0] + (10 * math.sqrt(1 / (1 + slope ** 2)))), (p2[1] + ((slope * 10) * math.sqrt(1 / (1 + slope ** 2))))

        return left, right

    def checkPathofBall(self, ball):
        utils.debugPrint("Checking Path of Ball to Hole.")
        holePoint = ((ball.innerBoundLeft[0] + ball.innerBoundRight[0])/2, (ball.innerBoundLeft[1] + ball.innerBoundRight[1])/2)
        angle = self.findAngle(holePoint, ball.center, (ball.center[0], holePoint[1]))
        if ball.slopeToHP < 0:
            angle = -angle

        newHolePoint = self.rotateAround(ball.center, holePoint, angle)


        tempPoints = []
        for b in self.ballList:
            if b.name == ball.name:
                continue
            else:
                newBallCenter = self.rotateAround(ball.center, b.center, angle)
                tempPoints.append((b.name, newBallCenter))

        #bounding box
        minX = min(newHolePoint[0] - 20, newHolePoint[0] + 20, ball.center[0] - 20, ball.center[0] + 20)
        maxX = max(newHolePoint[0] - 20, newHolePoint[0] + 20, ball.center[0] - 20, ball.center[0] + 20)
        minY = min(newHolePoint[1] - 20, newHolePoint[1] + 20, ball.center[1] - 20, ball.center[1] + 20)
        maxY = max(newHolePoint[1] - 20, newHolePoint[1] + 20, ball.center[1] - 20, ball.center[1] + 20)

        for p in tempPoints:
            if p[0] != ball.name:
                if p[1][0] > minX and p[1][0] < maxX and p[1][1] < maxY and p[1][1] > minY:
                    print("ball is in the way", p[0])
                    return False

        return True

    def checkPathofCue(self, ball):
        utils.debugPrint("Checking Path of Cue to Ball.")
        angle = self.findAngle(self.cueball, ball.hitPoint, (ball.hitPoint[0], self.cueball[1]))
        if ball.slopeToHP < 0:
            angle = -angle
        newCuePoint = self.rotateAround(ball.hitPoint, self.cueball, angle)


        tempPoints = []
        for b in self.ballList:
            if b == ball:
                continue
            else:
                newBallCenter = self.rotateAround(ball.hitPoint, b.center, angle)
                tempPoints.append((b.name, newBallCenter))

        # bounding box
        minX = min(newCuePoint[0] - 20, newCuePoint[0] + 20, ball.hitPoint[0] - 20, ball.hitPoint[0] + 20)
        maxX = max(newCuePoint[0] - 20, newCuePoint[0] + 20, ball.hitPoint[0] - 20, ball.hitPoint[0] + 20)
        minY = min(newCuePoint[1] - 20, newCuePoint[1] + 20, ball.hitPoint[1] - 20, ball.hitPoint[1] + 20)
        maxY = max(newCuePoint[1] - 20, newCuePoint[1] + 20, ball.hitPoint[1] - 20, ball.hitPoint[1] + 20)

        for p in tempPoints:
            if p[0] != "cueball" and p[0] != ball.name:
                if p[1][0] > minX and p[1][0] < maxX and p[1][1] < maxY and p[1][1] > minY:
                    print("ball is in the way", p[0])
                    return False

        return True

    def findAngle(self, p1, p2, p3):
        a = self.measureDistance(p1, p2)
        b = self.measureDistance(p2, p3)
        c = self.measureDistance(p3, p1)
        try:
            angle = math.degrees(math.acos((c ** 2 - b ** 2 - a ** 2) / (-2.0 * a * b)))
        except ZeroDivisionError:
            return 90.0

        return angle

    def measureDistance(self, firstInput, secondInput):
        dist = math.sqrt((int(secondInput[0]) - int(firstInput[0])) ** 2 + (int(secondInput[1]) - int(firstInput[1])) ** 2)
        return dist

    def rotateAround(self, anchor, point, angle):
        angle = math.radians(angle)
        s = math.sin(angle)
        c = math.cos(angle)

        pX = int(point[0]) - int(anchor[0])
        pY = int(point[1]) - int(anchor[1])

        newX = (pX * c - pY * s) + anchor[0]
        newY = (pX * s + pY * c) + anchor[1]

        center = self.tupleToInt((newX, newY))

        return center

    def frange(self, start, end=None, inc=None):
        if end is None:
            end = start + 0.0
            start = 0.0
        else:
            start += 0.0

        if inc is None:
            inc = 1.0

        count = int((end - start) / inc)
        if start + count * inc != end:
            count += 1

        L = [0, ] * count
        for i in range(count):
            L[i] = start + i * inc

        return L

    def openCVDrawHoles(self, ball):
        cv2.circle(self.roundImage, self.tupleToInt(ball.innerBoundLeft), 1,(3, 202, 252), -1)
        cv2.circle(self.roundImage, self.tupleToInt(ball.innerBoundRight), 1,(199, 18, 27), -1)

        cv2.circle(self.roundImage, self.tupleToInt(ball.leftMarkH), 1,(235, 186, 25), -1)
        cv2.circle(self.roundImage, self.tupleToInt(ball.rightMarkH), 1,(199, 18, 27), -1)

    def openCVDraw(self, ball):
        cv2.circle(self.roundImage, self.tupleToInt(ball.hitPoint), 9, (0, 0, 0), 1)
        cv2.line(self.roundImage, self.tupleToInt(ball.currentHole),self.tupleToInt(ball.hitPoint),(0, 0, 0), 1)
        cv2.line(self.roundImage, self.tupleToInt(ball.hitPoint), self.tupleToInt(self.cueball),(0, 0, 0), 1)
        cv2.line(self.roundImage, self.tupleToInt(ball.leftMarkH), self.tupleToInt(ball.leftMarkB1), (235, 186, 25), 1)
        cv2.line(self.roundImage, self.tupleToInt(ball.rightMarkH), self.tupleToInt(ball.rightMarkB1),(199, 18, 27), 1)
        cv2.line(self.roundImage, self.tupleToInt(ball.leftMarkB2), self.tupleToInt(ball.leftMarkC), (3, 202, 252), 1)
        cv2.line(self.roundImage, self.tupleToInt(ball.rightMarkB2), self.tupleToInt(ball.rightMarkC),(52, 52, 235), 1)
        cv2.line(self.roundImage, self.tupleToInt(ball.leftMarkB1), self.tupleToInt(ball.rightMarkB1),(255, 0, 0), 1)
        cv2.line(self.roundImage, self.tupleToInt(ball.leftMarkB2), self.tupleToInt(ball.rightMarkB2),(255, 255, 255), 1)

    def hitBall(self, ball):
        utils.debugPrint("Hitting ball.")

        self.powerAmount(ball)

        if ball.slopeToHP > 0:
            if ball.slopeToHPRise > 0:
                ball.hitPoint = (ball.hitPoint[0] - 2, ball.hitPoint[1] - 2)
            else:
                ball.hitPoint = (ball.hitPoint[0] + 2, ball.hitPoint[1] + 2)
        else:
            if ball.slopeToHPRise > 0:
                ball.hitPoint = (ball.hitPoint[0] - 2, ball.hitPoint[1] - 2)
            else:
                ball.hitPoint = (ball.hitPoint[0] + 2, ball.hitPoint[1] + 2)

        pyautogui.moveTo((ball.hitPoint[0] + self.offset[0], ball.hitPoint[1] + self.offset[1]))
        #time.sleep(90)
        pyautogui.dragTo((ball.hitPointEnd[0] + self.offset[0], ball.hitPointEnd[1] + self.offset[1]),
                         button="left", duration=1)

        cv2.circle(self.roundImage, self.tupleToInt(ball.hitPoint), 3, (0, 0, 255), -1)
        cv2.circle(self.roundImage, self.tupleToInt(ball.hitPointStart), 3, (0, 0, 255), -1)
        cv2.circle(self.roundImage, self.tupleToInt(ball.hitPointEnd), 2, (0, 100, 255),-1)
        self.savePic()

    def powerAmount(self, ball):
        velocity = 2324

        ratioCue = ball.distancetoCue / 664.0
        ratioBall = ball.distanceToHole / 664.0
        ratio = ratioCue + ratioBall
        if ratio < 1.0:
            distance = (ratio * 336) * 1.5
        else:
            distance = 336

        velocity = ratio * velocity

        print(ratioCue, ratioBall, ratio, velocity)


        if ball.slopeToHP > 0:
            if ball.slopeToHPRise > 0:
                print(111)
                x = (ball.hitPointStart[0] + (distance * math.sqrt(1 / (1 + ball.slopeToHP ** 2))))
                y = (ball.hitPointStart[1] + ((ball.slopeToHP * distance) * math.sqrt( 1 / (1 + ball.slopeToHP ** 2))))
            else:
                print(222)
                x = (ball.hitPointStart[0] - (distance * math.sqrt(1 / (1 + ball.slopeToHP ** 2))))
                y = (ball.hitPointStart[1] - ((ball.slopeToHP * distance) * math.sqrt(1 / (1 + ball.slopeToHP ** 2))))

            ball.hitPointEnd = (x, y)
        elif ball.slopeToHP < 0:
            if ball.slopeToHPRise > 0:
                print(333)
                x = (ball.hitPointStart[0] - (distance * math.sqrt(1 / (1 + ball.slopeToHP ** 2))))
                y = (ball.hitPointStart[1] - ((ball.slopeToHP * distance) * math.sqrt(1 / (1 + ball.slopeToHP ** 2))))
            else:
                print(444)
                x = (ball.hitPointStart[0] + (distance * math.sqrt(1 / (1 + ball.slopeToHP ** 2))))
                y = (ball.hitPointStart[1] + ((ball.slopeToHP * distance) * math.sqrt(1 / (1 + ball.slopeToHP ** 2))))

            ball.hitPointEnd = (x, y)
        else:
            if ball.slopeToHPRise == 0:
                print(555)
                x = (ball.hitPointStart[0] + distance)
                y = ball.hitPointStart[1]
            else:
                print(666)
                x = ball.hitPointStart[0]
                y = (ball.hitPointStart[1] - distance)

            ball.hitPointEnd = (x, y)
        #ball.stats()

    def moveMouseOut(self):  # moves ball tracer out of the way as much as possible. checks for empty areas
        rails = [constants.img_topRail, constants.img_bottomRail, constants.img_leftRail, constants.img_rightRail]

        for r in rails:
            pos = utils.imageSearch(r, self.poolRegion, confidence=.95)
            if pos is not None:
                pyautogui.moveTo(pos)
                count = self.quickBallCount()
                if count is True:
                    break


    def quickBallCount(self):
        # add line to make sure turn timer not blocked
        for b in self.ballList:
            contours = cv2.findContours(b.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if imutils.is_cv2() else contours[1]
            if len(contours) < 1:
                print("Contour of {} not found".format(b.name))
                return False
            else:
                continue

        print("Cue pole not in way of balls.")
        return True
