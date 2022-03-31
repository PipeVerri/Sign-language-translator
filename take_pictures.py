# imports
import cv2
import mediapipe
import json

cam = cv2.VideoCapture(0)  # our camera
mp_hands = mediapipe.solutions.hands  # our hand recognition api


def take_picture_and_parse():
    with mp_hands.Hands(max_num_hands=1) as hands:
        img = cam.read()[1]  # get the image from the camera
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert it from BRG to RGB
        results = hands.process(img_rgb)  # parse it

        # if we detect hands, iterate over the list and parse everything
        if results.multi_hand_landmarks:
            data = {}
            for ind, hand in enumerate(results.multi_hand_landmarks):
                hand_landmark_temp = {}
                for ind2, lm in enumerate(hand.landmark):
                    hand_landmark_temp["lm" + str(ind2)] = {"x": lm.x, "y": lm.y, "z": lm.z}
                data["hand" + str(ind)] = hand_landmark_temp
            return data


while True:
    x = take_picture_and_parse()
    if x is not None:
        print(x)
        f = open("json_dump.json", "w")
        json.dump(x, f)
        f.close()
        break
