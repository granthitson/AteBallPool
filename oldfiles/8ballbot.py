import os, webbrowser, time, urllib.request, pyautogui, sys, cv2, json, requests, imutils, random
import numpy as np
from win32api import GetSystemMetrics,MessageBox
from PIL import ImageGrab
from math import sqrt

def open8ballbot():#initiates start up procedure. asks if you want to start bot
    loginattempts = 3
    kenobi = ['Hello There', 'Hello there', 'hello There', 'hello there']
    start = input("Would you like to start 8-Ball-Bot? ")
    start.replace(' ', '')
    if start.lower() in yeswords:
        print('Enter input mode? Press Control+C to begin typing. ')
        try:
            for i in range(0,15):
                time.sleep(1)
            print('Waited 15 seconds for a response. No input mode.')
            noInput()
        except KeyboardInterrupt:
            startgame = input(': ')
            startgame.replace(' ', '')
            if startgame.lower() in yeswords:
                print('Entering input mode.')
###input mode
                tab = input('Is 8-ball already in a tab? ')
                tab.replace(' ', '')
                if tab.lower() in nowords:
                    print('Opening Tab. Please keep the tab in view.')
                    webbrowser.open(url)
                    time.sleep(3)
                    check = loginCheck()
                    if check == 'loggedintobot':
                        #time.sleep(20)
                        getGameRegion(True)
                        navigateStartMenu(True)
                    elif check == 'notlogged':
                        #time.sleep(20)
                        getGameRegion(False)
                        navigateStartMenu(False)
                    else:
                        print('Login Check failed. Try again later.')
                elif tab.lower() in yeswords:
                    print('Please log out of any non sanctioned accounts.')
                    canlog2 = input('Have you logged out? ')
                    canlog2.replace(' ', '')
                    if canlog2.lower() in yeswords:
                        testlog = loginCheck()
                        if testlog == 'loggedintobot':
                            getGameRegion(True)
                            navigateStartMenu(True)
                        elif testlog == 'notlogged':
                            getGameRegion(False)
                            navigateStartMenu(False)
                        else:
                            print('Please log out and try again.')
                            sys.exit()
                    elif canlog2.lower() in nowords:
                        botprobe = input('Are you logged into 8ballrobotguy? ')
                        botprobe.replace(' ', '')
                        if botprobe.lower() in yeswords:
                            testlog2 = loginCheck()
                            if testlog2 == 'loggedintobot':
                                getGameRegion(True)
                                navigateStartMenu(True)
                        elif botprobe.lower() in nowords:
                            print('Please log out and try again.')
                            sys.exit()
                        else:
                            print('Invalid. Exiting.')
                            sys.exit()
                        quit8 = input('Nice try. Would you like to quit? ')
                        quit8.replace(' ', '')
                        if quit8.lower() in yeswords:
                            print('Turning off 8 ball bot.')
                            sys.exit()
                        elif quit8.lower() in nowords:
                            print('Restarting.')
                            time.sleep(5)
                            open8ballbot()
                        else:
                            print('Take that as a \'yes\'.')
                    else:
                        print('Take that as a \'no\'.')
### input mode end                 
            elif startgame.lower() in nowords:
               print('Entering no input mode.')
               noInput()
            elif startgame.lower() in coinmode:
                print('Entering CoinCycle Mode.')
                collectCoinsCycle()
            else:
                print('Not a valid response. Exiting bot.')
                sys.exit()
               
    elif start.lower() in nowords:
        print('Powering down 8-Ball Bot')
        sys.exit()
    elif start.lower() in kenobi:
        print('General Kenobi!')
        genkenobi = 'https://www.youtube.com/watch?v=fPSRT0zNjds'
        webbrowser.open(genkenobi)
        time.sleep(10)
        check3 = loginCheck()
        if check3 == 'loggedintobot':
            #time.sleep(20)
            getGameRegion(True)
            navigateStartMenu(True)
        elif check3 == 'notlogged':
            #time.sleep(20)
            getGameRegion(False)
            navigateStartMenu(False)
        else:
            print('Login Check failed. Try again later.')
            sys.exit()
    else:
        print('Not a valid answer.')
        open8ballbot()

def noInput(): #no input mode, starts to play pool without any user input. automatic
    check4 = loginCheck()
    if check4 == 'loggedintobot':
        getGameRegion(True)
        navigateStartMenu(True)
    elif check4 == 'notlogged':
        getGameRegion(False)
        navigateStartMenu(False)
    else:
        print('Login check failed. Try again later.')
        sys.exit()
        
def navigateStartMenu(choice): # navigates the start menu if not logged in
    if choice is True:
        print('Navigated.')
        time.sleep(1)
        navigateGameMenu()
        
    elif choice is False:
        print('Searching for play button.')
        while True:
            pos = pyautogui.locateCenterOnScreen(imagePath('play_button.png'), region=GAME_REGION)
            if pos is not None:
                break
        print('Found button.')
        pyautogui.click(pos,duration=0.25)
        time.sleep(1)

    #vision to see if need to login or not
    while True:
        time.sleep(2)
        pos = pyautogui.locateCenterOnScreen(imagePath('login1_button.png'), region=GAME_REGION)
        if pos is not None:
            break
        else:
            pos = pyautogui.locateCenterOnScreen(imagePath('login2_button.png'), region=GAME_REGION)
            time.sleep(1)
            if pos is not None:
                break
            else:
                print('Second button to login not found. Restarting.')
                open8ballpool()
                
    pyautogui.click(pos,duration=0.25)
    time.sleep(1)

    print('Do you have an account you\'d like the bot to play on? Press Ctrl+C to begin typing.')
    try:
        for i in range(0,10):
            time.sleep(1)
        print('Waited 10 seconds for a response. Using default')
        logIn()
        navigateGameMenu()
    except KeyboardInterrupt:
        account = input(': ')
        account.replace(' ', '')
        if account.lower() in yeswords:
            email = input('Please enter the email. ')
            email.replace(' ', '')
            password = input('Please enter the email. ')
            password.replace(' ', '')
            logIn(email,password)
        elif account.lower() in nowords:
            print('Using default email.')
            logIn()
        else:
            print('Take that as a no.')
            logIn()

def navigateGameMenu(): # navigates the game menu after being logged in
    time.sleep(5)
    tries1 = 3
    while tries1 > 0:
        cointries = 15
        spinwintries = 15
        #allowSearch()
        time.sleep(1)
        pos = pyautogui.locateCenterOnScreen(imagePath('preregionx_button.png'), region=GAME_REGION)
        if pos is not None:
            pyautogui.click(pos,duration=0.25)
        else:
            pass
        pos = pyautogui.locateCenterOnScreen(imagePath('8ballspin_button.png'), region=GAME_REGION)
        if pos is None:
            pos = pyautogui.locateCenterOnScreen(imagePath('spinx_button.png'), region=GAME_REGION)
            if pos is not None:
                pos = pyautogui.locateCenterOnScreen(imagePath('spinx_button.png'), region=GAME_REGION)
                pyautogui.click(pos,duration=0.25)
            elif pos is None:
                pos = pyautogui.locateCenterOnScreen(imagePath('spinwinicon.png'), region=GAME_REGION)
                if pos is None:
                    while spinwintries > 0:
                        if pos is None:
                            spinwintries -= 1
                            if spinwintries == 0:
                                break
                        else:
                            spinWin(pos)
                            pos = pyautogui.locateCenterOnScreen(imagePath('spinwinicon.png'), region=GAME_REGION)
                            if pos is None:
                                break
                            else:
                                spinWin(pos)
                                break
                    
                elif pos is not None:
                    spinWin(pos)
                    pos = pyautogui.locateCenterOnScreen(imagePath('spinwinicon.png'), region=GAME_REGION)
                    if pos is None:
                        continue
                    else:
                        spinWin(pos)
                
        elif pos is not None:
            spinWin(pos)
            pos = pyautogui.locateCenterOnScreen(imagePath('spinwinicon.png'), region=GAME_REGION)
            if pos is None:
                continue
            else:
                spinWin(pos)
            
        pos = pyautogui.locateCenterOnScreen(imagePath('collectcoins.png'), region=GAME_REGION)
        if pos is None:
            while cointries > 0:
                if pos is None:
                    cointries -= 1
                    if cointries == 0:
                        tries1 -= 1
                        break
                elif pos is not None:
                    collectCoins(pos)
                    navigatePool()
                    break
        elif pos is not None:
            collectCoins(pos)
            navigatePool()
            break

    if tries1 == 0:
        print('Tried finding CollectCoins and Spin&Win 3 times and found none. Ignoring.')
        navigatePool()

def navigatePool(): #navigates to a random pool game, cheapest choice
    pf = playFriends()
    if pf is not True:
        time.sleep(1)
        pos = pyautogui.locateCenterOnScreen(imagePath('play_button_logged.png'), region=GAME_REGION)
        pyautogui.click(pos,duration=0.25)
        pos = pyautogui.locateCenterOnScreen(imagePath('poolchoice.png'), region=GAME_REGION)
        while pos is None:
            pos2 = pyautogui.locateCenterOnScreen(imagePath('cheap_button.png'), region=GAME_REGION)
            pyautogui.click(pos2,duration=0.25)
            time.sleep(1)
            pos = pyautogui.locateCenterOnScreen(imagePath('poolchoice.png'), region=GAME_REGION)
            
        pos = pyautogui.locateCenterOnScreen(imagePath('startgame_button.png'), region=GAME_REGION)
        if pos is not None:
            print('Begin game? Press Control+C to begin typing. ')
            try:
                for i in range(0,15):
                    time.sleep(1)
                print('Waited 15 seconds for a response. Beginning game.')
                pyautogui.click(pos,duration=0.25)
                time.sleep(8)
                poolGame()
            except KeyboardInterrupt:
                startgame = input(': ')
                startgame.replace(' ', '')
                if startgame.lower() in yeswords:
                    time.sleep(8)
                    poolGame()
                elif startgame.lower() in nowords:
                    pos = pyautogui.locateCenterOnScreen(imagePath('mainmenu_before.png'), region=GAME_REGION)
                    pyautogui.click(pos,duration=0.25)
                    begingame = input('Start a game?')
                    begingame.replace(' ', '')
                    if begingame.lower() in yeswords:
                        navigatePool()
                    else:
                        print('Exiting 8 ball bot.')
                        sys.exit()
                else:
                    pos = pyautogui.locateCenterOnScreen(imagePath('mainmenu_button.png'), region=GAME_REGION)
                    pyautogui.click(pos,duration=0.25)
                    begingame2 = input('Start?')
                    begingame2.replace(' ', '')
                    if begingame2.lower() in yeswords:
                        navigatePool()
                    else:
                        print('Exiting 8 ball bot.')
                        sys.exit()
        #End of input. May add option to pick and choose shots, but that sounds complex.
    else:
        poolGame()

