#hand tracking module

import cv2
import mediapipe as mp
import time

#create the Hand detector class


class handDetector():
    #initialization parametrs and defaults
    def __init__(self, mode = False, maxHands = 2, detectionConfd = 0.5,trackConfd = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfd = detectionConfd
        self.trackConfd = trackConfd
        self.mpHands = mp.solutions.hands
        #declaring the mphands 
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionConfd,
            min_tracking_confidence=self.trackConfd
        )
        #the mphands drawings class
        self.mpDraw = mp.solutions.drawing_utils
        #self.mpConnect = self.mpHands.HAND_CONNECTIONS()
    #defining the findlandmarks method
    def findLandmarks(self,img, draw = True):
        #convert image to RGB format which mediapipe can work with
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #process the image with mpHands to find hand landmarks
        self.results = self.hands.process(imgRGB)
        #check if landmarks are detected
        if self.results.multi_hand_landmarks:
            #loop through the hands present
            for handlms in self.results.multi_hand_landmarks:
                #only draw when draw = True in the method
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img
    #define find landmark positions method
    def findLmPositions(self, img):
        lmpositions = []
        lmpositions2 = []
        if self.results.multi_hand_landmarks:
            #when hands are detected and only one hand is required
            det_hands = self.results.multi_hand_landmarks
            #make sure to pick out the first hand i.e. hand 0 if there is only one hand, or hand 1 if the hands are more than one
            if len(det_hands) > 1: #if there are two hands
                myHand = det_hands[1]  #first hand
                myHand2 = det_hands[0] #second hand
                for Id,lm in enumerate(myHand.landmark):
                    #get the shape of the image
                    h, w, c = img.shape
                    #compute the pixel points of the landmarks
                    cx,cy = int(lm.x*w), int(lm.y*h) #x is the ratio of the width of the image and y is the ratio of the height of the image
                    lmpositions.append([Id,cx,cy])
                for Id,lm in enumerate(myHand2.landmark):
                    #get the shape of the image
                    h, w, c = img.shape
                    #compute the pixel points of the landmarks
                    cx,cy = int(lm.x*w), int(lm.y*h) #x is the ratio of the width of the image and y is the ratio of the height of the image
                    lmpositions2.append([Id,cx,cy])
                return lmpositions, lmpositions2      
            else: 
                #if there is only one hand, get the landmarks of that hand
                myHand = det_hands[0]
                for Id,lm in enumerate(myHand.landmark):
                    #get the shape of the image
                    h, w, c = img.shape
                    #compute the pixel points of the landmarks
                    cx,cy = int(lm.x*w), int(lm.y*h) #x is the ratio of the width of the image and y is the ratio of the height of the image
                    lmpositions.append([Id,cx,cy])
                return [lmpositions]      

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findLandmarks(img)
        handLists = detector.findLmPositions(img)
        #print(handLists)
        #To get the frames per second
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        if handLists:
            if len(handLists) > 1:
                for lmlist in handLists:
                    if lmlist[4][1] < lmlist[20][1]: 
                        #left hand
                        xi,yi = lmlist[4][1],lmlist[4][2]
                        cv2.circle(img, (xi,yi), 15, (0,0,255), cv2.FILLED)
            else:
                handLists = handLists[0]
                if handLists[4][1] < handLists[20][1]: 
                    #left hand
                    xi,yi = handLists[4][1],handLists[4][2]
                    cv2.circle(img, (xi,yi), 15, (0,0,255), cv2.FILLED)
        #flip image
        img2 = cv2.flip(img, 1)
        #display frames per second
        cv2.putText(img2, str(int(fps)), (10,70), cv2.FONT_ITALIC, 2, (0,0,255), 2)
        #image display
        cv2.imshow("video feed broski", img2)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break 


if __name__ == "__main__":
    main()