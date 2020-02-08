import cv2
import numpy as np
import imutils
import math

def surprise():
    cueball = (0,0)
    offsetCueball = (0,0)

    for i2 in range(807,0, -1):
        print(i2)
        try:
            img1 = cv2.imread('C:/Users/Grant/AppData/Local/Programs/Python/Projects/games/game{}/table/pooltable1.png'.format(i2),1)
            #img1 = cv2.resize(img1, ((img1.shape[1] * 2), (img1.shape[0] * 2)), interpolation=cv2.INTER_AREA)
            img651 = cv2.imread('C:/Users/Grant/AppData/Local/Programs/Python/Projects/games/game{}/table/pooltable1.png'.format(i2),1)
            hsv2 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        except Exception:
            print(44)
            continue

        #pyautogui.screenshot("temp1.png",
        #                     region=(515 + 725, 315 + 40, 50, 355))

        try:
            sunkBalls = cv2.imread("games/game{}/temp1.png".format(i2), 1)
            hsvSunkBall = cv2.cvtColor(sunkBalls, cv2.COLOR_BGR2HSV)
        except Exception:
            print(55)

        upper_white = np.array([0, 255, 255])
        lower_white = np.array([0, 0, 120])
        maskwhite = cv2.inRange(hsv2, lower_white, upper_white)
        maskwhiteSunk = cv2.inRange(hsvSunkBall, lower_white, upper_white)

        test1 = np.array([70, 0, 0])
        test2 = np.array([105, 255, 255])
        testmask = cv2.inRange(hsv2, test1, test2)
        testmask = cv2.bitwise_not(testmask)
        testmask = cv2.bitwise_or(img1,img1, mask=testmask)

        try:
            img = cv2.imread("games/game{}/temp.png".format(i2), 0)
            img = cv2.medianBlur(img, 3)
            img4 = cv2.imread("games/game{}/temp.png".format(i2), 1)

            hsv1 = cv2.cvtColor(img4, cv2.COLOR_BGR2HSV)
        except Exception:
            print(66)
            try:
                cv2.imwrite("games/game{}/temp.png".format(i2), testmask)

                img = cv2.imread("games/game{}/temp.png".format(i2), 0)
                img4 = cv2.imread("games/game{}/temp.png".format(i2), 1)

                hsv1 = cv2.cvtColor(img4, cv2.COLOR_BGR2HSV)
            except Exception:
                print(77)
                continue

            continue

        alist = masks(hsv1)

        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 17,
                                   param1=20, param2=9, minRadius=9, maxRadius=11)
        circles = np.uint16(np.around(circles))
        pointList = []
        for i in circles[0, :]:
            cv2.circle(img1, (i[0], i[1]), 10, (0, 0, 255), 1)
            pointList.append((i[0],i[1]))

        ignore = []
        for n, b, s in alist:
            print("Determining position of {} {}.".format(s, n))
            masks(hsv1)

            contours = cv2.findContours(b.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if imutils.is_cv2() else contours[1]
            contours = sorted(contours, key=cv2.contourArea)

            if n == "cueball" or n == "eightball":
                contours = contours[len(contours) - 1:len(contours)]
            else:
                contoursTemp = contours[len(contours) - 2:len(contours)]

                for k, c in enumerate(contoursTemp):
                    carea = cv2.contourArea(c)
                    (x, y), radius = cv2.minEnclosingCircle(c)
                    if radius > 25:
                        contoursTemp[k] = contours[len(contours) - 3]
                    else:
                        if carea > 0 and carea < 80:
                            b = cv2.morphologyEx(b, cv2.MORPH_CLOSE, np.ones((8, 8), np.uint8))
                            contoursTemp = cv2.findContours(b.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                            contoursTemp = contoursTemp[0] if imutils.is_cv2() else contoursTemp[1]
                            contoursTemp = sorted(contoursTemp, key=cv2.contourArea)

                contours = contoursTemp

            ball_1 = None
            ball_2 = None
            large = False
            # find center based on color
            for c in contours:
                carea = cv2.contourArea(c)
                (x, y), radius = cv2.minEnclosingCircle(c)
                center = (int(x), int(y))
                if center not in ignore:
                    if carea > 25:
                        if radius < 13:
                            roiMask = roi(maskwhite, center, 10)
                            contours1 = contourSetup(roiMask, False)
                            whiteArea, whiteCount = whiteMaskedArea(contours1, True, 0)

                            closest = (0, 1000)
                            closest = matchHoughCircleToMask(pointList, center, closest, 10)
                            if closest[1] == 1000:
                                continue
                            else:
                                if ball_1 is None:
                                    ball_1 = (
                                    pointList[closest[0]][0], pointList[closest[0]][1], carea, whiteArea, whiteCount,
                                    center)
                                else:
                                    ball_2 = (
                                    pointList[closest[0]][0], pointList[closest[0]][1], carea, whiteArea, whiteCount,
                                    center)

                                pointList.pop(closest[0])

                        else:
                            large = True
                            pointListCopy = pointList.copy()

                            closest = (0, 1000)
                            closest = matchHoughCircleToMask(pointListCopy, center, closest, 15)
                            point1 = pointListCopy.pop(closest[0])

                            closest1 = (0, 1000)
                            closest1 = matchHoughCircleToMask(pointListCopy, center, closest1, 15)
                            point2 = pointListCopy.pop(closest1[0])
                            if closest[1] == 1000 and closest1[1] == 1000:
                                continue
                            else:
                                points = [point1, point2]
                                for p in points:

                                    roiMask = roi(b, p, 10)
                                    contours = contourSetup(roiMask, False)
                                    for c in contours:
                                        carea = cv2.contourArea(c)
                                        (x, y), radius = cv2.minEnclosingCircle(c)
                                        center = (int(x), int(y))
                                        if carea > 30:
                                            roiMask = roi(maskwhite, p, 10)
                                            contours = contourSetup(roiMask, False)
                                            whiteArea, whiteCount = whiteMaskedArea(contours, True, 0)

                                            if ball_1 is None:
                                                ball_1 = (
                                                    pointList[closest[0]][0], pointList[closest[0]][1], carea, whiteArea,
                                                    whiteCount,
                                                    center)

                                                pointList.pop(pointList.index(p))
                                            else:
                                                ball_2 = (
                                                    pointList[closest1[0]][0], pointList[closest1[0]][1], carea, whiteArea,
                                                    whiteCount,
                                                    center)

                                                pointList.pop(pointList.index(p))

            if n == "cueball":
                if ball_1 is None:
                    ball_1 = backUpCenter(contours, maskwhite)
                    center = (ball_1[0], ball_1[1])
                else:
                    center = (ball_1[0], ball_1[1])

                print("ball_1 is cueball. {}. \n".format((ball_1[0], ball_1[1])))
                drawStripe(img1, center, stringToColor(n))
            elif n == "eightball":
                if ball_1 is None:
                    ball_1 = backUpCenter(contours, maskwhite)
                    center = (ball_1[0], ball_1[1])
                else:
                    center = (ball_1[0], ball_1[1])

                print("ball_1 is eightball. {}. \n".format((ball_1[0], ball_1[1])))
                drawStripe(img1, center, stringToColor(n))
            else:
                if ball_2 is None:
                    count = 0
                    for c in contours:
                        area = cv2.contourArea(c)
                        if area > 30:
                            count += 1

                    if count == 1:
                        alist_1 = masks(hsvSunkBall)
                        for n1, b1, s1 in alist_1:
                            if n == n1 and s == s1:
                                contours = cv2.findContours(b1.copy(), cv2.RETR_EXTERNAL,
                                                            cv2.CHAIN_APPROX_SIMPLE)
                                contours = contours[0] if imutils.is_cv2() else contours[1]
                                contours = sorted(contours, key=cv2.contourArea)

                                contours = contours[len(contours) - 2:len(contours)]

                                for c in contours:
                                    carea = cv2.contourArea(c)
                                    (x, y), radius = cv2.minEnclosingCircle(c)
                                    center = (int(x), int(y))

                                    if center not in ignore:
                                        if carea > 15:
                                            roiMask1 = roi(maskwhiteSunk, center, 10)
                                            contours1 = cv2.findContours(roiMask1.copy(), cv2.RETR_EXTERNAL,
                                                                         cv2.CHAIN_APPROX_SIMPLE)
                                            contours1 = contours1[0] if imutils.is_cv2() else contours1[1]

                                            whiteArea = 0
                                            whiteCount = 0
                                            for c1 in contours1:
                                                c1area = cv2.contourArea(c1)
                                                whiteCount += 1
                                                if c1area > 0:
                                                    whiteArea += c1area

                                            if ball_1 is None:
                                                ball_1 = (
                                                    center[0] + 725, center[1] + 40, carea, whiteArea, whiteCount,
                                                    center)
                                            else:
                                                ball_2 = (
                                                    center[0] + 725, center[1] + 40, carea, whiteArea, whiteCount,
                                                    center)

                if ball_2 is None:
                    if ball_1 is not None:
                        if s == "solid":
                            center = (ball_1[0], ball_1[1])
                            print(
                                "ball_1 is solid. {} - {} -- {} \n".format((ball_1[0], ball_1[1]),
                                                                           ball_1[2], ball_1[3]))
                            drawSolid(img1, center, stringToColor(n))
                        elif s == "stripe":
                            center = (ball_1[0], ball_1[1])
                            print(
                                "ball_1 is stripe. {} - {} -- {} \n".format((ball_1[0], ball_1[1]),
                                                                            ball_1[2], ball_1[3]))
                            drawStripe(img1, center, stringToColor(n))

                        ignore.append(ball_1[5])
                    else:
                        continue
                else:
                    confidence = suitConfidence(ball_1, ball_2)

                    if confidence > 0:
                        if s == "solid":
                            center = (ball_1[0], ball_1[1])
                            print(
                                "ball_1 is solid. {} - {} -- {}".format((ball_1[0], ball_1[1]), ball_1[2],
                                                                        ball_1[3]))
                            drawSolid(img1, center, stringToColor(n))
                            if large is False:
                                ignore.append(ball_1[5])
                                pointList.append((ball_2[0], ball_2[1]))
                            else:
                                pointList.append((ball_1[0], ball_1[1]))
                                pointList.append((ball_2[0], ball_2[1]))
                        elif s == "stripe":
                            center = (ball_2[0], ball_2[1])
                            print(
                                "ball_2 is stripe. {} - {} -- {}".format((ball_2[0], ball_2[1]), ball_2[2],
                                                                         ball_2[3]))
                            drawStripe(img1, center, stringToColor(n))
                            if large is False:
                                ignore.append(ball_2[5])
                                pointList.append((ball_1[0], ball_1[1]))
                            else:
                                pointList.append((ball_1[0], ball_1[1]))
                                pointList.append((ball_2[0], ball_2[1]))
                    elif confidence < 0:
                        if s == "stripe":
                            center = (ball_1[0], ball_1[1])
                            print("ball_1 is stripe. {} - {} -- {}".format((ball_1[0], ball_1[1]), ball_1[2],
                                                                           ball_1[3]))
                            drawStripe(img1, center, stringToColor(n))
                            if large is False:
                                ignore.append(ball_1[5])
                                pointList.append((ball_2[0], ball_2[1]))
                            else:
                                pointList.append((ball_1[0], ball_1[1]))
                                pointList.append((ball_2[0], ball_2[1]))
                        elif s == "solid":
                            center = (ball_2[0], ball_2[1])
                            print("ball_2 is solid. {} - {} -- {}".format((ball_2[0], ball_2[1]), ball_2[2],
                                                                          ball_2[3]))
                            drawSolid(img1, center, stringToColor(n))
                            if large is False:
                                ignore.append(ball_2[5])
                                pointList.append((ball_1[0], ball_1[1]))
                            else:
                                pointList.append((ball_1[0], ball_1[1]))
                                pointList.append((ball_2[0], ball_2[1]))
                    else:
                        # random chance at this point
                        print("confidence is 0")
                        if s == "solid":
                            center = (ball_1[0], ball_1[1])
                            print("ball_1 is solid. {} - {} -- {}".format((ball_1[0], ball_1[1]), ball_1[2], ball_1[3]))
                            drawSolid(img1, center, stringToColor(n))
                            if large is False:
                                ignore.append(ball_1[5])
                                pointList.append((ball_2[0], ball_2[1]))
                            else:
                                pointList.append((ball_1[0], ball_1[1]))
                                pointList.append((ball_2[0], ball_2[1]))
                        elif s == "stripe":
                            center = (ball_2[0], ball_2[1])
                            print(
                                "ball_2 is stripe. {} - {} -- {}".format((ball_2[0], ball_2[1]), ball_2[2], ball_2[3]))
                            drawStripe(img1, center, stringToColor(n))
                            if large is False:
                                ignore.append(ball_2[5])
                                pointList.append((ball_1[0], ball_1[1]))
                            else:
                                pointList.append((ball_1[0], ball_1[1]))
                                pointList.append((ball_2[0], ball_2[1]))

        cv2.imshow("{}".format(i2), img1)
        cv2.imshow("orig", img651)
        #cv2.imshow(n, b)
        #cv2.imshow("white", maskwhite)
        # cv2.imshow('maskedColor', testmask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def drawStripe(img1, center, colorRGB):
    #cv2.circle(img1, (center[0], center[1]), 9, colorRGB, 2)
    #cv2.circle(img1, (center[0], center[1]), 10, (0, 0, 0), 1)
    cv2.line(img1, (center[0], center[1] + 10), (center[0], center[1] - 10), (0, 0, 0))
    cv2.line(img1, (center[0] - 10, center[1]), (center[0] + 10, center[1]), (0, 0, 0))


def drawSolid(img1, center, colorRGB):
    #cv2.circle(img1, (center[0], center[1]), 10, colorRGB, -1)
    #cv2.circle(img1, (center[0], center[1]), 10, (0, 0, 0), 1)
    cv2.line(img1, (center[0], center[1] + 10), (center[0], center[1] - 10), (255, 255, 255))
    cv2.line(img1, (center[0] - 10, center[1]), (center[0] + 10, center[1]), (255, 255, 255))

def suitConfidence(ball_1, ball_2):
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
    if aDifference > 60:
        confidence = 0.25
    else:
        if aDifference > 0:
            confidence += (aDifference/60) * 0.25
        else:
            if aDifference < -60:
                confidence = -0.25
            else:
                confidence += math.fabs(aDifference/60) * -0.25

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

    max = 100
    if whiteCount1 > whiteCount2:
        if 0.10 > confidence > -0.10:
            confidence += -0.5
        else:
            if confidence == -0.50:
                confidence += (math.fabs(whiteDifference/ max)* colorRatio2) * -0.25
            else:
                confidence += (math.fabs(whiteDifference / max)* colorRatio2) * -0.5
    elif whiteCount1 < whiteCount2:
        if 0.10 > confidence > -0.10:
            confidence += 0.5
        else:
            if confidence == 0.50:
                confidence += (math.fabs(whiteDifference / max)* colorRatio1) * 0.25
            else:
                confidence += (math.fabs(whiteDifference / max) * colorRatio1) * 0.5

    if confidence > 1:
        confidence = 1
    elif confidence < -1:
        confidence = -1

    print("ball_1 confidence value: {}".format(confidence))

    return confidence

def contourSetup(mask, sort):
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]

    if sort is True:
        contours = sorted(contours, key=cv2.contourArea)

    return contours

def whiteMaskedArea(contours, count, min):
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

def matchHoughCircleToMask(pointList, center, closest, max):
    for k2, p in enumerate(pointList):
        dist = math.sqrt((p[0] - center[0]) ** 2 + (p[1] - center[1]) ** 2)

        if dist < max and dist < closest[1]:
            closest = (k2, dist)

    return closest

def backUpCenter(contours, maskwhite):
    ball_1 = (0,0,0,0,0,0)
    for c in contours:
        carea = cv2.contourArea(c)
        (x, y), radius = cv2.minEnclosingCircle(c)
        if carea > 30 and carea > ball_1[2]:
            center = (int(x), int(y))

            roiMask1 = roi(maskwhite, center, 10)
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




def roi(img, center, radius):
    mask = np.zeros_like(img)
    cv2.circle(mask, center, radius, (255,255,255), -1)
    masked = cv2.bitwise_and(img, mask)
    return masked

def averagePosition(ball, center):
    if ball is not None:
        xDif = math.fabs((ball[0] - center[0]))
        yDif = math.fabs((ball[1] - center[1]))
        if 0 < xDif <= 2:
            averaged = ((ball[0] + center[0]) / 2, ball[1])
            ball = (int(averaged[0]), averaged[1], ball[2], ball[3], ball[4])

        if 0 < yDif <= 2:
            averaged = (ball[0], (ball[1] + center[1]) / 2)
            ball = (averaged[0], int(averaged[1]), ball[2], ball[3], ball[4])

    return ball

def isPocketed(center, min, max):
    if (center[0] + min) < min or (center[0] + min) > max:
        return True
    else:
        return False

def stringToColor(color):  # takes the list of colors and based on name, returns a rgb color value
    '''

    :param color:
    :return:
    '''
    if color == 'cueball':
        return 255, 255, 255
    elif color == 'eightball':
        return 17, 17, 17,
    elif color == 'blueball':
        return 196, 112, 58
    elif color == 'lightredball':
        return 14, 14, 252
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
    upper_whitecue = np.array([27, 36, 255])
    lower_whitecue = np.array([18, 0, 120])
    maskwhiteball = cv2.inRange(hsv, lower_whitecue, upper_whitecue)
    maskwhiteball = cv2.morphologyEx(maskwhiteball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    alist.append(('cueball',maskwhiteball, "nosuit"))

    upper_black = np.array([0, 0, 110])
    lower_black = np.array([0, 0, 30])
    maskblackball = cv2.inRange(hsv, lower_black, upper_black)
    maskblackball = cv2.morphologyEx(maskblackball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    alist.append(('eightball',maskblackball, "nosuit"))

    upper_yellow = np.array([31, 255, 255])
    lower_yellow = np.array([19, 50, 160])
    maskyellowball = cv2.inRange(hsv, lower_yellow, upper_yellow)
    maskyellowball = cv2.morphologyEx(maskyellowball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    alist.append(('yellowball',maskyellowball, "solid"))
    alist.append(('yellowball',maskyellowball, "stripe"))

    upper_blue = np.array([120, 220, 255])
    lower_blue = np.array([105, 60, 120])
    maskblueball = cv2.inRange(hsv, lower_blue, upper_blue)
    maskblueball = cv2.morphologyEx(maskblueball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    alist.append(('blueball',maskblueball, "solid"))
    alist.append(('blueball',maskblueball, "stripe"))

    upper_lightred = np.array([180, 255, 250])
    lower_lightred = np.array([170, 0, 150])
    masklightredball = cv2.inRange(hsv, lower_lightred, upper_lightred)
    masklightredball = cv2.morphologyEx(masklightredball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    alist.append(('lightredball',masklightredball, "solid"))
    alist.append(('lightredball',masklightredball, "stripe"))

    upper_purple = np.array([139, 255, 255])
    lower_purple = np.array([130, 11, 70])
    maskpurpleball = cv2.inRange(hsv, lower_purple, upper_purple)
    maskpurpleball = cv2.morphologyEx(maskpurpleball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    alist.append(('purpleball',maskpurpleball, "solid"))
    alist.append(('purpleball',maskpurpleball, "stripe"))

    upper_orange = np.array([14, 255, 255])
    lower_orange = np.array([10, 30, 0])
    maskorangeball = cv2.inRange(hsv, lower_orange, upper_orange)
    maskorangeball = cv2.morphologyEx(maskorangeball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    alist.append(('orangeball',maskorangeball, "solid"))
    alist.append(('orangeball',maskorangeball, "stripe"))

    upper_green = np.array([70, 255, 255])
    lower_green = np.array([50, 0, 140])
    maskgreenball = cv2.inRange(hsv, lower_green, upper_green)
    maskgreenball = cv2.morphologyEx(maskgreenball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    alist.append(('greenball',maskgreenball, "solid"))
    alist.append(('greenball',maskgreenball, "stripe"))

    upper_darkred = np.array([7, 255, 255])
    lower_darkred = np.array([3, 100, 100])
    maskdarkredball = cv2.inRange(hsv, lower_darkred, upper_darkred)
    maskdarkredball = cv2.morphologyEx(maskdarkredball, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    alist.append(('darkredball',maskdarkredball, "solid"))
    alist.append(('darkredball',maskdarkredball, "stripe"))

    
    return alist


def test():
    img = cv2.imread('C:/Users/Grant/AppData/Local/Programs/Python/Projects/games/game710/table/pooltable1.png',0)

    mask = cv2.imread('mask2.png', 0)

    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    cv2.imshow('dst', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    surprise()

if __name__ == '__main__':
    main()
