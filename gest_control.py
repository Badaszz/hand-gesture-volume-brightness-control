import cv2
import mediapipe as mp
import hand_tracking_module3 as htm
import numpy as np
import time
import math 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

#####################
wCam, hCam = 240,240
#####################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
cTime = 0

detector = htm.handDetector(detectionConfd = 0.7) #a higher confidence s required for detection

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#volume.GetMute()
#volume.GetMasterVolumeLevel()
volume.GetVolumeRange()

# Volume Range is (-65.25, 0.0, 0.75) 0 is highest and -65.25 is lowest
#volume.SetMasterVolumeLevel(-20.0, None)
volume_range = volume.GetVolumeRange()
minVol = volume_range[0]
maxVol = volume_range[1]
vol=0
vol_for_bar = 100

brightness = 0
brightness_for_bar = 0
minBrightness = 0
maxBrightness = 100

while True:
    success, img = cap.read()
    img = detector.findLandmarks(img, draw=False)
    handLists = detector.findLmPositions(img)
    if handLists:
            if len(handLists) > 1:
                for lmlist in handLists:
                    if lmlist[4][1] < lmlist[20][1]: 
                        #left hand for volume control
                        
                        x1,y1 = lmlist[4][1],lmlist[4][2] #x,y point for the tip of the thumb landmark
                        x2,y2 = lmlist[8][1],lmlist[8][2] #x,y point for the tip of the index finger
                        cx,cy = (x1+x2)//2, (y1+y2)//2 #center point between the thumb and index finger
                        
                        if lmlist[8][2] < lmlist[20][2]:
                            #pinky must be above the index to change the volume
                            cv2.circle(img, (x1,y1), 7, (0,255,0),cv2.FILLED)
                            cv2.circle(img, (x2,y2), 7, (0,255,0),cv2.FILLED)
                            cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 1)
                            cv2.circle(img, (cx,cy), 3, (0,255,0),cv2.FILLED) #center point
                            length = math.hypot(x2-x1, y2-y1) #distance between the thumb and index finger
                            #Hand range is 25 to 100
                            #Volume range is -65.25 to 0
                            vol = np.interp(length, [25, 100], [minVol, maxVol])
                            vol_for_bar = np.interp(length, [25, 100], [100, 200])
                            #vol_percent = np.interp(length, [25, 100], [0, 100])
                            print(f'Volume: {vol}')
                            volume.SetMasterVolumeLevel(vol, None)
                    else:
                        #right hand for brightness control
                        
                        x1,y1 = lmlist[4][1],lmlist[4][2] #x,y point for the tip of the thumb landmark
                        x2,y2 = lmlist[8][1],lmlist[8][2] #x,y point for the tip of the index finger
                        cx,cy = (x1+x2)//2, (y1+y2)//2 #center point between the thumb and index finger
                        
                        if lmlist[8][2] < lmlist[20][2]:
                            #pinky must be above the index to change the volume
                            cv2.circle(img, (x1,y1), 7, (0,255,0),cv2.FILLED)
                            cv2.circle(img, (x2,y2), 7, (0,255,0),cv2.FILLED)
                            cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 1)
                            cv2.circle(img, (cx,cy), 3, (0,255,0),cv2.FILLED) #center point
                            length = math.hypot(x2-x1, y2-y1) #distance between the thumb and index finger
                            #Hand range is 25 to 100
                            #Brightness range is 0 to 100
                            brightness = np.interp(length, [25, 100], [minBrightness, maxBrightness])
                            brightness_for_bar = np.interp(length, [25, 100], [100, 200])
                            #vol_percent = np.interp(length, [25, 100], [0, 100])
                            print(f'Volume: {brightness}')
                            sbc.set_brightness(brightness)
                        
            else:
                lmlist = handLists[0]
                if lmlist[4][1] < lmlist[20][1]: 
                    #left hand for volume control
                    
                    
                    x1,y1 = lmlist[4][1],lmlist[4][2] #x,y point for the tip of the thumb landmark
                    x2,y2 = lmlist[8][1],lmlist[8][2] #x,y point for the tip of the index finger
                    cx,cy = (x1+x2)//2, (y1+y2)//2 #center point between the thumb and index finger
                    
                    if lmlist[8][2] < lmlist[20][2]:
                        # the pinky must be above the index to change the volume
                        cv2.circle(img, (x1,y1), 7, (0,255,0),cv2.FILLED)
                        cv2.circle(img, (x2,y2), 7, (0,255,0),cv2.FILLED)
                        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 1)
                        cv2.circle(img, (cx,cy), 3, (0,255,0),cv2.FILLED) #center point
                        length = math.hypot(x2-x1, y2-y1) #distance between the thumb and index finger
                        #print(length) #print the distance between the thumb and index finger
                        #Hand range is 25 to 100
                        #Volume range is -65.25 to 0
                        vol = np.interp(length, [25, 100], [minVol, maxVol])
                        vol_for_bar = np.interp(length, [25, 100], [100, 200])
                        #vol_percent = np.interp(length, [25, 100], [0, 100])
                        print(vol_for_bar)
                        volume.SetMasterVolumeLevel(vol, None)
                else:
                    #right hand for brightness control
                    x1,y1 = lmlist[4][1],lmlist[4][2] #x,y point for the tip of the thumb landmark
                    x2,y2 = lmlist[8][1],lmlist[8][2] #x,y point for the tip of the index finger
                    cx,cy = (x1+x2)//2, (y1+y2)//2 #center point between the thumb and index finger
                    
                    if lmlist[8][2] < lmlist[20][2]:
                        #pinky must be above the index to change the volume                            
                        cv2.circle(img, (x1,y1), 7, (0,255,0),cv2.FILLED)
                        cv2.circle(img, (x2,y2), 7, (0,255,0),cv2.FILLED)
                        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 1)
                        cv2.circle(img, (cx,cy), 3, (0,255,0),cv2.FILLED) #center point
                        length = math.hypot(x2-x1, y2-y1) #distance between the thumb and index finger
                        #Hand range is 25 to 100
                        #Brightness range is 0 to 100
                        brightness = np.interp(length, [25, 100], [minBrightness, maxBrightness])
                        brightness_for_bar = np.interp(length, [25, 100], [100, 200])
                        #vol_percent = np.interp(length, [25, 100], [0, 100])
                        print(f'Volume: {brightness}')
                        sbc.set_brightness(brightness)
        
    filled_height = int(((vol - minVol) / (maxVol - minVol)) * (100)) # Calculate the filled height of the volume bar
    cv2.rectangle(img, (25,100), (40,200), (0,255,0), 2) 
    cv2.rectangle(img, (25, 200 - filled_height), (40, 200), (0,255,0), cv2.FILLED)
    
    filled_height_b = int(((brightness - minBrightness) / (maxBrightness - minBrightness)) * (100)) 
    cv2.rectangle(img, (5,100), (20,200), (255,0,0), 2) 
    cv2.rectangle(img, (5, 200 - filled_height_b), (20, 200), (255,0,0), cv2.FILLED)
    
    img2 = cv2.flip(img,1) #flip image if required
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img2, f'FPS: {int(fps)}', (10,25), cv2.FONT_ITALIC, 1, (0,0,255), 1)
    cv2.imshow("VIDEO FEED BROSKI", img2)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break
    
    



