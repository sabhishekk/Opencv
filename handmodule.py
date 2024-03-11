import cv2
import mediapipe as mp 
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=1, trackCon=0.5):
        self.mode = mode 
        self.maxHands = maxHands 
        self.detectionCon = detectionCon 
        self.trackCon = trackCon 

        self.mphand= mp.solutions.hands 
        self.hands=self.mphand.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpdraw=mp.solutions.drawing_utils
    
    def findHands(self, frame, draw=True):
        rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result=self.hands.process(rgb)
        # print(result.multi_hand_landmarks)

        if self.result.multi_hand_landmarks:
            for handlms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(frame, handlms, self.mphand.HAND_CONNECTIONS)
        return frame

    def findPositon(self, frame, handNo=0, draw=False, drawid=(range(0,22))):
        lmlist=[]
        if self.result.multi_hand_landmarks:
            myhands=self.result.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myhands.landmark):
                h,w,c=frame.shape
                cx,cy=int(lm.x * w), int(lm.y * h)
                # print(id, cx,cy)
                lmlist.append([id,cx,cy])
                if draw:
                    for i in drawid:
                        if id==i:
                            cv2.circle(frame, (cx,cy), 7, (255,0,255), cv2.FILLED)
        return lmlist   

def main():
    ptime=0
    ctime=0
    detector=handDetector()
    cap=cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        frame=detector.findHands(frame)
        lmlist=detector.findPositon(frame, drawid=9)
        # if len(lmlist)!=0:
        #     print(lmlist[4])
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        cv2.putText(frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 4)
        

        cv2.imshow("cap", frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

    cv2.destroyAllWindows()


if __name__=="__main__":
    main()