def playFriends(): #for if the user wants to bot versus a friend
    friendchoice = ['friends', 'friend', 'friennd', 'friennds']
    randomchoice = ['randoms', 'random']
    trynoresponse = 10
    trytopleft = 5
    print('Play with \'friends\' or \'randoms\'? Press Control+C to begin typing. ')
    try:
        for i in range(0,20):
            time.sleep(1)
        print('Waited 20 seconds for a response. Beginning random game.')
        return False
    except KeyboardInterrupt:
        playchoice = input(': ')
        playchoice.replace(' ', '')
        if playchoice.lower() in friendchoice:
            pos = pyautogui.locateCenterOnScreen(imagePath('playfriends.png'), region=GAME_REGION)
            pyautogui.click(pos,duration=0.25)
            time.sleep(1)
            pos = pyautogui.locateCenterOnScreen(imagePath('search_friends.png'), region=GAME_REGION)
            if pos is None:
                pos1 = pyautogui.locateCenterOnScreen(imagePath('search_friends1.png'), region=GAME_REGION)
                username = input('Please enter the username of your opponent: ')
                time.sleep(1)
                pyautogui.click(pos1,duration=0.25)
                time.sleep(1)
                pyautogui.typewrite(username)
                pyautogui.press('enter')
                time.sleep(1)
            else:
                username = input('Please enter the username of your opponent: ')
                time.sleep(1)
                pyautogui.click(pos,duration=0.25)
                time.sleep(1)
                pyautogui.typewrite(username)
                pyautogui.press('enter')
                time.sleep(1)
            pos = pyautogui.locateCenterOnScreen(imagePath('add_friend.png'), region=GAME_REGION)
            if pos is not None:
                pyautogui.click(pos,duration=0.25)
                time.sleep(1)
                pos = pyautogui.locateCenterOnScreen(imagePath('challenge_friend.png'), region=GAME_REGION)
                pyautogui.click(pos,duration=0.25)
                return True
            else:
                pos = pyautogui.locateCenterOnScreen(imagePath('challenge_friend.png'), region=GAME_REGION)
                if pos is not None:
                    pyautogui.click(pos,duration=0.25)
                    print('Waiting for response.')
                    while trynoresponse > 0:
                        time.sleep(1)
                        pos = pyautogui.locateCenterOnScreen(imagePath('no_response.png'), region=GAME_REGION)
                        if pos is None:
                            trynoresponse -= 1
                        else:
                            time.sleep(2)
                            pos = pos = pyautogui.locateCenterOnScreen(imagePath('preregionx_button.png'), region=GAME_REGION)
                            pyautogui.click(pos,duration=0.25)
                            navigatePool()
                    print('Checking to see if game has started.')
                    if trynoresponse == 0:
                        while trytopleft > 0:
                            time.sleep(1)
                            pos = pyautogui.locateCenterOnScreen(imagePath('toplefthole.png'), region=GAME_REGION)
                            if pos is not None:
                                print('Game Started.')
                                return True
                            else:
                                trytopleft -= 1
                    if trytopleft == 0:
                        time.sleep(2)
                        pos = pyautogui.locateCenterOnScreen(imagePath('search_friendsmagni.png'), region=GAME_REGION)
                        if pos is not None:
                            pos = pyautogui.locateCenterOnScreen(imagePath('preregionx_button.png'), region=GAME_REGION)
                            pyautogui.click(pos,duration=0.25)
                            navigatePool()
                        else:
                            refreshPage()
                            while True:
                                pos = pyautogui.locateCenterOnScreen(imagePath('loading100.png'), region=GAME_REGION)
                                if pos is not None:
                                    break
                            time.sleep(5)
                            navigatePool()
                else:
                    print('Can\'t find friend.')
                    pos = pos = pyautogui.locateCenterOnScreen(imagePath('preregionx_button.png'), region=GAME_REGION)
                    pyautogui.click(pos,duration=0.25)
                    navigatePool()
        elif playchoice in randomchoice:
            return False


def poolGame(): #function for intializing a pool game
    turnnum = 0
    leftpocketnum = 0
    
    with open('gamecounter.txt','r') as g: #keeps track of the number of games. opens the file, reads, and writes over it
        for line in g:
            if line == None:
                g.write(0)
            else:
                gamenum = int(line)
                newgamenum = str(gamenum + 1)
                with open('gamecounter.txt','w') as g:
                    g.write(newgamenum)
                    g.close()
                
    while True: #searches for the top left hole and gets a smaller region for determining region of the pool table
        pos = pyautogui.locateOnScreen(imagePath('toplefthole.png'), region=GAME_REGION)
        if pos is not None:
            print('Game in session. Checking for turn.')
            poolreg = pyautogui.locateOnScreen(imagePath('poolrightcorner.png'), region=GAME_REGION)
            if poolreg is None:
                poolreg = pyautogui.locateOnScreen(imagePath('toprighthole.png'), region=GAME_REGION)
            topRightX = poolreg[0] + poolreg[2]
            topRightY = poolreg[1]
            POOL_REGION = (topRightX - 605, topRightY, 605, 314)
            print('Table region acquired.' + str(POOL_REGION))
            break
        else:
            pos = pyautogui.locateOnScreen(imagePath('poolrightcorner.png'), region=GAME_REGION)
            if pos is not None:
                print('Game in session. Checking for turn.')
                poolreg = pyautogui.locateOnScreen(imagePath('poolrightcorner.png'), region=GAME_REGION)
                if poolreg is None:
                    poolreg = pyautogui.locateOnScreen(imagePath('toprighthole.png'), region=GAME_REGION)
                topRightX = poolreg[0] + poolreg[2]
                topRightY = poolreg[1]
                POOL_REGION = (topRightX - 605, topRightY, 605, 314)
                print('Table region acquired.' + str(POOL_REGION))
                break
            else:
                time.sleep(1)
                leftpocketnum += 1
            
        if leftpocketnum == 5:
            print('Tried finding top left pocket 5 times. Refreshing page. Please don\'t click anything.')
            refreshPage()
            time.sleep(10)
            navigatePool()
            
    holesxy = markHoles(POOL_REGION)        
    print('Game #' + newgamenum)
    cwd = (r'C:\Users\Grant\AppData\Local\Programs\Python\Projects')
    os.makedirs('games\game'+newgamenum+'\\table', exist_ok=True)
    os.makedirs('games\game'+newgamenum+'\\outlined', exist_ok=True)
    while True: #begins the game cycle.
        time.sleep(1)
        turnnum = turnCycle(turnnum) #checks for turn, stops cycling until it is bots turn
        print('Turn #' + str(turnnum))
        pyautogui.screenshot(('games\game'+newgamenum+'\\table\pooltable'+str(turnnum)+'.png'),region=POOL_REGION)
        imgpath = cwd+'/games/game'+newgamenum+'/table/pooltable'+str(turnnum)+'.png' #takes that picture and assigns variable
        sldorstpe, ballist = ballCheck(GAME_REGION) #checks which balls are in need of being hit and returns suit needed to hit and a list of all balls needed
        if sldorstpe == 'nosuit':
            print('Ball Suit: Either.')
        elif sldorstpe == 'solid':
            print('Ball Suit: Solids.')
        else:
            print('Ball Suit: Stripes.')
        playRound(sldorstpe,ballist,imgpath,turnnum,newgamenum,holesxy) #initiates function for each round. basically, checks turn number, if its first turn hit the triangle, or if the other
        checkGameOver()
        
                

def playRound(suit,listofballs,imagepath,count,gamenum,holelocation):#takes the turn number, suit(solid or stripes), the list of colors of balls needed to be hit, and the image
    #pyautogui.moveTo(957,305)
    pyautogui.moveTo(815,405)
    if suit == 'nosuit':#if suit is none, it is either beginning of the game and no one has hit ball in, or it is the very end and the eight ball is the only left
        if count == 1:#opening hit
            cpoints, c, eight, suit2, c2points = prepareBalls(suit,listofballs,imagepath,count,gamenum)
            if c[0] < 815:
                print('Breaking.')
                pyautogui.moveTo(x=1104,y=448)
                pyautogui.mouseDown(button='left')
                pyautogui.moveRel(-210,-3)
                pyautogui.mouseUp(button='left')
                pyautogui.moveTo(x=968,y=455)
                moveMouseOut(c)
                time.sleep(8)
            else:
                cpoints, c, eight, suit2, c2points = prepareBalls(suit,listofballs,imagepath,count,gamenum)
                #print(cpoints, c, eight, suit2)
                determineDistanceToHole(suit2,cpoints,c2points,c,eight,holelocation)
                time.sleep(2)
                moveMouseOut(c)
        elif count > 1 and count <= 6: #if it has reached turn 6 and no ball has been hit in, idk what they are doing
            cpoints, c, eight, suit2, c2points = prepareBalls(suit,listofballs,imagepath,count,gamenum)
            #print(cpoints, c, eight, suit2)
            determineDistanceToHole(suit2,cpoints,c2points,c,eight,holelocation)
            time.sleep(2)
            moveMouseOut(c)
        elif count > 8: #hit eight ball
            cpoints, c, eight, suit2, c2points = prepareBalls(suit,listofballs,imagepath,count,gamenum)
            #print(cpoints, c, eight, suit2)
            determineDistanceToHole(None,cpoints,c2points,c,eight,holelocation)
            time.sleep(2)
            moveMouseOut(c)
    elif suit == 'solids': #hitting solid balls
        cpoints, c, eight, suit2, c2points = prepareBalls(suit,listofballs,imagepath,count,gamenum)
        determineDistanceToHole(suit,cpoints,c2points,c,eight,holelocation)
        time.sleep(2)
        moveMouseOut(c)
    elif suit == 'stripes': #hitting striped balls
        cpoints, c, eight, suit2, c2points = prepareBalls(suit,listofballs,imagepath,count,gamenum)
        determineDistanceToHole(suit,cpoints,c2points,c,eight,holelocation)
        time.sleep(2)
        moveMouseOut(c)

