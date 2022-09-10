import pickle
import cv2
import csv
import numpy as np


# cv2.rectangle(img=frame_image,pt1=left_tap_zone[0],pt2=left_tap_zone[1],color=(255,0,0),thickness=0)
# cv2.rectangle(img=frame_image,pt1=right_tap_zone[0],pt2=right_tap_zone[1],color=(0,255,0),thickness=0)

# mean_pixel: output the mean pixel value in the zone
# zone:[(x1,y1),(x2,y2)] x:downward y:rightward
# img:input img
def vector_distance(vector1, vector2):
    npvec1 = np.array(vector1)
    npvec2 = np.array(vector2)
    distance = np.linalg.norm(npvec1 - npvec2)
    return distance


def mean_pixel(zone, img):
    y_start = zone[0][0]
    x_start = zone[0][1]
    y_end = zone[1][0]
    x_end = zone[1][1]
    zone_image = img[x_start:x_end, y_start:y_end]
    zone_B = zone_image[:, :, 0]
    zone_G = zone_image[:, :, 1]
    zone_R = zone_image[:, :, 2]
    mean_zone_B = np.mean(zone_B)
    mean_zone_G = np.mean(zone_G)
    mean_zone_R = np.mean(zone_R)
    mean_pixel_value = [mean_zone_B, mean_zone_G, mean_zone_R]
    return mean_pixel_value


# cv2.imshow(wname,frame_image)
# cv2.waitKey(0)

image_save = "./veryhard"
wname = "img"
left_tap_zone = [(236, 392), (520, 400)]
right_tap_zone = [(760, 392), (1044, 400)]
left_slide_zone = [(146, 360), (166, 370)]
right_slide_zone = [(1120, 360), (1130, 370)]
left_fast_tap_zone = [(530, 386), (546, 390)]
right_fast_tap_zone = [(730, 386), (746, 390)]
frame_image_left_none = cv2.imread(image_save + "/image104.jpg", cv2.IMREAD_COLOR)
frame_image_left_tap = cv2.imread(image_save + "/image103.jpg", cv2.IMREAD_COLOR)

frame_image_right_none = cv2.imread(image_save + "/image103.jpg", cv2.IMREAD_COLOR)
frame_image_right_tap = cv2.imread(image_save + "/image88.jpg", cv2.IMREAD_COLOR)

frame_image_both_press = cv2.imread(image_save + "/image8212.jpg", cv2.IMREAD_COLOR)
frame_image_both_tap = cv2.imread(image_save + "/image3848.jpg", cv2.IMREAD_COLOR)

frame_image_left_slide = cv2.imread(image_save + "/image5008.jpg", cv2.IMREAD_COLOR)
frame_image_right_slide = cv2.imread(image_save + "/image8278.jpg", cv2.IMREAD_COLOR)

frame_image_left_fast_tap = cv2.imread(image_save + "/image5743.jpg", cv2.IMREAD_COLOR)
frame_image_right_fast_tap = cv2.imread(image_save + "/image5748.jpg", cv2.IMREAD_COLOR)

# left no beat
mean_left_tap_none = mean_pixel(left_tap_zone, frame_image_left_none)
mean_left_slide_none = mean_pixel(left_slide_zone, frame_image_left_none)
mean_left_fast_tap_none = mean_pixel(left_fast_tap_zone, frame_image_left_none)

# left beats and types
mean_left_tap = mean_pixel(left_tap_zone, frame_image_left_tap)
mean_left_press = mean_pixel(left_tap_zone, frame_image_both_press)
mean_left_slide = mean_pixel(left_slide_zone, frame_image_left_slide)
mean_left_fast_tap = mean_pixel(left_fast_tap_zone, frame_image_left_fast_tap)

# right no beat
mean_right_tap_none = mean_pixel(right_tap_zone, frame_image_right_none)
mean_right_slide_none = mean_pixel(right_slide_zone, frame_image_right_none)
mean_right_fast_tap_none = mean_pixel(right_fast_tap_zone, frame_image_right_none)

