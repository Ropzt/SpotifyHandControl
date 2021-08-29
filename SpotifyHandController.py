import math
import spotipy as spot
from spotipy.oauth2 import SpotifyOAuth


class spotifyControl():
    def __init__(self, client_id, client_secret, scope='user-read-playback-state user-modify-playback-state user-top-read'):
        """
        Cette fonction s'occupe de générer un ticket d'autorisation à l'API Spotify Developpers grâce aux identifiants utilisateurs.
        Elle s'occupe également du choix d'appareil à utiliser pour l'exécution du programme.
        :param client_id: le client id Spotify Developpers de l'utilisateur.
        :param client_secret: le client secret Spotify Developpers de l'utilisateur.
        :param scope: les droits requis pour l'exécution des fonctions du programme.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = 'https://example.com/callback/'
        self.scope = scope
        self.sp = spot.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                    client_secret=self.client_secret,
                                                    redirect_uri=self.redirect_uri,
                                                    scope=self.scope)) # cette fonction s'occupe de la génération du tocket d'autorisation grâce aux informations utilisateur.
        devices = self.sp.devices() #on récupère la liste des appareils connextés associés à l'utilisateur.
        self.deviceID = None
        selector = []
        x = 1
        for d in devices['devices']:
            d['name'] = d['name'].replace('’', '\'')
            selector.append([x, d['name']])
            x += 1
        print('Id', "| ", 'Device')
        print('_______________________')
        for line in selector:
            print(line[0], " | ", line[1])
        print('Enter the Id of the Device you want to use : ') # on invite l'utilisateur à selectionner l'appareil qu'il désire.
        selection = input()
        selection = int(selection)
        selection = selection - 1
        device_name = selector[selection][1]
        print('Vous avez selectionné : ', device_name)
        for d in devices['devices']:
            d['name'] = d['name'].replace('’', '\'')
            if d['name'] == device_name:
                self.deviceID = d['id']
                break
        self.active = False
        self.activeCheck()


    def setVolume(self, markList):
        """
        Cette fonction sert à changer le volume dans le lecteur de Spotify.
        Elle récupère la distance entre le bout du pouce et le bout de l'index et retraite cette valeur pour avoir une étendue allant de  100.
        :param markList: la liste comprenant les valeurs x et y des 21 points de la main obtenus grâce à mediapipe.
        """
        xPouce, yPouce = markList[4][1], markList[4][2] ##on récupère le x et le y du bout du pouce (point n°4).
        xIndex, yIndex = markList[8][1], markList[8][2] ##on récupère le x et le y du bout de l'index (point n°8).
        longueur = math.hypot(xIndex-xPouce,yIndex-yPouce) ##on calcule la distance entre ces deux points.
        volume = int(abs(longueur-20)/2) ##on retraite la valeur de cette distance. On enlève 20 et on garde la valeur absolue car la distance minimale est généralement entre 10 et 20. On divise par 2 car la distance miximale est généralement entre 250 et 350.
        if volume > 100:
            volume = 100 ##en divisant par 2 on se retrouve avec des valeurs pouvant aller jusqu'à presque 200. on doit donc mettre un miximal de 100.
        self.sp.volume(volume, device_id=self.deviceID) ##on lance la fonction de modification du volume.

    def nextTrack(self):
        """
        Cette fonction sert à lancer la musique suivante d'une playlist.
        """
        self.sp.next_track(device_id=self.deviceID)

    def previousTrack(self):
        """
        Cette fonction sert à lancer la musique précédente d'une playlist.
        """
        self.sp.previous_track(device_id=self.deviceID)

    def playPauseTrack(self):
        """
        Cette fonction permet de lancer une chanson, ainsi que de faire play/pause.
        """
        self.activeCheck() ##regarde si une chanson est en cours de lecture. self.active est un booléen qui indique si la chanson est en cours de lecture.
        if self.active :
            self.sp.pause_playback(device_id=self.deviceID) ##si la chanson est en cours de lecture, cela veut dire que nous voulons faire pause.
        else:
            current = self.sp.current_playback() ##si il n'y a pas de chanson en cours de lecture, on regarde si il y a une chanson en mémoire.
            progression=0
            if current is not None :
                self.sp.start_playback(device_id=self.deviceID) ##si il y a une chanson en mémoire, on lance la lecture.
            else:
                toptracks = self.sp.current_user_top_tracks(limit=5) ##si il n'y a pas de chanson en mémoire, on récupère les 5 chansons préférées de l'utilisateur.
                current_uri=[]
                for i in range(0,5):
                    current_uri.append(toptracks['items'][i]['uri']) ##on récupère les uri des chansons de notre playlist préférées.
                print("Aucun morceau en cours de lecture. Lecture de vos 5 titres préférés.")
                self.sp.start_playback(device_id=self.deviceID, uris=current_uri, position_ms=progression) ##on lance la lecture de cette playlist préférée.

    def activeCheck(self):
        """
        Cette fonction vérifie si une chanson est en cours de lecture.
        """
        current = self.sp.current_user_playing_track()
        if current is not None:
            self.active = current['is_playing']
        else:
            self.active = False

"""
if you can't reach 100, bring your hand closer to the camera.
if you can't reach 0, move back your hand from camera.
"""