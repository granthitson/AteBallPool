import os
import time
import pyautogui

import round
import utils
import constants

class Game:

    def __init__(self, inputWindow):
        self.poolRegion = (0, 0, 0, 0)
        self.gameWindow = inputWindow
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
        if region is False:
            return False
        print("Game #" + self.gameNum)

        while True:
            self.turnCycle()
            pyautogui.screenshot(("games\game" + self.gameNum + "\\table\pooltable" + str(self.turnNum) + ".png"),
                                 region=self.poolRegion)
            roundstart = round.Round(self.turnNum, self.gameNum, self.poolRegion, self.gameWindow)
            roundstart.start()
            # check for end of game and return True

    def regionSetup(self, attempts):
        while attempts > 0:
            reg = pyautogui.locateOnScreen(utils.imagePath(constants.img_trh), self.gameWindow)
            if reg is None:
                time.sleep(1)
                attempts -= 1
            else:
                topRX = reg[0] + reg[2]
                topRY = reg[1]
                self.poolRegion = (topRX - 605, topRY, 605, 314)
                utils.debugPrint("Table region acquired." + str(self.poolRegion))
                return True

            if attempts == 0:
                utils.debugPrint("Acquisition of table region failed.")
                return False

    def turnCycle(self):
        pyautogui.moveTo(1248, 363)
        while True:
            turn1 = self.checkTurn()
            if turn1 is True:
                self.turnNum += 1
                print("Bot\'s turn.")
                break
            else:
                time.sleep(1)

    def checkTurn(self):
        while True:
            pos = utils.imageSearch(constants.img_turn)
            if pos is not None:
                return True
            else:
                pos = utils.imageSearch(constants.img_turn1)
                if pos is not None:
                    return True
                else:
                    return False