import os
import time
import pyautogui
import cv2

import round
import utils
import constants

class Game:

    def __init__(self, inputWindow = None):
        self.poolRegion = (0, 0, 0, 0)
        self.gameWindow = inputWindow
        self.holeLocation = {constants.img_trh: (0, 0), constants.img_tmh: (0, 0), constants.img_tlh: (0, 0),
                             constants.img_blh: (0, 0),
                             constants.img_bmh: (0, 0),
                             constants.img_brh: (0, 0)}
        self.gameNum = 0
        self.turnNum = 0
        self.imgPath = None

    def gameSetup(self):
        with open("gamecounter.txt", "r") as g:
            data = g.readlines()
            for line in data:
                if line is None:
                    g.write("0")
                self.gameNum = str(int(line) + 1)
                with open("gamecounter.txt", "w") as g2:
                    g2.write(self.gameNum)

        os.makedirs("games\game" + self.gameNum + "\\table", exist_ok=True)
        os.makedirs("games\game" + self.gameNum + "\\outlined", exist_ok=True)
        time.sleep(1)

        region = self.regionSetup(5)
        limit = 5
        while region is False:
            if limit <= 0:
                utils.debugPrint("Game did not load or failed.")
                return False
            else:
                limit -= 1

                wait = utils.imageSearch(constants.img_beginningGame, self.gameWindow)
                if wait is True:
                    utils.debugPrint("Waiting on game to load.")
                    region = self.regionSetup(1)
                else:
                    region = self.regionSetup(1)

        self.markHoles()

        print("Game #" + self.gameNum)
        roundTime = 0
        while True:
            self.turnCycle()
            pyautogui.moveTo(1186, 386)
            time.sleep(.1)
            pyautogui.screenshot(("games\game" + self.gameNum + "\\table\pooltable" + str(self.turnNum) + ".png"),
                                 region=self.poolRegion)
            roundstart = round.Round(self.turnNum, self.gameNum, self.poolRegion, self.gameWindow, self.holeLocation)
            startTime = time.clock()

            roundEnd = roundstart.start()

            endTime = time.clock()
            totalTimePassed = endTime - startTime
            remainingTime = 30 - totalTimePassed
            print("Total time passed: {}".format(totalTimePassed))
            if roundEnd is False:
                time.sleep(remainingTime)
                print("Waiting {} seconds.".format(remainingTime))
            else:
                time.sleep(10)

            nextRound = self.checkTurn(constants.img_opponentTurn, constants.img_opponentTurn1)
            if nextRound is True:
                print("Waiting on Bot's turn.")

    def regionSetup(self, attempts):
        # TODO if ball is in the way of hole detection
        pyautogui.moveTo(1186, 386)
        time.sleep(.1)
        while attempts > 0:
            reg = pyautogui.locateOnScreen(utils.imagePath(constants.img_trh))
            if reg is None:
                time.sleep(.5)
                attempts -= 1
            else:
                topRX = reg[0] + reg[2]
                topRY = reg[1]
                self.poolRegion = (topRX - 687, topRY, 687, 355)
                utils.debugPrint("Table region acquired." + str(self.poolRegion))
                return True

            if attempts == 0:
                utils.debugPrint("Acquisition of table region failed.")
                return False

    def markHoles(self):
        utils.debugPrint("Marking pocket locations.")
        pyautogui.moveTo(1186, 386)
        prev = None
        self.roundImage = cv2.imread(self.imgPath, 1)
        for k, v in self.holeLocation.items():
            if v == (0, 0):
                pos = utils.imageSearch(k, self.poolRegion)
                if pos is not None:
                    self.holeLocation[k] = (pos[0], pos[1])
                    utils.debugPrint(k + " " + str(self.holeLocation[k]))
                else:
                    utils.debugPrint("Could not find " + k + " hole. Using previous hole to find.")
                    prevHole = self.holeLocation.get(prev)
                    if "t" in prev:
                        if "tm" in k:
                            self.holeLocation[k] = (prevHole[0] - 339, prevHole[1] - 3)
                            utils.debugPrint(k + " " + str(self.holeLocation[k]))
                        elif "tl" in k:
                            self.holeLocation[k] = (prevHole[0] - 340, prevHole[1] + 3)
                            utils.debugPrint(k + " " + str(self.holeLocation[k]))
                        else:
                            self.holeLocation[k] = (prevHole[0], prevHole[1] + 345)
                            utils.debugPrint(k + " " + str(self.holeLocation[k]))
                    else:
                        if "bm" in k:
                            self.holeLocation[k] = (prevHole[0] + 339, prevHole[1] + 2)
                            utils.debugPrint(k + " " + str(self.holeLocation[k]))
                        else:
                            self.holeLocation[k] = (prevHole[0] + 340, prevHole[1] - 2)
                            utils.debugPrint(k + " " + str(self.holeLocation[k]))

            prev = k

    def turnCycle(self):
        pyautogui.moveTo(1186, 386)
        while True:
            turn1 = self.checkTurn(constants.img_turn, constants.img_turn1)
            if turn1 is True:
                self.turnNum += 1
                print("Bot\'s turn.")
                break

    def checkTurn(self, img1, img2):
        pos = utils.imageSearch(img1)
        if pos is not None:
            return True
        else:
            pos = utils.imageSearch(img2)
            if pos is not None:
                return True
            else:
                return False

def main():
    g = Game()
    g.gameSetup()
    constants.debug = True

if __name__ == '__main__':
    main()
