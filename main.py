import cv2
import HandTracker as ht
import SpotifyHandController as shc

"""
client_id=""
client_secret=""
"""

client_id=''
client_secret=''

stream = cv2.VideoCapture(0)
tracker = ht.handTracker(detectionCon=0.7)
spot = shc.spotifyControl(client_id=client_id, client_secret=client_secret)
while True :
    success, frame = stream.read()
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    markList = tracker.findHands(frameRGB)
    if len(markList) != 0:
        tracker.process(spotifyControl=spot, markList = markList)
    cv2.imshow("Display", frameRGB)
    cv2.waitKey(1)