def prepareBalls(suit,listofb,imagepath,count,gamenum): #prepares balls for being hit. creates masks for necessary balls, puts the list of balls into a dictionary, and then outlines balls and puts centerpoints into a list
    mask, maskimage = maskSetup(imagepath,listofb)
    markballs = maskDict(listofb,mask)
    points, c, eight, suit, otherpoints = outlineBall(maskimage,suit,markballs,count,gamenum)
    return points,c,eight,suit, otherpoints

def stringToColor(color): #takes the list of colors and based on name, returns a rgb color value
    if color == 'white':
        return (255,255,255)
    elif color == 'black':
        return (255,255,0)
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

def ballCheck(region): #searches for pictures of balls in game region and complies list of balls to be hit
    solidlist = ['cue','eightball']
    stripelist = ['cue','eightball']
    nosuit = ['cue','eightball','yellow','blue','lightred','purple','orange','green','darkred']
    pyautogui.moveTo(957,305)
    pos = pyautogui.locateOnScreen(imagePath('ballpic1.png'), region=region)
    if pos is not None:
        topRightX = pos[0] + pos[2]
        topRightY = pos[1]
        reg = (topRightX - 176, topRightY, 176, 90)
    else:
        reg = (region[0]+78, region[1]+80, 176, 90)
    while True:
        pos = pyautogui.locateCenterOnScreen(imagePath('1ball.png'), region=reg)
        if pos is not None:
            solidlist.append('yellow')
        pos = pyautogui.locateCenterOnScreen(imagePath('2ball.png'), region=reg)   
        if pos is not None:
            solidlist.append('blue')
        pos = pyautogui.locateCenterOnScreen(imagePath('3ball.png'), region=reg)
        if pos is not None:
            solidlist.append('lightred')
        pos = pyautogui.locateCenterOnScreen(imagePath('4ball.png'), region=reg)
        if pos is not None:
            solidlist.append('purple')
        pos = pyautogui.locateCenterOnScreen(imagePath('5ball.png'), region=reg)
        if pos is not None:
            solidlist.append('orange')
        pos = pyautogui.locateCenterOnScreen(imagePath('6ball.png'), region=reg)
        if pos is not None:
            solidlist.append('green')
        pos = pyautogui.locateCenterOnScreen(imagePath('7ball.png'), region=reg)
        if pos is not None:
            solidlist.append('darkred')
            break
        else:
            break
    while True:
        pos = pyautogui.locateCenterOnScreen(imagePath('9ball.png'), region=reg)
        if pos is not None:
            stripelist.append('yellow')
        pos = pyautogui.locateCenterOnScreen(imagePath('10ball.png'), region=reg)
        if pos is not None:
            stripelist.append('blue')
        pos = pyautogui.locateCenterOnScreen(imagePath('11ball.png'), region=reg)
        if pos is not None:
            stripelist.append('lightred')
        pos = pyautogui.locateCenterOnScreen(imagePath('12ball.png'), region=reg)
        if pos is not None:
            stripelist.append('purple')
        pos = pyautogui.locateCenterOnScreen(imagePath('13ball.png'), region=reg)
        if pos is not None:
            stripelist.append('orange')
        pos = pyautogui.locateCenterOnScreen(imagePath('14ball.png'), region=reg)
        if pos is not None:
            stripelist.append('green')
        pos = pyautogui.locateCenterOnScreen(imagePath('15ball.png'), region=reg)
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

