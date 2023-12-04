from tensorflow.lite.python.interpreter import Interpreter
import os
import cv2
import numpy as np
import math


class Obj_model():
    def __init__(self, model_path, lblpath,min_conf=0.5):
        self.model_path = model_path
        self.lblpath = lblpath
        self.min_conf = min_conf
        self.labelmap = {'sai':0,
                         'wtr':1,
                         'zam':2,
                         'taw':3}
        self.dest = None
    

        with open(self.lblpath, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]


        # Load the Tensorflow Lite model into memory
        self.interpreter = Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()

        # Get model details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]

        self.float_input = (self.input_details[0]['dtype'] == np.float32)

        self.input_mean = 127.5
        self.input_std = 127.5
    
    def predict(self, image, obj=None, min_conf=0.5):
        self.min_conf=min_conf
        # Load image and resize to expected shape [1xHxWx3]
        self.image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.imH, self.imW, _ = self.image.shape
        self.image_resized = cv2.resize(self.image_rgb, (self.width, self.height))
        self.input_data = np.expand_dims(self.image_resized, axis=0)
        
        self.detected = False
        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if self.float_input:
            self.input_data = (np.float32(self.input_data) - self.input_mean) / self.input_std
        
        # Perform the actual detection by running the model with the image as input
        self.interpreter.set_tensor(self.input_details[0]['index'],self.input_data)
        self.interpreter.invoke()

        # Retrieve detection results
        self.boxes = self.interpreter.get_tensor(self.output_details[1]['index'])[0] # Bounding box coordinates of detected objects
        self.classes = self.interpreter.get_tensor(self.output_details[3]['index'])[0] # Class index of detected objects
        self.scores = self.interpreter.get_tensor(self.output_details[0]['index'])[0] # Confidence of detected objects

        self.detections = []
        
        for i in range(len(self.scores)):
            if obj == None:
                continue
            if ((self.scores[i] > self.min_conf) and (self.scores[i] <= 1.0) and (self.labelmap[obj] == self.classes[i])):
                self.detected = True
                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                self.ymin = int(max(1,(self.boxes[i][0] * self.imH)))
                self.xmin = int(max(1,(self.boxes[i][1] * self.imW)))
                self.ymax = int(min(self.imH,(self.boxes[i][2] * self.imH)))
                self.xmax = int(min(self.imW,(self.boxes[i][3] * self.imW)))
                if obj == 'wtr' or obj == 'zam':
                    self.a = self.xmax-self.xmin
                    self.b = self.ymax-self.ymin
                    self.dest = math.sqrt(self.a**2 + self.b**2)

                cv2.rectangle(self.image, (self.xmin,self.ymin), (self.xmax,self.ymax), (10, 255, 0), 2)

                # Draw label
                self.object_name = self.labels[int(self.classes[i])] # Look up object name from "labels" array using class index
                self.label = '%s: %d%%' % (self.object_name, int(self.scores[i]*100)) # Example: 'person: 72%'
                self.labelSize, self.baseLine = cv2.getTextSize(self.label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                self.label_ymin = max(self.ymin, self.labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(self.image, (self.xmin, self.label_ymin-self.labelSize[1]-10), (self.xmin+self.labelSize[0], self.label_ymin+self.baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(self.image, self.label, (self.xmin, self.label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1) # Draw label text

                self.detections.append([self.object_name, self.scores[i], self.xmin, self.ymin, self.xmax, self.ymax])

        return self.image, self.detected, self.dest