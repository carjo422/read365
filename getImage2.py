import os.path
import re

import pyscreenshot as ImageGrab
import pytesseract
from pynput.mouse import Listener

from functions import contains
from functions import get_isolated_number
from functions import most_common
from functions import normalize

global count_input
global time
global input_text

input_text = ["","","","","","","","","","","","","",""]
count_input = 0
input_coords = [0, 0, 0, 0]
csv_string = ''
head = 'ID,Odds1,OddsX,Odds2,Below25,Above25,Min,Sec,Att1,Att2,Dng1,Dng2,Pos1,Pos2,OnT1,OnT2,OffT1,OffT2,Yel1,Yel2,Red1,Red2,Corn1,Corn2,Score1,Score2'

import sys

odds1=float(sys.argv[2])
oddsX=float(sys.argv[3])
odds2=float(sys.argv[4])
odds25u=float(sys.argv[5])
odds25o=float(sys.argv[6])

matchID = sys.argv[1]
odds1X2 = normalize([odds1,oddsX,odds2])
odds25 = normalize([odds25u, odds25o])


strID = str(matchID)
pre_text = ""

data_folder = "match_data/"
file_to_open = data_folder + "testdata" + strID + ".txt"

if os.path.isfile(file_to_open):
    f = open(file_to_open, "r")
    pre_text = f.read()
    f.close()
else:
    f = open(file_to_open, "w+")
    f.write(head)
    f.close()

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

    if count_input == 4:
        listener.stop()

with Listener(on_click=on_click) as listener:
        listener.join()  ### Run script X times ###

pV = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
fV = ['0', '0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

while int(fV[0]) < 90 and fV[0]:

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
    fV = ['0','0','','','','','','','','','','','','','','','','','','']


    for t in range(0,10):

        # Variables to get

        # Split up text in lines and delete empty lines
        text_list = input_text[t].splitlines()
        #print(text_list)

        for k in range(0,len(text_list)):

            text_list[k] = text_list[k].replace("O", "0")
            text_list[k] = text_list[k].lower()

            if k > 0 and k < len(text_list):
                if text_list[k - 1] == " " or text_list[k-1].isdigit():
                    if text_list[k + 1] == " " or text_list[k+1].isdigit():

                        text_list[k] = text_list[k].replace("I", "1")

            if len(text_list[k]) < 4:
                text_list[k] = ""


        #Get time:
        time_row = 0
        for i in range(1,len(text_list)):
            if ":" in text_list[i]:
                if len(text_list[i]) == 5:
                    pV[0].append(text_list[i])
                    time_row = i


        #Find out if possession is included or not
            #PUT CODE HERE


        #Get attacks, dangerous attacks, possession
        for i in range(0, len(text_list)):
            if len(text_list[i]) > 6 and contains(text_list[i].upper(), "TARGET", 4) == False:

                text_list[i] = text_list[i].replace(">", "")
                text_list[i] = text_list[i].replace(")", "")
                text_list[i] = text_list[i].replace("(", "")
                text_list[i] = text_list[i].replace("C", "")

                #print(text_list[i])

                if len(get_isolated_number(text_list[i])) > 2:

                    list = get_isolated_number(text_list[i])
                    #print(list)

                    for j in range(0, len(list)):
                        list[j] = re.sub("[^0-9]", "", list[j])

                    if len(list) == 4:
                        pV[1].append(list[0])
                        pV[2].append(list[1])
                        pV[3].append(list[2])
                        pV[4].append(list[3])

                        pos1 = float(int(list[0])) * 1.5
                        pos2 = float(int(list[1])) * 1.5
                        pos3 = float(int(list[2]))
                        pos4 = float(int(list[3]))

                        ep1 = 100*(pos1+pos3)/(pos1+pos2+pos3+pos4)
                        ep2 = 100-ep1

                        est_pos1 = str(round(ep1))
                        est_pos2 = str(round(ep2))

                        pV[5].append(est_pos1)
                        pV[6].append(est_pos2)

                    elif len(list) == 6:
                        pV[1].append(list[0])
                        pV[2].append(list[1])
                        pV[3].append(list[2])
                        pV[4].append(list[3])
                        pV[5].append(list[4])
                        pV[6].append(list[5])

                    elif len(list) > 6:
                        pass


        #Get Shots on target and shot outside
        #print(text_list[-1])
        if len(text_list[-1]) > 10 and contains(text_list[-1], "Off Target", 6) == True:
            for k in range(0,len(text_list[-1])):
                text_list[-1] = text_list[-1].replace("l", "1")
                text_list[-1] = text_list[-1].replace("'", "")
                text_list[-1] = text_list[-1].replace("´", "")
                text_list[-1] = text_list[-1].replace("‘", "")
                text_list[-1] = text_list[-1].replace(">", "")
                text_list[-1] = text_list[-1].replace(")", "")
                text_list[-1] = text_list[-1].replace("(", "")
                text_list[-1] = text_list[-1].replace("C", "")

                list = get_isolated_number(text_list[-1])

                if len(list) == 8:
                    pV[9] = list[3]
                    pV[10] = list[4]
                    pV[11] = list[2]
                    pV[12] = list[5]
                    pV[13] = list[1]
                    pV[14] = list[6]
                    pV[15] = list[0]
                    pV[16] = list[7]

        for i in range(0, len(text_list)):
            if len(text_list[i]) > 8 and contains(text_list[i], "On Target", 7) == True:
                list = get_isolated_number(text_list[i])

                if len(list) == 2:
                    pV[7] = list[0]
                    pV[8] = list[1]

        #Get score
        for i in range(0, time_row):
            if len(get_isolated_number(text_list[i])) > 1:
                pV[17].append(get_isolated_number(text_list[i])[0])
                pV[18].append(get_isolated_number(text_list[i])[1])



    ### Create final suggested vector based on the five versions ###

    # Code to import last files and compare to check that results make sense

    write_ready = 1

    if pV[0]:
        fV[0] = most_common(pV[0][:])[0:2]
        fV[1] = most_common(pV[0][:])[3:5]

    if not fV[0]:
        write_ready = 0

    for i in range(1,19):
        if len(pV[i][:]) > 1:
            fV[i+1] = most_common(pV[i][:])
        elif len(pV[i][:]) == 1:
            fV[i+1] = pV[i][0]

        if not fV[i]:
            write_ready = 0



    csv_string = str(matchID) + ',' + str(odds1X2[0]) + ',' + str(odds1X2[1]) + ',' + str(odds1X2[2]) + ',' + str(odds25[0]) + ',' + str(odds25[1])
    csv_string = csv_string + ',' + fV[0] + ',' + fV[1] + ',' + fV[2] + ',' + fV[3] + ',' + fV[4] + ',' + fV[5] + ',' + fV[6] + ',' + fV[7] + \
                 ',' + fV[8] + ',' + fV[9] + ',' + fV[10] + ',' + fV[11] + ',' + fV[12] + ',' + fV[13] + ',' + fV[14] + ',' + fV[15] + ',' + \
                     fV[16] + ',' + fV[17] + ',' + fV[18] + ',' + fV[19]

    print(fV)
    #print(pV)

    f = open(file_to_open,"r")
    pre_text = f.read()
    #print(pre_text)

    f.close()
    f = open(file_to_open, "w")

    if pre_text:
        f.write(pre_text)


    if write_ready == 1:
        f.write("\n")
        f.write(csv_string)

    f.close()

    if fV[0].isdigit() == False:
        fV[0] = '0'