def maskSetup(img,listofb): #sets up masks for each ball based on which are in need to be hit
    balls = []
    img = cv2.imread(img,1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for c in listofb:
        if c == 'cue':
            upper_whitecue = np.array([30,255,255])
            lower_whitecue = np.array([26,0,100])
            maskwhiteball = cv2. inRange(hsv, lower_whitecue, upper_whitecue)
            maskwhiteball = cv2.erode(maskwhiteball,None,iterations=2)
            maskwhiteball = cv2.dilate(maskwhiteball,None,iterations=3)
            balls.append(maskwhiteball)
        elif c == 'eightball':
            upper_black = np.array([50,225,70])
            lower_black = np.array([10,0,0])
            maskblackball = cv2. inRange(hsv, lower_black, upper_black)
            maskblackball = cv2.erode(maskblackball,None,iterations=1)
            maskblackball = cv2.dilate(maskblackball,None,iterations=3)
            balls.append(maskblackball)
        elif c == 'yellow':
            upper_yellow = np.array([30,255,255])
            lower_yellow = np.array([23,70,0])
            maskyellowball = cv2.inRange(hsv, lower_yellow, upper_yellow)
            maskyellowball = cv2.erode(maskyellowball,None,iterations=1)
            maskyellowball = cv2.dilate(maskyellowball,None,iterations=2)
            balls.append(maskyellowball)
        elif c == 'blue':
            upper_blue = np.array([140,255,255])
            lower_blue = np.array([110,0,0])
            maskblueball = cv2.inRange(hsv, lower_blue,upper_blue)
            upper_blue2 = np.array([135,255,255])
            lower_blue2 = np.array([105,60,100])
            maskblueball2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
            maskblueball_1 = cv2.bitwise_and(maskblueball,maskblueball2)
            maskblueball = cv2.dilate(maskblueball_1,None,iterations=3)
            balls.append(maskblueball)
        elif c == 'lightred':
            upper_lightred = np.array([4,255,200])
            lower_lightred = np.array([0,200,110])
            masklightredball = cv2.inRange(hsv,lower_lightred, upper_lightred)
            masklightredball = cv2.dilate(masklightredball,None,iterations=3)
            balls.append(masklightredball)
        elif c == 'purple':
            upper_purple = np.array([150,255,255])
            lower_purple = np.array([135,0,70])
            maskpurpleball = cv2.inRange(hsv, lower_purple, upper_purple)
            maskpurpleball = cv2.dilate(maskpurpleball,None,iterations=2)
            balls.append(maskpurpleball)
        elif c == 'orange':
            upper_orange = np.array([18,255,230])
            lower_orange = np.array([11,190,120])
            maskorangeball = cv2.inRange(hsv,lower_orange, upper_orange)
            maskorangeball = cv2.dilate(maskorangeball,None,iterations=2)
            balls.append(maskorangeball)
        elif c == 'green':
            upper_green = np.array([70,255,255])
            lower_green = np.array([35,170,50])
            maskgreenball = cv2.inRange(hsv, lower_green, upper_green)
            maskgreenball = cv2.dilate(maskgreenball,None,iterations=2)
            balls.append(maskgreenball)
        elif c == 'darkred':
            upper_darkred = np.array([5,255,150])
            lower_darkred = np.array([3,100,70])
            maskdarkredball = cv2.inRange(hsv,lower_darkred, upper_darkred)
            maskdarkredball = cv2.erode(maskdarkredball,None,iterations=1)
            #maskdarkredball = cv2.dilate(maskdarkredball,None,iterations=3)
            balls.append(maskdarkredball)
        try:
            cv2.imshow('mask',maskwhiteball)
            cv2.imshow('mask1',maskblackball)
            cv2.imshow('mask2',maskblueball)
            cv2.imshow('mask3',masklightredball)
            cv2.imshow('mask4',maskdarkredball)
            cv2.imshow('mask5',maskgreenball)
            cv2.imshow('mask6',maskorangeball)
            cv2.imshow('mask7',maskyellowball)
            cv2.imshow('mask8',maskpurpleball)

            cv2.imshow('circle',img)
            

            while(1):
                k = cv2.waitKey(0)
                if (k == 27):
                    break
        except UnboundLocalError:
            pass

        cv2.destroyAllWindows()
    return balls,img

def outlineBall(image,suit, ballcolordict,count,gamenum): #draws contours, but more importantly, gets the center points of each ball
    solids = []
    stripes = []
    cue = (0,0)
    eightball = (0,0)
    for k,v in ballcolordict.items():
        a = stringToColor(k)
        contours = cv2.findContours(v.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if imutils.is_cv2() else contours[1]
        center = None
        for c in contours:
            if k == 'cue':
                if len(contours) == 1:
                    ((x,y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                    cue = center
                    #print(cue)
                    if radius > 6 and radius < 12:
                        cv2.circle(image, (int(x), int(y)), int(radius-2),
                        a, 2)
                        cv2.circle(image, center, 7, a, -1)
                    #cv2.imwrite(os.path.join(imgpath,imgname),image)
                        
                elif len(contours) >= 2:
                    c = max(contours, key=cv2.contourArea)
                    ((x,y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                    cue = center

                    if radius > 6 and radius < 12:
                        cv2.circle(image, (int(x), int(y)), int(radius-2),a, 2)
                        cv2.circle(image, center, 7, a, -1)
                    #cv2.imwrite(os.path.join(imgpath,imgname),image)
                    
            elif k == 'eightball':
                if len(contours) == 1:
                    ((x,y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                    eightball = center

                    if radius > 5 and radius < 12:
                        cv2.circle(image, (int(x), int(y)), int(radius-2),
                        a, 2)
                        cv2.circle(image, center, 7, a, -1)
                    #cv2.imwrite(os.path.join(imgpath,imgname),image)
                        
                elif len(contours) >= 2:
                    c = max(contours, key=cv2.contourArea)
                    ((x,y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                    eightball = center

                    if radius > 5 and radius < 12:
                        cv2.circle(image, (int(x), int(y)), int(radius-2),
                        a, 2)
                        cv2.circle(image, center, 7, a, -1)
                    #cv2.imwrite(os.path.join(imgpath,imgname),image)

            else:
                if len(contours) == 1: #only one suit on the board
                    if suit == 'solids':
                        cmax = max(contours, key=cv2.contourArea)
                        ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                        M = cv2.moments(cmax)
                        centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                        solids.append(centermax)

                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(x), int(y)), int(radius-2),
                            a, 2)
                            cv2.circle(image, centermax, 7, a, -1)
                                
                        imgpath = 'games/game'+gamenum+'/outlined'
                        imgname = 'pooltable'+str(count)+'.png'
                        cv2.imwrite(os.path.join(imgpath,imgname),image)
                            
                    elif suit == 'stripes':
                        cmax = min(contours, key=cv2.contourArea)
                        ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                        M = cv2.moments(cmax)
                        centermin = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                        stripes.append(centermin)

                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(x), int(y)), int(radius-2),
                        (a[0]-20,a[1]-25,a[2]-20), 2)

                        imgpath = 'games/game'+gamenum+'/outlined'
                        imgname = 'pooltable'+str(count)+'.png'
                        cv2.imwrite(os.path.join(imgpath,imgname),image)
                            
                    elif suit == 'nosuit':
                        cmax = max(contours, key=cv2.contourArea)
                        ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                        M = cv2.moments(cmax)
                        centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                        solids.append(centermax)

                        if radius > 0 and radius < 12:
                            cv2.circle(image, (int(x), int(y)), int(radius-2),
                            a, 2)
                            cv2.circle(image, centermax, 7, a, -1)

                        #removearray(contours,cmax)##################
                        cmax2 = min(contours, key=cv2.contourArea)
                        ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmax2)
                        M = cv2.moments(cmax2)
                        centermin = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                        stripes.append(centermin)

                        if radius > 0 and radius < 12:
                            cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),
                        (a[0]-20,a[1]-25,a[2]-20), 2)

                        imgpath = 'games/game'+gamenum+'/outlined'
                        imgname = 'pooltable'+str(count)+'.png'
                        cv2.imwrite(os.path.join(imgpath,imgname),image)
                 
                elif len(contours) == 2: #both solid and stripes on the board
                    if suit == 'solids':
                        cmax = max(contours, key=cv2.contourArea)
                        ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                        M = cv2.moments(cmax)
                        centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                        solids.append(centermax)
                        #print(centermax, '2suit-solids')

                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(x), int(y)), int(radius-2),
                            a, 2)
                            cv2.circle(image, centermax, 7, a, -1)

                        #removearray(contours,cmax)
                        cmin = min(contours, key=cv2.contourArea)############
                        ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmin)
                        M1 = cv2.moments(cmin)
                        centermin = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))
                        stripes.append(centermin)
                        
                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),
                            (a[0]-20,a[1]-25,a[2]-20), 2)

                        imgpath = 'games/game'+gamenum+'/outlined'
                        imgname = 'pooltable'+str(count)+'.png'
                        cv2.imwrite(os.path.join(imgpath,imgname),image)
                            
                    elif suit == 'stripes':
                        cmax = max(contours, key=cv2.contourArea)
                        ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                        M = cv2.moments(cmax)
                        centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                        solids.append(centermax)

                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(x), int(y)), int(radius-2),
                            a, 2)
                            cv2.circle(image, centermax, 7, a, -1)
                            
                        cmin = min(contours, key=cv2.contourArea)
                        ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmin)
                        M1 = cv2.moments(cmin)
                        centermin = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))
                        stripes.append(centermin)
                        
                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),
                            (a[0]-20,a[1]-25,a[2]-20), 2)

                        imgpath = 'games/game'+gamenum+'/outlined'
                        imgname = 'pooltable'+str(count)+'.png'
                        cv2.imwrite(os.path.join(imgpath,imgname),image)

                    elif suit == 'nosuit':
                        print('here')
                        cmax = max(contours, key=cv2.contourArea)
                        ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                        M = cv2.moments(cmax)
                        centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                        solids.append(centermax)

                        if radius > 0 and radius < 12:
                            cv2.circle(image, (int(x), int(y)), int(radius-2),
                            a, 2)
                            cv2.circle(image, centermax, 7, a, -1)

                        cmin = min(contours, key=cv2.contourArea)
                        ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmin)
                        M1 = cv2.moments(cmin)
                        centermin = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))
                        stripes.append(centermin)

                        if radius > 0 and radius < 12:
                            cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),
                        (a[0]-20,a[1]-25,a[2]-20), 2)

                        imgpath = 'games/game'+gamenum+'/outlined'
                        imgname = 'pooltable'+str(count)+'.png'
                        cv2.imwrite(os.path.join(imgpath,imgname),image)
                            
                elif len(contours) > 2: #both solid and stripes plus the possibility of false positives
                    if suit == 'solids':
                        cmax = max(contours, key=cv2.contourArea)
                        ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                        M = cv2.moments(cmax)
                        centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                        solids.append(centermax)
                        
                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(x), int(y)), int(radius-2),
                            a, 2)
                            cv2.circle(image, centermax, 7, a, -1)

                        removearray(contours,cmax)##########################################
                        cmin = max(contours, key=cv2.contourArea)
                        ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmin)
                        M1 = cv2.moments(cmin)
                        centermin = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))
                        stripes.append(centermin)
                        
                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),
                            (a[0]-20,a[1]-25,a[2]-20), 2)

                        imgpath = 'games/game'+gamenum+'/outlined'
                        imgname = 'pooltable'+str(count)+'.png'
                        cv2.imwrite(os.path.join(imgpath,imgname),image)
                            
                    elif suit == 'stripes':
                        cmax = max(contours, key=cv2.contourArea)
                        ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                        M = cv2.moments(cmax)
                        centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                        solids.append(centermax)
                        
                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(x), int(y)), int(radius-2),
                            a, 2)
                            cv2.circle(image, centermax, 7, a, -1)

                        removearray(contours,cmax)########################################
                        cmax2 = max(contours, key=cv2.contourArea)
                        ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmax2)
                        M1 = cv2.moments(cmax2)
                        centermax2 = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))
                        stripes.append(centermax2)
                        
                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),
                            (a[0]-20,a[1]-25,a[2]-20), 2)

                        imgpath = 'games/game'+gamenum+'/outlined'
                        imgname = 'pooltable'+str(count)+'.png'
                        cv2.imwrite(os.path.join(imgpath,imgname),image)

                    elif suit == 'nosuit':
                        cmax = max(contours, key=cv2.contourArea)
                        ((x,y), radius) = cv2.minEnclosingCircle(cmax)
                        M = cv2.moments(cmax)
                        centermax = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                        solids.append(centermax)

                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(x), int(y)), int(radius-2),
                            a, 2)
                            cv2.circle(image, centermax, 7, a, -1)

                        removearray(contours,cmax)############################
                        cmax2 = max(contours, key=cv2.contourArea)
                        ((xmin,ymin), radiusmin) = cv2.minEnclosingCircle(cmax2)
                        M1 = cv2.moments(cmax2)
                        centermax2 = (int(M1['m10'] / M1['m00']), int(M1['m01'] / M1['m00']))
                        stripes.append(centermax2)

                        if radius > 6 and radius < 12:
                            cv2.circle(image, (int(xmin), int(ymin)), int(radiusmin-2),
                        (a[0]-20,a[1]-25,a[2]-20), 2)

                        imgpath = 'games/game'+gamenum+'/outlined'
                        imgname = 'pooltable'+str(count)+'.png'
                        cv2.imwrite(os.path.join(imgpath,imgname),image)
                        
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
            
def removearray(L,arr):
    ind = 0
    size = len(L)
    while ind != size and not np.array_equal(L[ind],arr):
        ind += 1
    if ind != size:
        L.pop(ind)
    else:
        raise ValueError('array not found in list.')

def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0
    else:
        start += 0.0 # force it to be a float

    if inc == None:
        inc = 1.0

    count = int((end - start) / inc)
    if start + count * inc != end:
        count += 1

    L = [None,] * count
    for i in range(count):
        L[i] = start + i * inc

    return L

def markHoles(reg):
    holes = {}
    pos = pyautogui.locateCenterOnScreen(imagePath('tlh.png'), region=reg)
    if pos is not None:
        holes['tlh'] = pos
    pos = pyautogui.locateCenterOnScreen(imagePath('tmh.png'), region=reg)
    if pos is not None:
        holes['tmh'] = pos
        pos = pyautogui.locateCenterOnScreen(imagePath('trh.png'), region=reg)
    if pos is not None:
        holes['trh'] = pos
        pos = pyautogui.locateCenterOnScreen(imagePath('blh.png'), region=reg)
    if pos is not None:
        holes['blh'] = pos
        pos = pyautogui.locateCenterOnScreen(imagePath('bmh.png'), region=reg)
    if pos is not None:
        holes['bmh'] = pos
        pos = pyautogui.locateCenterOnScreen(imagePath('brh.png'), region=reg)
    if pos is not None:
        holes['brh'] = pos
    if len(holes) != 6:
        print('Could not find all 6 holes')
        return holes
    else:
        return holes

