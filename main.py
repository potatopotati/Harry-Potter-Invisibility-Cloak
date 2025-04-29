import cv2
import numpy as np
import time

def create_background(capture, num_frame=30):
    print("Starting to capture background....")
    background=[]
    for i in range (num_frame):
        capturedFrame = capture.read()
        if capturedFrame[0]:
            background.append(capturedFrame[1])
        else: print(f"Failed to capture frame at {i+1}/{num_frame}")
        time.sleep(0.1)
    if background:
        return np.median(background,axis=0).astype(np.uint8)
    else: raise ValueError("Unable to capture any frames")

def create_mask(frame, lower,upper):
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower,upper)
    #the mask will be black and white (white for pixels within the target color range)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)
    return mask

def apply_effect(mask,frame,background):
    notMask= cv2.bitwise_not(mask) #the mask will be black and white (black for pixels within the target color range)
    foreground = cv2.bitwise_and(frame,frame,mask=notMask) #Extract part of the frame that do not match the target color
    background=cv2.bitwise_and(background,background,mask=mask) #Extract part of the frame that match the target color
    return cv2.add(foreground,background) 

def main():
    capture = cv2.VideoCapture(0)
    if not capture.isOpened:
        print("Error: Unable to open camera")
        return
    try:
        background = create_background(capture)
    except ValueError as e:
        print(f'Error: {e}')
        capture.release()
        return
    lower_blue = np.array([90, 50, 50])    # Lower bound
    upper_blue = np.array([150, 255, 255]) # Upper bound
    print("Starting soon... press 'q' to quit.")
    while True:
        captureFrame = capture.read()
        if not captureFrame[0]:
            print("Cannot capture frame")
            time.sleep(0.1)
            continue
        mask= create_mask(captureFrame[1],lower_blue,upper_blue)
        result=apply_effect(mask,captureFrame[1],background)
        cv2.imshow('Invisible Cloak',result)
        key = cv2.waitKey(1)#wait for 1 ms
        if key == ord('q'):break
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



#capture background image
#continuously process new frame
#detect blue color
#create mask for blue area
#replaces blue area with background
#display result in real time
