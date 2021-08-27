import cv2
import math
import HandTracker as ht
import spotipy as spot
from spotipy.oauth2 import SpotifyOAuth


class spotifyControl():
    def __init__(self, client_id, client_secret, scope='user-read-playback-state user-modify-playback-state user-top-read'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = 'https://example.com/callback/'
        self.scope = scope
        self.sp = spot.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                    client_secret=self.client_secret,
                                                    redirect_uri=self.redirect_uri,
                                                    scope=self.scope))
        devices = self.sp.devices()
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
        print('Enter the Id of the Device you want to use : ')
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
        xPouce, yPouce = markList[4][1], markList[4][2]
        xIndex, yIndex = markList[8][1], markList[8][2]
        longueur = math.hypot(xIndex-xPouce,yIndex-yPouce)
        volume = int(abs(longueur-20)/2)
        if volume > 100:
            volume = 100
        self.sp.volume(volume, device_id=self.deviceID)

    def nextTrack(self):
        self.sp.next_track(device_id=self.deviceID)

    def previousTrack(self):
        self.sp.previous_track(device_id=self.deviceID)

    def playPauseTrack(self):
        self.activeCheck()
        if self.active :
            self.sp.pause_playback(device_id=self.deviceID)
        else:
            current = self.sp.current_playback()
            progression=0
            if current is not None :
                current_uri = current['item']['uri']
                progression = current['progress_ms']
                progression = abs(int(progression))
            else:
                toptracks = self.sp.current_user_top_tracks(limit=5)
                current_uri = toptracks['items'][0]['uri']
                print("Aucun morceau en cours de lecture. Lecture de votre titre préféré.")
            current_uri = [current_uri]
            self.sp.start_playback(device_id=self.deviceID, uris=current_uri, position_ms=progression)

    def activeCheck(self):
        current = self.sp.current_user_playing_track()
        if current is not None:
            self.active = current['is_playing']
        else:
            self.active = False

"""
if you can't reach 100, bring your hand closer to the camera.
if you can't reach 0, move back your hand from camera.
"""