import controller as cr
import camera as cam
import cv2
import numpy as np
from motorModule import Motor

def preprocess_image(img):
    img = cv2.GaussianBlur(img,  (5, 7), 5)
    img = cv2.bitwise_not(img)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, -10)
    img = img / 255.0 
    return np.expand_dims(img, axis=0)

def manual_drv(motor):
    manual_drv = True
    while manual_drv:
            jsVal = cr.getJS()
            img = cam.getImg(show=True)
            img_m = preprocess_image(img)
            motor.move(-(jsVal['axis2']), jsVal['axis1'])
            
            if jsVal['t'] == 1:
                manual_drv = False
                cv2.destroyAllWindows()
                break


def to_sai(motor,model_obj, model, main_mission):
    taw_detected = False
    while taw_detected == False:
        img_r = cam.getImg()
        img_m = preprocess_image(img_r)
        steering, throttle = model.predict(img_m)
        motor.move(-(throttle[0][0]), steering[0][0], op=main_mission)
        _, taw_detected, dest = model_obj.predict(img_r, 'taw', 0.80)
        if taw_detected == True:
            motor.to_sai()

def main():
    motor= Motor(21,20,16,19,13,26)
    manual_drv(motor)
    
 
if __name__ == '__main__':
    main()
            

