import pandas as pd
import os
import cv2
from camera import *
from datetime import datetime

global imgList, steeringList
countFolder = 0
count = 0
imgList = []
steeringList = []
throttleList = []

#GET CURRENT DIRECTORY PATH
myDirectory = os.path.join(os.getcwd(), 'data')
# print(myDirectory)

# CREATE A NEW FOLDER BASED ON THE PREVIOUS FOLDER COUNT
while os.path.exists(os.path.join(myDirectory,f'ROUND{str(countFolder)}')):
        countFolder += 1
newPath = myDirectory +"/ROUND"+str(countFolder)
os.makedirs(newPath)

# SAVE IMAGES IN THE FOLDER
def saveData(img,steering, throttle):
    global imgList, steeringList
    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).replace('.', '')
    #print("timestamp =", timestamp)
    fileName = os.path.join(newPath,f'Image_{timestamp}.jpg')
    cv2.imwrite(fileName, img)
    imgList.append(fileName)
    steeringList.append(steering)
    throttleList.append(throttle)

# SAVE LOG FILE WHEN THE SESSION ENDS
def saveLog():
    global imgList, steeringList
    rawData = {'Image': imgList,
                'Steering': steeringList,
               'throttle':throttleList}
    df = pd.DataFrame(rawData)
    df.to_csv(os.path.join(myDirectory,f'log_{str(countFolder)}.csv'), index=False, header=False)
    print(f'Log Saved, ROUND: {countFolder}')
    print('Total Images: ',len(imgList))

if __name__ == '__main__':
    MAX_DISTANCE, cam = init()
    for i in range(10):
        img = getImg(MAX_DISTANCE, cam, True)
        saveData(img,1)
    saveLog()
