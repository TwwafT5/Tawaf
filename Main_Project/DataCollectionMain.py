import camera as wM
import DataCollectionModule as dcM
from motorModule import Motor
import controller as cr
import cv2
import camera as cam
from time import sleep
import controller as cr


motor= Motor(21,20,16,19,13,26)




record = 0
while True:
    joyVal = cr.getJS()
    steering = joyVal['axis1']
    throttle = joyVal['axis2']
    if joyVal['x'] == 1: # Press x to start recrding
        if record ==0: print('Recording Started ...')
        record +=1

    if record == 1:
        img = wM.getImg(show=True)
        dcM.saveData(img,steering,throttle)
    elif record == 2:
        cv2.destroyAllWindows() 
        dcM.saveLog()
        record = 0
    
    motor.move(-throttle,steering)
    cv2.waitKey(1)