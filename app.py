from email import message
from socket import timeout
from flask import Flask,render_template,Response,url_for
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from matplotlib.pyplot import title
from plyer import notification
from datetime import datetime as dt
import os

                        
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help():
    return render_template('help.html')

def Notification1(t): 
    notification.notify(
        title='Blink',
        message='Dear Developer its time to blink!',
        app_icon=None,
        timeout=3
    )

def Notification2(): 
    notification.notify(
        title='Relax!',
        message='Take some time off, you are working hard enough!',
        app_icon=None,
        timeout=3
    )

        

def BlinkCountDetector():
                cap = cv2.VideoCapture(0)
                detector = FaceMeshDetector(maxFaces=1)
                idList = [22,23,24,26,110,157,158,160,161,130,243]
                ratioList = []
                blinkCounter = 0
                cnt = 0
                now = dt.now()
                flag_=0
                
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
                    (flag,encodedImage) = cv2.imencode(".jpg",img)
                    if not flag:
                        continue
                    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
                    cv2.waitKey(25)
                    after = dt.now()
                    tt = (after-now).total_seconds()
                    if tt>3:  #SECONDS
                        if blinkCounter<100:
                            Notification1(blinkCounter)
                        now=after
                        blinkCounter=0
                        flag_+=1
                    if flag_>4:
                        print("entered")
                        flag_=0
                        Notification2()
                    print(flag_)
                    
                    #print(tt,blinkCounter)
                            

                    
                    
                    



                        
                    

                    


@app.route('/video_feed')
def video_feed():
    return Response(BlinkCountDetector(),
    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

