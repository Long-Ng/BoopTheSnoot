from cv2 import cv2
import numpy as np
import os


squares ={}
def coordinates2squares():
    counter = 1
    for height in range(0,1000,50):
        for width in range(0,1000,50):
            squares[counter] = str(width)+","+str(height)+","+str(width+50)+","+str(height+50)
            counter +=1

def mousepos2squares(event,x,y,int,param):
    if(event == cv2.EVENT_MOUSEMOVE):
        return((1+(x//50)+20*(y//50)))

def mousesegmentation(event,x,y,flags,param):
    global img,squares,tempSquareList
    currentsquare = (1+(x//50)+20*(y//50))
    if(event == cv2.EVENT_LBUTTONDOWN):
        if(not(currentsquare in tempSquareList)):
            tempSquareList.append(currentsquare)
            print("Square " + str(currentsquare)+ " is selected")
            lx,ly,hx,hy = ((squares[currentsquare]).split(","))
            cv2.rectangle(img,(int(lx),int(ly)),(int(hx),int(hy)),(255,255,0),3)
            cv2.imshow("GridClassifier",img)
    elif(event == cv2.EVENT_RBUTTONDOWN):
        if(currentsquare in tempSquareList):
            tempSquareList.remove(currentsquare)
            print("Square " + str(currentsquare)+ " is de-selected")
            lx,ly,hx,hy = ((squares[currentsquare]).split(","))
            cv2.rectangle(img,(int(lx),int(ly)),(int(hx),int(hy)),(0,0,255),3)
        else:
            print("Square is not in list")
    cv2.imshow("GridClassifier",img)
    return tempSquareList





            
def drawgrid(img):
    for width in range(0,1000,50):
        cv2.line(img,(width,0),(width,1000),(255,0,0),1)
    for height in range(0,1000,50):
        cv2.line(img,(0,height),(1000,height),(255,0,0),1)    
    



if __name__ == "__main__":
    #Set up notepad file and image folder
    snoot_txt = open("snoot.txt",'r')
    #implement anti dupes here
    dupesCheckList = []
    squares2snoot = {}
    for line in snoot_txt:
        square,images = line.replace(" ","").rstrip("\n").replace("'",'').split(":")
        images = images.split(",")
        squares2snoot[square] = images
        dupesCheckList += squares2snoot[square]
    print(squares2snoot)
    dupesCheckList = set(dupesCheckList)
    print(dupesCheckList)
    snoot_txt.close()
    coordinates2squares()
    directory = (os.path.dirname(os.getcwd()) + "\\img")
    counter = 0
    for filename in os.listdir(directory):
        counter +=1
        print(str(counter) + " out of " + str(len((os.listdir(directory)))))
        cv2.namedWindow("GridClassifier",cv2.WINDOW_AUTOSIZE)
        img = cv2.imread(directory + "\\" +filename)
        drawgrid(img)
        tempSquareList = []
        (cv2.setMouseCallback("GridClassifier",mousesegmentation))

        if(filename in dupesCheckList):
            print("image is classified already, skipping")
            continue
        elif(cv2.waitKey()==ord('a')):
            if(len(tempSquareList) == 0):
                print("No square logged, skipping image")
                if(not(filename in squares2snoot['-1'])):
                    squares2snoot['-1'].append(filename)
            else:
                print("Squares logged, next image")
                print(tempSquareList)
                for each in tempSquareList:
                    if(str(each) in squares2snoot):
                        print("square exists in database")
                        if(not(filename in squares2snoot[str(each)])):
                            print("before append:")
                            print((squares2snoot[str(each)]))
                            squares2snoot[str(each)].append(filename)
                            print("after append:")
                            print((squares2snoot[str(each)]))
        elif(cv2.waitKey()==ord('d')):
            continue
        elif(cv2.waitKey()==ord('s')):
            print("quit")
            break 
            #change image name here
            #os.rename(directory + "\\" + filename,directory + "\\" + "DONE" + filename)
    #write to file
    cv2.setMouseCallback("GridClassifier", lambda *args : None)
    cv2.imshow("GridClassifier",cv2.imread(directory + "\\" + "folderEmpty.png"))
    snoot_txt = open("snoot.txt",'w')
    for each in squares2snoot:
        snoot_txt.write(str(each) + ":" + str(squares2snoot[each]).strip('[]') + "\n")
    snoot_txt.close()
    print("folder is empty, press escape to quit")
    if (cv2.waitKey()==27):   
        cv2.destroyAllWindows()

