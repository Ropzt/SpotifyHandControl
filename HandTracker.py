import cv2
import mediapipe as mp


class handTracker():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5,trackCon=0.5):
        """
        Cette fonction initialise l'objet qui controllera les fonctions de récupération des points de la main à partir de l'image.
        :param mode:
        :param maxHands: le nombre maximal de mains que le programme acceptera de reconnaitre.
        :param detectionCon:
        :param trackCon:
        """
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
        """
        Cette fonction s'occupe de la récupération de la liste des coordonnées x et y des 21 points de la main.
        :param frameRGB: l'image qui sera analysée.
        :return: la liste des coordonnées x et y des 21 points de la main
        """
        self.resultat = self.hands.process(frameRGB)
        markList=[]
        if self.resultat.multi_hand_landmarks:
            handLms = self.resultat.multi_hand_landmarks[0]
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frameRGB.shape
                cx, cy = int(lm.x * w), int(lm.y * h) #conversion des coordonnées relatives en coordonnées absolues.
                markList.append([id,cx,cy])
        return markList

    def process(self, spotifyControl, markList):
        """
        Cette fonction s'occupe de l'exécution des différentes fonction du module SpotifyHandController en fonction des événements lancés par l'utilisateur.
        Elle empeche les événements de s'activer à chaque frame (30 fois par seconde) en demandant à ce que l'événement soit terminé pour pouvoir être réactivé.
        :param spotifyControl: l'objet de controle du module SpotifyHandController.
        :param markList: la liste des coordonnées x et y des 21 points de la main
        """
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

