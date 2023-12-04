import sys
import cv2
import numpy as np
import ArducamDepthCamera as ac

MAX_DISTANCE = 4
cam = ac.ArducamCamera()
if cam.open(ac.TOFConnect.CSI,0) != 0 :
    print("initialization failed")
if cam.start(ac.TOFOutput.DEPTH) != 0 :
    print("Failed to start camera")
else:print('success!')

def process_frame(depth_buf: np.ndarray, amplitude_buf: np.ndarray) -> np.ndarray:
        
    depth_buf = np.nan_to_num(depth_buf)

    amplitude_buf[amplitude_buf<=7] = 0
    amplitude_buf[amplitude_buf>7] = 255

    depth_buf = (1 - (depth_buf/MAX_DISTANCE)) * 255
    depth_buf = np.clip(depth_buf, 0, 255)
    result_frame = depth_buf.astype(np.uint8)  & amplitude_buf.astype(np.uint8)
    return result_frame

    
def getImg(show=False, img_process=False):    
    frame = cam.requestFrame(200)
    if frame != None:
        depth_buf = frame.getDepthData()
        amplitude_buf = frame.getAmplitudeData()
        cam.releaseFrame(frame)
        amplitude_buf*=(255/1024)
        amplitude_buf = np.clip(amplitude_buf, 0, 255)
        img = amplitude_buf.astype(np.uint8)
        img_v = cv2.flip(img, 0)
        img_h = cv2.flip(img_v, 1)
        
        alpha = 0.9 # Contrast control
        beta = 10 # Brightness control

        # call convertScaleAbs function
        adjusted = cv2.convertScaleAbs(img_h, alpha=alpha, beta=beta)
        if show:
            cv2.imshow("preview_amplitude", img)
            key = cv2.waitKey(1)
            if key == ord("q"):
                exit_ = True
                cam.stop()
                cam.close()
                sys.exit(0)
                GPIO.cleanup()
                

        
    return img
            
    

        
if __name__ == '__main__':
    while True:
       getImg(show=True)
        
        
        
    