import time
import os
import numpy as np
import cv2
import win32api
import win32con
import win32gui
import mss
import mss.tools
from PIL import Image


#FIXME
#Front slash breaks single quote despite rawstring...
PATH = r'D:\github\GTA5AutonomusPlane'
FILENAME = r'\data'
FILENAME_COUNTER = 1

#Correction margins (appropriate screen capture)
CORR_LEFT = 8
CORR_TOP = 35
CORR_WIDTH = -20
CORR_HEIGHT = -45

PAUSED = False

#Countdown delay in seconds
DELAY = 5

#For "Extended" multi-screen mode, choose 0, others - select number of monitor
MONITOR_NUM = 0

#Number of frames + keys combinations per file
FILE_SIZE = 200
RESIZE = (180, 120)


#Do not touch, frame counter
COUNTER = 0

def capture_screenshot(monitorNum: int, dimensions: tuple):
    with mss.mss() as sct:
        mon = sct.monitors[monitorNum]
        rect = {
            "left": mon['left'] + dimensions[0] + CORR_LEFT,
            "top": mon['top'] + dimensions[1] + CORR_TOP,
            "width": dimensions[2] - dimensions[0] + CORR_WIDTH,
            "height": dimensions[3] - dimensions[1] + CORR_HEIGHT,
            "mon": monitorNum
            }
        
        sct_img = sct.grab(rect)

        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'RGBX')
        #return np.array(sct_img)

#TODO
#Add key list generator

def getKey():
    keys = [0, 0, 0, 0, 0]
    if win32api.GetAsyncKeyState(ord('W')):
        keys[0] = 1
    if win32api.GetAsyncKeyState(ord('A')):
        keys[1] = 1
    if win32api.GetAsyncKeyState(ord('S')):
        keys[2] = 1
    if win32api.GetAsyncKeyState(ord('D')):
        keys[3] = 1
    if win32api.GetAsyncKeyState(win32con.VK_SPACE):
        keys[4] = 1
    if win32api.GetAsyncKeyState(ord('R')):
        return False
    return keys


while os.path.isfile(f'{PATH}{FILENAME}{FILENAME_COUNTER}.npz'):
    print(f'{PATH}{FILENAME}{FILENAME_COUNTER}.npz exists')
    FILENAME_COUNTER += 1

print('Open GTA V, enter game and press "R" when ready to begin frames recording!')
print('Press "R" again to pause recording')

while True:
    if getKey() == False:
        print(getKey())
        break
    time.sleep(0.2)


WINDOW_DIMS = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
print('[*]window captured')
#print(WINDOW_DIMS)

print(f'Recording to file beginning from {FILENAME}{FILENAME_COUNTER}.npz')

collectedData = []
while True:
    if not PAUSED:
        tmp = time.time()
        frame = capture_screenshot(
            monitorNum=MONITOR_NUM,
            dimensions=WINDOW_DIMS
            )
        frame = frame.resize(RESIZE)
        frame = np.array(frame)

        cv2.imshow("test", frame)
        cv2.waitKey(1)

        keys = getKey()
        print(keys)
        print(time.time()-tmp)
        if not keys:
            print("-- PAUSED! --")
            PAUSED = True
            continue

        #Saving data into numpy array
        # [[frame1_keys, frame1_image], [frame2_keys, frame2_image], [frame3_keys, frame3_image], ...]
        collectedData.append([frame, keys])

        COUNTER += 1
        if COUNTER % FILE_SIZE == 0:
            np.savez_compressed(fr"{PATH}{FILENAME}{FILENAME_COUNTER}", collectedData)
            print(rf'========== SAVED to {PATH}{FILENAME}{FILENAME_COUNTER}! ==================')
            collectedData = []
            COUNTER = 0
            FILENAME_COUNTER += 1
    else:
        time.sleep(0.2)
        keys = getKey()
        if not keys:
            print("-- resumed! --")
            PAUSED = False
