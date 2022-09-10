import cv2
import os
import pickle
#TODO: 3 frames delay for each tap change.
video_path = "ingame_special.mp4"
image_save = "./ingame_special"
if not os.path.exists(image_save):
    os.mkdir(image_save)
cap = cv2.VideoCapture(video_path)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
for i in range(int(frame_count)):
    _,img = cap.read()
    cv2.imwrite(image_save + "/image{}.jpg".format(i), img)