# right beat and value
mean_right_tap = mean_pixel(right_tap_zone, frame_image_right_tap)
mean_right_press = mean_pixel(right_tap_zone, frame_image_both_press)
mean_right_slide = mean_pixel(right_slide_zone, frame_image_right_slide)
mean_right_fast_tap = mean_pixel(right_fast_tap_zone, frame_image_right_fast_tap)

# both tap
mean_left_both_tap = mean_pixel(left_tap_zone, frame_image_both_tap)
mean_right_both_tap = mean_pixel(right_tap_zone, frame_image_both_tap)

mean_left_tap_zone = [mean_left_tap_none, mean_left_tap, mean_left_press, mean_left_both_tap]
mean_left_slide_zone = [mean_left_slide_none, mean_left_slide]
mean_left_fast_tap_zone = [mean_left_fast_tap_none, mean_left_fast_tap]
mean_right_tap_zone = [mean_right_tap_none, mean_right_tap, mean_right_press, mean_right_both_tap]
mean_right_slide_zone = [mean_right_slide_none, mean_right_slide]
mean_right_fast_tap_zone = [mean_right_fast_tap_none, mean_right_fast_tap]


# tap_zone_value_list: a list including all mean value
# tap_value: the mean pixel value of current frame
# tap_zone_flag:
# 0:none
# 1:tap
# 2:press
def tap_zone_detection(tap_zone_value_list, tap_value):
    distance = []
    for value in tap_zone_value_list:
        distance.append(vector_distance(value, tap_value))
    min_tap_pos = distance.index(min(distance))

    if min_tap_pos == 0:
        tap_zone_flag = 0
    elif min_tap_pos == 1:
        tap_zone_flag = 1
    elif min_tap_pos == 2:
        tap_zone_flag = 2
    elif min_tap_pos == 3:
        # both tap is also a kind of tap
        tap_zone_flag = 1
    return tap_zone_flag


def slide_zone_detection(slide_zone_value_list, slide_value):
    distance = []
    for value in slide_zone_value_list:
        distance.append(vector_distance(value, slide_value))
    min_tap_pos = distance.index(min(distance))

    if min_tap_pos == 0:
        slide_zone_flag = 0
    elif min_tap_pos == 1:
        slide_zone_flag = 1

    return slide_zone_flag


def fast_tap_zone_detection(fast_tap_zone_value_list, fast_tap_value):
    distance = []
    for value in fast_tap_zone_value_list:
        distance.append(vector_distance(value, fast_tap_value))
    min_tap_pos = distance.index(min(distance))

    if min_tap_pos == 0:
        fast_tap_zone_flag = 0
    elif min_tap_pos == 1:
        fast_tap_zone_flag = 1

    return fast_tap_zone_flag


def action_determine(img):
    left_tap = mean_pixel(left_tap_zone, img)
    right_tap = mean_pixel(right_tap_zone, img)
    left_slide = mean_pixel(left_slide_zone, img)
    right_slide = mean_pixel(right_slide_zone, img)
    left_fast_tap = mean_pixel(left_fast_tap_zone, img)
    right_fast_tap = mean_pixel(right_fast_tap_zone, img)

    left_tap_flag = tap_zone_detection(mean_left_tap_zone, left_tap)
    right_tap_flag = tap_zone_detection(mean_right_tap_zone, right_tap)
    left_slide_flag = slide_zone_detection(mean_left_slide_zone, left_slide)
    right_slide_flag = slide_zone_detection(mean_right_slide_zone, right_slide)
    left_fast_tap_flag = fast_tap_zone_detection(mean_left_fast_tap_zone, left_fast_tap)
    right_fast_tap_flag = fast_tap_zone_detection(mean_right_fast_tap_zone, right_fast_tap)

    action = [0, 0]
    if left_tap_flag == 1:
        # tap
        action[0] = 1
    if left_tap_flag == 2:
        # press
        action[0] = 2
    if left_fast_tap_flag:
        # fast_tap(different zone)
        action[0] = 1
    if left_slide_flag:
        # slide
        action[0] = 3
        left_tap_flag = 0

    if right_tap_flag == 1:
        # tap
        action[1] = 1
    if right_tap_flag == 2:
        # press
        action[1] = 2
    if right_fast_tap_flag:
        # fast_tap(different zone)
        action[1] = 1
    if right_slide_flag:
        # slide
        action[1] = 3
        right_tap_flag = 0

    return action, left_tap_flag, right_tap_flag, left_slide_flag \
        , right_slide_flag


