import os.path

import pyscreenshot as ImageGrab
import pytesseract
import sqlite3
import numpy as np

from functions import most_common
from functions import normalize
from functions import contains
from functions import isnumber
from functions import get_isolated_number
from functions import get_all_numbers

from closeOCR import OCRscore

from import_base_data import import_base_data
from check_numbers import check_numbers
from re_check_numbers import re_check_numbers

from pynput.mouse import Listener

global count_input
global time
global input_text

conn = sqlite3.connect('gamedata.db')
firstwrite = 1

#c.execute("""CREATE TABLE footballdata (
#                ID integer,
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
pV = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
fV = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
input_coords = [0, 0, 0, 0]

#System imports from terminal window
import sys

odds1=float(sys.argv[2])
oddsX=float(sys.argv[3])
odds2=float(sys.argv[4])
odds25u=float(sys.argv[5])
odds25o=float(sys.argv[6])

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

    input_text[0] = pytesseract.image_to_string(ImageGrab.grab(bbox=(c1, c2 + c2 * 0.2, c3, c4 + c2 * 0.2)))
    input_text[1] = pytesseract.image_to_string(ImageGrab.grab(bbox=(c1, c2 + c2 * 0.5, c3, c4 + c2 * 0.5)))
    input_text[2] = pytesseract.image_to_string(ImageGrab.grab(bbox=(c1, c2 - c2 * 0.8, c3, c4 - c2 * 0.2)))
    input_text[3] = pytesseract.image_to_string(ImageGrab.grab(bbox=(c1, c2 - c2 * 0.2, c3, c4 - c2 * 0.2)))
    input_text[4] = pytesseract.image_to_string(ImageGrab.grab(bbox=(c1, c2 - c2 * 0.3, c3, c4 - c2 * 0.3)))
    input_text[5] = pytesseract.image_to_string(ImageGrab.grab(bbox=(c1, c2 + c2 * 0.2, c3, c4 + c2 * 0.1)))
    input_text[6] = pytesseract.image_to_string(ImageGrab.grab(bbox=(c1, c2 + c2 * 0.5, c3, c4 + c2 * 0.2)))
    input_text[7] = pytesseract.image_to_string(ImageGrab.grab(bbox=(c1, c2 + c2 * 0.3, c3, c4 + c2 * 0.1)))
    input_text[8] = pytesseract.image_to_string(ImageGrab.grab(bbox=(c1, c2 + c2 * 0.4, c3, c4 + c2 * 0.2)))
    input_text[9] = pytesseract.image_to_string(ImageGrab.grab(bbox=(c1, c2 + c2 * 0.4, c3, c4 + c2 * 0.1)))


    ### Run through all ten images to compare results ###

    pV = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    fV = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    for t in range(0,10):
        pV = import_base_data(pV,input_text,t)
        #print(input_text[t])

    ### Create final suggested vector based on the five versions ###

    if pV[0]:
        if isnumber(most_common(pV[0][:])[0:2]) and isnumber(most_common(pV[0][:])[3:5]):
            fV[0] = int(most_common(pV[0][:])[0:2])
            fV[1] = int(most_common(pV[0][:])[3:5])

    for i in range(1,19):
        if len(pV[i][:]) > 1:
            if isnumber(most_common(pV[i][:])):
                fV[i+1] = int(most_common(pV[i][:]))
            else:
                fV[i + 1] = -1

        elif len(pV[i][:]) == 1:
            if isnumber((pV[i][0])):
                fV[i+1] = int(pV[i][0])
            else:
                fV[i+1] = -1

    print(fV)

    #Check variables

    fV = check_numbers(fV,matchID,c,firstwrite)

    print(fV)

    #All variables checked - Look for numbers to input where missing

    fV = re_check_numbers(input_text, firstwrite, matchID, c, fV)

    print(fV)

    fV = check_numbers(fV, matchID, c, firstwrite)

    print(fV)

    #If numbers still missing, try finding by close OCR

    OCRscore([c1,c2,c3,c4])


    #Store variables in sqlite database

    c.execute("""INSERT INTO
                footballdata (
                    ID,odds1,oddsX,odds2,b25,o25,timeMin,timeSec,att1,att2,dng1,dng2,pos1,pos2,onT1,onT2,offT1,offT2,yel1,yel2,red1,red2,corn1,corn2,score1,score2)
                VALUES
                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (matchID,odds1,oddsX,odds2,odds25u,odds25o,fV[0],fV[1],fV[2],fV[3],fV[4],fV[5],fV[6],fV[7],fV[8],fV[9],fV[10],fV[11],fV[12],fV[13],fV[14],fV[15],fV[16],fV[17],fV[18],fV[19]))
    conn.commit()
    c.close()
    firstwrite = 0

