import cv2
import handmodule

def findDistance(p1,p2, lmlist):
    import math
    x1,y1=lmlist[p1][1], lmlist[p1][2]
    x2,y2=lmlist[p2][1], lmlist[p2][2]
    ln=math.hypot((x2-x1),(y2-y1))
    return ln


cap=cv2.VideoCapture(0)
detector=handmodule.handDetector()
color=(253,52,64)
cx,cy,h,w=150,150,150,150

while True:
    ret, frame=cap.read()
    frame=cv2.flip(frame, 1)
    frame=detector.findHands(frame)
    lmlist= detector.findPositon(frame, draw=True, drawid=(8,12))
    if lmlist:
        pointer=lmlist[8]
        l=findDistance(8,12,lmlist)
        if l<30:
            if cx-w//2<pointer[1]<cx+w//2 and cy-h//2<pointer[2]<cy+h//2:
                color=(56,46,23)
                cx,cy=pointer[1],pointer[2]
        else:
            color= (253,52,64)
    cv2.rectangle(frame, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), color, cv2.FILLED)
    cv2.imshow("img", frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cv2.destroyAllWindows()