# using for remember the last tag
last_left_tap_flag = 0
last_right_tap_flag = 0
last_left_slide_flag = 0
last_right_slide_flag = 0
video_path = "veryhard.mp4"
cap = cv2.VideoCapture(video_path)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
frame_time_list = []
action_list = []

# img = cv2.imread(image_save + "/image7478.jpg", cv2.IMREAD_COLOR)
# action,left_tap_flag,right_tap_flag,left_slide_flag,right_slide_flag=action_determine(img)
# last_left_tap_flag=left_tap_flag
# last_right_tap_flag=right_tap_flag
# last_left_slide_flag=left_slide_flag
# last_right_slide_flag=right_slide_flag
# img = cv2.imread(image_save + "/image1169.jpg", cv2.IMREAD_COLOR)
# action,left_tap_flag,right_tap_flag,left_slide_flag,right_slide_flag=action_determine(img)
# if last_left_slide_flag==1:
#     action[0]=0
#     left_tap_flag=0
# if last_right_slide_flag==1:
#     action[1]=0
#     right_tap_flag=0
# last_left_tap_flag=left_tap_flag
# last_right_tap_flag=right_tap_flag
# last_left_slide_flag=left_slide_flag
# last_right_slide_flag=right_slide_flag
#
# img = cv2.imread(image_save + "/image1170.jpg", cv2.IMREAD_COLOR)
# action,left_tap_flag,right_tap_flag,left_slide_flag,right_slide_flag=action_determine(img)
# sleep(5)


for i in range(int(frame_count)):
    frame_time = cap.get(cv2.CAP_PROP_POS_MSEC)
    _, img = cap.read()
    action, left_tap_flag, right_tap_flag, left_slide_flag, right_slide_flag = action_determine(img)

    if last_left_slide_flag == 1:
        action[0] = 0
        left_tap_flag = 0
    if last_right_slide_flag == 1:
        action[1] = 0
        right_tap_flag = 0

    # fix the tiny error when the tap shifts as time passes
    if not (last_left_tap_flag == 1 or last_left_tap_flag == 2):
        if left_tap_flag == 2:
            left_tap_flag = 1
            action[0] = 1

    if not (last_right_tap_flag == 1 or last_right_tap_flag == 2):
        if right_tap_flag == 2:
            right_tap_flag = 1
            action[1] = 1

    # detemine when to release key
    if last_left_tap_flag == 2 and left_tap_flag == 0:
        action_list[-1][0] = 5
    if last_right_tap_flag == 2 and right_tap_flag == 0:
        action_list[-1][1] = 5

    # determine when to press key and keep it
    if left_tap_flag == 2 and last_left_tap_flag == 1:
        action_list[-1][0] = 4
    if right_tap_flag == 2 and last_right_tap_flag == 1:
        action_list[-1][1] = 4

    if not action[0] + action[1] == 0:
        frame_time_list.append(frame_time)
        action_list.append(action)
    last_left_tap_flag = left_tap_flag
    last_right_tap_flag = right_tap_flag
    last_left_slide_flag = left_slide_flag
    last_right_slide_flag = right_slide_flag

with open("vh_frame_time.pkl","wb") as f:
    pickle.dump(frame_time_list,f)
with open("vh_beatmap.pkl","wb") as f:
    pickle.dump(action_list,f)



#action label:
#0: none
#1: tap
#2: keep press
#3: slide
#4: start press
#5: release press
