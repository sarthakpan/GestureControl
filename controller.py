# %%

import cv2
import imutils
from pynput.keyboard import Controller, Key

# %%
URL = "http://192.168.0.136:8080/video"
counter = 0
redLower = (0, 70, 110)
redUpper = (10, 255, 140)
width, height = 300, 600
# %%
cam = cv2.VideoCapture(0) #set URL if want to use IP Webcam
keyboard = Controller()

# %%


def event(direction):
    if direction == 'right':
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    elif direction == 'left':
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    elif direction == 'up':
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif direction == 'down':
        keyboard.press(Key.down)
        keyboard.release(Key.down)


# %%
while True:
    direction = ""
    ret_val, img = cam.read()
    img = cv2.flip(img, 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, redLower, redUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None
    cnts = imutils.grab_contours(cnts)
    cv2.rectangle(img, (50, 150), (250, 350), (255, 100, 100), 2)
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        cv2.circle(img, center, 5, (0, 0, 255), -1)
        if center[1] <= 150:
            direction = 'up'
        elif center[1] >= 350:
            direction = 'down'
        elif center[0] <= 50:
            direction = 'left'
        elif center[0] >= 250:
            direction = 'right'
        counter += 1
    if counter == 6:
        if direction != '':
            print(direction)
            event(direction)
        counter = 0
    cv2.imshow('my webcam', img)
    cv2.namedWindow('my webcam', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('my webcam', width, height)

    if cv2.waitKey(1) == 27:
        break  # esc to quit
cv2.destroyAllWindows()
