import json
import os
import sys
import time
import webbrowser
import random

import cv2
import imutils
import numpy as np
import pyautogui
import requests


class Bot:

    def __init__(self):
        self.miniclipurl = 'https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/'
        self.height = None
        self.width = None
        self.email = "pefumewora@fxprix.com"
        self.password = "thisisapassword1"
        self.gameWindow = None

    @staticmethod
    def imageSearch(image, region=None):
        if region is None:
            pos = pyautogui.locateCenterOnScreen(Bot.imagePath(image))
            return pos
        else:
            pos = pyautogui.locateCenterOnScreen(Bot.imagePath(image), region=region)
            return pos

    @staticmethod
    def imagePath(filename):
        return os.path.join('images', filename)

    def start(self):
        count = 5
        while count > 0:
            print('Checking for URL...')
            pos = self.imageSearch('url.png')
            if pos is None:
                pos = self.imageSearch('url2.png')
                if pos is None:
                    count -= 1
                    time.sleep(1)
                else:
                    count = 5
                    break
            else:
                count = 5
                break

        if count == 0:
            print('Did not detect website. Opening new tab.')
            webbrowser.open(self.miniclipurl)
            time.sleep(5)
            self.start()
        else:
            self.ifLogin()

    def ifLogin(self):
        check = self.loginCheck()
        if check is True:
            self.getGameRegion(check)
            self.navigateMenu(check)
        else:
            self.getGameRegion(check)
            self.navigateMenu(check)

    def getGameRegion(self, truthVal):
        tries = 3
        regiontries = 20
        self.height, self.width = self.miniclipAPI()
        time.sleep(3)
        self.clickX()
        while tries > 0:
            pos = self.imageSearch('alreadystarted.png')
            if pos is None:
                pos = self.imageSearch('alreadystarted1.png')
                if pos is None:
                    time.sleep(1)
                    tries -= 1
                else:
                    print('Game menu found.')
            else:
                print('Game menu found.')

            if truthVal is False:
                time.sleep(1)
                print('Searching for game region..')
                reg = pyautogui.locateOnScreen(self.imagePath('top_right_corner.png'))
                if reg is not None:
                    topRX = reg[0] + reg[2]
                    topRY = reg[1]
                    self.gameWindow = (topRX - self.width, topRY, self.width, self.height)
                    print('Region acquired.' + str(self.gameWindow))
                    break
                else:
                    while regiontries > 0:
                        reg2 = pyautogui.locateOnScreen(self.imagePath('top_right_corner.png'))
                        if reg2 is None:
                            regiontries -= 1
                        elif reg2 is not None:
                            topRX = reg2[0] + reg2[2]
                            topRY = reg2[1]
                            self.gameWindow = (topRX - self.width, topRY, self.width, self.height)
                            print('Region acquired.' + str(self.gameWindow))
                            return

            elif truthVal is True:
                time.sleep(1)
                print('Searching for game region..')
                reg = pyautogui.locateOnScreen(self.imagePath('top_right_corner_logged.png'))
                if reg is not None:
                    topRX = reg[0] + reg[2]
                    topRY = reg[1]
                    self.gameWindow = (topRX - self.width, topRY, self.width, self.height)
                    print('Region acquired.' + str(self.gameWindow))
                    break
                elif reg is None:
                    while regiontries > 0:
                        reg2 = pyautogui.locateOnScreen(self.imagePath('top_right_corner_logged.png'))
                        if reg2 is None:
                            regiontries -= 1
                        elif reg2 is not None:
                            topRX = reg2[0] + reg2[2]
                            topRY = reg2[1]
                            self.gameWindow = (topRX - self.width, topRY, self.width, self.height)
                            print('Region acquired.' + str(self.gameWindow))
                            return
        if 3 > tries > 0:
            tries -= 1
            print(str(tries) + ' official tries left.')
            regiontries = 20

    def miniclipAPI(self):
        api_url_base = 'https://webmasters.miniclip.com/api/'
        api_url = '{0}/games/2471/en.json'.format(api_url_base)

        try:
            response = requests.get(api_url)
        except requests.exceptions.ConnectionError:
            requests.status_code = 'Connection refused'
            for i in range(1, 5):
                time.sleep(1)
                response = requests.get(api_url)
                self.miniclipAPI()

        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            h = int(data['2471'].get('height'))
            w = int(data['2471'].get('width'))
            return h, w

    def navigateMenu(self, truthVal):
        if truthVal is True:
            time.sleep(1)
            self.spinWin()
            self.collectCoins()
            self.decideGame()
        else:
            pos = self.imageSearch('play_button.png', self.gameWindow)
            if pos is None:
                self.refreshPage()
                self.navigateMenu(truthVal)
            else:
                print('Logging in.')
                pyautogui.click(pos)
                time.sleep(2)
                pos = self.imageSearch('login1_button.png', self.gameWindow)
                if pos is None:
                    time.sleep(1)
                    pos = self.imageSearch('login2_button.png', self.gameWindow)
                    if pos is None:
                        print('Unable to find login button. Please try again.')
                        self.start()
                    else:
                        pyautogui.click(pos)
                        time.sleep(1)
                        self.logIn()
                        self.navigateMenu(truthVal)
                else:
                    pyautogui.click(pos)
                    time.sleep(1)
                    self.logIn()
                    self.navigateMenu(truthVal)

    def decideGame(self):
        self.clickX()
        while True:
            pos = self.imageSearch('alreadystarted.png')
            if pos is None:
                pos = self.imageSearch('alreadystarted1.png')
                if pos is None:
                    time.sleep(1)
                else:
                    break
            else:
                break

        pf = self.playFriends()
        if pf is False:
            time.sleep(1)
            pos = self.imageSearch('play_button_logged.png', region=self.gameWindow)
            pyautogui.click(pos)
            pos = self.imageSearch('poolchoice.png', region=self.gameWindow)
            pos2 = self.imageSearch('cheap_button.png', region=self.gameWindow)
            while pos is None:
                pyautogui.click(pos2)
                time.sleep(1)
                pos = self.imageSearch('poolchoice.png', region=self.gameWindow)

            pos = self.imageSearch('startgame_button.png', region=self.gameWindow)
            if pos is not None:
                print('Begin game? Press Control+C to begin typing. ')
                try:
                    for i in range(0, 15):
                        time.sleep(1)
                    print('Waited 15 seconds for a response. Beginning game.')
                    pyautogui.click(pos)
                    time.sleep(8)
                    self.playPoolGame()
                except KeyboardInterrupt:
                    startgame = input(': ').replace(' ', '')
                    if any(c in startgame.lower() for c in ('y', 'e', 's')):
                        time.sleep(8)
                        self.playPoolGame()
                    elif any(c in startgame.lower() for c in ('n', 'o')):
                        pos = self.imageSearch('mainmenu_before.png', region=self.gameWindow)
                        pyautogui.click(pos)
                        begingame = input('Start a game?')
                        begingame.replace(' ', '')
                        if any(c in begingame.lower() for c in ('y', 'e', 's')):
                            self.decideGame()
                        else:
                            print('Exiting 8 ball bot.')
                            sys.exit()
                    else:
                        pos = self.imageSearch('mainmenu_button.png', region=self.gameWindow)
                        pyautogui.click(pos)
                        begingame2 = input('Start?')
                        begingame2.replace(' ', '')
                        if any(c in begingame2.lower() for c in ('y', 'e', 's')):
                            self.decideGame()
                        else:
                            print('Exiting 8 ball bot.')
                            sys.exit()
        else:
            self.playPoolGame()

    def playFriends(self):
        friendchoice = ['friends', 'friend', 'friennd', 'friennds']
        randomchoice = ['randoms', 'random']
        noresponse = 10
        findhole = 10
        print('Play with \'friends\' or \'randoms\'? Press Control+C to begin typing. ')
        try:
            for i in range(0, 20):
                time.sleep(1)
            print('Waited 20 seconds for a response. Beginning random game.')
            return False
        except KeyboardInterrupt:
            playchoice = input(': ').replace(' ', '')
            if playchoice.lower() in friendchoice:
                pos = self.imageSearch('playfriends.png', self.gameWindow)
                pyautogui.click(pos)
                time.sleep(1)
                pos = self.imageSearch('search_friends.png', self.gameWindow)
                if pos is not None:
                    username = input('Please enter the username of your opponent: ')
                    time.sleep(1)
                    pyautogui.click(pos)
                    time.sleep(1)
                    pyautogui.typewrite(username)
                    pyautogui.press('enter')
                    time.sleep(1)
                pos = self.imageSearch('add_friend.png', self.gameWindow)
                if pos is not None:
                    pyautogui.click(pos)
                    time.sleep(1)
                    pos = self.imageSearch('challenge_friend.png', self.gameWindow)
                    pyautogui.click(pos)
                    return True
                else:
                    pos = self.imageSearch('challenge_friend.png', self.gameWindow)
                    if pos is not None:
                        pyautogui.click(pos)
                        print('Waiting for response.')
                        while noresponse > 0:
                            time.sleep(1)
                            pos = self.imageSearch('no_response.png', self.gameWindow)
                            if pos is None:
                                noresponse -= 1
                            else:
                                time.sleep(2)
                                self.decideGame()
                        print('Checking to see if game has started.')
                        if noresponse == 0:
                            while findhole > 0:
                                time.sleep(1)
                                pos = self.imageSearch('toplefthole.png', self.gameWindow)
                                if pos is not None:
                                    print('Game Started.')
                                    return True
                                else:
                                    findhole -= 1
                        if findhole == 0:
                            time.sleep(2)
                            pos = self.imageSearch('search_friendsmagni.png', self.gameWindow)
                            if pos is not None:
                                self.decideGame()
                            else:
                                self.refreshPage()
                                time.sleep(1)
                                self.decideGame()
                    else:
                        print('Can\'t find friend.')
                        self.decideGame()
            elif playchoice in randomchoice:
                return False

    def playPoolGame(self):
        print(self.gameWindow)
        game = Game(self.gameWindow)
        game.gameSetup()
        if game.status == 'failed':
            print('Refreshing page.')
            self.refreshPage()
            time.sleep(3)
            self.start()

    def loginCheck(self):
        time.sleep(1)
        pos = self.imageSearch('url.png')
        pos2 = self.imageSearch('url2.png')
        if pos is None and pos2 is None:
            print('Opening new tab because old one is now longer visible.')
            webbrowser.open('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
            time.sleep(2)
            check1 = self.loginCheck()
            if check1 is True:
                return True
            else:
                return False

        else:
            time.sleep(2)
            pos = self.imageSearch('enableflash_0.png')
            if pos is None:
                pos = self.imageSearch('enableflash_1.png')
                if pos is None:
                    pos = self.imageSearch('enableflash_2.png')
                    if pos is None:
                        pos = self.imageSearch('allow.png')
                        if pos is None:
                            pos = self.imageSearch('url.png')
                            pos2 = self.imageSearch('url2.png')
                            if pos is None and pos2 is None:
                                print('Please stay on the opened web page.')
                                webbrowser.open('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
                                time.sleep(2)
                                check1 = self.loginCheck()
                                if check1 is True:
                                    return True
                                else:
                                    return False
                            else:
                                pass
                        else:
                            pyautogui.click(pos)
                            time.sleep(1)
                    else:
                        pyautogui.click(pos)
                        time.sleep(1)
                else:
                    pyautogui.click(pos)
                    time.sleep(1)
                    pos = self.imageSearch('enableflash_2.png')
                    if pos is None:
                        self.refreshPage()
                        time.sleep(2)
                        check1 = self.loginCheck()
                        if check1 is True:
                            return True
                        else:
                            return False
                    else:
                        pyautogui.click(pos)
                        time.sleep(1)
                        pos = self.imageSearch('allow.png')
                        if pos is None:
                            pass
                        else:
                            pyautogui.click(pos)
                            time.sleep(1)
            else:
                pyautogui.click(pos)
                time.sleep(1)
                pos = self.imageSearch('enableflash_2.png')
                if pos is None:
                    print('Please stay on the opened web page.')
                    webbrowser.open('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
                    time.sleep(2)
                    check1 = self.loginCheck()
                    if check1 is True:
                        return True
                    else:
                        return False
                else:
                    pyautogui.click(pos)
                    time.sleep(1)
                    pos = self.imageSearch('allow.png')
                    if pos is None:
                        pass
                    else:
                        pyautogui.click(pos)
                        time.sleep(1)

        pos = self.imageSearch('signup_login_button.png')
        if pos is None:
            pos = self.imageSearch('defaultaccount.png')
            if pos is None:
                pos = self.imageSearch('url.png')
                if pos is None:
                    print('Opening new tab because old one is now longer visible.')
                    webbrowser.open('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
                    time.sleep(2)
                    check1 = self.loginCheck()
                    if check1 is True:
                        return True
                    else:
                        return False
                else:
                    account = input('Are you logged into your own account?')
                    if any(c in account.lower().replace(' ', '') for c in ('y', 'e', 's')):
                        default = input('Would you like to save it as the default?')
                        if any(c in default.lower().replace(' ', '') for c in ('y', 'e', 's')):
                            reg = self.imageSearch('facebooklogo.png')
                            pyautogui.screenshot('images\defaultaccount.png',
                                                 region=((reg[0] + reg[2]) - 170, reg[1], 170, 40))
                            newemail = input('Please enter the email associated with the account.')
                            newpass = input('Please enter the password associated with the account.')
                            confirm = input('User is {} and the password is {}?'.format(newemail, newpass))
                            if any(c in default.lower().replace(' ', '') for c in ('y', 'e', 's')):
                                with open('default.txt', 'w') as f:
                                    for line in f:
                                        if line is None:
                                            f.write('{} {}'.format(newemail, newpass))
                                            print('New default account set.')
                                            f.close()
                                            return True
                                        else:
                                            with open('default.txt', 'w') as g:
                                                g.write('{} {}'.format(newemail, newpass))
                                                print('New default account set.')
                                                g.close()
                                                return True
                            else:
                                newemail = input('Please enter the email associated with the account.')
                                newpass = input('Please enter the password associated with the account.')
                                confirm = input('User is {} and the password is {}?'.format(newemail, newpass))
                                if any(c in confirm.lower().replace(' ', '') for c in ('y', 'e', 's')):
                                    with open('default.txt', 'r') as f:
                                        for line in f:
                                            if line is None:
                                                f.write('{} {}'.format(newemail, newpass))
                                                print('New default account set.')
                                                f.close()
                                                return True
                                            else:
                                                with open('default.txt', 'w') as g:
                                                    g.write('{} {}'.format(newemail, newpass))
                                                    print('New default account set.')
                                                    g.close()
                                                    return True
                                else:
                                    print('Restarting login check.')
                                    check1 = self.loginCheck()
                                    if check1 is True:
                                        return True
                                    else:
                                        return False
                        else:
                            print('Proceeding without official check.')
                            return True
                    else:
                        time.sleep(1)
                        self.refreshPage()
                        time.sleep(1)
                        check1 = self.loginCheck()
                        if check1 is True:
                            return True
                        else:
                            return False
            else:
                print('Logged into default account.')
                return True
        else:
            time.sleep(1)
            print('You are not logged in.')
            return False

    def logIn(self):
        print('Do you have an account you\'d like the bot to play on? Press Ctrl+C to begin typing.')
        try:
            for i in range(0, 10):
                time.sleep(1)
            print('Waited 10 seconds for a response. Using default.')
            with open('default.txt', 'r') as f:
                for line in f:
                    self.email, self.password = line.split(' ')
            pos = self.imageSearch('email_area.png', self.gameWindow)
            pyautogui.click(pos)
            time.sleep(1)
            pyautogui.typewrite(self.email)
            time.sleep(1)
            pos = self.imageSearch('password_area.png', self.gameWindow)
            pyautogui.click(pos)
            time.sleep(1)
            pyautogui.typewrite(self.password)
            time.sleep(1)
            pos = self.imageSearch('login3_button.png', self.gameWindow)
            pyautogui.click(pos)

        except KeyboardInterrupt:
            account = input(': ').replace(' ', '')
            if any(c in account.lower() for c in ('y', 'e', 's')):
                self.email = input('Please enter the email. ').replace(' ', '')
                self.password = input('Please enter the email. ').replace(' ', '')
                self.logIn()
            else:
                print('Using default email.')
                with open('default.txt', 'r') as f:
                    for line in f:
                        if line is None:
                            print("No account on file. Using default.")
                            break
                        else:
                            email, password = line.split(' ')
                            break
                pos = self.imageSearch('email_area.png', self.gameWindow)
                pyautogui.click(pos)
                time.sleep(1)
                pyautogui.typewrite(self.email)
                time.sleep(1)
                pos = self.imageSearch('password_area.png', self.gameWindow)
                pyautogui.click(pos)
                time.sleep(1)
                pyautogui.typewrite(self.password)
                time.sleep(1)
                pos = self.imageSearch('login3_button.png', self.gameWindow)
                pyautogui.click(pos)

    def spinWin(self):
        tries_2 = 15
        time.sleep(1)
        while True:
            pos = self.imageSearch('alreadystarted.png')
            if pos is None:
                pos = self.imageSearch('alreadystarted1.png')
                if pos is None:
                    self.clickX()
                    time.sleep(1)
                else:
                    break
            else:
                break

        while tries_2 > 0:
            pos = self.imageSearch('spinwinicon.png')
            if pos is None:
                tries_2 -= 1
            else:
                pyautogui.click(pos)
                time.sleep(1)
                pos = self.imageSearch('8ballspin_button.png')
                pyautogui.moveTo(pos)
                pyautogui.mouseDown(button='left')
                pyautogui.moveRel(None, 250)
                pyautogui.mouseUp(button='left')
                time.sleep(7)
                pos = self.imageSearch('8ballwinx.png')
                pyautogui.click(pos)
                time.sleep(2)
                pos = self.imageSearch('xout.png')
                pyautogui.click(pos)

    def collectCoins(self):
        tries_3 = 15
        time.sleep(1)
        while True:
            pos = self.imageSearch('alreadystarted.png')
            if pos is None:
                pos = self.imageSearch('alreadystarted1.png')
                if pos is None:
                    self.clickX()
                    time.sleep(1)
                else:
                    break
            else:
                break

        while tries_3 > 0:
            pos = self.imageSearch('collectcoins.png')
            if pos is None:
                tries_3 -= 1
            else:
                pyautogui.click(pos)
                time.sleep(1)

    def clickX(self):
        xtries = 5
        print('Searching for \'X\'s...')
        while xtries > 0:
            pos = self.imageSearch('xout.png')
            if pos is None:
                xtries -= 1
            else:
                pyautogui.click(pos)
                pos = self.imageSearch('alreadystarted.png')
                if pos is None:
                    continue
                else:
                    break

    def refreshPage(self):
        pos = self.imageSearch('urlbar.png')
        if pos is None:
            pos = self.imageSearch('unsecure.png')
            pyautogui.moveTo(pos)
            pyautogui.moveRel(100, None)
            pyautogui.click(clicks=3, duration=0.50)
            pyautogui.typewrite(self.miniclipurl)
            pyautogui.press('enter')
        else:
            pyautogui.moveTo(pos)
            pyautogui.moveRel(100, None)
            pyautogui.click(clicks=3, duration=0.50)
            pyautogui.typewrite(self.miniclipurl)
            pyautogui.press('enter')


class Game:

    def __init__(self, inputWindow):
        self.poolRegion = (0, 0, 0, 0)
        self.gameWindow = inputWindow
        self.gameNum = 0
        self.newGameNum = 0
        self.turnNum = 0
        self.imgPath = None
        self.status = "working"

    def gameSetup(self):

        with open('gamecounter.txt', 'r') as g:
            for line in g:
                if line is None:
                    g.write('0')
                else:
                    self.gameNum = int(line)
                    self.newGameNum = str(self.gameNum + 1)
                    with open('gamecounter.txt', 'w') as g2:
                        g2.write(self.newGameNum)
                        g2.close()
            g.close()

        os.makedirs('games\game' + self.newGameNum + '\\table', exist_ok=True)
        os.makedirs('games\game' + self.newGameNum + '\\outlined', exist_ok=True)

        self.isGameStart()
        print('Game #' + self.newGameNum)

        while True:
            pyautogui.screenshot(('games\game' + self.newGameNum + '\\table\pooltable' + str(self.turnNum) + '.png'),
                                 region=self.poolRegion)
            roundstart = Round(self.turnNum, self.newGameNum, self.poolRegion, self.gameWindow)
            roundstart.start()

    def isGameStart(self):
        leftpocketnum = 10

        while True:
            pos = Bot.imageSearch('toplefthole.png', self.gameWindow)
            if pos is not None:
                print('Game in session. Checking for turn.')
                time.sleep(1)
                reg = pyautogui.locateOnScreen(Bot.imagePath('poolrightcorner.png'), region=self.gameWindow)
                if reg is None:
                    reg = pyautogui.locateOnScreen(Bot.imagePath('toprighthole.png'), region=self.gameWindow)
                topRX = reg[0] + reg[2]
                topRY = reg[1]
                self.poolRegion = (topRX - 605, topRY, 605, 314)
                print('Table region acquired.' + str(self.poolRegion))
                break
            else:
                pos = Bot.imageSearch('poolrightcorner.png', self.gameWindow)
                if pos is not None:
                    print('Game in session. Checking for turn.')
                    reg = pyautogui.locateOnScreen(Bot.imagePath('poolrightcorner.png'), region=self.gameWindow)
                    if reg is None:
                        reg = pyautogui.locateOnScreen(Bot.imagePath('toprighthole.png'), region=self.gameWindow)
                    topRX = reg[0] + reg[2]
                    topRY = reg[1]
                    self.poolRegion = (topRX - 605, topRY, 605, 314)
                    print('Table region acquired.' + str(self.poolRegion))
                    break
                else:
                    time.sleep(1)
                    leftpocketnum -= 1

            if leftpocketnum == 0:
                print('Did not find top left pocket.')
                self.status = 'failed'
                time.sleep(2)

    def turnCycle(self):
        while True:
            turn1 = self.checkTurn()
            if turn1 is True:
                self.turnNum += 1
                print('Bot\'s turn.')
            else:
                time.sleep(1)

    def checkTurn(self):
        while True:
            pos = Bot.imageSearch('turn.png', self.poolRegion)
            if pos is not None:
                return True
            else:
                pos = Bot.imageSearch('turn1.png', self.poolRegion)
                if pos is not None:
                    return True
                else:
                    return False


class Round:

    def __init__(self, inputTurn, inputGameNum, inputPoolRegion, inputGameWindow):
        self.ballList = []
        self.opponentList = []
        self.suit = None
        self.turnNum = inputTurn
        self.gameNum = inputGameNum
        self.holeLocation = {'tlh.png', 'tmh.png', 'tlh.png', 'blh.png', 'bmh.png', 'brh.png'}
        self.imgPath = '/games/game' + self.gameNum + '/table/pooltable' + str(self.turnNum) + '.png'
        self.roundImage = None
        self.poolRegion = inputPoolRegion
        self.gameWindow = inputGameWindow

    def start(self):
        cwd = os.getcwd()
        self.imgPath = cwd + self.imgPath

        self.markHoles()

        time.sleep(1)
        print('Turn #' + str(self.turnNum))

        self.ballCheck()
        self.prepareBalls()

        if self.turnNum > 10 and self.suit == 'nosuit':
            print('No suit detected.')
            self.breakBalls()
        else:
            print('Assigned suit: {}'.format(self.suit))

            self.ballCalc()
            self.hitBall()

        self.moveMouseOut()

        self.checkRoundOver()
        self.checkGameOver()

    def markHoles(self):
        for k, v in self.holeLocation:
            if v is None:
                pos = Bot.imageSearch(k, self.poolRegion)
                if pos is not None:
                    self.holeLocation[k] = pos
                else:
                    print('Could not find ' + k + ' hole.')
            else:
                pass

    def ballCalc(self):
        for b in self.ballList:
            self.determineDistanceBetween()
            self.determineAngleBetween()
            self.checkPathofBall()

######################
    def breakBalls(self):
        breakRack = True

        for b in self.ballList:
            if 829 > b.center[0] > 797 and 466 > b.center[1] > 434 or 1178 > b.center[0] > 1089 and 503 > b.center[1] > 401:
                continue
            else:
                breakRack = False
                break

        if breakRack is True:
            print('Breaking.')
            randNum = random.randint(0,10)
            if randNum > 5:
                for b in self.ballList:
                    if b.name == 'cueball':
                        pyautogui.click(b.center[0]+190, b.center[1], duration=1.5)
                        pyautogui.moveRel(-200, 0)
            else:
                #generate new break
                x,y = random.randrange(-100, 0), random.randrange(-100,100)
                pyautogui.click(b.center, duration= 1.5)
                pyautogui.moveRel(random.randrange(x,y))
                b.center = x, y

                self.ballCalc()
                pass
        else:
            self.ballCalc()

            self.hitBall()

##################


    def ballCheck(self):
        standard = {'cueball': 'white', 'eightball': 'black'}
        solids = {'1ball.png': 'yellow', '2ball.png': 'blue', '3ball.png': 'lightred', '4ball.png': 'purple',
                  '5ball.png': 'orange', '6ball.png': 'green', '7ball.png': 'darkred'}
        stripes = {'9ball.png': 'yellow', '10ball.png': 'blue', '11ball.png': 'lightred', '12ball.png': 'purple',
                   '13ball.png': 'orange', '14ball.png': 'green', '15ball.png': 'darkred'}

        pyautogui.moveTo(0, 0)
        pos = Bot.imageSearch('ballpic1.png', self.gameWindow)

        if pos is not None:
            topRX = pos[0] + pos[2]
            topRY = pos[1]
            reg = (topRX - 176, topRY, 176, 90)
        else:
            reg = (pos[0] + 78, pos[1] + 80, 176, 90)

        for k, v in standard:
            ball = Ball('nosuit', k, v)
            self.ballList.append(ball)

        for k, v in solids:
            pos = Bot.imageSearch(k, reg)
            if pos is not None:
                self.suit = 'solid'
                ball = Ball('solid', k.replace('.png', ''), v)
                self.ballList.append(ball)

        for k, v in stripes:
            pos = Bot.imageSearch(k, reg)
            if pos is not None:
                self.suit = 'stripe'
                ball = Ball('stripe', k.replace('.png', ''), v)
                self.ballList.append(ball)

        if len(self.ballList) >= 2:
            self.suit = 'nosuit'
            for k, v in solids:
                ball = Ball('solid', k.replace('.png', ''), v)
                self.ballList.append(ball)

            for k, v in stripes:
                ball = Ball('stripe', k.replace('.png', ''), v)
                self.ballList.append(ball)

    def prepareBalls(self):
        self.maskSetup()
        self.outlineBall()

    def maskSetup(self):  # sets up masks for each ball based on which are in need to be hit
        self.roundImage = cv2.imread(self.imgPath, 1)
        hsv = cv2.cvtColor(self.roundImage, cv2.COLOR_BGR2HSV)

        for b in self.ballList:
            if b.color == 'white':
                upper_whitecue = np.array([180, 50, 255])
                lower_whitecue = np.array([0, 10, 80])
                maskwhiteball = cv2.inRange(hsv, lower_whitecue, upper_whitecue)
                b.mask = maskwhiteball
            elif b.color == 'black':
                upper_black = np.array([50, 225, 50])
                lower_black = np.array([10, 0, 0])
                maskblackball = cv2.inRange(hsv, lower_black, upper_black)
                b.mask = maskblackball
            elif b.color == 'yellow':
                upper_yellow = np.array([25, 255, 255])
                lower_yellow = np.array([23, 150, 100])
                maskyellowball = cv2.inRange(hsv, lower_yellow, upper_yellow)
                maskyellowball = cv2.dilate(maskyellowball, None, iterations=1)
                b.mask = maskyellowball
            elif b.color == 'blue':
                upper_blue = np.array([135, 255, 255])
                lower_blue = np.array([112, 70, 100])
                maskblueball = cv2.inRange(hsv, lower_blue, upper_blue)
                b.mask = maskblueball
            elif b.color == 'lightred':
                upper_lightred = np.array([4, 255, 250])
                lower_lightred = np.array([0, 105, 150])
                masklightredball = cv2.inRange(hsv, lower_lightred, upper_lightred)
                b.mask = masklightredball
            elif b.color == 'purple':
                upper_purple = np.array([160, 255, 255])
                lower_purple = np.array([135, 50, 70])
                maskpurpleball = cv2.inRange(hsv, lower_purple, upper_purple)
                b.mask = maskpurpleball
            elif b.color == 'orange':
                upper_orange = np.array([19, 255, 255])
                lower_orange = np.array([11, 150, 170])
                maskorangeball = cv2.inRange(hsv, lower_orange, upper_orange)
                b.mask = maskorangeball
            elif b.color == 'green':
                upper_green = np.array([60, 255, 255])
                lower_green = np.array([53, 70, 50])
                maskgreenball = cv2.inRange(hsv, lower_green, upper_green)
                b.mask = maskgreenball
            elif b.color == 'darkred':
                upper_darkred = np.array([4, 255, 180])
                lower_darkred = np.array([3, 50, 50])
                maskdarkredball = cv2.inRange(hsv, lower_darkred, upper_darkred)
                b.mask = maskdarkredball

        try:
            cv2.imshow('mask', maskwhiteball)
            cv2.imshow('mask1', maskblackball)
            cv2.imshow('mask2', maskblueball)
            cv2.imshow('mask3', masklightredball)
            cv2.imshow('mask4', maskdarkredball)
            cv2.imshow('mask5', maskgreenball)
            cv2.imshow('mask6', maskorangeball)
            cv2.imshow('mask7', maskyellowball)
            cv2.imshow('mask8', maskpurpleball)

            cv2.imshow('circle', self.roundImage)

            while 1:
                k = cv2.waitKey(0)
                if k == 27:
                    break
        except UnboundLocalError:
            pass

            cv2.destroyAllWindows()

    def outlineBall(self):  # draws contours, but more importantly, gets the center points of each ball

        for b in self.ballList:
            colorRGB = self.stringToColor(b.color)
            contours = cv2.findContours(b.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if imutils.is_cv2() else contours[1]
            if b.name == 'cue' or 'eightball':
                if len(contours) >= 1:
                    c = max(contours, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    m = cv2.moments(c)
                    center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                    b.center = center

                    if 12 > radius > 6:
                        cv2.circle(self.roundImage, (int(x), int(y)), int(radius - 2), colorRGB, 2)
                        cv2.circle(self.roundImage, b.center, 7, colorRGB, -1)

                    print('{} found at {}.'.format(b.name, b.center))
                else:
                    print('{} could not be found. {}.'.format(b.name, b.center))

            else:
                if len(contours) == 0:
                    print('{} could not be found. {}.'.format(b.name, b.center))
                    continue
                elif len(contours) == 1:  # only one suit on the board
                    if self.suit == 'solid':
                        c = max(contours, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        m = cv2.moments(c)
                        center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                        b.center = center

                        if 12 > radius > 6:
                            cv2.circle(self.roundImage, (int(x), int(y)), int(radius - 2), colorRGB, 2)
                            cv2.circle(self.roundImage, center, 7, colorRGB, -1)

                    elif self.suit == 'stripe':
                        c = min(contours, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        m = cv2.moments(c)
                        center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                        b.center = center

                        if 12 > radius > 6:
                            cv2.circle(self.roundImage, (int(x), int(y)), int(radius - 2),
                                       (colorRGB[0] - 20, colorRGB[1] - 25, colorRGB[2] - 20), 2)

                    elif self.suit == 'nosuit':
                        c = max(contours, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        m = cv2.moments(c)
                        center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                        b.center = center

                        if 12 > radius > 6:
                            cv2.circle(self.roundImage, (int(x), int(y)), int(radius - 2), colorRGB, 2)

                    self.savePic()
                    print('{} found at {}.'.format(b.name, b.center))

                elif len(contours) == 2:  # both solid and stripes on the board
                    if self.suit == 'solid':
                        cmax = max(contours, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(cmax)
                        m = cv2.moments(cmax)
                        centermax = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                        b.center = centermax

                        if 12 > radius > 6:
                            cv2.circle(self.roundImage, (int(x), int(y)), int(radius - 2), colorRGB, 2)
                            cv2.circle(self.roundImage, centermax, 7, colorRGB, -1)

                        cmin = min(contours, key=cv2.contourArea)
                        ((xmin, ymin), radiusmin) = cv2.minEnclosingCircle(cmin)
                        m1 = cv2.moments(cmin)
                        centermin = (int(m1['m10'] / m1['m00']), int(m1['m01'] / m1['m00']))
                        self.opponentList.append(centermin)

                        if 12 > radius > 6:
                            cv2.circle(self.roundImage, (int(xmin), int(ymin)), int(radiusmin - 2),
                                       (colorRGB[0] - 20, colorRGB[1] - 25, colorRGB[2] - 20), 2)

                        self.savePic()
                        print('{} found at {}.'.format(b.name, b.center))

                    elif self.suit == 'stripe':
                        cmax = max(contours, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(cmax)
                        m = cv2.moments(cmax)
                        centermax = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                        self.opponentList.append(centermax)

                        if 12 > radius > 6:
                            cv2.circle(self.roundImage, (int(x), int(y)), int(radius - 2), colorRGB, 2)
                            cv2.circle(self.roundImage, centermax, 7, colorRGB, -1)

                        cmin = min(contours, key=cv2.contourArea)
                        ((xmin, ymin), radiusmin) = cv2.minEnclosingCircle(cmin)
                        m1 = cv2.moments(cmin)
                        centermin = (int(m1['m10'] / m1['m00']), int(m1['m01'] / m1['m00']))
                        b.center = centermin

                        if 12 > radius > 6:
                            cv2.circle(self.roundImage, (int(xmin), int(ymin)), int(radiusmin - 2),
                                       (colorRGB[0] - 20, colorRGB[1] - 25, colorRGB[2] - 20), 2)

                        self.savePic()
                        print('{} found at {}.'.format(b.name, b.center))

                    elif self.suit == 'nosuit':
                        if b.suit == 'solid':
                            c = max(contours, key=cv2.contourArea)
                            ((x, y), radius) = cv2.minEnclosingCircle(c)
                            m = cv2.moments(c)
                            center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                            b.center = center

                            if 12 > radius > 6:
                                cv2.circle(self.roundImage, (int(x), int(y)), int(radius - 2), colorRGB, 2)
                                cv2.circle(self.roundImage, center, 7, colorRGB, -1)
                        else:
                            c = min(contours, key=cv2.contourArea)
                            ((x, y), radius) = cv2.minEnclosingCircle(c)
                            m1 = cv2.moments(c)
                            center = (int(m1['m10'] / m1['m00']), int(m1['m01'] / m1['m00']))
                            b.center = center

                            if 12 > radius > 6:
                                cv2.circle(self.roundImage, (int(x), int(y)), int(radius - 2),
                                           (colorRGB[0] - 20, colorRGB[1] - 25, colorRGB[2] - 20), 2)

                            self.savePic()
                            print('{} found at {}.'.format(b.name, b.center))


                elif len(contours) > 2:
                    if self.suit == 'solid':
                        cmax = max(contours, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(cmax)
                        m = cv2.moments(cmax)
                        centermax = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                        b.center = centermax

                        if 12 > radius > 6:
                            cv2.circle(self.roundImage, (int(x), int(y)), int(radius - 2), colorRGB, 2)
                            cv2.circle(self.roundImage, centermax, 7, colorRGB, -1)

                        contours.remove(max(contours))
                        cmid = max(contours, key=cv2.contourArea)
                        ((xmid, ymid), radiusmid) = cv2.minEnclosingCircle(cmid)
                        m1 = cv2.moments(cmid)
                        centermid = (int(m1['m10'] / m1['m00']), int(m1['m01'] / m1['m00']))
                        self.opponentList.append(centermid)

                        if 12 > radiusmid > 6:
                            cv2.circle(self.roundImage, (int(xmid), int(ymid)), int(radius - 2),
                                       (colorRGB[0] - 20, colorRGB[1] - 25, colorRGB[2] - 20), 2)

                        self.savePic()
                        print('{} found at {}.'.format(b.name, b.center))

                    elif self.suit == 'stripe':
                        c = max(contours, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        m = cv2.moments(c)
                        centermax = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                        b.center = centermax

                        if 12 > radius > 6:
                            cv2.circle(self.roundImage, (int(x), int(y)), int(radius - 2), colorRGB, 2)
                            cv2.circle(self.roundImage, centermax, 7, colorRGB, -1)

                        contours.remove(max(contours))
                        cmid = max(contours, key=cv2.contourArea)
                        ((xmid, ymid), radiusmid) = cv2.minEnclosingCircle(cmid)
                        m1 = cv2.moments(cmid)
                        centermid = (int(m1['m10'] / m1['m00']), int(m1['m01'] / m1['m00']))
                        self.opponentList.append(centermid)

                        if 12 > radiusmid > 6:
                            cv2.circle(self.roundImage, (int(xmid), int(ymid)), int(radiusmid - 2),
                                       (colorRGB[0] - 20, colorRGB[1] - 25, colorRGB[2] - 20), 2)

                        self.savePic()
                        print('{} found at {}.'.format(b.name, b.center))

                    elif self.suit == 'nosuit':
                        if b.suit == 'solid':
                            c = max(contours, key=cv2.contourArea)
                            ((x, y), radius) = cv2.minEnclosingCircle(c)
                            m = cv2.moments(c)
                            centermax = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                            b.center = centermax

                            if 12 > radius > 6:
                                cv2.circle(self.roundImage, (int(x), int(y)), int(radius - 2), colorRGB, 2)
                                cv2.circle(self.roundImage, centermax, 7, colorRGB, -1)

                        else:
                            contours.remove(max(contours))
                            cmid = max(contours, key=cv2.contourArea)
                            ((xmid, ymid), radiusmid) = cv2.minEnclosingCircle(cmid)
                            m1 = cv2.moments(cmid)
                            centermid = (int(m1['m10'] / m1['m00']), int(m1['m01'] / m1['m00']))
                            b.center = centermid

                            if 12 > radiusmid > 6:
                                cv2.circle(self.roundImage, (int(xmid), int(ymid)), int(radiusmid - 2),
                                           (colorRGB[0] - 20, colorRGB[1] - 25, colorRGB[2] - 20), 2)

                        self.savePic()
                        print('{} found at {}.'.format(b.name, b.center))

    def stringToColor(self, color):  # takes the list of colors and based on name, returns a rgb color value
        if color == 'cue':
            return 255, 255, 255
        elif color == 'eightball':
            return 0, 0, 0
        elif color == 'blue':
            return 255, 99, 61
        elif color == 'lightred':
            return 117, 117, 225
        elif color == 'darkred':
            return 25, 25, 181
        elif color == 'green':
            return 64, 128, 0
        elif color == 'orange':
            return 7, 135, 255
        elif color == 'yellow':
            return 0, 255, 255
        elif color == 'purple':
            return 155, 0, 77
        else:
            return 127, 0, 225

    def savePic(self):
        imgpath = 'games/game' + self.gameNum + '/outlined'
        imgname = 'pooltable' + str(self.turnNum) + '.png'
        cv2.imwrite(os.path.join(imgpath, imgname), self.roundImage)

    def determineDistanceBetween(self):
        #distance from ball to hole
        #distance from cue to ball

        cueball = (0,0)
        eightball = (0,0)

        minDist = 1000

        for b in self.ballList:
            if b.name == 'cueball':
                b.center  = cueball
            elif b.name == 'eightball':
                b.center = eightball
            elif b.name == 'eightball' and len(self.ballList) > 3:
                #hit eightball
                pass
            else:
                for name, coord in self.holeLocation:
                    distance = self.measureDistance(b.center, coord)
                    if distance < minDist:
                        minDist = distance

    def determineAngleBetween(self):
        pass

    def checkPathofBall(self):
        pass

    def hitBall(self):
        pass

    def checkRoundOver(self):
        pass

    def checkGameOver(self):
        pass

    def moveMouseOut(self):  # moves ball tracer out of the way as much as possible. checks for empty areas
        pockets = ['topleftholeclear.png', 'bottomleftholeclear.png', 'topmidholeclear.png', 'bottommidholeclear.png',
                   'toprightholeclear.png', 'bottomrightholeclear.png']
        rails = ['toprail.png', 'bottom.png', 'leftrail.png', 'rightrail.png']

        for h in pockets:
            pos = Bot.imageSearch(h, self.poolRegion)
            if pos is not None:
                pyautogui.moveTo(pos)
                count = self.quickBallCount()
                if count is True:
                    break
            else:
                for h2 in rails:
                    pos = Bot.imageSearch(h2, self.poolRegion)
                    if pos is not None:
                        pyautogui.moveTo(pos)
                        count = self.quickBallCount()
                        if count is True:
                            break

    def quickBallCount(self):
        for b in self.ballList:
            contours = cv2.findContours(b.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if imutils.is_cv2() else contours[1]
            if len(contours) > 1:
                return False

            return True

    def maxContour(self):
        pass

    def minContour(self):
        pass


class Ball:
    def __init__(self, inputSuit, inputName, inputColor):
        self.center = (0, 0)
        self.suit = inputSuit
        self.color = inputColor
        self.name = inputName
        self.mask = None

        pass


def main():
    print('This bot has only been tested to work on a 1920x1080 screen using Google Chrome.')
    print('Please use make sure the window is the largest it can be for the best results.\n')
    print('Every question asked can be answered with a \'yes\' or \'no\'.')
    start = input('Start 8 ball pool bot? ')
    if any(c in start.lower().replace(' ', '') for c in ('y', 'e', 's')):
        print('Starting..')
        bot1 = Bot()
        bot1.start()
    else:
        print('Exiting..')
        time.sleep(2)
        sys.exit()


if __name__ == "__main__":
    main()
