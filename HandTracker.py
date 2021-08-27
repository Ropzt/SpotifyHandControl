import cv2
import mediapipe as mp


class handTracker():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon =detectionCon
        self.trackCon=trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon, self.trackCon)
        self.annulaireWasDown = False
        self.indexWasDown = False
        self.pouceWasDown = False

    def findHands(self, frameRGB):
        self.resultat = self.hands.process(frameRGB)
        markList=[]
        if self.resultat.multi_hand_landmarks:
            handLms = self.resultat.multi_hand_landmarks[0]
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frameRGB.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                markList.append([id,cx,cy])
        return markList

    def process(self, spotifyControl, markList):
        ##Etat du petit doigt
        if markList[20][2] > markList[18][2]:
            self.petitDoigtDown = True
        else :
            self.petitDoigtDown = False

        ##Etat de l'annulaire
        if (markList[16][2] > markList[14][2]):
            self.annulaireDown = True
        else :
            self.annulaireDown = False

        ##Etat de l'index
        if markList[8][2] > markList[6][2]:
            self.indexDown = True
        else:
            self.indexDown = False

        ##Etat du pouce
        if (markList[17][1] < markList[4][1] < markList[5][1]) or (markList[17][1] > markList[4][1] > markList[5][1]):
            self.pouceDown = True
        else :
            self.pouceDown = False

        ##Actions
        if self.petitDoigtDown is True:
            spotifyControl.setVolume(markList=markList)
        elif self.annulaireDown is True and self.annulaireWasDown is False:
            spotifyControl.nextTrack()
        elif self.indexDown is True and self.indexWasDown is False:
            spotifyControl.previousTrack()
        elif self.pouceDown is True and self.pouceWasDown is False:
            spotifyControl.playPauseTrack()

        ##Conservation de l'état antérieur
        self.annulaireWasDown = self.annulaireDown
        self.indexWasDown = self.indexDown
        self.pouceWasDown = self.pouceDown


def main():
    stream = cv2.VideoCapture(0)
    tracker = handTracker()
    while True :
        success, frame = stream.read()
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        markList = tracker.findHands(frameRGB)
        if len(markList) != 0:
            print(markList[4])
        cv2.imshow("Display", frameRGB)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
