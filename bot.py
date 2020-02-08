import json
import sys
import time
import webbrowser
import uuid
import subprocess as sub
from win32api import GetSystemMetrics

import pyautogui
import requests

import game
import utils
import constants


class Bot:
    miniclipURL = "https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/"

    def __init__(self):
        self.name = self.uuidGenerator()
        self.height = None
        self.width = None
        self.gameWindow = None

    def uuidGenerator(self):
        stringLength = 8

        randomString = uuid.uuid4().hex
        randomString = randomString.lower()[0:stringLength]
        return randomString

    def gameMenuSearch(self, r):
        imgs = [constants.img_alreadyStarted, constants.img_alreadyStarted1]
        utils.debugPrint("Checking for Game Menu...")
        r += 1
        for img in imgs:
            utils.debugPrint("Image {}...".format(img))
            for i in range(0, r + 1):
                pos = utils.imageSearch(img)
                if pos is None:
                    utils.debugPrint("Attempts: " + str(r - i))
                    self.dismiss(1)
                    time.sleep(.5)
                else:
                    return True

        return False

    def dismiss(self, r):
        imgs = [constants.img_cueUpdate, constants.img_cues, constants.img_backButton]
        utils.debugPrint("Checking for cue notification.")
        r += 1
        for img in imgs:
            utils.debugPrint("Image {}...".format(img))
            for i in range(0, r + 1):
                pos = utils.imageSearch(constants.img_cueUpdate)
                if pos is None:
                    utils.debugPrint("Attempts: " + str(r-i))
                    time.sleep(.1)
                else:
                    return True

    def click(self, img, gameWindow):
        for i in range(0, 5):
            if gameWindow is None:
                pos = utils.imageSearch(img)
            else:
                pos = utils.imageSearch(img, gameWindow)

            if pos is None:
                continue
            else:
                pyautogui.click(pos)
                utils.debugPrint("{} found and clicked.".format(img))
                time.sleep(.5)
                break

    def start(self):
        uuid = self.uuidGenerator()
        print("Bot {} beginning setup.".format(uuid))

        # Checks if webpage still present
        result = utils.CheckForUrl(5)

        if result is False:
            nWin = utils.timedInput("Did not detect website. Open new tab/window?  Press CTRL+C to begin typing.")
            if nWin is True:
                webbrowser.open(Bot.miniclipURL)
                time.sleep(5)
                self.start()
            else:
                print("Exiting..")
                sys.exit()
        else:
            # webpage is still visible
            login = self.ifLogin()
            if login is None:
                utils.debugPrint("Error confirming login status. Waiting 10 seconds and attempting once more.")
                time.sleep(10)
                login = self.ifLogin()
                if login is None:
                    utils.debugPrint("Login systems failed. Cannot proceed.\nExiting..")
                    time.sleep(2)
                    sys.exit()

            # login status confirmed, either logged in or not
            # if login is None, exits. login is either True or False
            gameReg = self.getGameRegion(login)
            if gameReg is False or gameReg is None:
                utils.debugPrint("Error acquiring game region. Waiting 10 seconds and attempting once more.")
                time.sleep(10)
                gameReg = self.getGameRegion(login)
                if gameReg is False:
                    utils.debugPrint("Acquisition of game region failed. Cannot proceed.\nExiting..")
                    time.sleep(2)
                    sys.exit()

            # game region successfully acquired
            if login is False:
                # user not logged in, navigate menu that only shows for users not logged in
                nM = self.navigateMenu(login)
                if nM is False:
                    # play as guest
                    self.playPoolGame()
                else:
                    # log in and play game
                    self.logIn()

            time.sleep(.5)
            #self.spinWin(5)
            #self.collectCoins(5)
            dG = self.decideGame(5)
            if dG is False:
                utils.debugPrint("Game choice not made. Cannot proceed.\nExiting..")
                time.sleep(2)
                sys.exit()
            else:
                play = self.playPoolGame()
                if play is True:
                    while play is True:
                        pA = utils.timedInput("Play another game? Press CTRL+C to begin typing.", 15)
                        if pA is True:
                            play = self.playPoolGame()
                        else:
                            utils.debugPrint("Exiting..")
                            time.sleep(2)
                            sys.exit()
                utils.debugPrint("Terminating Bot..")
                time.sleep(3)
                sys.exit()

    def ifLogin(self):
        limit = 30
        utils.debugPrint("Checking to see if already logged in.")
        loggedIn = self.loginCheck()
        while loggedIn is None and limit > 0:
            utils.debugPrint("Did not find URL.\nRetrying..")
            time.sleep(1)
            limit -= 1
            loggedIn = self.loginCheck()
        if loggedIn is None:
            return None
        utils.debugPrint("loginCheck succeeded.")
        return True

    def loginCheck(self):
        imgs = [constants.img_allowFlash, constants.img_allowFlash1, constants.img_allowFlash2, constants.img_allow]
        time.sleep(1)
        loggedIn = utils.CheckForUrl(5)
        if loggedIn is False:
            print("Could not identify visible tab. Opening new tab.")
            webbrowser.open(Bot.miniclipURL)
            return None
        else:
            for img in imgs:
                utils.debugPrint("Searching for image {}...".format(img))
                pos = utils.imageSearch(img)
                if pos is None:
                    utils.debugPrint("{} not detected.".format(img))
                    continue
                else:
                    self.click(img, self.gameWindow)
                    if img == constants.img_allowFlash or img == constants.img_allowFlash1:
                        for i, v in enumerate(imgs):
                            if 3 >= i >= 2:
                                p = utils.imageSearch(v)
                                if p is None:
                                    utils.debugPrint("{} not detected.".format(v))
                                    return None
                                else:
                                    self.click(img, self.gameWindow)
                                    continue

        imgs = [constants.img_signUpLogin, constants.img_defaultAcct]
        for img in imgs:
            utils.debugPrint("Searching for image {}...".format(img))
            for i in range(0, 5):
                pos = utils.imageSearch(img)
                if pos is None:
                    utils.debugPrint("{} not detected.".format(img))
                    continue
                else:
                    if img == constants.img_signUpLogin:
                        utils.debugPrint("User not logged in.")
                        return False
                    if img == constants.img_defaultAcct:
                        utils.debugPrint("Logged into default account.")
                        return True

        loggedIn = utils.CheckForUrl(5)
        if loggedIn is False:
            return None
        else:
            utils.debugPrint("Correct tab still visible.")
            account = utils.timedInput("Are you logged into your own account? Press CTRL+C to begin typing.")
            if account is False:
                utils.debugPrint("User not logged into their own account and default account not detected.")
                return None
            else:
                utils.debugPrint("User logged into their own account.")
                default = utils.timedInput("Would you like to save it as the default?")
                if default is False:
                    utils.debugPrint("User using account other than default.")
                    print("Proceeding...")
                    return True
                else:
                    utils.debugPrint("Saving new account as default.")
                    reg = utils.imageSearch(constants.img_facebookLogo)
                    pyautogui.screenshot("images/" + constants.img_defaultAcct,
                                         region=((reg[0] + reg[2]) - 170, reg[1], 170, 40))
                    utils.debugPrint("Overwriting pre-existing image of default account.")
                while True:
                    newemail = input("Please enter the email associated with the account.")
                    newpass = input("Please enter the password associated with the account.")
                    confirm = utils.timedInput("User is {} and the password is {}?".format(newemail, newpass))
                    if confirm is True:
                        with open("default.txt", "w") as f:
                            for line in f:
                                if line is None:
                                    utils.debugPrint("Default username file is empty.")
                                else:
                                    utils.debugPrint("Overwriting pre-existing contents.")
                                f.write("{} {}".format(newemail, newpass))
                                print("New default account set. {}:{}".format(newemail, newpass))
                                f.close()
                                return True

    def getGameRegion(self, loginTruthVal):
        limit = 3
        self.height, self.width = self.miniclipAPI()
        utils.debugPrint("Size of game window retrieved.")
        time.sleep(1)
        self.clickX()
        utils.debugPrint("Searching for top right of game window.")
        gM = self.gameMenuSearch(5)
        if gM is False:
            result = utils.CheckForUrl(5)
            if result is True:
                proceed = utils.timedInput("Game menu not found. Proceed anyway?  Press CTRL+C to begin typing.")
                if proceed is True:
                    utils.debugPrint("Proceeding..")
                    return False
                else:
                    utils.debugPrint("Backing out..")
                    return None
            else:
                proceed = utils.timedInput(
                    "Game menu not found. Webpage not found. Open new tab/window?  Press CTRL+C to begin typing.")
                if proceed is True:
                    utils.debugPrint("Opening new tab..")
                    webbrowser.open(Bot.miniclipURL)
                    time.sleep(5)
                    self.start()
                else:
                    utils.debugPrint("Backing out..")
                    return None

        utils.debugPrint("Game menu found.")
        if loginTruthVal is False:
            utils.debugPrint("User not logged in.")
            time.sleep(1)
            utils.debugPrint("Searching for game region..")
            cor = self.searchForGameCorner(constants.img_topRightCorner, 20)
            if cor is True:
                return True
            if limit > 0:
                utils.debugPrint("{} tries left.".format(limit))
            else:
                return False
        else:
            utils.debugPrint("User logged in.")
            time.sleep(1)
            utils.debugPrint("Searching for game region..")
            cor = self.searchForGameCorner(constants.img_topRightCornerLogged, 20)
            if cor is True:
                return True
            if limit > 0:
                utils.debugPrint("{} tries left.".format(limit))
            else:
                return False

    def miniclipAPI(self):
        utils.debugPrint("Accessing miniclip's API.")

        api_url_base = "https://webmasters.miniclip.com/api/"
        api_url = "{0}/games/2471/en.json".format(api_url_base)

        try:
            response = requests.get(api_url)
            utils.debugPrint("Requesting connection.")

            if response.status_code == 200:
                utils.debugPrint("Connection accepted.")
                data = json.loads(response.content.decode("utf-8"))
                h = int(data["2471"].get("height"))
                w = int(data["2471"].get("width"))
                return h, w
        except requests.exceptions.ConnectionError:
            requests.status_code = "Connection refused"
            utils.debugPrint("Connection refused. Retrying 5 times.")
            for i in range(1, 5):
                time.sleep(1)
                response = requests.get(api_url)
                self.miniclipAPI()

    def searchForGameCorner(self, img, attempts):
        reg = pyautogui.locateOnScreen(utils.imagePath(img))
        if reg is not None:
            topRX = reg[0] + reg[2]
            topRY = reg[1]
            self.gameWindow = (topRX - self.width, topRY, self.width, self.height)
            utils.debugPrint("Region acquired." + str(self.gameWindow))
            return True
        else:
            utils.debugPrint("Region not found. Attempting {} more times.".format(attempts))
            #self.spinWin()
            #self.clickX()
            while attempts > 0:
                reg = pyautogui.locateOnScreen(utils.imagePath(img))
                if reg is None:
                    utils.debugPrint("Attempts: " + str(attempts))
                    attempts -= 1
                elif reg is not None:
                    topRX = reg[0] + reg[2]
                    topRY = reg[1]
                    self.gameWindow = (topRX - self.width, topRY, self.width, self.height)
                    utils.debugPrint("Region acquired." + str(self.gameWindow))
                    return True

            return False

    def navigateMenu(self, truthVal):
        pos = utils.imageSearch(constants.img_loginWithMiniclip, self.gameWindow)
        pos1 = utils.imageSearch(constants.img_playButtonGuest, self.gameWindow)
        if pos is None and pos1 is None:
            utils.debugPrint("Cannot find play buttons.\nRefreshing page.")
            self.refreshPage()
            utils.debugPrint("Attempting to renavigate menu.")
            self.navigateMenu(truthVal)
        else:
            utils.debugPrint("Found play buttons.")
            guest = utils.timedInput("Login? Or play as a guest?  Press CTRL+C to begin typing.", 10, ["guest", "log"])
            if guest is True or guest is None:
                utils.debugPrint("Playing as guest.")
                pyautogui.click(pos1)
                return False
            else:
                utils.debugPrint("Logging in.")
                pyautogui.click(pos)
                return True

    def logIn(self):
        email = ""
        password = ""
        acct = utils.timedInput("Do you have an account you\'d like the bot to play on?  Press CTRL+C to begin typing.")
        if acct is False or acct is None:
            print("Using default.")
            with open("default.txt", "r") as f:
                for line in f:
                    if line is None:
                        utils.debugPrint("No default account found.")
                    else:
                        email, password = line.split(" ")
        else:
            email = input("Please enter the email. No time limit. Does not save your info.\n:")
            password = input("Please enter the email. No time limit. Does not save your info.\n:")

        self.click(constants.img_emailArea, self.gameWindow)
        pyautogui.typewrite(email)
        time.sleep(.5)
        self.click(constants.img_passwordArea, self.gameWindow)
        pyautogui.typewrite(password)
        time.sleep(.5)
        self.click(constants.img_loginButton3, self.gameWindow)

    def decideGame(self, attempts):
        attempts += 1
        for i in range(1, attempts + 1):
            utils.debugPrint("Initiating game selection.")
            gM = self.gameMenuSearch(5)
            if gM is False:
                url = utils.CheckForUrl(5)
                if url is False:
                    proceed = utils.timedInput(
                        "Game menu not found. Webpage not found. Open new tab/window?  Press CTRL+C to begin typing.")
                    if proceed is True:
                        utils.debugPrint("Opening new tab..")
                        webbrowser.open(Bot.miniclipURL)
                        time.sleep(5)
                        self.start()
                    else:
                        utils.debugPrint("Backing out..")
                        return False
                else:
                    while True:
                        self.clickX()
                        gM = self.gameMenuSearch(5)
                        if gM is True:
                            utils.debugPrint("Game menu reacquired..")
                            break

            choice = utils.timedInput("\"Practice\"? or \"Play\"? Press Control+C to begin typing. ", 30,
                                ["practice", "play"])
            if choice is True:
                gamechoice = self.playPractice()
            else:
                playChoice = utils.timedInput("Play with \"friends\" or \"randoms\"? Press Control+C to begin typing. ", 30,
                                ["friend", "random"])
                if playChoice is True:
                    gamechoice = self.playFriends()
                else:
                    gamechoice = self.playRandoms()

                if gamechoice is True:
                    return True
                else:
                    self.click(constants.img_mainMenuBefore, self.gameWindow)

        return False

    def playPractice(self):
        utils.debugPrint("Practicing")
        # TODO

    def playRandoms(self):
        utils.debugPrint("Playing against random opponent.")
        self.click(constants.img_playButtonLogged, self.gameWindow)
        gameType = utils.timedInput("Enter wager amount (Only options are 50 and 100). Press CTRL+C to begin typing.", 15,
                              ["50", "100"])
        if gameType is True:
            pos = utils.imageSearch(constants.img_poolChoice, self.gameWindow)
        else:
            pos = utils.imageSearch(constants.img_poolChoice200, self.gameWindow)
        pos2 = utils.imageSearch(constants.img_cheapButton, self.gameWindow)
        if pos is None:
            while pos is None:
                pyautogui.click(pos2)
                time.sleep(.5)
                pos = utils.imageSearch(constants.img_poolChoice, self.gameWindow)
        pyautogui.click(pos)
        time.sleep(5)

        bG = utils.timedInput("Begin game? Press Control+C to begin typing. Autoplays after 10 seconds.")
        if bG is True or bG is None:
            pyautogui.click(pos)
            time.sleep(1)
            while True:
                begin = self.isGameStart()
                if begin is True:
                    return True
                else:
                    return False
        else:
            self.click(constants.img_mainMenuBefore, self.gameWindow)
            return False

    def playFriends(self):
        utils.debugPrint("Playing against \"friendly\" opponent.")
        self.click(constants.img_playFriends, self.gameWindow)
        time.sleep(.5)
        pos = utils.imageSearch(constants.img_searchFriends, self.gameWindow)
        if pos is None:
            return False
        else:
            username = input("Please enter the username of your opponent: ")
            self.click(constants.img_searchFriends, self.gameWindow)
            time.sleep(.5)
            pyautogui.typewrite(username)
            pyautogui.press("enter")
            time.sleep(.5)
            pos = utils.imageSearch(constants.img_challengeFriend, self.gameWindow)
            if pos is not None:
                self.click(constants.img_challengeFriend, self.gameWindow)
                gameType = utils.timedInput("Enter wager amount (Only options are 50 and 100). Press CTRL+C to begin typing.",
                                      15, ["50", "100"])
                if gameType is True:
                    pos = utils.imageSearch(constants.img_poolChoice1, self.gameWindow)
                    if pos is None:
                        while pos is None:
                            self.click(constants.img_cheapButtonFriend, self.gameWindow)
                            pos = utils.imageSearch(constants.img_poolChoice1, self.gameWindow)
                        self.click(constants.img_poolChoice1, self.gameWindow)
                    else:
                        self.click(constants.img_poolChoice1, self.gameWindow)
                else:
                    self.click(constants.img_poolChoice200_1, self.gameWindow)
                    if pos is None:
                        while pos is None:
                            self.click(constants.img_cheapButtonFriend, self.gameWindow)
                            pos = utils.imageSearch(constants.img_poolChoice200_1, self.gameWindow)
                        self.click(constants.img_poolChoice200_1, self.gameWindow)
                    else:
                        self.click(constants.img_poolChoice200_1, self.gameWindow)

                pos = utils.imageSearch(constants.img_playNow, self.gameWindow)
                while pos is None:
                    pos = utils.imageSearch(constants.img_playNow, self.gameWindow)

                self.click(constants.img_playNow, self.gameWindow)

                return True
            else:
                imgs = [constants.img_inviteFriend, constants.img_searchFriends1, constants.img_searchFriends2, constants.img_addFriend,
                        constants.img_backButton, constants.img_playFriends]
                utils.debugPrint("Adding friend..")
                for img in imgs:
                    utils.debugPrint("Searching for image {}...".format(img))
                    for i in range(0, 5):
                        pos = utils.imageSearch(img)
                        if pos is None:
                            utils.debugPrint("Error occured when searching and adding friend.")
                            self.click(constants.img_backButton, self.gameWindow)
                            return False
                        else:
                            self.click(img, self.gameWindow)
                            if img == constants.img_searchFriends1:
                                pyautogui.typewrite(username)
                                time.sleep(.5)
                            if img == constants.img_backButton:
                                self.click(img, self.gameWindow)
                            break
                pos = utils.imageSearch(constants.img_challengeFriend, self.gameWindow)
                if pos is not None:
                    self.click(constants.img_challengeFriend, self.gameWindow)
                    gameType = utils.timedInput(
                        "Enter wager amount (Only options are 50 and 100). Press CTRL+C to begin typing.",
                        15, ["50", "100"])
                    if gameType is True:
                        pos = utils.imageSearch(constants.img_poolChoice1, self.gameWindow)
                    else:
                        pos = utils.imageSearch(constants.img_poolChoice200_1, self.gameWindow)
                    while pos is None:
                        self.click(constants.img_cheapButtonFriend, self.gameWindow)
                        pos = utils.imageSearch(constants.img_poolChoice1, self.gameWindow)
                    self.click(constants.img_poolChoice1, self.gameWindow)

                    pos = utils.imageSearch(constants.img_playNow, self.gameWindow)
                    while pos is None:
                        pos = utils.imageSearch(constants.img_playNow, self.gameWindow)

                    self.click(constants.img_playNow, self.gameWindow)

                    return True
                else:
                    print("Can\'t challenge friend.")
                    time.sleep(1)
                    return False

    def isGameStart(self):
        limit = 500
        utils.debugPrint("Checking if game has started.")
        pos = utils.imageSearch(constants.img_isGameStart)
        if pos is None:
            while pos is None:
                pos = utils.imageSearch(constants.img_isGameStart)
                if pos is not None:
                    utils.debugPrint("Game in session.")
                    return True
                limit -= 1
                if limit == 0:
                    utils.debugPrint("Unable to determine if game is in session.")
                    return False
                time.sleep(.5)
        else:
            utils.debugPrint("Game in session.")
            return True

    def playPoolGame(self):
        utils.debugPrint("Instancing game.")
        g = game.Game(self.gameWindow)
        utils.debugPrint("Setting up game.")
        status = g.gameSetup()
        if status is False:
            utils.debugPrint("Failed to setup game.")
            return False
        return True

    def spinWin(self, attempts):
        tries_2 = 15
        time.sleep(1)
        gM = self.gameMenuSearch(5)
        if gM is True:
            pass
        else:
            pass

        while tries_2 > 0:
            pos = utils.imageSearch(constants.img_spinWinIcon)
            if pos is None:
                tries_2 -= 1
            else:
                pyautogui.click(pos)
                time.sleep(1)
                while True:
                    pos = utils.imageSearch(constants.img_eightBallSpinButton)
                    if pos is not None:
                        pyautogui.click(pos)
                        break
                time.sleep(.5)
                while True:
                    pos = utils.imageSearch(constants.img_spinWinCollect)
                    if pos is not None:
                        pyautogui.click(pos)
                        break
                time.sleep(.5)
                x_button = 5
                while x_button > 0:
                    pos = utils.imageSearch(constants.img_spinWinX)
                    if pos is not None:
                        pyautogui.click(pos)
                        time.sleep(1)
                    x_button -= 1
                time.sleep(.5)

    def collectCoins(self,attempts):
        attempts += 1
        for i in range(0,attempts):
            time.sleep(.5)
            pos = utils.imageSearch(constants.img_collectCoins)
            if pos is None:
                continue
            else:
                utils.debugPrint("Collecting reward.")
                pyautogui.click(pos)
                time.sleep(.5)
                self.click(constants.img_collectCoins, self.gameWindow)


        tries_3 = 15
        time.sleep(1)
        while True:
            pos = utils.imageSearch(constants.img_alreadyStarted)
            if pos is None:
                pos = utils.imageSearch(constants.img_alreadyStarted1)
                if pos is None:
                    self.clickX()
                    time.sleep(1)
                else:
                    break
            else:
                break

        while tries_3 > 0:
            pos = utils.imageSearch(constants.img_collectCoins)
            if pos is None:
                tries_3 -= 1
            else:
                pyautogui.click(pos)
                time.sleep(1)

    def luckyShot(self, attempts):
        attempts += 1
        for i in range(0, attempts):
            time.sleep(.1)
            pos = utils.imageSearch(constants.img_luckyShot)
            if pos is None:
                continue
            else:
                pos = utils.imageSearch(constants.img_playFree)
                if pos is not None:
                    self.click(constants.img_playFree)
                    utils.debugPrint("LuckyShot minigame beginning")

    def clickX(self):
        xtries = 5
        utils.debugPrint("Searching for \"X\"s...")
        while xtries > 0:
            pos = utils.imageSearch(constants.img_xOut)
            if pos is None:
                utils.debugPrint("\"X\" not found.\nAttempts: " + str(xtries))
                xtries -= 1
            else:
                utils.debugPrint("\"X\" found.")
                pyautogui.click(pos)
                pos = utils.imageSearch(constants.img_alreadyStarted)
                if pos is not None:
                    utils.debugPrint("No additional \"X's\" discovered.")
                    break
                utils.debugPrint("Additional \"X's\" may be onscreen.")

    def refreshPage(self):
        utils.debugPrint("Refreshing page.")
        pos = utils.imageSearch(constants.img_urlBar)
        if pos is None:
            pos = utils.imageSearch(constants.img_unsecure)
            pyautogui.moveTo(pos)
            pyautogui.moveRel(100, None)
            pyautogui.click(clicks=3, duration=0.50)
            pyautogui.typewrite(self.miniclipURL)
            pyautogui.press("enter")
        else:
            pyautogui.moveTo(pos)
            pyautogui.moveRel(100, None)
            pyautogui.click(clicks=3, duration=0.50)
            pyautogui.typewrite(self.miniclipURL)
            pyautogui.press("enter")

        time.sleep(5)

def startBot():
    bot1 = Bot()
    print("Bot {} initialized.".format(bot1.name))

def main():
    resolutions = ["1920x1080", "1680x1050", "1600x900", "1440x900", "1366x768", "1360x768", "1280x1024", "1280x800"]
    currentRes = str(GetSystemMetrics(0)) + "x" + str(GetSystemMetrics(1))
    if currentRes not in resolutions:
        print("*Resolution not supported* \nSupported Resolutions: " + " - ".join(str(i) for i in resolutions))
    else:
        print("Detected Supported Screen Resolution: {}".format(currentRes))
        print("-" * 47 + "\nThis bot has been tested to work in Google Chrome.\nFunctionality with other browsers is"
                         " not currently available.")
        start = utils.timedInput("Launch bot? Press CTRL+C to being typing. ", 30, ["yes", "no"])
        if start is False:
            print("Exiting..")
            sys.exit()
        else:
            bot1 = Bot()
            log = utils.timedInput("Enable Developer/Debug Log? Press CTRL+C to begin typing.", 10, ["yes", "no"])
            if log is True:
                constants.debug = True
                print("DEV/DEBUG LOGS ENABLED\n--------------\nStarting..")
            bot1.start()


if __name__ == "__main__":
    main()
