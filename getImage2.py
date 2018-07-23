import os.path

import pyscreenshot as ImageGrab
import pytesseract
import sqlite3

from functions import most_common
from functions import normalize
from functions import contains
from functions import isnumber
from import_base_data import import_base_data
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

    #Check if time makes sense
    if isnumber(fV[0]) and isnumber(fV[1]):
        c.execute("SELECT timeMin*100+timeSec as times FROM footballdata where ID = ?", [str(matchID)])
        times = c.fetchall()
        c.execute("SELECT timeMin as mins FROM footballdata where ID = ?", [str(matchID)])
        mins = c.fetchall()

        check_number = 1

        #Check if time numbers are reasonable
        if fV[0] < 0 or fV[0] > 90:
            check_number = 0
        if fV[1] < 0 or fV[1] > 59:
            check_number = 0

        if len(times) > 1:
            if fV[0] < max(mins)[0] and (fV[0] > 55 or fV[0] < 45):
                check_number = 0
            if fV[0] > max(mins)[0]+2 and firstwrite == 0:
                check_number = 0

        if check_number == 0:
            fV[0] = -1
            fV[1] = -1


    #Check if attacks makes sense
    if isnumber(fV[2]) & isnumber(fV[3]):

        c.execute("SELECT att1 as mins FROM footballdata where ID = ?", [str(matchID)])
        att1 = c.fetchall()
        c.execute("SELECT att2 as mins FROM footballdata where ID = ?", [str(matchID)])
        att2 = c.fetchall()

        check_number = 1

        if fV[0] >= 0:
            if fV[2] > fV[0]*3+20 or fV[3] > fV[0]*3+20:
                check_number = 0
            if fV[2]+fV[3]+10 < fV[0]*0.7:
                check_number = 0

        if len(att1) > 1:
            if fV[2] < max(att1)[0]:
                check_number = 0
            if fV[3] < max(att2)[0]:
                check_number = 0

        if check_number == 0:
            fV[2] = -1
            fV[3] = -1


    #Check if dangerous attacks makes sense
    if isnumber(fV[4]) & isnumber(fV[5]):

        c.execute("SELECT dng1 as mins FROM footballdata where ID = ?", [str(matchID)])
        dng1 = c.fetchall()
        c.execute("SELECT dng2 as mins FROM footballdata where ID = ?", [str(matchID)])
        dng2 = c.fetchall()

        check_number = 1

        if fV[0] >= 0:
            if fV[4] > fV[0] * 2 + 20 or fV[5] > fV[0] * 2 + 20:
                check_number = 0
            if fV[4] + fV[5] + 10 < fV[0] * 0.4:
                check_number = 0

        if len(dng1) > 1:
            if fV[2] < max(dng1)[0]:
                check_number = 0
            if fV[3] < max(dng2)[0]:
                check_number = 0

        if fV[2] > 0 & fV[3] > 0:
            if fV[4]>fV[2]:
                check_number = 0
            if fV[5]>fV[3]:
                check_number = 0

        if check_number == 0:
            fV[4] = -1
            fV[5] = -1

    #Check if possesion makes sense
    if isnumber(fV[6]) & isnumber(fV[7]):

        check_number = 1

        if fV[6]+fV[7] != 100:
            check_number = 0

        if check_number == 0:
            fV[6] = -1
            fV[7] = -1

    # Check if shots on target makes sense
    if isnumber(fV[8]) & isnumber(fV[9]):

        c.execute("SELECT onT1 as mins FROM footballdata where ID = ?", [str(matchID)])
        onT1 = c.fetchall()
        c.execute("SELECT onT2 as mins FROM footballdata where ID = ?", [str(matchID)])
        onT2 = c.fetchall()

        check_number = 1

        if len(onT1) > 1 and len(onT2) > 1:
            if fV[8] < max(onT1)[0]:
                check_number = 0
            if fV[9] < max(onT2)[0]:
                check_number = 0

                if fV[0] > 0:
                    if (fV[8] - max(onT1)[0]) > (fV[0] - max(mins)[0]) + 2:
                        check_number = 0
                    if (fV[9] - max(onT2)[0]) > (fV[0] - max(mins)[0]) + 2:
                        check_number = 0

        if fV[8] > fV[0]/3+5 or fV[9] > fV[0]/3+5:
            check_number = 0



        if check_number == 0:
            fV[8] = -1
            fV[9] = -1

    #Check if shots off target makes sense
    if isnumber(fV[10]) & isnumber(fV[11]):

        c.execute("SELECT offT1 as mins FROM footballdata where ID = ?", [str(matchID)])
        offT1 = c.fetchall()
        c.execute("SELECT offT2 as mins FROM footballdata where ID = ?", [str(matchID)])
        offT2 = c.fetchall()

        check_number = 1

        if len(offT1) > 1 and len(offT2) > 1:
            if fV[10] < max(offT1)[0]:
                check_number = 0
            if fV[11] < max(offT2)[0]:
                check_number = 0

            if fV[0] > 0:
                if (fV[10] - max(offT1)[0]) > (fV[0] - max(mins)[0]) + 2:
                    check_number = 0
                if (fV[11] - max(offT2)[0]) > (fV[0] - max(mins)[0]) + 2:
                    check_number = 0

        if fV[10] > fV[0] / 3 + 5 or fV[11] > fV[0] / 3 + 5:
            check_number = 0

        if check_number == 0:
            fV[10] = -1
            fV[11] = -1

    #Check if yellow cards makes sense
    if isnumber(fV[12]) & isnumber(fV[13]):

        c.execute("SELECT yel1 as mins FROM footballdata where ID = ?", [str(matchID)])
        yel1 = c.fetchall()
        c.execute("SELECT yel2 as mins FROM footballdata where ID = ?", [str(matchID)])
        yel2 = c.fetchall()

        check_number = 1

        if len(yel1) > 1 and len(yel2) > 1:
            if fV[12] < max(yel1)[0]:
                check_number = 0
            if fV[13] < max(yel2)[0]:
                check_number = 0

            if fV[0] > 0:
                if (fV[12] - max(yel1)[0]) > (fV[0] - max(mins)[0])/10 + 3:
                    check_number = 0
                if (fV[13] - max(yel2)[0]) > (fV[0] - max(mins)[0])/10 + 3:
                    check_number = 0

            if fV[12] > 10 or fV[13] > 10:
                check_number = 0

        if check_number == 0:
            fV[12] = -1
            fV[13] = -1

    #Check if red cards makes sense
    if isnumber(fV[14]) & isnumber(fV[15]):

        c.execute("SELECT red1 as mins FROM footballdata where ID = ?", [str(matchID)])
        red1 = c.fetchall()
        c.execute("SELECT red2 as mins FROM footballdata where ID = ?", [str(matchID)])
        red2 = c.fetchall()

        check_number = 1

        if len(red1) > 1 and len(red2) > 1:
            if fV[14] < max(red1)[0]:
                check_number = 0
            if fV[15] < max(red2)[0]:
                check_number = 0

            if fV[0] > 0:
                if (fV[14] - max(red1)[0]) > (fV[0] - max(mins)[0]) / 10 + 3:
                    check_number = 0
                if (fV[15] - max(red2)[0]) > (fV[0] - max(mins)[0]) / 10 + 3:
                    check_number = 0

            if fV[14] > 4 or fV[15] > 4:
                check_number = 0

        if check_number == 0:
            fV[14] = -1
            fV[15] = -1

    #Check if corners makes sense
    if isnumber(fV[16]) & isnumber(fV[17]):

        c.execute("SELECT corn1 as mins FROM footballdata where ID = ?", [str(matchID)])
        corn1 = c.fetchall()
        c.execute("SELECT corn2 as mins FROM footballdata where ID = ?", [str(matchID)])
        corn2 = c.fetchall()

        check_number = 1

        if len(corn1) > 1 and len(corn2) > 1:
            if fV[16] < max(corn1)[0]:
                check_number = 0
            if fV[17] < max(corn2)[0]:
                check_number = 0

            if fV[0] > 0:
                if (fV[16] - max(corn1)[0]) > (fV[0] - max(mins)[0]) / 10 + 3:
                    check_number = 0
                if (fV[17] - max(corn2)[0]) > (fV[0] - max(mins)[0]) / 10 + 3:
                    check_number = 0

        if check_number == 0:
            fV[14] = -1
            fV[15] = -1

    #Check if score makes sense
    if isnumber(fV[18]) & isnumber(fV[19]):

        c.execute("SELECT score1 as mins FROM footballdata where ID = ?", [str(matchID)])
        score1 = c.fetchall()
        c.execute("SELECT score2 as mins FROM footballdata where ID = ?", [str(matchID)])
        score2 = c.fetchall()

        check_number = 1

        if len(score1) > 1 and len(score2) > 1:
            if fV[18] < max(score1)[0]:
                check_number = 0
            if fV[19] < max(score2)[0]:
                check_number = 0

            if fV[0] > 0:
                if (fV[18] - max(score1)[0]) > (fV[0] - max(mins)[0]) / 20 + 2:
                    check_number = 0
                if (fV[19] - max(score2)[0]) > (fV[0] - max(mins)[0]) / 20 + 2:
                    check_number = 0

        if score1 > 20 or score2 > 20:
            check_number = 0

        if check_number == 0:
            fV[18] = -1
            fV[19] = -1

    #All variables checked

    for i in range(0,1):
        

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

