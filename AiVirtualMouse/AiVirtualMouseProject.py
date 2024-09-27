import cv2
import numpy as  np 
import HandTrackingModule as htm 
import time 
import pynput
import pyautogui
from pynput.mouse import Controller
######################

wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 7
plocX, plocY = 0, 0
clocX, cloclY = 0, 0
######################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()
print(wScr, hScr)
mouse = Controller()

while True:
   # find the hand landmarks

   success, img = cap.read()
   img = detector.findHands(img)
   lmList, bbox = detector.findPosition(img)

   

   # get the tip of the index and middle fingers 
   if len(lmList) != 0:
      x1, y1 = lmList[8][1:]
      x2, y2 = lmList[12][1:]
      #print(x1, y1, x2, y2)
      #print(lmList[8])
   else : 
     print("No hand detected. Please move your hand into the frame.") 

   
   # check which of the fingers are up 
   fingers = detector.fingersUp()
   print(fingers)
   
   cv2.rectangle(img, (frameR,frameR),(wCam - frameR, hCam - frameR), (255, 0, 255), 2)
   #only index finger aka Moving mode 
   if fingers[1] == 1 and fingers[2] == 0:
      
     # convert coordinates 
     
     x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
     y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))


     # smoothing values 
     clocX = plocX + (x3 - plocX) / smoothening
     clocY = plocY + (y3 - plocY) / smoothening

     #Move our mouse 
     mouse.position = (wScr - clocX, clocY)
     cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
     plocX, plocY = clocX, clocY

   # check if we are in clicking mode , booth index and fingers are up : Clicking mode 
   if fingers[1] == 1 and fingers[2] == 1:
      
      # find distance between fingers
      length, img, lineInfo = detector.findDistance(8, 12, img)
      print(length)

      # click mouse if distance short less than 40
      if length < 40:
         cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
         mouse.click(pynput.mouse.Button.left, 1)
         # frame rate

   
   cTime = time.time()
   fps = 1/(cTime - pTime) 
   pTime = cTime
   cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)
     # display 
  
   cv2.imshow("Image", img)
  
    # Break the loop on 'q' key press
   if cv2.waitKey(1) & 0xFF == ord('q'):
     break

cap.release()
cv2.destroyAllWindows()