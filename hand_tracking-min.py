import cv2
import mediapipe as mp 
import time

cap=cv2.VideoCapture(0)
mphand= mp.solutions.hands 
hands=mphand.Hands()
mpdraw=mp.solutions.drawing_utils
ptime=0
ctime=0

while True:
    ret,frame=cap.read()
    rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result=hands.process(rgb)
    # print(result.multi_hand_landmarks)

    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                h,w,c=frame.shape
                cx,cy=int(lm.x * w), int(lm.y * h)
                # if id==0:
                #     cv2.circle(frame, (cx,cy), 12, (255,0,133), -1)
            mpdraw.draw_landmarks(frame, handlms, mphand.HAND_CONNECTIONS)

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 4)

    cv2.imshow("cap", frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cv2.destroyAllWindows()
