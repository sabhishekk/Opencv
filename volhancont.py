import cv2
import numpy as np 
import time
import handmodule as hm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


cap=cv2.VideoCapture(0)
ptime=0
dete=hm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()
maxvol=volrange[1]
minvol=volrange[0]
volbar=400
volper=0

while True:
    ret, frame=cap.read()
    frame=dete.findHands(frame)
    lmlist=dete.findPositon(frame, draw=True, drawid=(4,8))
    if len(lmlist)!=0:
        # print(lmlist[4], lmlist [8])

        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2, (y1+y2)//2

        cv2.line(frame, (x1,y1),(x2,y2), (224,53,0), 2)
        cv2.circle(frame, (cx,cy), 7, (0,0,0), cv2.FILLED)
        length=math.hypot((x2-x1), (y2-y1))
        if length<15:
            cv2.circle(frame, (cx,cy), 7, (67,255,200), cv2.FILLED)

        vol=np.interp(length,[15,210], [minvol,maxvol])
        volume.SetMasterVolumeLevel(vol, None)
        volbar=np.interp(length, [15,210],[400,100])
        volper=np.interp(length, [15,210], [0,100])
        # print(length)
        
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    
    cv2.putText(frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 4)
    cv2.rectangle(frame,(70,100), (100,400), (54,32,113), 2)
    cv2.rectangle(frame, (100,400), (70, int(volbar)), (54,32,115), cv2.FILLED)
    cv2.putText(frame, str(int(volper))+"%", (65,450), cv2.FONT_HERSHEY_PLAIN,2, (255,45,53), 1  )
    cv2.imshow("img", frame)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cv2.destroyAllWindows()

