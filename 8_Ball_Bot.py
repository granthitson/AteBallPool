import os, webbrowser, time, urllib.request, pyautogui, sys, cv2, json, requests, imutils, random
import numpy as np
from win32api import GetSystemMetrics,MessageBox
from PIL import ImageGrab
from math import sqrt

class Bot():
    miniclipurl = 'https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/'
    
    def __init__(self):
        self.height = None
        self.width = None
        self.gameWindow = None

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
            webbrowser.open(miniclipurl)
            time.sleep(5)
            self.start()
        else:
            self.ifLogin()

    def miniclipAPI(self):
        api_url_base = 'https://webmasters.miniclip.com/api/'
        api_url = '{0}/games/2471/en.json'.format(api_url_base)

        try:
            response = requests.get(api_url)
        except requests.exceptions.ConnectionError:
            requests.status_code = 'Connection refused'
            for i in range(1,5):
                time.sleep(1)
                response = requests.get(api_url)
                self.miniclipAPI()
        
        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            h = int(data['2471'].get('height'))
            w = int(data['2471'].get('width'))
            return h,w
            
    def imageSearch(self,image,region=None):
        if region is None:
            pos = pyautogui.locateCenterOnScreen(self.imagePath(image))
            return pos
        else:
            pos = pyautogui.locateCenterOnScreen(self.imagePath(image), region=region)
            return pos#

    def imagePath(self,filename):
        return os.path.join('images',filename)

    def ifLogin(self):
        check = self.loginCheck()
        if check == True:
            self.getGameRegion(check)
            self.navigateMenu(check)
        else:
            self.getGameRegion(check)
            self.navigateMenu(check)

    def getGameRegion(self,truthVal):
        tries = 3
        self.height,self.width = self.miniclipAPI()
        time.sleep(3)
        self.clickX()
        while tries > 0:
            regiontries = 20
            pos = self.imageSearch('alreadystarted.png')
            if pos is None:
                pos = self.imageSearch('alreadystarted1.png')
                if pos is None:
                    time.sleep(1)
                    tries -= 1
                else:
                    print('Game menu found.')
                    break
            else:
                print('Game menu found.')
                break

            if truthVal is False:
                time.sleep(1)
                print('Searching for game region..')
                reg = self.imageSearch('top_right_corner.png')
                print(reg)
                if reg is not None:
                    topRX = reg[0] + reg[2]
                    topRY = reg[1]
                    self.gameWindow = (topRX - width, topRY, width, height)
                    print('Region acquired.' + str(gameWindow))
                    break
                else:
                    while regiontries > 0: 
                        region = self.imageSearch('top_right_corner.png')
                        if region is None:
                            regiontries -= 1
                        elif reg is not None:
                            topRX = reg[0] + reg[2]
                            topRY = reg[1]
                            self.gameWindow = (topRX - width, topRY, width, height)
                            print('Region acquired.' + str(self.gameWindow))
                            return

            elif truthVal is True:
                time.sleep(1)
                print('Searching for game region..')
                reg = self.imageSearch('top_right_corner_logged.png')
                if reg is not None:
                    topRX = reg[0] + reg[2]
                    topRY = reg[1]
                    self.gameWindow = (topRX - width, topRY, width, height)
                    print('Region acquired.' + str(gameWindow))
                    break
                elif reg is None:
                    while regiontries > 0:
                        reg2 = self.imageSearch('top_right_corner_logged.png')
                        if region2 is None:
                            regiontries -=1
                        elif reg2 is not None:
                            topRX = region2[0] + region2[2]
                            topRY = region2[1]
                            self.gameWindow = (topRX - width, topRY, width, height)
                            print('Region acquired.' + str(gameWindow))
                            return 
        if tries > 0:
            tries -= 1
            print(str(tries) + ' official tries left.')
            regiontries = 20

    def navigateMenu(self,truthVal):
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
                        self.startBot()
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

    def decideGame():
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
                    for i in range(0,15):
                        time.sleep(1)
                    print('Waited 15 seconds for a response. Beginning game.')
                    pyautogui.click(pos)
                    time.sleep(8)
                    self.playPoolGame()
                except KeyboardInterrupt:
                    startgame = input(': ').replace(' ','')
                    if startgame.lower() in yeswords:
                        time.sleep(8)
                        self.playPoolGame()
                    elif startgame.lower() in nowords:
                        pos = self.imageSearch('mainmenu_before.png', region=self.gameWindow)
                        pyautogui.click(pos)
                        begingame = input('Start a game?')
                        begingame.replace(' ', '')
                        if begingame.lower() in yeswords:
                            self.decideGame()
                        else:
                            print('Exiting 8 ball bot.')
                            sys.exit()
                    else:
                        pos = self.imageSearch('mainmenu_button.png', region=self.gameWindow)
                        pyautogui.click(pos)
                        begingame2 = input('Start?')
                        begingame2.replace(' ', '')
                        if begingame2.lower() in yeswords:
                            self.decideGame()
                        else:
                            print('Exiting 8 ball bot.')
                            sys.exit()
        else:
            self.playPoolGame()