def bestHole(x,y,h1,h2,slope,perp,z1,z2,listA,listB):
    print('starting hole procedure')
    topleft1 = (h1-9,h1+16)
    topleft2 = (h1+16,-9)
    
    bottomleft1 = (h1-9,h1-16)
    bottomleft2 = (h1+16,+9)

    topmiddle = (h1-16,h2)
    bottommiddle = (h1+16,h2)

    topright1 = (h1-9,h1-16)
    topright2 = (h1+16,+9)
    
    bottomright1 = (h1+9,h1-16)
    bottomright2 = (h1-16,+9)

    if z2 == 'left':
        if slope > 0:
            upperx = (x+(9*sqrt(1 / (1+perp**2))))
            lowerx = (x-(9*sqrt(1 / (1+perp**2))))
            uppery = (y-((perp*9)*sqrt(1 / (1+perp**2))))
            lowery = (y+((perp*9)*sqrt(1 / (1+perp**2))))
            
            slope1 = (topleft1[1] - lowery) / (topleft1[0] - lowerx)
            slope2 = (topleft2[1] - uppery) / (topleft2[0] - upperx)

            pointxy = ((x+(17*sqrt(1 / (1+slope**2)))),(y+((slope*17)*sqrt(1 / (1+slope**2)))))
            
            for h in listA:
                for i in frange(topleft1[0],lowerx,slope1):
                    for j in frange(topleft1[1],lowery,slope1):
                        if h[0] > i and h[1] < j:
                            for k in frange(topleft2[0],upperx,slope2):
                                for l in frange(topleft2[1],uppery,slope2):
                                    if h[0] < k and h[1] > j:
                                        pass
                                    else:
                                        return True, poinxy
                        else:
                            return True,pointxy
                        
                    
        elif slope < 0:
            upperx = (x-(9*sqrt(1 / (1+slope**2))))
            lowerx = (x+(9*sqrt(1 / (1+slope**2))))
            uppery = (y-((slope*9)*sqrt(1 / (1+slope**2))))
            lowery = (y+((slope*9)*sqrt(1 / (1+slope**2))))
            
            slope1 = (lowery - bottomleft1[1]) / (lowerx - bottomleft1[0])
            slope2 = (uppery - bottomleft2[1]) / (upperx - bottomleft2[0])

            pointxy = ((x+(17*sqrt(1 / (1+slope**2)))),(y-((slope*17)*sqrt(1 / (1+slope**2)))))

            for h in listA:
                for i in frange(lowerx,topleft1[0],slope1):
                    for j in frange(lowery,topleft1[1],slope1):
                        if h[0] > i and h[1] > j:
                            for k in frange(upperx,topleft2[0],slope2):
                                for l in frange(uppery,topleft2[1],slope2):
                                    if h[0] < k and h[1] < j:
                                        pass
                                    else:
                                        return True, poinxy
                        else:
                            return True,pointxy
        else:
            upperx = (x)
            lowerx = (x)
            uppery = (y-9)
            lowery = (y+9)

            pointxy = ((x+(17*sqrt(1 / (1+slope**2)))), y)

            for h in listA:
                for i in frange(topleft1[0],lowerx,1):
                    for j in frange(topleft1[1],lowery,1):
                        if h[0] < i and h[1] < lowery:
                            for k in frange(topleft2[0],upperx,1):
                                for l in frange(topleft2[1],uppery,1):
                                    if h[0] < k and h[1] > j:
                                        pass
                                    else:
                                        return True, poinxy
                        else:
                            return True,pointxy
        
        
    elif z2 == 'right':
        if slope < 0:
            upperx = (x-(9*sqrt(1 / (1+slope**2))))
            lowerx = (x+(9*sqrt(1 / (1+slope**2))))
            uppery = (y-((slope*9)*sqrt(1 / (1+slope**2))))
            lowery = (y+((slope*9)*sqrt(1 / (1+slope**2))))
            
            slope1 = (topleft1[1] - lowery) / (topleft1[0] - lowerx)
            slope2 = (topleft2[1] - uppery) / (topleft2[0] - upperx)

            pointxy = ((x-(17*sqrt(1 / (1+slope**2)))),(y+((slope*17)*sqrt(1 / (1+slope**2)))))
            
            for h in listA:
                for i in frange(topleft1[0],lowerx,slope1):
                    for j in frange(topleft1[1],lowery,slope1):
                        if h[0] > i and h[1] > j:
                            for k in frange(topleft2[0],upperx,slope2):
                                for l in frange(topleft2[1],uppery,slope2):
                                    if h[0] < k and h[1] < j:
                                        pass
                                    else:
                                        return True, poinxy
                        else:
                            return True,pointxy
        
        elif slope > 0:
            upperx = (x+(9*sqrt(1 / (1+slope**2))))
            lowerx = (x-(9*sqrt(1 / (1+slope**2))))
            uppery = (y-((slope*9)*sqrt(1 / (1+slope**2))))
            lowery = (y+((slope*9)*sqrt(1 / (1+slope**2))))
            
            slope1 = (lowery - bottomleft1[1]) / (lowerx - bottomleft1[0])
            slope2 = (uppery - bottomleft2[1]) / (upperx - bottomleft2[0])

            pointxy = ((x-(17*sqrt(1 / (1+slope**2)))),(y+((slope*17)*sqrt(1 / (1+slope**2)))))

            for h in listA:
                for i in frange(topleft1[0],lowerx,slope1):
                    for j in frange(topleft1[1],lowery,slope1):
                        if h[0] > i and h[1] < j:
                            for k in frange(topleft2[0],upperx,slope2):
                                for l in frange(topleft2[1],uppery,slope2):
                                    if h[0] < k and h[1] > j:
                                        pass
                                    else:
                                        return True, poinxy
                        else:
                            return True,pointxy
        else:
            upperx = (x)
            lowerx = (x)
            uppery = (y-9)
            lowery = (y+9)

            pointxy = ((x-(17*sqrt(1 / (1+slope**2)))),y)

            for h in listA:
                for i in frange(topleft1[0],lowerx,1):
                    for j in frange(topleft1[1],lowery,1):
                        if h[0] > i and h[1] < j:
                            for k in frange(topleft2[0],upperx,1):
                                for l in frange(topleft2[1],uppery,1):
                                    if h[0] > k and h[1] > j:
                                        pass
                                    else:
                                        return True, poinxy
                        else:
                            return True,pointxy
        
    if z2 == 'middle':
            if z1 == 'above':
                upperx = (x+(9*sqrt(1 / (1+slope**2))))
                lowerx = (x-(9*sqrt(1 / (1+slope**2))))
                uppery = (y+((slope*9)*sqrt(1 / (1+slope**2))))
                lowery = (y-((slope*9)*sqrt(1 / (1+slope**2))))

                slope1 = (topleft1[1] - lowery) / (topleft1[0] - lowerx)
                slope2 = (topleft2[1] - uppery) / (topleft2[0] - upperx)

                pointxy = ((x),(y+((slope*17)*sqrt(1 / (1+slope**2)))))

                for h in listA:
                    for i in frange(topleft1[0],lowerx,slope1):
                        for j in frange(topleft1[1],lowery,slope1):
                            if h[0] > i and h[1] < j:
                                for k in frange(topleft2[0],upperx,slope2):
                                    for l in frange(topleft2[1],uppery,slope2):
                                        if h[0] < k and h[1] < j:
                                            pass
                                        else:
                                            return True, poinxy
                            else:
                                return True,pointxy
        
            elif z1 == 'below':
                upperx = (x+(9*sqrt(1 / (1+slope**2))))
                lowerx = (x-(9*sqrt(1 / (1+slope**2))))
                uppery = (y-((slope*9)*sqrt(1 / (1+slope**2))))
                lowery = (y+((slope*9)*sqrt(1 / (1+slope**2))))

                slope1 = (lowery - bottomleft1[1]) / (lowerx - bottomleft1[0])
                slope2 = (uppery - bottomleft2[1]) / (upperx - bottomleft2[0])

                pointxy = ((x),(y-((slope*17)*sqrt(1 / (1+slope**2)))))

                for h in listA:
                    for i in frange(lowerx,topleft1[0],slope1):
                        for j in frange(lowery,topleft1[1],slope1):
                            if h[0] > i and h[1] > j:
                                for k in frange(upperx,topleft2[0],slope2):
                                    for l in frange(uppery,topleft2[1],slope2):
                                        if h[0] < k and h[1] > j:
                                            pass
                                        else:
                                            return True, poinxy
                            else:
                                return True,pointxy

