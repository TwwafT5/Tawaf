import RPi.GPIO as GPIO
from time import sleep
import math
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
class Motor():
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B):
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(self.EnaA,GPIO.OUT)
        GPIO.setup(self.In1A,GPIO.OUT)
        GPIO.setup(self.In2A,GPIO.OUT)
        GPIO.setup(self.EnaB,GPIO.OUT)
        GPIO.setup(self.In1B,GPIO.OUT)
        GPIO.setup(self.In2B,GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100);
        self.pwmA.start(0);
        self.pwmB = GPIO.PWM(self.EnaB, 100);
        self.pwmB.start(0);
        self.on=False
    
    def move(self,speed=0.100,turn=0,t=0, op='sai'):
        if self.on == False:
                self.on = True
                self.forward(0.2)
        if turn<=-0.33:
            turn= -0.32
        if op == 'taw':
            speed *=83
            turn *=83
        else:
            speed *=83
            turn *=82
        
        leftSpeed = speed - turn
        rightSpeed = speed + turn
        if leftSpeed>100: leftSpeed=100
        elif leftSpeed<-100: leftSpeed= -100
        if rightSpeed>100: rightSpeed=100
        elif rightSpeed<-100: rightSpeed= -100
 
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))
 
        if leftSpeed>0:
            GPIO.output(self.In1A,GPIO.HIGH)
            GPIO.output(self.In2A,GPIO.LOW)
        else:
            GPIO.output(self.In1A,GPIO.LOW)
            GPIO.output(self.In2A,GPIO.HIGH)
 
        if rightSpeed>0:
            GPIO.output(self.In1B,GPIO.HIGH)
            GPIO.output(self.In2B,GPIO.LOW)
        else:
            GPIO.output(self.In1B,GPIO.LOW)
            GPIO.output(self.In2B,GPIO.HIGH)
 
        sleep(t)
    def stop(self,t=0):
        self.pwmA.ChangeDutyCycle(0);
        self.pwmB.ChangeDutyCycle(0);
        sleep(t)
        
    def forward(self, t=0):
        GPIO.output(self.In1A,GPIO.HIGH)
        GPIO.output(self.In2A,GPIO.LOW)
        self.pwmA.ChangeDutyCycle(100);
        GPIO.output(self.In1B,GPIO.HIGH)
        GPIO.output(self.In2B,GPIO.LOW)
        self.pwmB.ChangeDutyCycle(100);
        sleep(t)
    
    def left(self, t=0):
        # Turn left
        GPIO.output(self.In1A,GPIO.HIGH)
        GPIO.output(self.In2A,GPIO.LOW)
        self.pwmA.ChangeDutyCycle(100);
        GPIO.output(self.In1B,GPIO.LOW)
        GPIO.output(self.In2B,GPIO.HIGH)
        self.pwmB.ChangeDutyCycle(100);
        sleep(t)
    
    def right(self, t=0):
        #Turn right
        GPIO.output(self.In1A,GPIO.LOW)
        GPIO.output(self.In2A,GPIO.HIGH)
        self.pwmA.ChangeDutyCycle(100);
        GPIO.output(self.In1B,GPIO.HIGH)
        GPIO.output(self.In2B,GPIO.LOW)
        self.pwmB.ChangeDutyCycle(100);
        sleep(t)
        
        
    def park(self):        
        self.forward(0.15)
        self.stop(0.8)
        self.right(0.4)
        self.stop(0.7)
        self.forward(0.4)
        self.stop(0.9)
        sleep(5)
        self.left(0.45)
        self.stop(0.8)
        self.forward(0.1)
    

    def to_tawaf(self):
        self.right(0.4)
        self.stop(0.5)
        self.forward(0.6)
        self.stop(0.5)
        self.right(0.3)
        self.stop(0.5)
        self.forward(0.1)
        
    
    def to_sai(self):
        self.stop(0.5)
        self.forward(0.9)
        self.stop(0.5)
        self.right(0.5)
        self.stop(0.5)
        self.forward(0.1)

def main():
    #motor.to_tawaf()
    motor.stop()
    
 
if __name__ == '__main__':
    motor= Motor(21,20,16,19,13,26)
    main()