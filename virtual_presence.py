import numpy as np
import cv2
from PIL import Image, ImageChops



def adjustThreshold(v):
    global thresholdLimit
    print("threshold value "+ str(v))
    thresholdLimit = v






cap = cv2.VideoCapture(0)
bgCap = cv2.VideoCapture("sky.mp4")

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))

loop_num = 0
thresholdLimit = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    retBg, frameBg = bgCap.read()

    if not retBg:
        bgCap = cv2.VideoCapture("sky.mp4")
        retBg, frameBg = bgCap.read()

    if(loop_num <= 20):
        bg_frame = frame
        bg_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_bg_gray = cv2.GaussianBlur(bg_gray, (5, 5), 0)
        cv2.imshow('Bg frame',blur_bg_gray)
        print("loop for background" + str(loop_num))

    if(loop_num > 20):
        frameH, frameW, channels = frame.shape
        #bgImage = cv2.imread('cartoonbg.jpg')
        resizedBg = cv2.resize(frameBg, (frameW, frameH))

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_frame_gray = cv2.GaussianBlur(frame_gray, (5, 5), 0)

        blur_sub_image = cv2.subtract(blur_bg_gray,blur_frame_gray) #ImageChops.subtract(blur_frame_gray,blur_bg_gray)
        cv2.imshow('blur_sub_image',blur_sub_image)
        #blur_sub_image = cv2.absdiff(blur_bg_gray,blur_frame_gray)
        #blur_sub_image = blur_bg_gray - blur_frame_gray
        # threshold dynamic change
        cv2.createTrackbar("threshold", "CV_Result", thresholdLimit, 255, adjustThreshold)

        (t, maskLayer) = cv2.threshold(blur_sub_image, thresholdLimit, 255, cv2.THRESH_BINARY)
        morphMask = cv2.morphologyEx(maskLayer, cv2.MORPH_OPEN, kernel)
        cv2.imshow('threasholdMask',morphMask)

        morphMask_inv = cv2.bitwise_not(morphMask)
        bg_image_stripped = cv2.bitwise_and(resizedBg,resizedBg,mask = morphMask_inv)
        fg_image_stripped = cv2.bitwise_and(frame,frame, mask = morphMask)
        cv2.imshow('fg_image_stripped',fg_image_stripped)
        # add both the image
        mergedImage = cv2.add(bg_image_stripped,fg_image_stripped)
        
        cv2.imshow('CV_Result',mergedImage)
    	
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    loop_num = loop_num + 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
