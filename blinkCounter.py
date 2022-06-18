import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector


def BlinkCountDetector():
                cap = cv2.VideoCapture(0)
                detector = FaceMeshDetector(maxFaces=1)
                idList = [22,23,24,26,110,157,158,160,161,130,243]
                ratioList = []
                blinkCounter = 0
                cnt = 0
                while True:
                    success,img = cap.read()
                    img,faces = detector.findFaceMesh(img)
                    
                    if faces:
                        face = faces[0]
                        for id in idList:
                        # cv2.circle(img,face[id],5,(255,0,255),cv2.FILLED)
                            pass

                        leftUp = face[159]
                        leftDown = face[23]
                        leftLeft = face[130]
                        leftRight = face[243]
                        lengthVer,_=detector.findDistance(leftUp,leftDown)
                        lengthHor,_=detector.findDistance(leftLeft,leftRight)
                        
                    # cv2.line(img,leftUp,leftDown,(0,200,0),3)
                        #cv2.line(img,leftLeft,leftRight,(0,200,0),3)
                    try:
                        ratio = (lengthVer/lengthHor)*100
                        ratioList.append(ratio)
                        if len(ratioList)>3:
                            ratioList.pop(0)
                        ratioAvg = sum(ratioList)/len(ratioList)
                        if ratioAvg<35 and cnt==0:
                            blinkCounter+=1
                            cnt = 1
                        if cnt!=0:
                                cnt+=1
                                if cnt>10:
                                    cnt=0
                    except Exception:
                        pass
                    cvzone.putTextRect(img,f'Blink Count {blinkCounter}',(0,100))
                    cv2.imshow("Image",img)
                    cv2.waitKey(25)
BlinkCountDetector()
                        