def playPoolGame():
    turnNum = 0
    leftpocketnum = 10
    game = Game()
    
    with open('gamecounter.txt','r') as g:
        for line in g:
            if line == None:
                g.write(0)
            else:
                gameNum = int(line)
                newGameNum = str(gameNum + 1)
                with open('gamecounter.txt','w') as g:
                    g.write(newGameNum)
                    g.close()
                
    while True:
        pos = Bot.imageSearch('toplefthole.png', region=gameWindow)
        if pos is not None:
            print('Game in session. Checking for turn.')
            reg = Bot.imageSearch('poolrightcorner.png', region=gameWindow)
            if reg is None:
                reg = Bot.imageSearch('toprighthole.png', region=gameWindow)
            topRX = reg[0] + reg[2]
            topRY = reg[1]
            poolRegion = (topRX - 605, topRY, 605, 314)
            print('Table region acquired.' + str(poolRegion))
            break
        else:
            pos = Bot.imageSearch('poolrightcorner.png', region=gameWindow)
            if pos is not None:
                print('Game in session. Checking for turn.')
                reg = Bot.imageSearch('poolrightcorner.png', region=gameWindow)
                if reg is None:
                    reg = Bot.imageSearch('toprighthole.png', region=gameWindow)
                topRX = reg[0] + reg[2]
                topRY = reg[1]
                poolRegion = (topRX - 605, topRY, 605, 314)
                print('Table region acquired.' + str(poolRegion))
                break
            else:
                time.sleep(1)
                leftpocketnum -= 1
            
        if leftpocketnum == 0:
            print('Tried finding top left pocket 10 times. Refreshing page. Please don\'t click anything.')
            refreshPage()
            time.sleep(1)
            decideGame()

    holeLocation = markHoles()        
    print('Game #' + newGameNum)
    cwd = (r'C:\Users\Grant\AppData\Local\Programs\Python\Projects')
    os.makedirs('games\game'+newGameNum+'\\table', exist_ok=True)
    os.makedirs('games\game'+newGameNum+'\\outlined', exist_ok=True)
    while True:
        time.sleep(1)
        turnNum = turnCycle(turnNum)
        print('Turn #' + str(turnNum))
        pyautogui.screenshot(('games\game'+newGameNum+'\\table\pooltable'+str(turnNum)+'.png'),region=poolRegion)
        imgPath = cwd+'/games/game'+newGameNum+'/table/pooltable'+str(turnNum)+'.png' 
        suit, listOfBalls = ballCheck()
        if suit == 'nosuit':
            print('Ball Suit: Either.')
            if turnNum == 1:
                centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imgPath,turnNum,newGameNum)
                if cuepoint[0] < 155 and cuepoint[0] > 150:
                    print('Breaking.')
                    pyautogui.moveTo(x=1104,y=448)
                    pyautogui.mouseDown(button='left')
                    pyautogui.moveRel(-210,-3)
                    pyautogui.mouseUp(button='left')
                    pyautogui.moveTo(x=968,y=455)
                    moveMouseOut(cuepoint)
                    time.sleep(8)
                else:
                    centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imgPath,turnNum,newGameNum)
                    determineDistanceToHole(suit,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                    time.sleep(2)
                    moveMouseOut(cuepoint)
            elif turnNum > 1 and turnNum <= 6:
                centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imgPath,turnNum,newGameNum)
                determineDistanceToHole(suit,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                time.sleep(2)
                moveMouseOut(cuepoint)
            elif turnNum > 8:
                centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imgPath,turnNum,newGameNum)
                determineDistanceToHole(None,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                time.sleep(2)
                moveMouseOut(cuepoint)
        elif suit == 'solid':
            print('Ball Suit: Solids.')
            centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imgPath,turnNum,newGameNum)
            determineDistanceToHole(suit,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
            time.sleep(2)
            moveMouseOut(c)
        else:
            print('Ball Suit: Stripes.')
            centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imgPath,turnNum,newGameNum)
            determineDistanceToHole(suit,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
            time.sleep(2)
            moveMouseOut(cuepoint)
        checkGameOver()

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
                pyautogui.moveRel(None,250)
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
                    clickX()
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
                pos = self.imageSearch('8ballspin_button.png')

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
            pyautogui.moveRel(100,None)
            pyautogui.click(clicks=3, duration=0.50)
            pyautogui.typewrite(miniclipurl)
            pyautogui.press('enter')
        else:
            pyautogui.moveTo(pos)
            pyautogui.moveRel(100,None)
            pyautogui.click(clicks=3, duration=0.50)
            pyautogui.typewrite(miniclipurl)
            pyautogui.press('enter')

class Game():
    def __init__(self,name):   
        poolRegion = (0,0,0,0)
        gameNum = 0
        newGameNum = 0
        turnNum = 0

    def gameSetup():
        leftpocketnum = 10
        
        with open('gamecounter.txt','r') as g:
            for line in g:
                if line == None:
                    g.write(0)
                else:
                    self.gameNum = int(line)
                    self.newGameNum = str(self.gameNum + 1)
                    with open('gamecounter.txt','w') as g:
                        g.write(self.newGameNum)
                        g.close()
                    
        while True:
            pos = Bot.imageSearch('toplefthole.png', region=Bot.gameWindow)
            if pos is not None:
                print('Game in session. Checking for turn.')
                reg = Bot.imageSearch('poolrightcorner.png', region=Bot.gameWindow)
                if reg is None:
                    reg = Bot.imageSearch('toprighthole.png', region=Bot.gameWindow)
                topRX = reg[0] + reg[2]
                topRY = reg[1]
                self.poolRegion = (topRX - 605, topRY, 605, 314)
                print('Table region acquired.' + str(self.poolRegion))
                break
            else:
                pos = Bot.imageSearch('poolrightcorner.png', region=Bot.gameWindow)
                if pos is not None:
                    print('Game in session. Checking for turn.')
                    reg = Bot.imageSearch('poolrightcorner.png', region=Bot.gameWindow)
                    if reg is None:
                        reg = Bot.imageSearch('toprighthole.png', region=Bot.gameWindow)
                    topRX = reg[0] + reg[2]
                    topRY = reg[1]
                    self.poolRegion = (topRX - 605, topRY, 605, 314)
                    print('Table region acquired.' + str(self.poolRegion))
                    break
                else:
                    time.sleep(1)
                    leftpocketnum -= 1
                
            if leftpocketnum == 0:
                print('Tried finding top left pocket 10 times. Refreshing page. Please don\'t click anything.')
                Bot.refreshPage()
                time.sleep(1)
                Bot.decideGame()

        holeLocation = markHoles()        
        print('Game #' + newGameNum)
        cwd = (r'C:\Users\Grant\AppData\Local\Programs\Python\Projects')
        os.makedirs('games\game'+newGameNum+'\\table', exist_ok=True)
        os.makedirs('games\game'+newGameNum+'\\outlined', exist_ok=True)
        while True:
            time.sleep(1)
            turnNum = turnCycle(turnNum)
            print('Turn #' + str(turnNum))
            pyautogui.screenshot(('games\game'+newGameNum+'\\table\pooltable'+str(turnNum)+'.png'),region=poolRegion)
            imgPath = cwd+'/games/game'+newGameNum+'/table/pooltable'+str(turnNum)+'.png' 
            suit, listOfBalls = ballCheck()
            if suit == 'nosuit':
                print('Ball Suit: Either.')
                if turnNum == 1:
                    centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imgPath,turnNum,newGameNum)
                    if cuepoint[0] < 155 and cuepoint[0] > 150:
                        print('Breaking.')
                        pyautogui.moveTo(x=1104,y=448)
                        pyautogui.mouseDown(button='left')
                        pyautogui.moveRel(-210,-3)
                        pyautogui.mouseUp(button='left')
                        pyautogui.moveTo(x=968,y=455)
                        moveMouseOut(cuepoint)
                        time.sleep(8)
                    else:
                        centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imgPath,turnNum,newGameNum)
                        determineDistanceToHole(suit,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                        time.sleep(2)
                        moveMouseOut(cuepoint)
                elif turnNum > 1 and turnNum <= 6:
                    centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imgPath,turnNum,newGameNum)
                    determineDistanceToHole(suit,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                    time.sleep(2)
                    moveMouseOut(cuepoint)
                elif turnNum > 8:
                    centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imgPath,turnNum,newGameNum)
                    determineDistanceToHole(None,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                    time.sleep(2)
                    moveMouseOut(cuepoint)
            elif suit == 'solid':
                print('Ball Suit: Solids.')
                centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imgPath,turnNum,newGameNum)
                determineDistanceToHole(suit,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                time.sleep(2)
                moveMouseOut(c)
            else:
                print('Ball Suit: Stripes.')
                centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imgPath,turnNum,newGameNum)
                determineDistanceToHole(suit,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                time.sleep(2)
                moveMouseOut(cuepoint)
            checkGameOver()
        
class Ball():
    def __init__(self):
        centerpoints = []
        centerpoints2 = []
        cuepoint = (0,0)
        eightballpoint = (0,0)
        suit = None
        holeLocation = []
        
        pass



    def startBot():
        count = 5
        print('This bot has been created and only works on a 1920x1080 screen using Google Chrome.')
        print('Every question asked can be answered with a \'yes\' or \'no\'.\n')
        start = input('Start 8 ball pool bot? ')
        if any(c in start.lower().replace(' ','') for c in ('y','e','s')):
            while count > 0:
                print('Checking for URL...')
                pos = pyautogui.locateCenterOnScreen(imagePath('url.png'))
                if pos is None:
                    pos = pyautogui.locateCenterOnScreen(imagePath('url2.png'))
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
                webbrowser.open('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
                time.sleep(5)
                check = loginCheck()
            else:
                check = loginCheck()
                if check == True:
                    getGameRegion(check)
                    navigateMenu(check)
                else:
                    getGameRegion(check)
                    navigateMenu(check)
        else:
            print('Exiting..')
            time.sleep(2)
            sys.exit()

    def navigateMenu(truthVal):
        if truthVal is True:
            time.sleep(1)
            spinWin()
            collectCoins()
            decideGame()
        else:
            pos = pyautogui.locateCenterOnScreen(imagePath('play_button.png'), region=gameWindow)
            if pos is None:
                refreshPage()
                navigateMenu(truthVal)
            else:
                print('Logging in.')
                pyautogui.click(pos)
                time.sleep(1)
                while True:
                    time.sleep(1)
                    pos = pyautogui.locateCenterOnScreen(imagePath('login1_button.png'), region=gameWindow)
                    if pos is None:
                        time.sleep(1)
                        pos = pyautogui.locateCenterOnScreen(imagePath('login2_button.png'), region=gameWindow)
                        if pos is None:
                            print('Unable to find login button. Please try again.')
                            startBot()
                        else:
                            pyautogui.click(pos)
                            time.sleep(1)
                            logIn()
                            break
                    else:
                        pyautogui.click(pos)
                        time.sleep(1)
                        logIn()
                        break
                navigateMenu(truthVal)

    def decideGame():
        clickX()
        while True:
            pos = pyautogui.locateOnScreen(imagePath('alreadystarted.png'))
            if pos is None:
                pos = pyautogui.locateOnScreen(imagePath('alreadystarted1.png'))
                if pos is None:
                    time.sleep(1)
                else:
                    break
            else:
                break
            
        pf = playFriends()
        if pf is False:
            time.sleep(1)
            pos = pyautogui.locateCenterOnScreen(imagePath('play_button_logged.png'), region=gameWindow)
            pyautogui.click(pos)
            pos = pyautogui.locateCenterOnScreen(imagePath('poolchoice.png'), region=gameWindow)
            while pos is None:
                pos2 = pyautogui.locateCenterOnScreen(imagePath('cheap_button.png'), region=gameWindow)
                pyautogui.click(pos2)
                time.sleep(1)
                pos = pyautogui.locateCenterOnScreen(imagePath('poolchoice.png'), region=gameWindow)
                
            pos = pyautogui.locateCenterOnScreen(imagePath('startgame_button.png'), region=gameWindow)
            if pos is not None:
                print('Begin game? Press Control+C to begin typing. ')
                try:
                    for i in range(0,15):
                        time.sleep(1)
                    print('Waited 15 seconds for a response. Beginning game.')
                    pyautogui.click(pos)
                    time.sleep(8)
                    playPoolGame()
                except KeyboardInterrupt:
                    startgame = input(': ').replace(' ','')
                    if startgame.lower() in yeswords:
                        time.sleep(8)
                        playPoolGame()
                    elif startgame.lower() in nowords:
                        pos = pyautogui.locateCenterOnScreen(imagePath('mainmenu_before.png'), region=gameWindow)
                        pyautogui.click(pos)
                        begingame = input('Start a game?')
                        begingame.replace(' ', '')
                        if begingame.lower() in yeswords:
                            decideGame()
                        else:
                            print('Exiting 8 ball bot.')
                            sys.exit()
                    else:
                        pos = pyautogui.locateCenterOnScreen(imagePath('mainmenu_button.png'), region=gameWindow)
                        pyautogui.click(pos)
                        begingame2 = input('Start?')
                        begingame2.replace(' ', '')
                        if begingame2.lower() in yeswords:
                            decideGame()
                        else:
                            print('Exiting 8 ball bot.')
                            sys.exit()
        else:
            playPoolGame()

    def playPoolGame():
        global poolRegion
        turnNum = 0
        leftpocketnum = 10
        
        with open('gamecounter.txt','r') as g:
            for line in g:
                if line == None:
                    g.write(0)
                else:
                    gameNum = int(line)
                    newGameNum = str(gameNum + 1)
                    with open('gamecounter.txt','w') as g:
                        g.write(newGameNum)
                        g.close()
                    
        while True:
            pos = pyautogui.locateOnScreen(imagePath('toplefthole.png'), region=gameWindow)
            if pos is not None:
                print('Game in session. Checking for turn.')
                reg = pyautogui.locateOnScreen(imagePath('poolrightcorner.png'), region=gameWindow)
                if reg is None:
                    reg = pyautogui.locateOnScreen(imagePath('toprighthole.png'), region=gameWindow)
                topRX = reg[0] + reg[2]
                topRY = reg[1]
                poolRegion = (topRX - 605, topRY, 605, 314)
                print('Table region acquired.' + str(poolRegion))
                break
            else:
                pos = pyautogui.locateOnScreen(imagePath('poolrightcorner.png'), region=gameWindow)
                if pos is not None:
                    print('Game in session. Checking for turn.')
                    reg = pyautogui.locateOnScreen(imagePath('poolrightcorner.png'), region=gameWindow)
                    if reg is None:
                        reg = pyautogui.locateOnScreen(imagePath('toprighthole.png'), region=gameWindow)
                    topRX = reg[0] + reg[2]
                    topRY = reg[1]
                    poolRegion = (topRX - 605, topRY, 605, 314)
                    print('Table region acquired.' + str(poolRegion))
                    break
                else:
                    time.sleep(1)
                    leftpocketnum -= 1
                
            if leftpocketnum == 0:
                print('Tried finding top left pocket 10 times. Refreshing page. Please don\'t click anything.')
                refreshPage()
                time.sleep(1)
                decideGame()

        holeLocation = markHoles()        
        print('Game #' + newGameNum)
        cwd = (r'C:\Users\Grant\AppData\Local\Programs\Python\Projects')
        os.makedirs('games\game'+newGameNum+'\\table', exist_ok=True)
        os.makedirs('games\game'+newGameNum+'\\outlined', exist_ok=True)
        while True:
            time.sleep(1)
            turnNum = turnCycle(turnNum)
            print('Turn #' + str(turnNum))
            pyautogui.screenshot(('games\game'+newGameNum+'\\table\pooltable'+str(turnNum)+'.png'),region=poolRegion)
            imgPath = cwd+'/games/game'+newGameNum+'/table/pooltable'+str(turnNum)+'.png' 
            suit, listOfBalls = ballCheck()
            if suit == 'nosuit':
                print('Ball Suit: Either.')
                if turnNum == 1:
                    centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imagePath,turnNum,newGameNum)
                    if cuepoint[0] < 155 and cuepoint[0] > 150:
                        print('Breaking.')
                        pyautogui.moveTo(x=1104,y=448)
                        pyautogui.mouseDown(button='left')
                        pyautogui.moveRel(-210,-3)
                        pyautogui.mouseUp(button='left')
                        pyautogui.moveTo(x=968,y=455)
                        moveMouseOut(cuepoint)
                        time.sleep(8)
                    else:
                        centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imagePath,turnNum,newGameNum)
                        determineDistanceToHole(suit,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                        time.sleep(2)
                        moveMouseOut(cuepoint)
                elif turnNum > 1 and turnNum <= 6:
                    centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imagePath,turnNum,newGameNum)
                    determineDistanceToHole(suit,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                    time.sleep(2)
                    moveMouseOut(cuepoint)
                elif turnNum > 8:
                    centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imagePath,turnNum,newGameNum)
                    determineDistanceToHole(None,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                    time.sleep(2)
                    moveMouseOut(cuepoint)
            elif suit == 'solid':
                print('Ball Suit: Solids.')
                centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imagePath,turnNum,newGameNum)
                determineDistanceToHole(suit,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                time.sleep(2)
                moveMouseOut(c)
            else:
                print('Ball Suit: Stripes.')
                centerpoints, centerpoints2, cuepoint, eightballpoint = prepareBalls(suit,listOfBalls,imagePath,turnNum,newGameNum)
                determineDistanceToHole(suit,centerpoints,centerpoints2,cuepoint,eightballpoint,holeLocation)
                time.sleep(2)
                moveMouseOut(cuepoint)
            checkGameOver()

    def prepareBalls(suit,listOfBalls,imagePath,turnNum,GameNum):
        ballMask, maskImage = maskSetup(imagePath,listOfBalls)
        maskDict = maskDict(listOfBalls,ballMask)
        centerpoints, cuepoint, eightball, suit, othercenterpoints = outlineBall(maskImage,suit,maskDict,turnNum,gameNum)
        return centerpoints, othercenterpoints, cuepoint, eightball

    def outlineBall(image,suit,maskDict,turnNum,gameNum): #draws contours, but more importantly, gets the center points of each ball
        solids = []
        stripes = []
        cue = (0,0)
        eightball = (0,0)
        for k,v in maskDict.items():
            color = stringToColor(k)
            contours = cv2.findContours(v.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if imutils.is_cv2() else contours[1]
            center = None
            for c in contours:
                if k == 'cue':
                    if len(contours) >= 1:
                        c = max(contours, key=cv2.contourArea)
                        ((x,y), radius) = cv2.minEnclosingCircle(c)
                        M = cv2.moments(c)
                        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                        cue = center
                        print('cue {}'.format(cue))

                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(x), int(y)), int(radius-2),color, 2)
                            cv2.circle(image, center, 7, color, -1)
                        
                elif k == 'eightball':
                    if len(contours) >= 1:
                        c = max(contours, key=cv2.contourArea)
                        ((x,y), radius) = cv2.minEnclosingCircle(c)
                        M = cv2.moments(c)
                        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                        eightball = center
                        print('eightball {}'.format(eightball))

                        if radius > 5 and radius < 12:
                            cv2.circle(image, (int(x), int(y)), int(radius-2),color, 2)
                            cv2.circle(image, center, 7, color, -1)

                else:
                    if len(contours) == 1: #only one suit on the board
                        if suit == 'solids':
                            cmax = max(contours, key=cv2.contourArea)
                            ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                            M = cv2.moments(cmax)
                            centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                            solids.append(centermax)
                            print('suit {}, color {}, center {}'.format(suit,k,centermax))

                            if radius > 6 and radius < 12:
                                cv2.circle(image, (int(x), int(y)), int(radius-2),color, 2)
                                cv2.circle(image, centermax, 7, color, -1)
                                    
                            savePic(gameNum,turnNum,image)
                                
                        elif suit == 'stripes':
                            cmax = min(contours, key=cv2.contourArea)
                            ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                            M = cv2.moments(cmax)
                            centermin = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                            stripes.append(centermin)

                            if radius > 6 and radius < 12:
                                cv2.circle(image, (int(x), int(y)), int(radius-2),(color[0]-20,color[1]-25,color[2]-20), 2)

                            savePic(gameNum,turnNum,image)
                                
                        elif suit == 'nosuit':
                            cmax = max(contours, key=cv2.contourArea)
                            ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                            M = cv2.moments(cmax)
                            centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                            solids.append(centermax)

                            if radius > 0 and radius < 12:
                                cv2.circle(image, (int(x), int(y)), int(radius-2),color, 2)
                                cv2.circle(image, centermax, 7, color, -1)

                            cmax2 = min(contours, key=cv2.contourArea)
                            ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmax2)
                            M = cv2.moments(cmax2)
                            centermin = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                            stripes.append(centermin)

                            if radius > 0 and radius < 12:
                                cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),(color[0]-20,color[1]-25,color[2]-20), 2)

                            savePic(gameNum,turnNum,image)
                     
                    elif len(contours) == 2: #both solid and stripes on the board
                        if suit == 'solids':
                            cmax = max(contours, key=cv2.contourArea)
                            ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                            M = cv2.moments(cmax)
                            centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                            solids.append(centermax)

                            if radius > 6 and radius < 12:
                                cv2.circle(image, (int(x), int(y)), int(radius-2),color, 2)
                                cv2.circle(image, centermax, 7, color, -1)

                            cmin = min(contours, key=cv2.contourArea)
                            ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmin)
                            M1 = cv2.moments(cmin)
                            centermin = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))
                            stripes.append(centermin)
                            
                            if radius > 6 and radius < 12:
                                cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),(color[0]-20,color[1]-25,color[2]-20), 2)

                            savePic(gameNum,turnNum,image)
                                
                        elif suit == 'stripes':
                            cmax = max(contours, key=cv2.contourArea)
                            ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                            M = cv2.moments(cmax)
                            centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                            solids.append(centermax)

                            if radius > 6 and radius < 12:
                                cv2.circle(image, (int(x), int(y)), int(radius-2),color, 2)
                                cv2.circle(image, centermax, 7, color, -1)
                                
                            cmin = min(contours, key=cv2.contourArea)
                            ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmin)
                            M1 = cv2.moments(cmin)
                            centermin = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))
                            stripes.append(centermin)
                            
                            if radius > 6 and radius < 12:
                                cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),(color[0]-20,color[1]-25,color[2]-20), 2)

                            savePic(gameNum,turnNum,image)

                        elif suit == 'nosuit':
                            cmax = max(contours, key=cv2.contourArea)
                            ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                            M = cv2.moments(cmax)
                            centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                            solids.append(centermax)

                            if radius > 0 and radius < 12:
                                cv2.circle(image, (int(x), int(y)), int(radius-2),color, 2)
                                cv2.circle(image, centermax, 7, color, -1)

                            cmin = min(contours, key=cv2.contourArea)
                            ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmin)
                            M1 = cv2.moments(cmin)
                            centermin = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))
                            stripes.append(centermin)

                            if radius > 0 and radius < 12:
                                cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),(color[0]-20,color[1]-25,color[2]-20), 2)

                            savePic(gameNum,turnNum,image)
                                
                    elif len(contours) > 2: #both solid and stripes plus the possibility of false positives
                        if suit == 'solids':
                            cmax = max(contours, key=cv2.contourArea)
                            ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                            M = cv2.moments(cmax)
                            centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                            solids.append(centermax)
                            
                            if radius > 6 and radius < 12:
                                cv2.circle(image, (int(x), int(y)), int(radius-2),color, 2)
                                cv2.circle(image, centermax, 7, color, -1)

                            removearray(contours,cmax)
                            cmin = max(contours, key=cv2.contourArea)
                            ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmin)
                            M1 = cv2.moments(cmin)
                            centermin = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))
                            stripes.append(centermin)
                            
                            if radius > 6 and radius < 12:
                                cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),(color[0]-20,color[1]-25,color[2]-20), 2)

                            savePic(gameNum,turnNum,image)
                                
                        elif suit == 'stripes':
                            cmax = max(contours, key=cv2.contourArea)
                            ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                            M = cv2.moments(cmax)
                            centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                            solids.append(centermax)
                            
                            if radius > 6 and radius < 12:
                                cv2.circle(image, (int(x), int(y)), int(radius-2),color, 2)
                                cv2.circle(image, centermax, 7, color, -1)

                            removearray(contours,cmax)
                            cmax2 = max(contours, key=cv2.contourArea)
                            ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmax2)
                            M1 = cv2.moments(cmax2)
                            centermax2 = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))
                            stripes.append(centermax2)
                            
                            if radius > 6 and radius < 12:
                                cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),(color[0]-20,color[1]-25,color[2]-20), 2)

                            savePic(gameNum,turnNum,image)

                        elif suit == 'nosuit':
                            cmax = max(contours, key=cv2.contourArea)
                            ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                            M = cv2.moments(cmax)
                            centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                            solids.append(centermax)

                            if radius > 6 and radius < 12:
                                cv2.circle(image, (int(x), int(y)), int(radius-2),color, 2)
                                cv2.circle(image, centermax, 7, color, -1)

                            removearray(contours,cmax)
                            cmax2 = max(contours, key=cv2.contourArea)
                            ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmax2)
                            M1 = cv2.moments(cmax2)
                            centermax2 = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))
                            stripes.append(centermax2)

                            if radius > 6 and radius < 12:
                                cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),(color[0]-20,color[1]-25,color[2]-20), 2)

                            savePic(gameNum,turnNum,image)
                            
        if suit == 'solids':
            return solids, cue, eightball, suit, stipes
        elif suit == 'stripes':
            return stripes, cue, eightball, suit, solids
        elif suit == 'nosuit':
            if len(solids) < len(stripes):
                suit == 'solids'
                return solids,cue,eightball,suit, stripes
            elif len(stripes) < len(solids):
                suit == 'stripes'
                return stripes,cue,eightball,suit, solids
            else:
                randomnum = random.randint(0,10)
                if randomnum > 5:
                    suit == 'stripes'
                    return stripes,cue,eightball,suit, solids
                else:
                    suit == 'solids'
                    return solids,cue,eightball,suit, stripes

    def maxContour():
        pass

    def minContour():
        pass

    def maskDict(ballColor,ballMask):
        balls = {}
        for i in range(len(ballColor)):
            key = ballColor[i]
            value = ballMask[i]
            balls[key] = value
        return balls

    def savePic(gameNum,turnNum,image):
        imgpath = 'games/game'+gameNum+'/outlined'
        imgname = 'pooltable'+str(turnNum)+'.png'
        cv2.imwrite(os.path.join(imgpath,imgname),image)

    def markHoles():
        holes = {}
        pos = pyautogui.locateCenterOnScreen(imagePath('tlh.png'), region=poolRegion)
        if pos is not None:
            holes['tlh'] = pos
        pos = pyautogui.locateCenterOnScreen(imagePath('tmh.png'), region=poolRegion)
        if pos is not None:
            holes['tmh'] = pos
            pos = pyautogui.locateCenterOnScreen(imagePath('trh.png'), region=poolRegion)
        if pos is not None:
            holes['trh'] = pos
            pos = pyautogui.locateCenterOnScreen(imagePath('blh.png'), region=poolRegion)
        if pos is not None:
            holes['blh'] = pos
            pos = pyautogui.locateCenterOnScreen(imagePath('bmh.png'), region=poolRegion)
        if pos is not None:
            holes['bmh'] = pos
            pos = pyautogui.locateCenterOnScreen(imagePath('brh.png'), region=poolRegion)
        if pos is not None:
            holes['brh'] = pos
        if len(holes) != 6:
            print('Could not find all 6 holes')
            return holes
        else:
            return holes

    def stringToColor(color): #takes the list of colors and based on name, returns a rgb color value
        if color == 'cue':
            return (255,255,255)
        elif color == 'eightball':
            return (0,0,0)
        elif color == 'blue':
            return (255,99,61)
        elif color == 'lightred':
            return (117,117,225)
        elif color == 'darkred':
            return (25,25,181)
        elif color == 'green':
            return (64,128,0)
        elif color == 'orange':
            return (7,135,255)
        elif color == 'yellow':
            return (0,255,255)
        elif color == 'purple':
            return (155,0,77)
        else:
            return (127,0,225)

    def ballCheck():
        solidlist = ['cue','eightball']
        stripelist = ['cue','eightball']
        nosuit = ['cue','eightball','yellow','blue','lightred','purple','orange','green','darkred']
        pyautogui.moveTo(957,305)
        pos = pyautogui.locateOnScreen(imagePath('ballpic1.png'), region=gameWindow)
        if pos is not None:
            topRX = pos[0] + pos[2]
            topRY = pos[1]
            reg = (topRX - 176, topRY, 176, 90)
        else:
            reg = (region[0]+78, region[1]+80, 176, 90)
        while True:
            pos = pyautogui.locateCenterOnScreen(imagePath('1ball.png'), region=gameWindow)
            if pos is not None:
                solidlist.append('yellow')
            pos = pyautogui.locateCenterOnScreen(imagePath('2ball.png'), region=gameWindow)   
            if pos is not None:
                solidlist.append('blue')
            pos = pyautogui.locateCenterOnScreen(imagePath('3ball.png'), region=gameWindow)
            if pos is not None:
                solidlist.append('lightred')
            pos = pyautogui.locateCenterOnScreen(imagePath('4ball.png'), region=gameWindow)
            if pos is not None:
                solidlist.append('purple')
            pos = pyautogui.locateCenterOnScreen(imagePath('5ball.png'), region=gameWindow)
            if pos is not None:
                solidlist.append('orange')
            pos = pyautogui.locateCenterOnScreen(imagePath('6ball.png'), region=gameWindow)
            if pos is not None:
                solidlist.append('green')
            pos = pyautogui.locateCenterOnScreen(imagePath('7ball.png'), region=gameWindow)
            if pos is not None:
                solidlist.append('darkred')
                break
            else:
                break
        while True:
            pos = pyautogui.locateCenterOnScreen(imagePath('9ball.png'), region=gameWindow)
            if pos is not None:
                stripelist.append('yellow')
            pos = pyautogui.locateCenterOnScreen(imagePath('10ball.png'), region=gameWindow)
            if pos is not None:
                stripelist.append('blue')
            pos = pyautogui.locateCenterOnScreen(imagePath('11ball.png'), region=gameWindow)
            if pos is not None:
                stripelist.append('lightred')
            pos = pyautogui.locateCenterOnScreen(imagePath('12ball.png'), region=gameWindow)
            if pos is not None:
                stripelist.append('purple')
            pos = pyautogui.locateCenterOnScreen(imagePath('13ball.png'), region=gameWindow)
            if pos is not None:
                stripelist.append('orange')
            pos = pyautogui.locateCenterOnScreen(imagePath('14ball.png'), region=gameWindow)
            if pos is not None:
                stripelist.append('green')
            pos = pyautogui.locateCenterOnScreen(imagePath('15ball.png'), region=gameWindow)
            if pos is not None:
                stripelist.append('darkred')
                break
            else:
                break
        if len(stripelist) >= 3:
            return 'stripes', stripelist
        elif len(solidlist) >= 3:
            return 'solid', solidlist
        else:
            return 'nosuit', nosuit

    def maskSetup(img,listOfBalls): #sets up masks for each ball based on which are in need to be hit
        balls = []
        img = cv2.imread(img,1)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        for c in listofb:
            if c == 'cue':
                upper_whitecue = np.array([180,50,255])
                lower_whitecue = np.array([0,10,80])
                maskwhiteball = cv2. inRange(hsv, lower_whitecue, upper_whitecue)
                balls.append(maskwhiteball)
            elif c == 'eightball':
                upper_black = np.array([50,225,50])
                lower_black = np.array([10,0,0])
                maskblackball = cv2. inRange(hsv, lower_black, upper_black)
                balls.append(maskblackball)
            elif c == 'yellow':
                upper_yellow = np.array([25,255,255])
                lower_yellow = np.array([23,150,100])
                maskyellowball = cv2.inRange(hsv, lower_yellow, upper_yellow)
                maskyellowball = cv2.dilate(maskyellowball,None,iterations=1)
                balls.append(maskyellowball)
            elif c == 'blue':
                upper_blue = np.array([135,255,255])
                lower_blue = np.array([112,70,100])
                maskblueball = cv2.inRange(hsv, lower_blue, upper_blue)
                balls.append(maskblueball)
            elif c == 'lightred':
                upper_lightred = np.array([4,255,250])
                lower_lightred = np.array([0,105,150])
                masklightredball = cv2.inRange(hsv,lower_lightred, upper_lightred)
                balls.append(masklightredball)
            elif c == 'purple':
                upper_purple = np.array([160,255,255])
                lower_purple = np.array([135,50,70])
                maskpurpleball = cv2.inRange(hsv, lower_purple, upper_purple)
                balls.append(maskpurpleball)
            elif c == 'orange':
                upper_orange = np.array([19,255,255])
                lower_orange = np.array([11,150,170])
                maskorangeball = cv2.inRange(hsv,lower_orange, upper_orange)
                balls.append(maskorangeball)
            elif c == 'green':
                upper_green = np.array([60,255,255])
                lower_green = np.array([53,70,50])
                maskgreenball = cv2.inRange(hsv, lower_green, upper_green)
                balls.append(maskgreenball)
            elif c == 'darkred':
                upper_darkred = np.array([4,255,180])
                lower_darkred = np.array([3,50,50])
                maskdarkredball = cv2.inRange(hsv,lower_darkred, upper_darkred)
                balls.append(maskdarkredball)
    ##        try:
    ##            cv2.imshow('mask',maskwhiteball)
    ##            cv2.imshow('mask1',maskblackball)
    ##            cv2.imshow('mask2',maskblueball)
    ##            cv2.imshow('mask3',masklightredball)
    ##            cv2.imshow('mask4',maskdarkredball)
    ##            cv2.imshow('mask5',maskgreenball)
    ##            cv2.imshow('mask6',maskorangeball)
    ##            cv2.imshow('mask7',maskyellowball)
    ##            cv2.imshow('mask8',maskpurpleball)
    ##
    ##            cv2.imshow('circle',img)
    ##            
    ##
    ##            while(1):
    ##                k = cv2.waitKey(0)
    ##                if (k == 27):
    ##                    break
    ##        except UnboundLocalError:
    ##            pass
    ##
    ##        cv2.destroyAllWindows()
        return balls,img

    def turnCycle(turnnumber):
        while True:
            turn1 = checkTurn()
            if turn1 is True:
                turnnumber += 1
                print('Bot\'s turn.')
                return turnnumber
            else:
                time.sleep(1)

    def checkTurn():
        while True:
            pos = pyautogui.locateCenterOnScreen(imagePath('turn.png'))
            if pos is not None:
                return True
            else:
                pos = pyautogui.locateCenterOnScreen(imagePath('turn1.png'))
                if pos is not None:
                    return True
                else:
                    return False
                
                
    def loginCheck():
        time.sleep(1)
        pos = pyautogui.locateCenterOnScreen(imagePath('url.png'))
        pos2 = pyautogui.locateCenterOnScreen(imagePath('url2.png'))
        if pos is None and pos2 is None:
            print('Opening new tab because old one is now longer visible.')
            webbrowser.open('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
            time.sleep(2)
            check1 = loginCheck()
            if check1 is True:
                return True
            else:
                return False
                
        else:
            time.sleep(2)
            pos = pyautogui.locateCenterOnScreen(imagePath('enableflash_0.png'))
            if pos is None:
                pos = pyautogui.locateCenterOnScreen(imagePath('enableflash_1.png'))
                if pos is None:
                    pos = pyautogui.locateCenterOnScreen(imagePath('enableflash_2.png'))
                    if pos is None:
                        pos = pyautogui.locateCenterOnScreen(imagePath('allow.png'))
                        if pos is None:
                            pos = pyautogui.locateCenterOnScreen(imagePath('url.png'))
                            pos2 = pyautogui.locateCenterOnScreen(imagePath('url2.png'))
                            if pos is None and pos2 is None:
                                print('Please stay on the opened web page.')
                                webbrowser.open('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
                                time.sleep(2)
                                check1 = loginCheck()
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
                    pos = pyautogui.locateCenterOnScreen(imagePath('enableflash_2.png'))
                    if pos is None:
                        refreshPage()
                        time.sleep(2)
                        check1 = loginCheck()
                        if check1 is True:
                            return True
                        else:
                            return False
                    else:
                        pyautogui.click(pos)
                        time.sleep(1)
                        pos = pyautogui.locateCenterOnScreen(imagePath('allow.png'))
                        if pos is None:
                            pass
                        else:
                            pyautogui.click(pos)
                            time.sleep(1)
            else:
                pyautogui.click(pos)
                time.sleep(1)
                pos = pyautogui.locateCenterOnScreen(imagePath('enableflash_2.png'))
                if pos is None:
                    print('Please stay on the opened web page.')
                    webbrowser.open('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
                    time.sleep(2)
                    check1 = loginCheck()
                    if check1 is True:
                        return True
                    else:
                        return False
                else:
                    pyautogui.click(pos)
                    time.sleep(1)
                    pos = pyautogui.locateCenterOnScreen(imagePath('allow.png'))
                    if pos is None:
                        pass
                    else:
                        pyautogui.click(pos)
                        time.sleep(1)

        pos = pyautogui.locateCenterOnScreen(imagePath('signup_login_button.png'))
        if pos is None:
            pos = pyautogui.locateCenterOnScreen(imagePath('defaultaccount.png'))
            if pos is None:
                pos = pyautogui.locateCenterOnScreen(imagePath('url.png'))
                if pos is None:
                    print('Opening new tab because old one is now longer visible.')
                    webbrowser.open('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
                    time.sleep(2)
                    check1 = loginCheck()
                    if check1 is True:
                        return True
                    else:
                        return False
                else:
                    account = input('Are you logged into your own account?')
                    if any(c in account.lower().replace(' ','') for c in ('y','e','s')):
                        default = input('Would you like to save it as the default?')
                        if any(c in default.lower().replace(' ','') for c in ('y','e','s')):
                            reg = pyautogui.locateOnScreen(imagePath('facebooklogo.png'))
                            pyautogui.screenshot(('images\defaultaccount.png'),region=((reg[0]+reg[2])-170,reg[1],170,40))
                            newemail = input('Please enter the email associated with the account.')
                            newpass = input('Please enter the password associated with the account.')
                            confirm = input('User is {} and the password is {}?'.format(newemail,newpass))
                            if any(c in default.lower().replace(' ','') for c in ('y','e','s')):
                                with open('default.txt','w') as f:
                                    for line in f:
                                        if line == None:
                                            f.write('{} {}'.format(newemail,newpass))
                                            print('New default account set.')
                                            f.close()
                                            return True
                                        else:
                                            with open('default.txt','w') as g:
                                                g.write('{} {}'.format(newemail,newpass))
                                                print('New default account set.')
                                                g.close()
                                                return True
                            else:
                                newemail = input('Please enter the email associated with the account.')
                                newpass = input('Please enter the password associated with the account.')
                                confirm = input('User is {} and the password is {}?'.format(newemail,newpass))
                                if any(c in default.lower().replace(' ','') for c in ('y','e','s')):
                                    with open('default.txt','r') as f:
                                        for line in f:
                                            if line == None:
                                                f.write('{} {}'.format(newemail,newpass))
                                                print('New default account set.')
                                                f.close()
                                                return True
                                            else:
                                                with open('default.txt','w') as g:
                                                    g.write('{} {}'.format(newemail,newpass))
                                                    print('New default account set.')
                                                    g.close()
                                                    return True
                                else:
                                    print('Restarting login check.')
                                    check1 = loginCheck()
                                    if check1 is True:
                                        return True
                                    else:
                                        return False
                        else:
                            print('Proceeding without offical check.')
                            return True
                    else:       
                        time.sleep(1)
                        refreshPage()
                        time.sleep(1)
                        check1 = loginCheck()
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

    def getGameRegion(truthVal):
        global gameWindow
        height,width = miniclipAPI()
        tries = 3
        time.sleep(3)
        clickX()
        while tries > 0:
            regiontries = 20
            while True:
                pos = pyautogui.locateOnScreen(imagePath('alreadystarted.png'))
                if pos is None:
                    pos = pyautogui.locateOnScreen(imagePath('alreadystarted1.png'))
                    if pos is None:
                        time.sleep(1)
                    else:
                        print('Game menu found.')
                        break
                else:
                    print('Game menu found.')
                    break

            if truthVal is False:
                time.sleep(1)
                print('Searching for game region..')
                reg = pyautogui.locateOnScreen(imagePath('top_right_corner.png'))
                if reg is not None:
                    topRX = reg[0] + reg[2]
                    topRY = reg[1]
                    gameWindow = (topRX - width, topRY, width, height)
                    print('Region acquired.' + str(gameWindow))
                    break
                elif region is None:
                    while regiontries > 0: 
                        region = pyautogui.locateOnScreen(imagePath('top_right_corner.png'))
                        if region is None:
                            regiontries -= 1
                        elif reg is not None:
                            topRX = reg[0] + reg[2]
                            topRY = reg[1]
                            gameWindow = (topRX - width, topRY, width, height)
                            print('Region acquired.' + str(gameWindow))
                            return

            elif truthVal is True:
                time.sleep(1)
                print('Searching for game region..')
                reg = pyautogui.locateOnScreen(imagePath('top_right_corner_logged.png'))
                if reg is not None:
                    topRX = reg[0] + reg[2]
                    topRY = reg[1]
                    gameWindow = (topRX - width, topRY, width, height)
                    print('Region acquired.' + str(gameWindow))
                    break
                elif region2 is None:
                    while region2tries > 0:
                        region2 = pyautogui.locateOnScreen(imagePath('top_right_corner_logged.png'))
                        if region2 is None:
                            region2tries -=1
                        elif region2 is not None:
                            topRX = region2[0] + region2[2]
                            topRY = region2[1]
                            gameWindow = (topRX - width, topRY, width, height)
                            print('Region acquired.' + str(gameWindow))
                            return 
            if tries > 0:
                tries -= 1
                print(str(tries) + ' official tries left.')
                regiontries = 15

    def playFriends():
        friendchoice = ['friends', 'friend', 'friennd', 'friennds']
        randomchoice = ['randoms', 'random']
        noresponse = 10
        findhole = 10
        print('Play with \'friends\' or \'randoms\'? Press Control+C to begin typing. ')
        try:
            for i in range(0,20):
                time.sleep(1)
            print('Waited 20 seconds for a response. Beginning random game.')
            return False
        except KeyboardInterrupt:
            playchoice = input(': ').replace(' ','')
            if playchoice.lower() in friendchoice:
                pos = pyautogui.locateCenterOnScreen(imagePath('playfriends.png'), region=gameWindow)
                pyautogui.click(pos)
                time.sleep(1)
                pos = pyautogui.locateCenterOnScreen(imagePath('search_friends.png'), region=gameWindow)
                if pos is not None:
                    username = input('Please enter the username of your opponent: ')
                    time.sleep(1)
                    pyautogui.click(pos)
                    time.sleep(1)
                    pyautogui.typewrite(username)
                    pyautogui.press('enter')
                    time.sleep(1)
                pos = pyautogui.locateCenterOnScreen(imagePath('add_friend.png'), region=gameWindow)
                if pos is not None:
                    pyautogui.click(pos)
                    time.sleep(1)
                    pos = pyautogui.locateCenterOnScreen(imagePath('challenge_friend.png'), region=gameWindow)
                    pyautogui.click(pos)
                    return True
                else:
                    pos = pyautogui.locateCenterOnScreen(imagePath('challenge_friend.png'), region=gameWindow)
                    if pos is not None:
                        pyautogui.click(pos)
                        print('Waiting for response.')
                        while noresponse > 0:
                            time.sleep(1)
                            pos = pyautogui.locateCenterOnScreen(imagePath('no_response.png'), region=gameWindow)
                            if pos is None:
                                noresponse -= 1
                            else:
                                time.sleep(2)
                                decideGame()
                        print('Checking to see if game has started.')
                        if noresponse == 0:
                            while findhole > 0:
                                time.sleep(1)
                                pos = pyautogui.locateCenterOnScreen(imagePath('toplefthole.png'), region=gameWindow)
                                if pos is not None:
                                    print('Game Started.')
                                    return True
                                else:
                                    findhole -= 1
                        if findhole == 0:
                            time.sleep(2)
                            pos = pyautogui.locateCenterOnScreen(imagePath('search_friendsmagni.png'), region=gameWindow)
                            if pos is not None:
                                decideGame()
                            else:
                                refreshPage()
                                time.sleep(1)
                                decideGame()
                    else:
                        print('Can\'t find friend.')
                        decideGame()
            elif playchoice in randomchoice:
                return False

    def logIn():
        print('Do you have an account you\'d like the bot to play on? Press Ctrl+C to begin typing.')
        try:
            for i in range(0,10):
                time.sleep(1)
            print('Waited 10 seconds for a response. Using default.')
            with open('default.txt','r') as f:
                    for line in f:
                        email,password = line.split(' ')
            pos = pyautogui.locateCenterOnScreen(imagePath('email_area.png'), region=gameWindow)
            pyautogui.click(pos,)
            time.sleep(1)
            pos = pyautogui.typewrite(email)
            time.sleep(1)
            pos = pyautogui.locateCenterOnScreen(imagePath('password_area.png'), region=gameWindow)
            pyautogui.click(pos)
            time.sleep(1)
            pos = pyautogui.typewrite(password)
            time.sleep(1)
            pos = pyautogui.locateCenterOnScreen(imagePath('login3_button.png'), region=gameWindow)
            pyautogui.click(pos)

        except KeyboardInterrupt:
            account = input(': ').replace(' ','')
            if any(c in account.lower() for c in ('y','e','s')):
                email = input('Please enter the email. ').replace(' ','')
                password = input('Please enter the email. ').replace(' ','')
                logIn(email,password)
            else:
                print('Using default email.')
                with open('default.txt','r') as f:
                    for line in f:
                        email,password = line.split(' ')
                pos = pyautogui.locateCenterOnScreen(imagePath('email_area.png'), region=gameWindow)
                pyautogui.click(pos)
                time.sleep(1)
                pos = pyautogui.typewrite(email)
                time.sleep(1)
                pos = pyautogui.locateCenterOnScreen(imagePath('password_area.png'), region=gameWindow)
                pyautogui.click(pos)
                time.sleep(1)
                pos = pyautogui.typewrite(password)
                time.sleep(1)
                pos = pyautogui.locateCenterOnScreen(imagePath('login3_button.png'), region=gameWindow)
                pyautogui.click(pos)

    def spinWin():
        tries_2 = 15
        time.sleep(1)
        while True:
            pos = pyautogui.locateOnScreen(imagePath('alreadystarted.png'))
            if pos is None:
                pos = pyautogui.locateOnScreen(imagePath('alreadystarted1.png'))
                if pos is None:
                    clickX()
                    time.sleep(1)
                else:
                    break
            else:
                break

        while tries_2 > 0:
            pos = pyautogui.locateCenterOnScreen(imagePath('spinwinicon.png'))
            if pos is None:
                tries_2 -= 1
            else:
                pyautogui.click(pos)
                time.sleep(1)
                pos = pyautogui.locateCenterOnScreen(imagePath('8ballspin_button.png'))
                pyautogui.moveTo(pos)
                pyautogui.mouseDown(button='left')
                pyautogui.moveRel(None,250)
                pyautogui.mouseUp(button='left')
                time.sleep(7)
                pos = pyautogui.locateCenterOnScreen(imagePath('8ballwinx.png'))
                pyautogui.click(pos)
                time.sleep(2)
                pos = pyautogui.locateCenterOnScreen(imagePath('xout.png'))
                pyautogui.click(pos)

    def collectCoins():
        tries_3 = 15
        time.sleep(1)
        while True:
            pos = pyautogui.locateOnScreen(imagePath('alreadystarted.png'))
            if pos is None:
                pos = pyautogui.locateOnScreen(imagePath('alreadystarted1.png'))
                if pos is None:
                    clickX()
                    time.sleep(1)
                else:
                    break
            else:
                break

        while tries_3 > 0:
            pos = pyautogui.locateCenterOnScreen(imagePath('collectcoins.png'))
            if pos is None:
                tries_3 -= 1
            else:
                pyautogui.click(pos)
                time.sleep(1)
                pos = pyautogui.locateCenterOnScreen(imagePath('8ballspin_button.png'))

    def clickX():
        xtries = 5
        print('Searching for \'X\'s...')
        while xtries > 0:
            pos = pyautogui.locateCenterOnScreen(imagePath('xout.png'))
            if pos is None:
                xtries -= 1
            else:
                pyautogui.click(pos)
                pos = pyautogui.locateOnScreen(imagePath('alreadystarted.png'))
                if pos is None:
                    continue
                else:
                    break

    def refreshPage():
        pos = pyautogui.locateCenterOnScreen(imagePath('urlbar.png'))
        if pos is None:
            pos = pyautogui.locateCenterOnScreen(imagePath('unsecure.png'))
            pyautogui.moveTo(pos)
            pyautogui.moveRel(100,None)
            pyautogui.click(clicks=3, duration=0.50)
            pyautogui.typewrite('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
            pyautogui.press('enter')
        else:
            pyautogui.moveTo(pos)
            pyautogui.moveRel(100,None)
            pyautogui.click(clicks=3, duration=0.50)
            pyautogui.typewrite('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
            pyautogui.press('enter')

    def imagePath(filename):
        return os.path.join('images',filename)

    def miniclipAPI():
        api_url_base = 'https://webmasters.miniclip.com/api/'
        api_url = '{0}/games/2471/en.json'.format(api_url_base)

        try:
            response = requests.get(api_url)
        except requests.exceptions.ConnectionError:
            requests.status_code = 'Connection refused'
            for i in range(1,5):
                time.sleep(1)
                response = requests.get(api_url)
                miniclipAPI()
        
        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            h = int(data['2471'].get('height'))
            w = int(data['2471'].get('width'))
            return h,w

def main():
    print('This bot has only been tested to work on a 1920x1080 screen using Google Chrome.')
    print('Please use make sure the window is the largest it can be for the best results.\n')
    print('Every question asked can be answered with a \'yes\' or \'no\'.')
    start = input('Start 8 ball pool bot? ')
    if any(c in start.lower().replace(' ','') for c in ('y','e','s')):
        print('Starting..')
        bot1 = Bot()
        bot1.start()
    else:
        print('Exiting..')
        time.sleep(2)
        sys.exit()
    startBot()
    
if __name__ == "__main__":
    main()
