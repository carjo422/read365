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

from import_base_data import import_base_data
from check_numbers import check_numbers

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


#INTEGER,REAL,TEXT

count_input = 0
input_text = ["","","","","","","","","","","","","",""]
input_coords = [0, 0, 0, 0]

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

pV = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
fV = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

while int(fV[0]) < 90:

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


    ### Run through all five images to compare results ###

    pV = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    fV = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    for t in range(0,10):

        pV = import_base_data(pV,input_text,t)
        #print(input_text[t])

    ### Create final suggested vector based on the five versions ###

    # Code to import last files and compare to check that results make sense

    if pV[0]:
        if isnumber(most_common(pV[0][:])[0:2]) and isnumber(most_common(pV[0][:])[3:5]):
            fV[0] = int(most_common(pV[0][:])[0:2])
            fV[1] = int(most_common(pV[0][:])[3:5])
    print(pV)

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

    all_numbers = []

    for i in range(0,10):
        all_numbers.append(get_all_numbers(input_text[i]))

    #On missing values - Identify numbers to input

    #If time is missing

    if firstwrite == 0 and fV[0] == -1:
        c.execute("SELECT timeMin as mins FROM footballdata where ID = ?", [str(matchID)])
        mins = c.fetchall()
        c.execute("SELECT timeSec as secs FROM footballdata where ID = ?", [str(matchID)])
        secs = c.fetchall()

        last_time = max(mins)
        last_secs = max(secs)

        last_match = 0
        last_within_one = 0

        for i in range(0,10):
            if all_numbers[i][0] == last_time[0]:
                last_match +=1
                last_within_one +=1
            elif all_numbers[i][0] - last_time[0] < 2:
                last_within_one += 1

            if last_match > 1:
                fV[0] = all_numbers[i][0]
                fV[1] = min(59,last_secs+7)
            elif last_within_one > 2:
                fV[0] = all_numbers[i][0]
                fV[1] = 0

        if fV[0] == -1:
            pass #Do some more

    anums = []


    #if attacks/possesion is missing

    if 1==1:#fV[2] == -1 or fV[3] == -1 or fV[4] == -1 or fV[5] == -1 or fV[6] == -1 or fV[7] == -1:
        tot_cells = 0

        for i in range(0,10):
            text_list = input_text[i].splitlines()
            for j in range(0,len(text_list)):
                if "Attacks" in text_list[j] or "Danger" in text_list[j]:

                    if len(text_list[j+1]) > 10:
                        anums.append(get_all_numbers(text_list[j+1]))
                        tot_cells += len(get_all_numbers(text_list[j+1]))
                    elif len(text_list[j + 2]) > 10:
                        anums.append(get_all_numbers(text_list[j + 2]))
                        tot_cells += len(get_all_numbers(text_list[j + 2]))
                    elif len(text_list[j + 3]) > 10:
                        anums.append(get_all_numbers(text_list[j + 3]))
                        tot_cells += len(get_all_numbers(text_list[j + 3]))
                    elif len(text_list[j + 4]) > 10:
                        anums.append(get_all_numbers(text_list[j + 4]))
                        tot_cells += len(get_all_numbers(text_list[j + 4]))

        ave_cells = tot_cells / 10

        obs1 = []
        obs2 = []
        obs3 = []
        obs4 = []
        obs5 = []
        obs6 = []


        if ave_cells > 3 and ave_cells < 5.75:
            for i in range(0,len(anums)):
                if len(anums[i]) == 4:
                    obs1.append(anums[i][0])
                    obs2.append(anums[i][1])
                    obs3.append(anums[i][2])
                    obs4.append(anums[i][3])

            fV[2] = most_common(obs1)
            fV[3] = most_common(obs2)
            fV[4] = most_common(obs3)
            fV[5] = most_common(obs4)

            pos1 = float(fV[2]) * 1.5
            pos2 = float(fV[3]) * 1.5
            pos3 = float(fV[4])
            pos4 = float(fV[5])

            ep1 = 100 * (pos1 + pos3) / (pos1 + pos2 + pos3 + pos4)
            ep2 = 100 - ep1

            est_pos1 = str(round(ep1))
            est_pos2 = str(round(ep2))

            fV[7] = (est_pos1)
            fV[8] = (est_pos2)


        elif ave_cells >= 5.75:
            for i in range(0, len(anums)):
                if len(anums[i]) == 6:
                    obs1.append(anums[i][0])
                    obs2.append(anums[i][1])
                    obs3.append(anums[i][2])
                    obs4.append(anums[i][3])
                    obs5.append(anums[i][4])
                    obs6.append(anums[i][5])

            fV[2] = most_common(obs1)
            fV[3] = most_common(obs2)
            fV[4] = most_common(obs3)
            fV[5] = most_common(obs4)
            fV[6] = most_common(obs5)
            fV[7] = most_common(obs6)


    # if shots on target is missing

    anums = []

    obs1 = []
    obs2 = []

    if 2==2:
        for i in range(0, 10):
            text_list = input_text[i].splitlines()

            for j in range(0, len(text_list)):
                if "On T" in text_list[j] or "n Ta" in text_list[j]:
                    if len(get_all_numbers(text_list[j])) == 2:
                        anums.append(get_all_numbers(text_list[j]))
                    elif len(get_all_numbers(text_list[j])) > 2:
                        pass
                    else:
                        pass

        if len(anums) > 0:
            for i in range(0,len(anums)):
                obs1.append(anums[i][0])
                obs2.append(anums[i][1])

            fV[8] = most_common(obs1)
            fV[9] = most_common(obs2)

    # if shots off target is missing

    if 3 == 3:
        for i in range(0, 10):
            text_list = input_text[i].splitlines()

            for j in range(0, len(text_list)):
                if "Off " in text_list[j] or "f Ta" in text_list[j]:
                    pass#Continue code here when needed

    # If goals are missing

    if 7 == 7:
        for i in range(0, 10):
            text_list = input_text[i].splitlines()
            #print(text_list)

    #If values still missing - Find reasonable numbers to input

    #Store variables in sqlite database

    print(fV)

    c.execute("""INSERT INTO
                footballdata (
                    ID,odds1,oddsX,odds2,b25,o25,timeMin,timeSec,att1,att2,dng1,dng2,pos1,pos2,onT1,onT2,offT1,offT2,yel1,yel2,red1,red2,corn1,corn2,score1,score2)
                VALUES
                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (matchID,odds1,oddsX,odds2,odds25u,odds25o,fV[0],fV[1],fV[2],fV[3],fV[4],fV[5],fV[6],fV[7],fV[8],fV[9],fV[10],fV[11],fV[12],fV[13],fV[14],fV[15],fV[16],fV[17],fV[18],fV[19]))
    conn.commit()
    c.close()
    firstwrite = 0

