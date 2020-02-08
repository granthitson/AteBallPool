import os
import sys
import time
import pyautogui
import tkinter as tk

import constants


class StdoutRedirector():
    def __init__(self, text):
        self.output = text

    def write(self, string):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, string)
        self.output.configure(state=tk.DISABLED)
        self.output.see(tk.END)

    def flush(self):
        sys.__stdout__.flush()


def imagePath(filename):
    return os.path.join("images", filename)


def imageSearch(image, region=None, confidence=.99):
    if type(image) == list:
        for i in image:
            if region is None:
                pos = pyautogui.locateCenterOnScreen(imagePath(i), confidence=confidence)
                if pos is not None:
                    return pos
            else:
                pos = pyautogui.locateCenterOnScreen(imagePath(i), region=region, confidence=confidence)
                if pos is not None:
                    return pos
    else:
        if region is None:
            pos = pyautogui.locateCenterOnScreen(imagePath(image), confidence=confidence)
            return pos
        else:
            pos = pyautogui.locateCenterOnScreen(imagePath(image), region=region, confidence=confidence)
            return pos


def debugPrint(string):
    if constants.debug is True:
        print("DEBUG -- " + str(string))


def urlSearch():
    check = imageSearch([constants.img_url, constants.img_url2, constants.img_url3])
    if check is not None:
        debugPrint("URL present.")
        return True
    else:
        debugPrint("URL not present.")
        return False


def CheckForUrl(r, redirect = None):
    #debugPrint("Checking for URL...")
    stdoutRedirect(redirect)
    print("Checking for URL...")
    r += 1
    for i in range(1, r + 1):
        urlBool = urlSearch()
        if urlBool is False:
            #debugPrint("Attempts: " + str(r - i))
            print("Attempts: " + str(r - i))
            #time.sleep(.05)
        else:
            print("URL acquired.")
            pyautogui.screenshot("screenshot.jpg")
            return True
    #debugPrint("Failed to find URL...")
    print(("Failed to find URL..."))
    return False


def timedInput(string, t=10, choices=None):
    print(string)
    if choices is None:
        choices = ["yes", "no"]
    try:
        for i in range(0, t):
            time.sleep(1)
        print("Waited {} seconds for a response.".format(t))
        return False
    except KeyboardInterrupt:
        for i in range(0, 5):
            answer = input("\"{}\" or \"{}\"".format(choices[0], choices[1]) + ": ")
            if answer == choices[0]:
                return True
            if answer == choices[1]:
                return False
        return False

def stdoutRedirect(redirect = None):
    if redirect != None:
        sys.stdout = redirect