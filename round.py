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

    def __init__(self, inputTurn, inputGameNum, inputPoolRegion, inputGameWindow):
        self.ballList = []
        self.allBalls = []
        self.suit = None
        self.turnNum = inputTurn
        self.gameNum = inputGameNum
        self.holeLocation = {constants.img_tlh: (0, 0), constants.img_tmh: (0, 0), constants.img_trh: (0, 0), constants.img_blh: (0, 0),
                             constants.img_bmh: (0, 0),
                             constants.img_brh: (0, 0)}
        self.imgPath = "/games/game" + self.gameNum + "/table/pooltable" + str(self.turnNum) + ".png"
        self.roundImage = None
        self.poolRegion = inputPoolRegion
        self.gameWindow = inputGameWindow
        self.chosenBall = None
        self.cueball = (0, 0)

    def start(self):
        cwd = os.getcwd()
        self.imgPath = cwd + self.imgPath

        self.markHoles()

        print("Turn #" + str(self.turnNum))

        self.ballCheck()
        self.outlineBall()

        cfb = self.checkForBreak()
        if cfb is False:
            qB = self.queryBall()
            if qB is True:
                self.hitBall(self.chosenBall)
            else:
                print("Unable to query ball.")

        self.moveMouseOut()

        self.checkRoundOver()
        self.checkGameOver()

    def markHoles(self):
        pyautogui.moveTo(1248, 363)
        time.sleep(.25)
        for k, v in self.holeLocation.items():
            if v is None:
                pos = utils.imageSearch(k, self.poolRegion)
                if pos is not None:
                    self.holeLocation[k] = (pos[0] - 658, pos[1] - 297)
                else:
                    print("Could not find " + k + " hole.")
            else:
                pass

    def checkForBreak(self):
        breakRack = True
        if self.suit == "nosuit":
            print("No suit detected.")

            for b in self.ballList:
                if b.name == "cueball":
                    continue
                elif 529 > b.center[0] > 429 and 212 > b.center[1] > 103:
                    continue
                else:
                    breakRack = False
                    break
        else:
            print("Assigned suit: {}".format(self.suit))
            breakRack = False

        if breakRack is True:
            print("Breaking.")
            randNum = random.randint(0, 10) + 20
            if randNum > 5:
                pyautogui.moveTo(self.cueball[0] + 848, self.cueball[1] + 297)
                pyautogui.dragTo(self.cueball[0] + 658, self.cueball[1] + 297, button="left", duration=.5)
            else:
                print("Randomized Break.")
                x, y = self.cueball[0] + random.randrange(-100, 0), self.cueball[1] - random.randrange(-100, 100)
                pyautogui.moveTo((self.cueball[0] + 658, self.cueball[1] + 297))
                pyautogui.dragTo((x + 658, y + 297), button="left")
                self.cueball = x, y

                return False

        else:
            return False

    def ballCheck(self):
        solids = {constants.img_1ball: "yellow", constants.img_2ball: "blue", constants.img_3ball: "lightred",
                  constants.img_4ball: "purple",
                  constants.img_5ball: "orange", constants.img_6ball: "green", constants.img_7ball: "darkred"}
        stripes = {constants.img_9ball: "yellow", constants.img_10ball: "blue", constants.img_11ball: "lightred",
                   constants.img_12ball: "purple",
                   constants.img_13ball: "orange", constants.img_14ball: "green", constants.img_15ball: "darkred"}

        pyautogui.moveTo(1248, 363)

        while True:
            pos = pyautogui.locateOnScreen(utils.imagePath(constants.img_ballPic1), region=self.gameWindow, confidence=.99)
            if pos is not None:
                topRX = pos[0] + pos[2]
                topRY = pos[1]
                reg = (topRX - 176, topRY, 176, 90)
                break

        self.ballList.append(ball.Ball("nosuit", constants.img_cueball, "white"))
        self.ballList.append(ball.Ball("nosuit", constants.img_eightball, "black"))

        for k, v in solids.items():
            pos = utils.imageSearch(k, reg)
            if pos is not None:
                self.suit = "solid"
                b = ball.Ball("solid", k.replace(".png", ""), v)
                self.ballList.append(b)

        for k, v in stripes.items():
            pos = utils.imageSearch(k, reg)
            if pos is not None:
                self.suit = "stripe"
                b = ball.Ball("stripe", k.replace(".png", ""), v)
                self.ballList.append(b)

        if len(self.ballList) == 2:
            self.suit = "nosuit"
            for k, v in solids.items():
                b = ball.Ball("solid", k.replace(".png", ""), v)
                self.ballList.append(b)

            for k, v in stripes.items():
                b = ball.Ball("stripe", k.replace(".png", ""), v)
                self.ballList.append(b)

    def outlineBall(self):
        self.roundImage = cv2.imread(self.imgPath, 1)

        roundImageCopy = self.roundImage
        hsvRndImg = cv2.cvtColor(roundImageCopy, cv2.COLOR_BGR2HSV)

        blueTableLow = np.array([70, 0, 0])
        blueTableHigh = np.array([105, 255, 255])
        tableInvertMask = cv2.bitwise_not(cv2.inRange(hsvRndImg, blueTableLow, blueTableHigh))
        tableInvertMask = cv2.bitwise_and(roundImageCopy, roundImageCopy, mask=tableInvertMask)

        cv2.imwrite("temp.png", tableInvertMask)

        tableMaskedOutBW = cv2.imread("temp.png", 0)
        tableMaskedOutBW = cv2.medianBlur(tableMaskedOutBW, 3)

        tableMaskedOut = cv2.imread("temp.png", 1)

        hsvTableMaskedOut = cv2.cvtColor(tableMaskedOut, cv2.COLOR_BGR2HSV)

        for b in self.ballList:
            b.maskSetup(hsvTableMaskedOut)
            contours = cv2.findContours(b.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if imutils.is_cv2() else contours[1]
            contours = sorted(contours, key=cv2.contourArea)
            if b.name == "cueball" or b.name == "eightball":
                contours = contours[len(contours) - 1:len(contours)]
            else:
                contours = contours[len(contours) - 2:len(contours)]

            ball_1 = None
            ball_2 = None
            for c in contours:
                carea = cv2.contourArea(c)
                if carea > 15:
                    (x, y), radius = cv2.minEnclosingCircle(c)
                    center = (int(x), int(y))
                    b = cv2.circle(b, center, 10, (170, 0, 255), 1)
                    if ball_1 is None:
                        ball_1 = (center[0], center[1], carea)
                    else:
                        ball_2 = (center[0], center[1], carea)
                else:
                    continue

            circles = cv2.HoughCircles(tableMaskedOutBW, cv2.HOUGH_GRADIENT, .5, 13,
                                       param1=75, param2=9.75, minRadius=15, maxRadius=20)
            circles = np.uint16(np.around(circles))

            for i in circles[0, :]:
                if ball_1 is not None:
                    if math.fabs(i[0] - ball_1[0]) < 6 and math.fabs(i[1] - ball_1[1]) < 6:
                        ball_1 = (i[0], i[1], ball_1[2])
                if ball_2 is not None:
                    if math.fabs(i[0] - ball_2[0]) < 6 and math.fabs(i[1] - ball_2[1]) < 6:
                        ball_2 = (i[0], i[1], ball_2[2])

            if b.name == "cueball" or b.name == "eightball":
                b.center = (ball_1[0], ball_1[1])
                print("ball_1 is cueball or eightball. {}".format((ball_1[0], ball_1[1])))
                self.drawSolid(b.center, b.RGB)
            else:
                if ball_1[2] > ball_2[2]:
                    if b.suit == "solid":
                        b.center = (ball_1[0], ball_1[1])
                        # print("ball_1 is solid. {}".format((ball_1[0],ball_1[1])))
                        self.drawSolid(b.center, b.RGB)
                    else:
                        b.center = (ball_2[0], ball_2[1])
                        # print("ball_2 is stripe. {}".format((ball_2[0],ball_2[1])))
                        self.drawStripe(b.center, b.RGB)
                else:
                    if b.suit == "solid":
                        b.center = (ball_2[0], ball_2[1])
                        # print("ball_1 is stripe. {}".format((ball_1[0],ball_1[1])))
                        self.drawSolid(b.center, b.RGB)
                    else:
                        b.center = (ball_1[0], ball_1[1])
                        # print("ball_2 is solid. {}".format((ball_2[0],ball_2[1])))
                        self.drawStripe(b.center, b.RGB)
                self.allBalls.append(b.center)
                self.savePic()

            cv2.imshow("roundImageMask", roundImageCopy)
            cv2.imshow("ball mask", b.mask)
            cv2.imshow("table invert mask", tableInvertMask)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def roi(self, img, vertices):
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, vertices, (255, 255, 255))
        masked = cv2.bitwise_and(img, mask)
        return masked

    def drawStripe(self, center, colorRGB):
        cv2.circle(self.roundImage, center, 9, (colorRGB[0] - 20, colorRGB[1] - 25, colorRGB[2] - 20), 1)

    def drawSolid(self, center, colorRGB):
        cv2.circle(self.roundImage, center, 9, colorRGB, -1)

    def savePic(self):
        imgpath = "games/game" + self.gameNum + "/outlined"
        imgname = "pooltable" + str(self.turnNum) + ".png"
        cv2.imwrite(os.path.join(imgpath, imgname), self.roundImage)

    def queryBall(self):
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
                    continue
            else:
                if b.center == (0, 0):
                    continue
                else:
                    for name, coord in self.holeLocation.items():
                        b.currentHole = coord[0], coord[1]
                        # print("Hole location is at {}".format(coord))
                        # print("cueball at {}".format(self.cueball))
                        b.currentHoleName = name

                        eligible = self.holeEligibility(b)

                        if eligible is False:
                            continue

                        cp = self.setupCueParams(b)
                        hp = self.setupHoleParams(b, coord)
                        bp = self.setupBallParams(b)

                        if (cp is False) or (hp is False) or (bp is False):
                            continue
                        else:
                            clearpathBall = self.checkPathofBall(b)
                            clearpathCue = self.checkPathofCue(b)

                            print("clearpathBall", clearpathBall, "clearpathCue", clearpathCue)

                            if (clearpathBall is False) or (clearpathCue is False):
                                print("Path not clear.")
                                continue
                            elif (clearpathBall is True) and (clearpathCue is True):
                                break
                            else:
                                continue

                    self.openCVDraw(b)
                    self.savePic()
                    self.chosenBall = b
                    return True

    def openCVDraw(self, ball):
        # print((int(ball.leftMarkH[0]), int(ball.leftMarkH[1])), (int(ball.leftMarkB1[0]), int(ball.leftMarkB1[1])))
        cv2.line(self.roundImage, (int(ball.leftMarkH[0]), int(ball.leftMarkH[1])), (int(ball.leftMarkB2[0]),
                                                                                     int(ball.leftMarkB2[1])),
                 (255, 0, 0), 1)
        cv2.line(self.roundImage, (int(ball.rightMarkH[0]), int(ball.rightMarkH[1])), (int(ball.rightMarkB2[0]),
                                                                                       int(ball.rightMarkB2[1])),
                 (255, 0, 0), 1)
        cv2.line(self.roundImage, (int(ball.leftMarkB2[0]), int(ball.leftMarkB2[1])), (int(ball.leftMarkC[0]),
                                                                                       int(ball.leftMarkC[1])),
                 (0, 255, 0), 2)
        cv2.line(self.roundImage, (int(ball.rightMarkB2[0]), int(ball.rightMarkB2[1])), (int(ball.rightMarkC[0]),
                                                                                         int(ball.rightMarkC[1])),
                 (0, 255, 0), 2)

        cv2.line(self.roundImage, (int(ball.leftMarkB1[0]), int(ball.leftMarkB1[1])), (int(ball.rightMarkB1[0]),
                                                                                       int(ball.rightMarkB1[1])),
                 (255, 0, 0), 2)
        cv2.line(self.roundImage, (int(ball.leftMarkB2[0]), int(ball.leftMarkB2[1])), (int(ball.rightMarkB2[0]),
                                                                                       int(ball.rightMarkB2[1])),
                 (255, 255, 255), 2)

    def measureDistance(self, firstInput, secondInput):
        np.seterr(over="ignore")
        dist = math.sqrt((secondInput[0] - firstInput[0]) ** 2 + (secondInput[1] - firstInput[1]) ** 2)
        print("distance", dist)
        return dist

    def holeEligibility(self, ball):
        if ball.center[0] == 0 and ball.center[1] == 0:
            return False
        else:
            if ball.currentHole[0] < ball.center[0]:  # if hole is to the left of ball
                if ball.currentHole[1] < ball.center[1]:  # if hole is above ball (top of table)
                    if self.cueball[0] > ball.center[0]:
                        if self.cueball[1] > ball.center[1]:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:  # if hole is below ball
                    if self.cueball[0] > ball.center[0]:
                        if self.cueball[1] < ball.center[1]:
                            return True
                        else:
                            return False
                    else:
                        return False
            elif ball.currentHole[0] > ball.center[0]:  # if hole is to the right of ball
                if ball.currentHole[1] < ball.center[1]:  # if hole is above ball (top of table)
                    if self.cueball[0] < ball.center[0]:
                        if self.cueball[1] > ball.center[1]:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:  # if hole is below ball
                    if self.cueball[0] < ball.center[0]:
                        if self.cueball[1] < ball.center[1]:
                            return True
                        else:
                            return False
                    else:
                        return False
            else:  # if hole is directly inline with hole
                pass

    def setupHoleParams(self,
                        currentBall,
                        h):  # creates two points at corners of holes to use to check the area between hole and ball
        try:
            currentBall.distanceToHole = self.measureDistance(currentBall.center, h)
            currentBall.slopeToHoleRise = currentBall.center[1] - h[1]
            currentBall.slopeToHoleRun = currentBall.center[0] - h[0]
            currentBall.slopeToHole = (currentBall.slopeToHoleRise / currentBall.slopeToHoleRun)
            currentBall.perpSlopeH = -1 * (h[0] - currentBall.center[0] / currentBall.center[1] - h[1])
        except Exception:
            print("6")
            return False

        try:
            if currentBall.currentHoleName == "tlh" or "brh":
                currentBall.leftMarkH = currentBall.currentHole[0] + 18, currentBall.currentHole[1] - 6
                currentBall.rightMarkH = currentBall.currentHole[0] - 6, currentBall.currentHole[1] + 18
            elif currentBall.currentHoleName == "blh" or "trh":
                currentBall.leftMarkH = currentBall.currentHole[0] - 6, currentBall.currentHole[1] - 18
                currentBall.rightMarkH = currentBall.currentHole[0] + 18, currentBall.currentHole[1] + 6
            elif currentBall.currentHoleName == "tmh" or "bmh":
                currentBall.leftMarkH = currentBall.currentHole[0] + 18, currentBall.currentHole[1]
                currentBall.rightMarkH = currentBall.currentHole[0] - 18, currentBall.currentHole[1]

        except Exception:
            print(
                "1. Error assigning parameters. {} {} {}".format(currentBall.name, currentBall.color,
                                                                 currentBall.center))
            print(currentBall.center, self.cueball, currentBall.distanceToHole, currentBall.slopeToHoleRise,
                  currentBall.slopeToHoleRun, currentBall.slopeToHole, currentBall.perpSlopeH)
            print(h[0], currentBall.center[0])
            return False

        return True

    def setupBallParams(self,
                        currentBall):  # creates points to the left and right of ball relative to the slope to the hole and slope to the cueball to check if any ball falls in area between hole or cue
        try:
            if currentBall.slopeToHole < 0:
                currentBall.leftMarkB1 = (currentBall.center[0] - (
                        9 * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2)))), (currentBall.center[1] + (
                        (currentBall.slopeToHole * 9) * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
                currentBall.rightMarkB1 = (currentBall.center[0] + (
                        9 * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2)))), (currentBall.center[1] - (
                        (currentBall.slopeToHole * 9) * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
            elif currentBall.slopeToHole > 0:
                currentBall.rightMarkB1 = (currentBall.center[0] + (
                        9 * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2)))), (currentBall.center[1] + (
                        (currentBall.slopeToHole * 9) * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
                currentBall.leftMarkB1 = (currentBall.center[0] - (
                        9 * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2)))), (currentBall.center[1] - (
                        (currentBall.slopeToHole * 9) * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
            else:
                print("slope none or 0")
        except Exception:
            print(
                "2. Error assigning parameters. {} {} {}".format(currentBall.name, currentBall.color,
                                                                 currentBall.center))
            print(currentBall.center, self.cueball, currentBall.distanceToHole, currentBall.slopeToHoleRise,
                  currentBall.slopeToHoleRun, currentBall.slopeToHole, currentBall.perpSlopeH)
            return False

        try:
            if currentBall.slopeToHole < 0:
                currentBall.leftMarkB2 = (currentBall.center[0] - (
                        9 * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2)))), (
                                                 currentBall.center[1] + (
                                                 (currentBall.slopetoCue * 9) * math.sqrt(
                                             1 / (1 + currentBall.slopetoCue ** 2))))
                currentBall.rightMarkB2 = (currentBall.center[0] + (
                        9 * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2)))), (currentBall.center[1] - (
                        (currentBall.slopetoCue * 9) * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2))))
            elif currentBall.slopeToHole > 0:
                currentBall.leftMarkB2 = (currentBall.center[0] - (
                        9 * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2)))), (
                                                 currentBall.center[1] - (
                                                 (currentBall.slopetoCue * 9) * math.sqrt(
                                             1 / (1 + currentBall.slopetoCue ** 2))))
                currentBall.rightMarkB2 = (currentBall.center[0] + (
                        9 * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2)))), (currentBall.center[1] + (
                        (currentBall.slopetoCue * 9) * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2))))
            else:
                print("slope none or 0 - 2")

        except Exception:
            print(
                "3. Error assigning parameters. {} {} {}".format(currentBall.name, currentBall.color,
                                                                 currentBall.center))
            print(currentBall.center, self.cueball, currentBall.distanceToHole, currentBall.slopeToHoleRise,
                  currentBall.slopeToHoleRun, currentBall.slopeToHole, currentBall.perpSlopeH)
            return False

        return True

    def setupCueParams(self,
                       currentBall):  # creates point to left and right of center of cue to check to see if any ball falls in area between cue and ball
        try:
            currentBall.distancetoCue = self.measureDistance(currentBall.center, self.cueball)
            currentBall.slopetoCue = (self.cueball[1] - currentBall.center[1] / self.cueball[0] - currentBall.center[0])
            currentBall.perpSlopeC = -1 * (
                    self.cueball[0] - currentBall.center[0] / self.cueball[1] - currentBall.center[1])
        except Exception:
            print("5")
            return False

        try:
            if currentBall.slopetoCue < 0:
                currentBall.leftMarkC = (self.cueball[0] - (9 * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2)))), (
                        self.cueball[1] + (
                        (currentBall.slopetoCue * 9) * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2))))
                currentBall.rightMarkC = (self.cueball[0] + (9 * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2)))), (
                        self.cueball[1] - (
                        (currentBall.slopetoCue * 9) * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2))))
            elif currentBall.slopetoCue > 0:
                currentBall.leftMarkC = (self.cueball[0] - (9 * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2)))), (
                        self.cueball[1] - (
                        (currentBall.slopetoCue * 9) * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2))))
                currentBall.rightMarkC = (self.cueball[0] + (9 * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2)))), (
                        self.cueball[1] + (
                        (currentBall.slopetoCue * 9) * math.sqrt(1 / (1 + currentBall.slopetoCue ** 2))))
            else:
                print("slope none or 0 - cue")

            return True
        except Exception:
            print(
                "4. Error assigning parameters. {} {} {}".format(currentBall.name, currentBall.color,
                                                                 currentBall.center))
            print(currentBall.center, self.cueball, currentBall.distancetoCue, currentBall.slopetoCue,
                  currentBall.perpSlopeC)
            return False

    def setupSlopeRange(self, currentBall):
        currentBall.leftMarkSlopeH = (currentBall.leftMarkH[1] - currentBall.leftMarkB1[1]) / (
                currentBall.leftMarkH[0] - currentBall.leftMarkB1[0])
        currentBall.rightMarkSlopeH = (currentBall.rightMarkH[1] - currentBall.rightMarkB1[1]) / (
                currentBall.rightMarkH[0] - currentBall.rightMarkB1[0])

        currentBall.leftMarkSlopeC = (currentBall.leftMarkSlopeC[1] - currentBall.leftMarkB2[1]) / (
                currentBall.leftMarkSlopeC[0] - currentBall.leftMarkB2[0])
        currentBall.rightMarkSlopeC = (currentBall.rightMarkSlopeC[1] - currentBall.rightMarkB2[1]) / (
                currentBall.rightMarkSlopeC[0] - currentBall.rightMarkB2[0])

    def checkPathofBall(self, currentBall):
        # print("Checking Path of Ball to Hole.")
        for b in self.allBalls:
            if b == currentBall.center:
                continue
            else:
                if currentBall.slopeToHole < 0:
                    for x in self.frange(currentBall.leftMarkH[0], currentBall.leftMarkB1[0],
                                         1):
                        for y in self.frange(currentBall.leftMarkH[1], currentBall.leftMarkB1[1],
                                             1):
                            if b[0] == x and b[1] > y + 5:
                                print("Found ball in range. {}".format(b))
                                for x2 in self.frange(currentBall.rightMarkH[0], currentBall.rightMarkB1[0],
                                                      currentBall.rightMarkSlopeH):
                                    for y2 in self.frange(currentBall.rightMarkH[1], currentBall.rightMarkB1[1],
                                                          1):
                                        if b[0] == x2 and b[1] < y2 - 5:
                                            print("Found ball in the way. {}".format(b))
                                            return False
                                        else:
                                            continue
                            else:
                                continue
                    return True
                elif currentBall.slopeToHole > 0:
                    for x in self.frange(currentBall.leftMarkH[0], currentBall.leftMarkB1[0],
                                         1):
                        for y in self.frange(currentBall.leftMarkH[1], currentBall.leftMarkB1[1],
                                             1):
                            if b[0] == x and b[1] < y + 5:
                                print("Found ball in range. {}".format(b))
                                for x2 in self.frange(currentBall.rightMarkH[0], currentBall.rightMarkB1[0],
                                                      1):
                                    for y2 in self.frange(currentBall.rightMarkH[1], currentBall.rightMarkB1[1],
                                                          1):
                                        if b[0] == x2 and b[1] > y2 - 5:
                                            print("Found ball in the way. {}".format(b))
                                            return False
                                        else:
                                            continue
                            else:
                                continue
                    return True
                else:
                    for x in self.frange(currentBall.leftMarkH[0], currentBall.leftMarkB1[0], 1):
                        for y in self.frange(currentBall.leftMarkH[1], currentBall.leftMarkB1[1], 1):
                            if b[0] > x - 5 and b[1] == y:
                                print("Found ball in range. {}".format(b))
                                for x2 in self.frange(currentBall.rightMarkH[0], currentBall.rightMarkB1[0], 1):
                                    for y2 in self.frange(currentBall.rightMarkH[1], currentBall.rightMarkB1[1], 1):
                                        if b[0] < x2 + 5 and b[1] == y2:
                                            print("Found ball in the way. {}".format(b))
                                            return False
                                        else:
                                            continue
                            else:
                                continue
                    return True

    def checkPathofCue(self, currentBall):
        # print("Checking Path of Ball to Cue.")
        for b in self.allBalls:
            if b == currentBall.center:
                continue
            else:
                if currentBall.slopeToHole < 0:
                    for x in self.frange(currentBall.leftMarkH[0], currentBall.leftMarkB1[0],
                                         1):
                        for y in self.frange(currentBall.leftMarkH[1], currentBall.leftMarkB1[1],
                                             1):
                            if b[0] == x and b[1] > y + 5:
                                print("Found ball in range. {}".format(b))
                                for x2 in self.frange(currentBall.rightMarkH[0], currentBall.rightMarkB1[0],
                                                      1):
                                    for y2 in self.frange(currentBall.rightMarkH[1], currentBall.rightMarkB1[1],
                                                          1):
                                        if b[0] == x2 and b[1] < y2 - 5:
                                            print("Found ball in the way. {}".format(b))
                                            return False
                                        else:
                                            continue
                            else:
                                continue
                    return True

                elif currentBall.slopeToHole > 0:
                    for x in self.frange(currentBall.leftMarkH[0], currentBall.leftMarkB1[0],
                                         1):
                        for y in self.frange(currentBall.leftMarkH[1], currentBall.leftMarkB1[1],
                                             1):
                            if b[0] == x and b[1] < y + 5:
                                print("Found ball in range. {}".format(b))
                                for x2 in self.frange(currentBall.rightMarkH[0], currentBall.rightMarkB1[0],
                                                      1):
                                    for y2 in self.frange(currentBall.rightMarkH[1], currentBall.rightMarkB1[1],
                                                          1):
                                        if b[0] == x2 and b[1] > y2 - 5:
                                            print("Found ball in the way. {}".format(b))
                                            return False
                                        else:
                                            continue
                            else:
                                continue
                    return True
                else:
                    for x in self.frange(currentBall.leftMarkH[0], currentBall.leftMarkB1[0], 1):
                        for y in self.frange(currentBall.leftMarkH[1], currentBall.leftMarkB1[1], 1):
                            if b[0] > x - 5 and b[1] == y:
                                print("Found ball in range. {}".format(b))
                                for x2 in self.frange(currentBall.rightMarkH[0], currentBall.rightMarkB1[0], 1):
                                    for y2 in self.frange(currentBall.rightMarkH[1], currentBall.rightMarkB1[1], 1):
                                        if b[0] < x2 + 5 and b[1] == y2:
                                            print("Found ball in the way. {}".format(b))
                                            return False
                                        else:
                                            continue
                            else:
                                continue
                    return True

    def frange(self, start, end=None, inc=None):
        # gotten from stack overflow?

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

    def hitBall(self, currentBall):
        print("hitball")
        if currentBall.slopeToHole < 0:
            if currentBall.slopeToHoleRise < 0:
                x = (currentBall.center[0] - (17 * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
                y = (currentBall.center[1] + (
                        (currentBall.slopeToHole * 17) * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
                currentBall.hitPoint = (x, y)
            else:
                x = (currentBall.center[0] + (17 * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
                y = (currentBall.center[1] - (
                        (currentBall.slopeToHole * 17) * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
                currentBall.hitPoint = (x, y)
        elif currentBall.slopeToHole > 0:
            if currentBall.slopeToHoleRise < 0:
                x = (currentBall.center[0] + (17 * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
                y = (currentBall.center[1] + (
                        (currentBall.slopeToHole * 17) * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
                currentBall.hitPoint = (x, y)
            else:
                x = (currentBall.center[0] - (17 * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
                y = (currentBall.center[1] - (
                        (currentBall.slopeToHole * 17) * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
                currentBall.hitPoint = (x, y)
        else:
            x = (currentBall.center[0] + (17 * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
            y = (currentBall.center[1] - (
                    (currentBall.slopeToHole * 17) * math.sqrt(1 / (1 + currentBall.slopeToHole ** 2))))
            currentBall.hitPoint = (x, y)
            print("i dont think ill get here")

        print(currentBall.distanceToHole, currentBall.distancetoCue)
        self.powerAmount(currentBall)

        time.sleep(.5)

        pyautogui.moveTo((currentBall.hitPoint[0] + 658, currentBall.hitPoint[1] + 297))
        pyautogui.dragTo((currentBall.dragPoint[0] + 658, currentBall.dragPoint[1] + 297), button="left", duration=.5)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.roundImage, "Hit Point: {}".format(currentBall.hitPoint),
                    (int(currentBall.hitPoint[0] - 10), int(currentBall.hitPoint[1] + 10)), font, .25,
                    (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.roundImage, "Drag Point: {}".format(currentBall.dragPoint),
                    (int(currentBall.dragPoint[0] - 10), int(currentBall.dragPoint[1] + 10)), font, .25,
                    (0, 0, 0), 2, cv2.LINE_AA)
        self.savePic()

    def powerAmount(self, currentBall):
        power = None
        distance = None
        if currentBall.distanceToHole < 50:
            if currentBall.distancetoCue <= 50:
                power = "low"
            elif 150 >= currentBall.distancetoCue > 50:
                power = "medium"
            else:
                power = "high"
        elif 150 > currentBall.distanceToHole > 50:
            if 150 >= currentBall.distancetoCue > 50:
                power = "medium"
            else:
                power = "high"
        else:
            power = "high"

        if power == "low":  # draw range is 115 pixels roughly: 38 pixels for each range
            ratio = currentBall.distancetoCue / 50.0
            if ratio < 1.0:
                distance = ratio * 38
        elif power == "medium":
            ratio = currentBall.distancetoCue / 150.0
            if ratio < 1.0:
                distance = ratio * 76
        elif power == "high":
            ratio = currentBall.distancetoCue / 300.0
            if ratio < 1.0:
                distance = ratio * 115

        currentBall.slopetoDragPoint = (
                currentBall.hitPoint[1] - self.cueball[1] / currentBall.hitPoint[0] - self.cueball[1])

        x = (currentBall.center[0] + (distance * math.sqrt(1 / (1 + currentBall.slopetoDragPoint ** 2))))
        y = (currentBall.center[1] - (
                (currentBall.slopetoDragPoint * distance) * math.sqrt(1 / (1 + currentBall.slopetoDragPoint ** 2))))
        currentBall.dragPoint = (x, y)

    def checkRoundOver(self):
        print("checkroundover")
        time.sleep(5)
        pass

    def checkGameOver(self):
        print("checkgameover")
        time.sleep(5)
        pass

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
                # print("Contour of {} not found".format(b.name))
                return False
            else:
                continue

        print("Cue pole not in way of balls.")
        return True
