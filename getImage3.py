import os.path

import pyscreenshot as ImageGrab
import pytesseract
import sqlite3
import time
from time import sleep
import numpy as np
import datetime

from functions import most_common
from functions import normalize
from functions import contains
from functions import isnumber
from functions import get_isolated_number
from functions import get_all_numbers

from closeOCR import OCRscore
from closeOCR import OCRcorner
from closeOCR import ShotsOn
from closeOCR import ShotsOff
from closeOCR import OCRattacks
from closeOCR import check_possession
from closeOCR import get_number
from closeOCR import get_time

from import_base_data import import_base_data
from check_numbers import check_numbers
from re_check_numbers import re_check_numbers

from pynput.mouse import Listener

global count_input
global time
global input_text
possession = -1

conn = sqlite3.connect('gamedata.db')
firstwrite = 1
n_iter = 10
c = conn.cursor()

#c.execute("""CREATE TABLE tradedata (
#                ID integer,
#                time,
#                team1,
#                team2,
#                odds1 real,
#                oddsX real,
#                odds2 real,
#                b25 real,
#                o25 real,
#                timeMin int,
#                timeSec int,
#                att1 int,
#                att2 int,
#                dng1 int,
#                dng2 int,
#                pos1 int,
#                pos2 int,
#                onT1 int,
#                onT2 int,
#                offT1 int,
#                offT2 int,
#                yel1 int,
#                yel2 int,
#                red1 int,
#                red2 int,
#                corn1 int,
#                corn2 int,
#                score1 int,
#                score2 int)""")

count_input = 0
input_text = ["","","","","","","","","","","","","",""]
fV = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
input_coords = [0, 0, 0, 0]

#System imports from terminal window
import sys

odds1=float(sys.argv[2])
oddsX=float(sys.argv[3])
odds2=float(sys.argv[4])
odds25u=float(sys.argv[5])
odds25o=float(sys.argv[6])
team1 = sys.argv[7]
team2 = sys.argv[7]


matchID = sys.argv[1]
odds1X2 = normalize([odds1,oddsX,odds2])
odds25 = normalize([odds25u, odds25o])


### Get images by selecting part of the screen

def on_click(x,y, button, pressed):

    global count_input
    global input_text
    global c1
    global c2
    global c3
    global c4


    count_input += 1

    if count_input%2 == 0:
        input_coords[int(count_input-2)] = x
        input_coords[int(count_input-1)] = y

    if count_input%4 == 0:

        c1 = input_coords[count_input - 4]
        c2 = input_coords[count_input - 3]
        c3 = input_coords[count_input - 2]
        c4 = input_coords[count_input - 1]

    print(count_input)
    if count_input == 4:
        listener.stop()

with Listener(on_click=on_click) as listener:
        listener.join()  ### Run script X times ###

while 1 > 0:

    c = conn.cursor()

    ### Run through all ten images to compare results ###

    fV = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    #Time

    [min, sec] = get_time([c1, c2, c3, c4])

    fV[0] = min
    fV[1] = sec

    #Attack, Dangerous, Possession
    fV[2] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.12, (c3 - c1) * 0.02], [(c4 - c2) * 0.80, (c4 - c2) * 0.75])
    fV[3] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.30, (c3 - c1) * 0.22], [(c4 - c2) * 0.80, (c4 - c2) * 0.75])
    fV[4] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.45, (c3 - c1) * 0.30], [(c4 - c2) * 0.80, (c4 - c2) * 0.75])
    fV[5] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.70, (c3 - c1) * 0.55], [(c4 - c2) * 0.80, (c4 - c2) * 0.75])
    fV[6] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.78, (c3 - c1) * 0.70], [(c4 - c2) * 0.80, (c4 - c2) * 0.75])
    fV[7] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.98, (c3 - c1) * 0.88], [(c4 - c2) * 0.80, (c4 - c2) * 0.75])

    #Corners, cards
    fV[16] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.12, (c3 - c1) * 0.02], [(c4 - c2) * 0.95, (c4 - c2) * 0.91])
    fV[14] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.19, (c3 - c1) * 0.12], [(c4 - c2) * 0.95, (c4 - c2) * 0.91])
    fV[12] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.26, (c3 - c1) * 0.19], [(c4 - c2) * 0.95, (c4 - c2) * 0.91])
    fV[17] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.98, (c3 - c1) * 0.88], [(c4 - c2) * 0.95, (c4 - c2) * 0.91])
    fV[15] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.88, (c3 - c1) * 0.81], [(c4 - c2) * 0.95, (c4 - c2) * 0.91])
    fV[13] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.81, (c3 - c1) * 0.74], [(c4 - c2) * 0.95, (c4 - c2) * 0.91])

    #Shots
    fV[8] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.35, (c3 - c1) * 0.26], [(c4 - c2) * 0.91, (c4 - c2) * 0.86])
    fV[9] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.74, (c3 - c1) * 0.65], [(c4 - c2) * 0.91, (c4 - c2) * 0.86])
    fV[10] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.35, (c3 - c1) * 0.26], [(c4 - c2) * 0.97, (c4 - c2) * 0.91])
    fV[11] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.74, (c3 - c1) * 0.65], [(c4 - c2) * 0.97, (c4 - c2) * 0.91])

    print(fV)

    #Store variables in sqlite database


    if -1 in fV:
        print("Unsuccesful save of data")
        n_iter = 10
    else:

        c.execute("""INSERT INTO
                    tradedata (
                        ID,time,team1,team2,odds1,oddsX,odds2,b25,o25,timeMin,timeSec,att1,att2,dng1,dng2,pos1,pos2,onT1,onT2,offT1,offT2,yel1,yel2,red1,red2,corn1,corn2,score1,score2)
                    VALUES
                        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (matchID,datetime.datetime.now(),team1, team2, odds1, oddsX, odds2, odds25u, odds25o, fV[0], fV[1], fV[2], fV[3], fV[4], fV[5], fV[6],
                   fV[7], fV[8], fV[9], fV[10], fV[11], fV[12], fV[13], fV[14], fV[15], fV[16], fV[17], fV[18], fV[19]))
        conn.commit()
        c.close()
        firstwrite = 0

        print("Succesful save to database")

        if n_iter > 5:
            n_iter -= 2
        elif n_iter > 2:
            n_iter -=1
        else:
            pass

    sleep(20-n_iter*2)

