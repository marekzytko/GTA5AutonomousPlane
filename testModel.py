import time
import tensorflow as tf
import numpy as np
import win32api
import win32gui
import mss
import mss.tools
from PIL import Image
import keyboard


#FIXME
PATH = r'D:\AutonomusGTA5Plane'
FILENAME = r'\data'
FILENAME_COUNTER = 1
#FIXME


#Threshold for taking probability as '1' (>threshold) or '0' (<threshold)
#e.g.: (pred = 0.18):
#prediction =  [0.01791193 0.03657481 0.07042961 0.31700492 0.26643234 0.13070646 0.04718563 0.11375429]
#becames:      [0          0          0          1          1          0          0          0]
THRESHOLD = 0.18

#Correction margins (appropriate screen capture)
CORR_LEFT = 8
CORR_TOP = 35
CORR_WIDTH = -20
CORR_HEIGHT = -45

PAUSED = True

#Countdown delay
DELAY = 5

#For "Extended" multi-screen mode, choose 0, others - select number of monitor
MONITOR_NUM = 0

#Number of frames + keys combinations per file
FILE_SIZE = 200
RESIZE = (180, 120)

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

def pressKey(key: list):

    for i in ('j', 'k', 'l', 'i', 'w', 'a', 's', 'd'):
        keyboard.release(i)

    if key[0] > THRESHOLD:
        keyboard.press('i')
        print("DOWN")
    if key[1] > THRESHOLD:
        keyboard.press('j')
        print("YAW LEFT")
    if key[2] > THRESHOLD:
        keyboard.press('k')
        print("UP")
    if key[3] > THRESHOLD:
        keyboard.press('l')
        print("YAW RIGHT")
    if key[4] > THRESHOLD:
        keyboard.press('w')
        print("SPEED")
    if key[5] > THRESHOLD:
        keyboard.press('a')
        print("LEFT")
    if key[6] > THRESHOLD:
        keyboard.press('s')
        print("SLOW DOWN")
    if key[7] > THRESHOLD:
        keyboard.press('d')
        print("RIGHT")


def getKey():
    if win32api.GetAsyncKeyState(ord('R')):
        return False
    else:
        return True

tf.config.experimental.set_memory_growth(tf.config.list_physical_devices('GPU')[0], True)    

print('loading model...')

model = tf.keras.models.load_model(rf'{PATH}\gta5.model')

print('model loaded!\n')
print('Open GTA V, enter game and press "R" when ready to start autonomus ride!')
print('Press "R" again to pause')

while True:
    if not getKey():
        break
    time.sleep(0.2)

WINDOW_DIMS = win32gui.GetWindowRect(win32gui.GetForegroundWindow())

while True:
    if not PAUSED:
        tmp = time.time()
        frame = capture_screenshot(
            monitorNum=MONITOR_NUM,
            dimensions=WINDOW_DIMS
            )

        frame = frame.resize(RESIZE)
        frame = np.asarray(frame)
        frame = frame.reshape(1, RESIZE[1], RESIZE[0], 3)

        pred = model.predict(
            x=frame,
            use_multiprocessing=True,
        )
        pred = pred[0]
        keys = getKey()
        
        #Comment out to see raw prediction
        #print('Prediction: ', pred)
        
        print('\n\n')
        pressKey(pred)
        if not keys:
            print("-- PAUSED! --")
            PAUSED = True
            continue
    else:
        time.sleep(0.2)
        keys = getKey()
        if not keys:
            print("-- resumed! --")
            PAUSED = False