def bestOption(x,y,holelocation,zone1,zone2,list1,list2):
    print(x,y,holelocation,zone1,zone2,list1,list2)
    print('starting best option procedure')
    for k,v in holelocation.items():
        h1 = v[0]
        h2 = v[1]
        if zone2 == 'left':
            if zone1 == 'above':
                if k == 'tlh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'tmh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'trh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                    
            elif zone1 == 'below':
                if k == 'blh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'bmh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'brh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass

            elif zone1 == 'middle':
                if k == 'tlh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'tmh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'blh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'bmh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'tlh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'blh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                    
        elif zone2 == 'right':
            if zone1 == 'above':
                if k == 'tlh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'tmh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'trh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
            elif zone1 == 'below':
                if k == 'blh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'bmh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'brh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                    
            elif zone1 == 'middle':
                if k == 'tlh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'tmh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'blh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'bmh':
                   slope = ((y-h2) / (x-h1))
                   perp = (-(x-h1) / (y-h2))
                   print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                   torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                   if torf is True:
                        return point,h1,h2
                   elif torf is None:
                        pass
                   else:
                        pass
                elif k == 'trh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'brh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass

        if zone2 == 'middle':
            if zone1 == 'above':
                if k == 'tmh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'trh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'tlh':
                    slope = ((h2-y) / (h1-x))
                    perp = (-(h1-x) / (h2-y))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass

            elif zone1 == 'below':
                if k == 'blh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'bmh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                elif k == 'brh':
                    slope = ((y-h2) / (x-h1))
                    perp = (-(x-h1) / (y-h2))
                    print(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    torf,point = bestHole(x,y,h1,h2,slope,perp,zone1,zone2,list1,list2)
                    if torf is True:
                        return point,h1,h2
                    elif torf is None:
                        pass
                    else:
                        pass
                    
            elif zone1 == 'middle':
                pass

def determineDistanceToHole(suit,listofpoints,otherlistofpoints,cue,eightballpoint,holelocation):
    besthole = (0,0)
    bestball = (0,0)
    print('starting hit procedure')
    if suit == 'solids':
        if not listofpoints:
            x = eightballpoint[0]
            y = eightballpoint[1]
            p,hx,hy = bestOption(x,y,holelocation,'above','left',listP,otherlistofpoints)
            dtb, dth = distanceFunc(cuepoint,p,hx,hy)
            hitBall(p,dtb,dth)
        else:
            for i in listofpoints:
                x = i[0]
                y = i[1]
                x1 = x-9
                x2 = x+9
                y1 = y-9
                y2 = y+9
                listP = listofpoints
                listP.remove(i)
                if cue[0] > x1 and cue[0] > x2:
                    if cue[1] > y1 and cue[1] > y2:
                        p,hx,hy = bestOption(x,y,holelocation,'above','left',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit solid ball.')
                        time.sleep(5)
                    elif cue[1] < y2 and cue[1] < y1:
                        p,hx,hy = bestOption(x,y,holelocation,'below','left',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit solid ball.')
                        time.sleep(5)
                    elif cue[1] > y1 and cue[1] < y2:
                        p,hx,hy = bestOption(x,y,holelocation,'middle','left',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit solid ball.')
                        time.sleep(5)
                        
                elif cue[0] < x2 and cue[0] < x1:
                    if cue[1] > y1 and cue[1] > y2:
                        p,hx,hy = bestOption(x,y,holelocation,'above','right',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit solid ball.')
                        time.sleep(5)
                    elif cue[1] < y2 and cue[1] < y1:
                        p,hx,hy = bestOption(x,y,holelocation,'below','right',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit solid ball.')
                        time.sleep(5)
                    elif cue[1] > y1 and cue[1] < y2:
                        p,hx,hy = bestOption(x,y,holelocation,'middle','right',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit solid ball.')
                        time.sleep(5)

                elif cue[0] > x1 and cue[0] < x2:
                    if cue[1] > y1 and cue[1] > y2:
                        p,hx,hy = bestOption(x,y,holelocation,'above','middle',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit solid ball.')
                        time.sleep(5)
                    elif cue[1] < y2 and cue[1] < y1:
                        p,hx,hy = bestOption(x,y,holelocation,'below','middle',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit solid ball.')
                        time.sleep(5)
                    elif cue[1] > y1 and cue[1] < y2:
                        p,hx,hy = bestOption(x,y,holelocation,'middle','middle',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit solid ball.')
                        time.sleep(5)
                
    elif suit == 'stripes':
        if not listofpoints:
            x = eightballpoint[0]
            y = eightballpoint[1]
            p,hx,hy = bestOption(x,y,holelocation,'above','left',listP,otherlistofpoints)
            dtb, dth = distanceFunc(cuepoint,p,hx,hy)
            hitBall(p,dtb,dth)
        else:
            for i in listofpoints:
                x = i[0]
                y = i[1]
                x1 = x-7
                x2 = x+7
                y1 = y-7
                y2 = y+7
                listP = listofpoints
                listP.remove(i)
                if cue[0] > x1 and cue[0] > x2:
                    if cue[1] > y1 and cue[1] > y2:
                        p,hx,hy = bestOption(x,y,holelocation,'above','left',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit striped ball.')
                        time.sleep(5)
                    elif cue[1] < y2 and cue[1] < y1:
                        p,hx,hy = bestOption(x,y,holelocation,'below','left',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit striped ball.')
                        time.sleep(5)
                    elif cue[1] > y1 and cue[1] < y2:
                        p,hx,hy = bestOption(x,y,holelocation,'middle','left',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        time.sleep(5)
                        
                elif cue[0] < x2 and cue[0] < x1:
                    if cue[1] > y1 and cue[1] > y2:
                        p,hx,hy = bestOption(x,y,holelocation,'above','right',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit striped ball.')
                        time.sleep(5)
                    elif cue[1] < y2 and cue[1] < y1:
                        p,hx,hy = bestOption(x,y,holelocation,'below','right',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit striped ball.')
                        time.sleep(5)
                    elif cue[1] > y1 and cue[1] < y2:
                        p,hx,hy = bestOption(x,y,holelocation,'middle','right',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit striped ball.')
                        time.sleep(5)

                elif cue[0] > x1 and cue[0] < x2:
                    if cue[1] > y1 and cue[1] > y2:
                        p,hx,hy = bestOption(x,y,holelocation,'above','middle',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit striped ball.')
                        time.sleep(5)
                    elif cue[1] < y2 and cue[1] < y1:
                        p,hx,hy = bestOption(x,y,holelocation,'below','middle',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit striped ball.')
                        time.sleep(5)
                    elif cue[1] > y1 and cue[1] < y2:
                        p,hx,hy = bestOption(x,y,holelocation,'middle','middle',listP,otherlistofpoints)
                        hitBall(cuepoint,p,hx,hy)
                        print('Hit striped ball.')
                        time.sleep(5)
    elif suit == None:
        if not listofpoints:
            x = eightballpoint[0]
            y = eightballpoint[1]
            p,hx,hy = bestOption(x,y,holelocation,'above','left',listP,otherlistofpoints)
            dtb, dth = distanceFunc(cuepoint,p,hx,hy)
            hitBall(p,dtb,dth)
        else:
            for i in listofpoints:
                    x = i[0]
                    y = i[1]
                    x1 = x-7
                    x2 = x+7
                    y1 = y-7
                    y2 = y+7
                    listP = listofpoints
                    listP.remove(i)
                    if cue[0] > x1 and cue[0] > x2:
                        if cue[1] > y1 and cue[1] > y2:
                            p,hx,hy = bestOption(x,y,holelocation,'above','left',listP,otherlistofpoints)
                            hitBall(cuepoint,p,hx,hy)
                            print('Hit ball.')
                            time.sleep(5)
                        elif cue[1] < y2 and cue[1] < y1:
                            p,hx,hy = bestOption(x,y,holelocation,'below','left',listP,otherlistofpoints)
                            hitBall(cuepoint,p,hx,hy)
                            print('Hit ball.')
                            time.sleep(5)
                        elif cue[1] > y1 and cue[1] < y2:
                            p,hx,hy = bestOption(x,y,holelocation,'middle','left',listP,otherlistofpoints)
                            hitBall(cuepoint,p,hx,hy)
                            print('Hit ball.')
                            time.sleep(5)
                            
                    elif cue[0] < x2 and cue[0] < x1:
                        if cue[1] > y1 and cue[1] > y2:
                            p,hx,hy = bestOption(x,y,holelocation,'above','right',listP,otherlistofpoints)
                            hitBall(cuepoint,p,hx,hy)
                            print('Hit ball.')
                            time.sleep(5)
                        elif cue[1] < y2 and cue[1] < y1:
                            p,hx,hy = bestOption(x,y,holelocation,'below','right',listP,otherlistofpoints)
                            hitBall(cuepoint,p,hx,hy)
                            print('Hit ball.')
                            time.sleep(5)
                        elif cue[1] > y1 and cue[1] < y2:
                            p,hx,hy = bestOption(x,y,holelocation,'middle','right',listP,otherlistofpoints)
                            hitBall(cuepoint,p,hx,hy)
                            print('Hit ball.')
                            time.sleep(5)

                    elif cue[0] > x1 and cue[0] < x2:
                        if cue[1] > y1 and cue[1] > y2:
                            p,hx,hy = bestOption(x,y,holelocation,'above','middle',listP,otherlistofpoints)
                            hitBall(cuepoint,p,hx,hy)
                            print('Hit ball.')
                            time.sleep(5)
                        elif cue[1] < y2 and cue[1] < y1:
                            p,hx,hy = bestOption(x,y,holelocation,'below','middle',listP,otherlistofpoints)
                            hitBall(cuepoint,p,hx,hy)
                            print('Hit ball.')
                            time.sleep(5)
                        elif cue[1] > y1 and cue[1] < y2:
                            p,hx,hy = bestOption(x,y,holelocation,'middle','middle',listP,otherlistofpoints)
                            hitBall(cuepoint,p,hx,hy)
                            print('Hit ball.')
                            time.sleep(5)

def hitBall(cue,ballpoint,holex,holey): #using the coordinates of cue and the ball to hit, hit ball
    dcuetoball = sqrt(((cue[0]-point[0])**2) + ((cue[1]-point[1])**2))
    dballtohole = sqrt(((point[0]-hx)**2) + ((point[1]-hy)**2))
    slope = (cue[1]-point[1]) / (cue[0]-point[0])
    
    if dballtohole < 50:
        if dcuetoball >  0 and dcuetoball < 50:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+((dcuetoball*1.2)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*(dcuetoball*1.2))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-((dcuetoball*1.2)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*1.2))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+((dcuetoball*1.2)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*1.2))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+((dcuetoball*1.2)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*1.2))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(dcuetoball*1.2))
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-(dcuetoball*1.2))
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  50 and dcuetoball < 200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+100)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-100)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
        
    elif dballtohole > 50 and dballtohole < 100:
        if dcuetoball >  0 and dcuetoball < 50:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+((dcuetoball*1.4)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*(dcuetoball*1.4))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-((dcuetoball*1.4)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*1.4))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+((dcuetoball*1.4)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*1.4))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+((dcuetoball*1.4)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*1.4))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(dcuetoball*1.4))
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-(dcuetoball*1.4))
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  50 and dcuetoball < 200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+100)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-100)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
    elif dballtohole > 100 and dballtohole < 150:
        if dcuetoball >  0 and dcuetoball < 50:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+((dcuetoball*1.6)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*(dcuetoball*1.6))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-((dcuetoball*1.6)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*1.6))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+((dcuetoball*1.6)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*1.6))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+((dcuetoball*1.6)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*1.6))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(dcuetoball*1.6))
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-(dcuetoball*1.6))
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  50 and dcuetoball < 200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+100)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-100)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
    elif dballtohole > 150 and dballtohole < 200:
        if dcuetoball >  0 and dcuetoball < 50:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+((dcuetoball*1.8)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*(dcuetoball*1.8))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-((dcuetoball*1.8)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*1.8))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+((dcuetoball*1.8)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*1.8))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+((dcuetoball*1.8)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*1.8))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(dcuetoball*1.8))
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-(dcuetoball*1.8))
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  50 and dcuetoball < 200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(110*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*110)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(110*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*110)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(110*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*110)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(110*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*110)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+110)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-110)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
    elif dballtohole > 250 and dballtohole < 300:
        if dcuetoball >  0 and dcuetoball < 50:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+((dcuetoball*2.5)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*(dcuetoball*2.5))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-((dcuetoball*2.5)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*2.5))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+((dcuetoball*2.5)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*2.5))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+((dcuetoball*2.5)*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*(dcuetoball*2.5))*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(dcuetoball*2.5))
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-(dcuetoball*2.5))
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  50 and dcuetoball < 200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+120)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-120)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
    elif dballtohole > 350 and dballtohole < 400:
        if dcuetoball >  0 and dcuetoball < 50:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+100)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-100)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  50 and dcuetoball < 200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+120)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-120)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                                  
    elif dballtohole > 450 and dballtohole < 500:
        if dcuetoball >  0 and dcuetoball < 50:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+100)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-100)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  50 and dcuetoball < 200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+120)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-120)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                                  
    elif dballtohole > 550 and dballtohole < 600:
        if dcuetoball >  0 and dcuetoball < 50:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(100*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*100)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+100)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-100)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  50 and dcuetoball < 200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(120*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*120)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+120)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-120)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
        elif dcuetoball >  200:
            if slope > 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]+((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                    
                else:
                    dragpointx = (ballpoint[0]-(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            elif slope < 0:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]+(140*sqrt(1 / (1+slope**2))))
                    dragpointy = (ballpoint[1]-((slope*140)*sqrt(1 / (1+slope**2))))
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
            else:
                if ballpoint[0] < cue[0]:
                    dragpointx = (ballpoint[0]+140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                else:
                    dragpointx = (ballpoint[0]-140)
                    dragpointy = ballpoint[1]
                    pyautogui.moveTo(ballpoint)
                    pyautogui.dragTo(dragpointx,dragpointy, button='left')
                    pyautogui.mouseUp(button='left')
                                  

def getGameRegion(check): #minimizes region that the program has to search for pictures on screen
    global GAME_REGION
    h,w = miniclipAPI() #accesses miniclips api to determine the height and width of game. used to test working with apis
    tries = 3
    while tries > 0: #there are 3 total tries to find the game region
        regiontries = 15 #within 3 tries, looks for each corner 15 times per try - not logged
        region2tries = 15 #within 3 tries, looks for each corner 15 times per try - logged in
        if tries == 3:
            pos = pyautogui.locateOnScreen(imagePath('alreadystarted.png'))
            if pos is None:
                pos = pyautogui.locateOnScreen(imagePath('alreadystarted.png'))
                if pos is None:
                    time.sleep(15)

        if check is False:
            time.sleep(1)
            #allowSearch() #searches for a popup that the webbrowser (chrome) asks
            print('Searching for game region..')
            region = pyautogui.locateOnScreen(imagePath('top_right_corner.png'))
            if region is not None: #searches for picture of corner of game region.
                ### gotten from tutorial
                topRightX = region[0] + region[2] #width
                topRightY = region[1] #height
                GAME_REGION = (topRightX - w, topRightY, w, h)
                print('Region acquired.' + str(GAME_REGION))
                break
            elif region is None:
                while regiontries > 0: #if it does no find the corner associated with not being logged in, it searches for one associated with being logged in
                    region = pyautogui.locateOnScreen(imagePath('top_right_corner.png'))
                    if region is None:
                        regiontries -= 1
                        print(regiontries)
                        
                    elif region is not None:
                        topRightX = region[0] + region[2]
                        topRightY = region[1]
                        GAME_REGION = (topRightX - w, topRightY, w, h)
                        print('Region acquired.' + str(GAME_REGION))
                        return
                    
        elif check is True:
            time.sleep(2)
            #allowSearch()
            time.sleep(2)
            popUpSearch() #checks for any advertisements from the game itself and x's out of them
            print('Searching for game region..')
            region2 = pyautogui.locateOnScreen(imagePath('top_right_corner_logged.png'))
            if region2 is not None:
                topRightX = region2[0] + region2[2]
                topRightY = region2[1]
                GAME_REGION = (topRightX - w, topRightY, w, h)
                print('Region acquired.' + str(GAME_REGION))
                #pyautogui.screenshot('testetere.png', region=GAME_REGION)
                break
            elif region2 is None:
                while region2tries > 0:
                    region2 = pyautogui.locateOnScreen(imagePath('top_right_corner_logged.png'))
                    if region2 is None:
                        region2tries -=1
                        print(region2tries)
                    elif region2 is not None:
                        topRightX = region2[0] + region2[2]
                        topRightY = region2[1]
                        GAME_REGION = (topRightX - w, topRightY, w, h)
                        print('Region acquired.' + str(GAME_REGION))
                        return 
        if tries > 0:
            tries -= 1
            print(str(tries) + ' official tries left.')
            region2tries = 15
                   
    if tries == 0: # because it can try for a combined total of 45 times, making sure there are no pop ups, exits the program if it cannot find the region
        print('Tried finding region 3 times and found none. Exiting bot.')
        sys.exit()

def loginCheck(): #checks for a variety of login possiblities. if logged into a certain account or not logged in at all, login check is passed
    loginattempts = 3
    pos = pyautogui.locateCenterOnScreen(imagePath('url.png'))
    if pos is None: #checks to make sure you are on right website
        webbrowser.open(url)
    else:
        pass
    
    pos = pyautogui.locateCenterOnScreen(imagePath('flash1.png'))
    if pos is None:
        pass
    else:
        pyautogui.click(pos)
        time.sleep(1)
        pos = pyautogui.locateCenterOnScreen(imagePath('flash2.png'))
        if pos is None:
            pass
        else:
            pyautogui.click(pos)
            time.sleep(1)
        
    pos = pyautogui.locateCenterOnScreen(imagePath('8ballrobotguy.png'))
    if pos is not None: #checks to see if you are logged into default account
        print('Login Check passed.')
        return 'loggedintobot'
    else:
        while True:
            pos = pyautogui.locateCenterOnScreen(imagePath('loading100.png'))
            if pos is not None: #waits until game is loaded until beginning further checks
                break
        pos = pyautogui.locateCenterOnScreen(imagePath('liar.png'))
        if pos is None: # checks to see if there is possibility to login or not
            pos = pyautogui.locateCenterOnScreen(imagePath('url.png'))
            if pos is None: # checks to see if you are on the website, if not, opens url and checks again.
                webbrowser.open(url)
                time.sleep(3)
                check5 = loginCheck()
                if check5 == 'loggedintobot':
                    return 'loggedintobot'
                elif check5 == 'notlogged':
                    return 'notlogged'
                else:
                    return 'failed'
                
            elif pos is not None: # if on the website, but cannot find the login/sign in button, makes assumption that you are logged in
                while loginattempts > 0:
                    print('You are logged into a non-bot account. Please log out, close the tab, and try again. ' \
                      + str(loginattempts) + ' log in attempts left.')
                    canlog = input('Have you logged out? ')
                    canlog.replace(' ', '')
                    if canlog.lower() in yeswords:
                        refreshPage()
                        time.sleep(5)
                        pos = pyautogui.locateCenterOnScreen(imagePath('liar.png'))
                        if pos is None: #refreshes page and checks for login/sign in button again after receiving input that the user logged out
                            pos = pyautogui.locateCenterOnScreen(imagePath('8ballrobotguy.png'))
                            if pos is None: #checks for default account in case user has lied in attempt to bypass
                                loginattempts -= 1
                                print('You haven\'t logged out. '+str(loginattempts)+' attempt(s) left.')
                            else:
                                return 'loggedintorobot'
                        else:
                            return 'notlogged'
                    elif canlog.lower() in nowords:
                        quit8 = input('Would you like to quit? ')
                        quit8.replace(' ', '')
                        if quit8.lower() in yeswords:
                            print('Turning off 8 ball bot.')
                        elif quit8.lower() in nowords:
                            print('Waiting.')
                            time.sleep(10)
                            loginCheck()
                        else:
                            print('Take that as a \'yes\'.')
                    else:
                        print('Take that as a \'no\',.')
        elif pos is not None and loginattempts > 0:
            return 'notlogged'
        elif pos is not None and loginattempts == 0:
            return 'notloggedbutnotry'
        elif pos is None and loginattempts == 0:
            print('No login attempts left. Please try again later.')
            return 'notries'
        else:
            return 'failed'

def refreshPage(): # refreshes the web page
    pos = pyautogui.locateCenterOnScreen(imagePath('urlbar.png'))
    if pos is None:
        pos = pyautogui.locateCenterOnScreen(imagePath('unsecure.png'))
        pyautogui.moveTo(pos)
        pyautogui.moveRel(100,None)
        pyautogui.click(clicks = 3, duration=0.50)
        pyautogui.typewrite('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
        pyautogui.press('enter')
    else:
        pyautogui.moveTo(pos)
        pyautogui.moveRel(100,None)
        pyautogui.click(clicks = 3, duration=0.50)
        pyautogui.typewrite('https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/')
        pyautogui.press('enter')

def popUpSearch(): # searches for popups in game, such as ads
    xtries = 5
    print('Searching for popup...')
    while xtries > 0:
        pos = pyautogui.locateCenterOnScreen(imagePath('preregionx_button.png'))
        if pos is None:
            xtries -= 1
            #print(xtries)
        elif pos is not None:
            pyautogui.click(pos,duration=0.25)
            break
    if xtries == 0:
            print('No popup to close. Searched screen 5 times.')

def allowSearch(): # searches for a popup that chrome asks
    allowtries = 5
    while allowtries > 0:
        pos = pyautogui.locateCenterOnScreen(imagePath('allow.png'))
        if pos is not None:
            pyautogui.click(pos,duration=0.25)
            break
        else:
            allowtries -= 1

def logIn(user='pefumewora@fxprix.com',password='thisisapassword1'): #enters in email and password, has defaults if user provides no input
    pos = pyautogui.locateCenterOnScreen(imagePath('email_area.png'), region=GAME_REGION)
    pyautogui.click(pos,duration=0.25)
    time.sleep(1)
    pos = pyautogui.typewrite(user)
    time.sleep(1)
    pos = pyautogui.locateCenterOnScreen(imagePath('password_area.png'), region=GAME_REGION)
    pyautogui.click(pos,duration=0.25)
    time.sleep(1)
    pos = pyautogui.typewrite(password)
    time.sleep(1)
    pos = pyautogui.locateCenterOnScreen(imagePath('login3_button.png'), region=GAME_REGION)
    pyautogui.click(pos,duration=0.25)
    time.sleep(6)
    navigateGameMenu()

def collectCoins(position): #clicks the collect coins button
    pyautogui.click(position,duration=0.25)

def spinWin(position): #spins the spin and win game machine thing
    pyautogui.click(position, duration=0.25)
    time.sleep(1)
    pos = pyautogui.locateCenterOnScreen(imagePath('8ballspin_button.png'), region=GAME_REGION)
    pyautogui.moveTo(pos)
    pyautogui.mouseDown(button='left')
    pyautogui.moveRel(None,250)
    pyautogui.mouseUp(button='left')
    time.sleep(7)
    pos = pyautogui.locateCenterOnScreen(imagePath('8ballwinx.png'), region=GAME_REGION)
    pyautogui.click(pos,duration=0.25)
    time.sleep(2)
    pos = pyautogui.locateCenterOnScreen(imagePath('spunx.png'), region=GAME_REGION)
    pyautogui.click(pos,duration=0.25)

def collectCoinsCycle(): #cycle for checking if the bot needs to collect coins
    timescollected = 0
    getGameRegion(True)
    while True:
        pos = pyautogui.locateCenterOnScreen(imagePath('collectcoins.png'), region=GAME_REGION)
        if pos is not None:
            timescollected =+ 1
            collectCoins(pos)
            print('Collected 50 coins, ' + timescollected + ' times.')
        else:
            print('Searching again in 10 minutes.')
            time.sleep(600)

def turnCycle(counter): #checks for turn, if it is not bots turn, keeps searching until it is turn.
    while True:
        turn1 = checkTurn()
        if turn1 is True:
            counter += 1
            print('Bot\'s turn.')
            return counter
        else:
            time.sleep(1)

def checkTurn(): #searches for an image on screen for the turn cycle
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

def maskDict(list1,list2): #creates dictionary of ball colors and masks
    balls = {}
    for i in range(len(list1)):
        key = list1[i]
        value = list2[i]
        balls[key] = value
    return balls

def moveMouseOut(cueball): #moves ball tracer out of the way as much as possible. checks for empty areas
    if cueball[0] > 84 and cueball[0] < 228:
        if cueball[1] > 277:
            pos = pyautogui.locateCenterOnScreen(imagePath('topleftholeclear.png'), region=GAME_REGION)
            if pos is not None:
                pyautogui.moveTo(pos)
            else:
                pos = pyautogui.locateCenterOnScreen(imagePath('toprail.png'), region=GAME_REGION)
                if pos is not None:
                    pyautogui.moveTo(pos)
                else:
                    pos = pyautogui.locateCenterOnScreen(imagePath('leftrail.png'), region=GAME_REGION)
                    if pos is not None:
                        pyautogui.moveTo(pos)
                    else:
                        pos = pyautogui.locateCenterOnScreen(imagePath('bottomrail.png'), region=GAME_REGION)
                        if pos is not None:
                            pyautogui.moveTo(pos)
                        else:
                            pyautogui.moveTo(271,103)
        else:
            pos = pyautogui.locateCenterOnScreen(imagePath('bottomleftholeclear.png'), region=GAME_REGION)
            if pos is not None:
                pyautogui.moveTo(pos)
            else:
                pos = pyautogui.locateCenterOnScreen(imagePath('bottomrail.png'), region=GAME_REGION)
                if pos is not None:
                    pyautogui.moveTo(pos)
                else:
                    pos = pyautogui.locateCenterOnScreen(imagePath('leftrail.png'), region=GAME_REGION)
                    if pos is not None:
                        pyautogui.moveTo(pos)
                    else:
                        pos = pyautogui.locateCenterOnScreen(imagePath('toprail.png'), region=GAME_REGION)
                        if pos is not None:
                            pyautogui.moveTo(pos)
                        else:
                            pyautogui.moveTo(271,450)
    elif cueball[0] > 228 and cueball[0] < 522:
        if cueball[1] > 277:
            pos = pyautogui.locateCenterOnScreen(imagePath('topmidholeclear.png'), region=GAME_REGION)
            if pos is not None:
                pyautogui.moveTo(pos)
            else:
                pos = pyautogui.locateCenterOnScreen(imagePath('toprail.png'), region=GAME_REGION)
                if pos is not None:
                    pyautogui.moveTo(pos)
                else:
                    pos = pyautogui.locateCenterOnScreen(imagePath('bottomrail.png'), region=GAME_REGION)
                    if pos is not None:
                        pyautogui.moveTo(pos)
                    else:
                        pyautogui.moveTo(271,103)
        else:
            pos = pyautogui.locateCenterOnScreen(imagePath('bottommidholeclear.png'), region=GAME_REGION)
            if pos is not None:
                pyautogui.moveTo(pos)
            else:
                pos = pyautogui.locateCenterOnScreen(imagePath('bottomrail.png'), region=GAME_REGION)
                if pos is not None:
                    pyautogui.moveTo(pos)
                else:
                    pos = pyautogui.locateCenterOnScreen(imagePath('toprail.png'), region=GAME_REGION)
                    if pos is not None:
                        pyautogui.moveTo(pos)
                    else:
                        pyautogui.moveTo(271,450)
    elif cueball[0] > 522 and cueball[0] < 664:
        if cueball[1] > 277:
            pos = pyautogui.locateCenterOnScreen(imagePath('toprightholeclear.png'), region=GAME_REGION)
            if pos is not None:
                pyautogui.moveTo(pos)
            else:
                pos = pyautogui.locateCenterOnScreen(imagePath('toprail.png'), region=GAME_REGION)
                if pos is not None:
                    pyautogui.moveTo(pos)
                else:
                    pos = pyautogui.locateCenterOnScreen(imagePath('rightrail.png'), region=GAME_REGION)
                    if pos is not None:
                        pyautogui.moveTo(pos)
                    else:
                        pos = pyautogui.locateCenterOnScreen(imagePath('bottomrail.png'), region=GAME_REGION)
                        if pos is not None:
                            pyautogui.moveTo(pos)
                        else:
                            pyautogui.moveTo(493,103)
        else:
            pos = pyautogui.locateCenterOnScreen(imagePath('bottomrightholeclear.png'), region=GAME_REGION)
            if pos is not None:
                pyautogui.moveTo(pos)
            else:
                pos = pyautogui.locateCenterOnScreen(imagePath('bottomrail.png'), region=GAME_REGION)
                if pos is not None:
                    pyautogui.moveTo(pos)
                else:
                    pos = pyautogui.locateCenterOnScreen(imagePath('rightrail.png'), region=GAME_REGION)
                    if pos is not None:
                        pyautogui.moveTo(pos)
                    else:
                        pos = pyautogui.locateCenterOnScreen(imagePath('toprail.png'), region=GAME_REGION)
                        if pos is not None:
                            pyautogui.moveTo(pos)
                        else:
                            pyautogui.moveTo(493,450)

def resolution(): # determines resolution of screen. used for testing
    #thought resolution matter for pictures, doesnt. tried at various resolutions
    w = str(GetSystemMetrics(0))
    return w

def gameWindow(): #not needed, used for testing purposes. from tutorial
    x_pad = 584
    y_pad = 129
    window = (x_pad+1,y_pad+1,x_pad+750,y_pad+603)
    im = ImageGrab.grab(window)
    im.save(os.getcwd() + '\\snapshotingamead' + '.png', 'PNG')

def imagePath(filename): #gets the path of the images in the folder
    return os.path.join('images',filename)

def miniclipAPI(): # accesses miniclip api to get width and height of game. gotten from tutorial
    api_token = '8ball_token'
    api_url_base = 'https://webmasters.miniclip.com/api/' #dont need headers or token for miniclip api
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(api_token)}

    api_url = '{0}/games/2471/en.json'.format(api_url_base)

    try:
        response = requests.get(api_url, headers=headers)
    except requests.exceptions.ConnectionError:
        requests.status_code = 'Connection refused'
        for i in range(1,5):
            time.sleep(1)
            response = requests.get(api_url, headers=headers)
            miniclipAPI()
        

    if response.status_code == 200:
        response2 = json.loads(response.content.decode('utf-8'))
        data = json.dumps(response2)
        #could probs do this better
        for ch in ['"','\'','{','}']:
            if ch in data:
                data = data.replace(ch,'')
        e = data.split(',')
        f = e[3].split(' ')
        g = e[4].split(' ')
        h = int(f[2])
        w = int(g[2])
        return h,w
    else:
        return None

def main():
    global url, url2, yeswords, nowords, w, coinmode
    url = 'https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/'
    url2 = 'https://www.youtube.com/watch?v=Vj7G35H-Q-g'
    yeswords = ['yes', 'ye', 'y', 'ys', 'ues', 'yed']
    nowords = ['no', 'n', 'mo', 'mno', 'bno', 'bo']
    coinmode = ['coins', 'coinmode', 'collect', 'collectcoins', 'collectcoin', 'coin']
    #open8ballbot()
    #poolGame()
    suit = 'nosuit'
    count = '1'
    gamenum = '70'
    listofb = ['cue','eightball','yellow','blue','lightred','purple','orange','green','darkred']
    mask, maskimage = maskSetup(r'C:\Users\Grant\AppData\Local\Programs\Python\Projects\games\game70\table\pooltable1.png',['cue','eightball','yellow','blue','lightred','purple','orange','green','darkred'])
    markballs = maskDict(listofb,mask)
    points, c, eight, suit, otherpoints = outlineBall(maskimage,suit,markballs,count,gamenum)

if __name__ == "__main__":
    main()
