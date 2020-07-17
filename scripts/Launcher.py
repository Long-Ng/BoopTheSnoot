from cv2 import cv2
import numpy as np
import time
import os
import pyglet
import random
import winsound

drumrolling = False
idle = True
show = False
still = True
preshow = False
mousex = -1
mousey = -1
directory = (os.path.dirname(os.getcwd()) + "\\img")


def idleScreenMouse(event,x,y,flags,param):
    global idle,still,show,t,t0,t1,mousex,mousey,drumrolling
    if(event == cv2.EVENT_LBUTTONDOWN and idle == True):
        idle = False
        print("Show Ready Screen")
    elif(event == cv2.EVENT_LBUTTONDOWN and show == True):
        print("resetting")
        show = False
        drumrolling = False
        t0 = 0
        t1 = 0
        t = 0 
    elif(event == cv2.EVENT_RBUTTONDOWN and idle == True):
        print("Show instruction screen")
        cv2.imshow("Left Click After The Image Shown To Continue",cv2.imread(directory + "\\" + "Instruction.png"))
    if(event == cv2.EVENT_MOUSEMOVE and idle == False and show == False):
        still = False
    mousex = x
    mousey = y

if __name__ == "__main__":
    #set up window
    cv2.namedWindow("Left Click After The Image Shown To Continue")
    cv2.imshow("Left Click After The Image Shown To Continue",cv2.imread(directory + "\\" + "Click to Start.png"))
    cv2.setMouseCallback("Left Click After The Image Shown To Continue",idleScreenMouse)
    #set up database
    snoot_txt = open("snoot.txt","r")
    squares2snoot = {}
    for line in snoot_txt:
        square,images = line.replace(" ","").rstrip("\n").replace("'",'').split(":")
        images = images.split(",")
        squares2snoot[square] = images
        print(squares2snoot[square])
        squares2snoot[square].remove("")
    print(squares2snoot)

    t0 = 0
    t1 = 0
    t = 0 
    while(1):
        if(idle == True):
            print("In idle")
        elif(idle == False):
            if(still == False):
                t1 = time.time()
                t= t1-t0
                t0 = time.time()
            elif(still == True):
                t1 = time.time()
                t= t1-t0
            if(t<0.5 and show == False):
                cv2.imshow("Left Click After The Image Shown To Continue",cv2.imread(directory + "\\" + "Ready.png"))
                print(1+(mousex//50)+20*(mousey//50))
                #winsound.PlaySound(None,winsound.SND_ASYNC|winsound.SND_ALIAS)                     
            elif ((t>0.5 and t < 1.25) and show == False):
                #winsound.PlaySound("E:\\Hobbies Project\\Ongoing Programming Project\\Boop Snoot without AI\\sfxc\\drum.wav",winsound.SND_ASYNC|winsound.SND_ALIAS)                
                cv2.imshow("Left Click After The Image Shown To Continue",cv2.imread(directory + "\\" + "Waiting.png"))
                print(1+(mousex//50)+20*(mousey//50))
                still = True
            elif (still == True and drumrolling == False):
                winsound.PlaySound(os.path.dirname(os.getcwd()) + "\\sfx\\drumwav.wav",winsound.SND_ASYNC|winsound.SND_ALIAS)   
                drumrolling = True    
            elif (t>1.25 and t<50000 and show == False):
                #print("show snoot")
                #Mega code goes here
                winsound.PlaySound(os.path.dirname(os.getcwd()) + "\\sfx\\crashwav.wav",winsound.SND_ASYNC|winsound.SND_ALIAS)   
                print(1+(mousex//50)+20*(mousey//50))
                currentsquare = (1+(mousex//50)+20*(mousey//50))
                print(len(squares2snoot[str(currentsquare)]))
                print(str(random.choice(squares2snoot[str(currentsquare)])))
                if(len(squares2snoot[str(currentsquare)])>0):
                    cv2.imshow("Left Click After The Image Shown To Continue",cv2.imread(directory + "\\" +str(random.choice(squares2snoot[str(currentsquare)]))))
                else:
                    print("No img found")
                    cv2.imshow("Left Click After The Image Shown To Continue", cv2.imread(directory + "\\" + "NoImg.png"))
                show = True
            still = True


        if(cv2.waitKey(1) == 27):
            break
    #See you next time window
    cv2.imshow("Left Click After The Image Shown To Continue",cv2.imread(directory + "\\" + "End.png"))
    winsound.PlaySound(os.path.dirname(os.getcwd()) + "\\sfx\\cyntwav.wav",winsound.SND_ASYNC|winsound.SND_ALIAS)
    if(cv2.waitKey(3000) == 27):
        cv2.destroyAllWindows



    # if(cv2.waitKey() == 27):
    #     cv2.destroyAllWindows