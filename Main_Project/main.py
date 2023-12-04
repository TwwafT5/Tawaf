from motorModule import Motor
import controller as cr
import cv2
from utils import *
import camera as cam
import numpy as np
from tensorflow.keras.models import load_model
import model_utils as model
from obj_model import Obj_model
from time import sleep
import tkinter as tk
from threading import Thread


motor = Motor(21, 20, 16, 19, 13, 26)
lblpath = 'labelmap.txt'
min_conf = 0.5
modelpath = 'detect.tflite'
model = load_model('/home/pi/selfDriving_wheelchair/23Nov959.h5')
model_obj = Obj_model(modelpath, lblpath, min_conf)


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Self-Driving Wheelchair Interface")

        self.counter_label = tk.Label(master, text="Counter: 0", font=("Arial", 16))
        self.counter_label.pack(pady=20)

        self.start_button = tk.Button(master, text="Start", command=self.start_processing)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_processing)
        self.stop_button.pack()
        self.i = 0
        self.counter = 0
        self.processing = False
        self.usr_req = None
        self.det = False
        self.main_mission = 'taw'
        self.det_for_count = False
        self.loc = True
        self.dest = None
        self.go_to = False

    def update_counter_label(self):
        self.counter_label.config(text=f"Counter: {self.counter}")

    def process_data(self):
        while self.processing:
            jsVal = cr.getJS()
            if jsVal['t'] == 1:
                self.usr_req = 'wtr'
            elif jsVal['o'] == 1:
                self.usr_req = 'zam'

            
            elif self.counter == 4 and self.main_mission == 'taw':
                to_sai(motor, model_obj, model,self.main_mission)
                self.main_mission = 'sai'
                self.counter = 0
                self.update_counter_label()
                


                
            

            img_r = cam.getImg()
            img_m = preprocess_image(img_r)
            steering, throttle = model.predict(img_m)
            motor.move(-(throttle[0][0]), steering[0][0], op=self.main_mission)
            _, self.det_for_count, self.dest = model_obj.predict(img_r, self.main_mission, 0.8)
            if self.usr_req is not None and self.det == False:
                self.det = True
                img_obj, self.det, self.dest = model_obj.predict(img_r, self.usr_req, 0.7)
                

            if self.det_for_count == True and self.loc==False:
                self.counter += 1
                self.update_counter_label()
                self.det_for_count = False
                self.loc = True
            
            if self.loc==True:
                self.i+=1
                if self.i >=20:
                    self.i=0
                    self.loc = False

            if self.usr_req == 'sai' and self.counter == 4:
                print('Sai completed!')
                motor.stop()
                self.stop_processing()
                break

            print('Rounds: ', self.counter, 'distance:', self.dest)

            if self.usr_req == 'wtr' and self.det == True:
                motor.park()
                self.det = False
                self.usr_req = None

            elif self.usr_req == 'zam' and self.det == True:
                motor.park()
                self.det = False
                self.usr_req = None

            # Adjust the sleep time based on your requirements

    def start_processing(self):
        if not self.processing:
            self.processing = True
            self.update_counter_label()
            Thread(target=self.process_data).start()

    def stop_processing(self):
        self.processing = True
        cv2.destroyAllWindows()
        motor.stop()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
