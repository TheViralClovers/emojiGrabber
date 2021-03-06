import pyperclip #this is a clipboard works on both windows and linux
import string 
import random
import time
import os
import requests
from PIL import Image
from colorama import Fore, Back, Style, init

init(convert=True) #I used this so that colored output occurs

recentValue = "" #initialising recentvalue to blank for now --> stores clipboard data soon
home = ""  # linux and mac have the env variable HOME instead of USERPROFILE, this will point to the home directory

platform = os.name #this helps us to identify the platform thats running (i.e windows or linux)

if platform == "nt":
    home = os.environ.get("USERPROFILE") 

else:
    home = os.environ.get("HOME")

# to create the directory if it doesn't already exist
def directorycheck():
    destination = os.path.join(home, "Desktop", "Discord emojis")
    if not (os.path.isdir(destination)):
        os.mkdir(destination)


directorycheck()

# to get the value from the clipboard
def getClipboard():
    return pyperclip.paste()


# to get a random name for the file
def getRandomFileName():
    fileDestList = []  # created this list so that i can pass both the file destination and file name in the return statement
    letters = string.ascii_lowercase  # this is actually a string of all the lowercase letters
    fileName = "".join((random.choice(letters)) for i in range(8)) #this generates a random 8 lettered word for the filename
    destination = os.path.join(home, "Desktop", "Discord emojis", fileName + ".png") #where the file should be saved,(a folder called Discord Emojis in discord)
    fileDestList.append(fileName)
    fileDestList.append(destination)
    return fileDestList #if i hadnt passed the filename and destination as a list, then the random function would generate different values for both


# to write the file we obtain from the clipboardData
def createResizedImage():
    fileName = getRandomFileName()[0]
    destination = getRandomFileName()[1]
    try:
        r = requests.get(getClipboard()) #this sends a request to grab the emoji from the URl
        with open(destination, "wb") as f:
            f.write(r.content) #this creates the image
        image = Image.open(destination)  # I have combined the function that downloads the image and resizes the image because due to getRandomFileName, it would change value as soon as its called a second time
        image = image.resize((48, 48), Image.ANTIALIAS) #this resizes the image to 48x48 (standard discord emoji size)
        image.save(destination) #this replaces the original image with the 48x48 image
        status = "Image processing done"
    except:
        print(Fore.RED + "lmao, try copying an image url next time") #if the copied text is not an URL, requests module will raise an error, to prevent that i have included this
        status = "Image processing Failed"

    return status

while True: #this makes sure that the program keeps downloading the images as soon as a new one is copied instead of exiting the program as soon as one emoji is copied
    if recentValue != getClipboard():  # this is to check if some new link has been copied
        recentValue = getClipboard() 
        if "discord" in recentValue and "png" in recentValue:  # This makes sure, that the code is run only when a discord emoji link is copied and not everytie the clipboard changes value lol
            getRandomFileName()
            status = createResizedImage()
            if "failed" in status:
                print(Fore.RED + status)
            else:
                print(Fore.GREEN + status)
    time.sleep(0.4)  # if this statement wasnt included, the program would consume all of the CPUs memeory, so the while statement now happens once every 0.4s
