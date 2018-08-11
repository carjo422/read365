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
team2 = sys.argv[8]
betting_live = sys.argv[9]


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

global pc

while 1 > 0:

    c = conn.cursor()

    ### Run through all ten images to compare results ###

    fV = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    #Time

    [min, sec] = get_time([c1, c2, c3, c4])

    fV[0] = min
    fV[1] = sec

    #Attack, Dangerous, Possession
    fV[2] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.56, (c3 - c1) * 0.51], [(c4 - c2) * 0.585, (c4 - c2) * 0.52],2)
    fV[3] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.64, (c3 - c1) * 0.61], [(c4 - c2) * 0.585, (c4 - c2) * 0.52],3)
    fV[4] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.72, (c3 - c1) * 0.645], [(c4 - c2) * 0.585, (c4 - c2) * 0.52],4)
    fV[5] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.82, (c3 - c1) * 0.77], [(c4 - c2) * 0.585, (c4 - c2) * 0.52],5)
    fV[6] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.885, (c3 - c1) * 0.83], [(c4 - c2) * 0.585, (c4 - c2) * 0.52],6)
    fV[7] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.99, (c3 - c1) * 0.93], [(c4 - c2) * 0.585, (c4 - c2) * 0.52],7)

    #Corners, cards
    fV[16] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.54, (c3 - c1) * 0.51], [(c4 - c2) * 0.86, (c4 - c2) * 0.79],16)
    fV[14] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.58, (c3 - c1) * 0.55], [(c4 - c2) * 0.86, (c4 - c2) * 0.79],14)
    fV[12] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.62, (c3 - c1) * 0.59], [(c4 - c2) * 0.86, (c4 - c2) * 0.79],12)
    fV[17] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.91, (c3 - c1) * 0.87], [(c4 - c2) * 0.86, (c4 - c2) * 0.79],17)
    fV[15] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.945, (c3 - c1) * 0.90], [(c4 - c2) * 0.86, (c4 - c2) * 0.79],15)
    fV[13] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.985, (c3 - c1) * 0.945], [(c4 - c2) * 0.86, (c4 - c2) * 0.79],13)

    #Shots
    fV[8] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.66, (c3 - c1) * 0.64], [(c4 - c2) * 0.78, (c4 - c2) * 0.69],8)
    fV[9] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.85, (c3 - c1) * 0.83], [(c4 - c2) * 0.78, (c4 - c2) * 0.69],9)
    fV[10] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.66, (c3 - c1) * 0.64], [(c4 - c2) * 0.88, (c4 - c2) * 0.79],10)
    fV[11] = get_number([c1, c2, c3, c4], [(c3 - c1) * 0.85, (c3 - c1) * 0.83], [(c4 - c2) * 0.88, (c4 - c2) * 0.79],11)

    #Score
    [fV[18],fV[19]] = OCRscore([c1, c2, c3, c4])

    print(fV)

    #Store variables in sqlite database

    tt = 0

    sv = 1

    for i in range(0,len(fV)):
        if fV[1] == -1:
            sv = 0


    if sv == 1:
        if fV[0] > 0 or fV[1] > 0:
            print("Unsuccesful save of data")
            tt = 3
        else:
            print("Game hasn't started")
            tt = 5
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

        tt = 8


    sleep(tt)

    if betting_live == 1:
        print("You are betting live man")
