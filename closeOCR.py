import pyscreenshot as ImageGrab
import pytesseract
from PIL import Image
from functions import isnumber
from functions import get_all_numbers
from check_numbers import test_number
import numpy as np
from numpy import array

def OCRscore(cV):

    h1 = (cV[2] - cV[0]) * 0.715
    h2 = (cV[2] - cV[0]) * 0.74
    h3 = (cV[2] - cV[0]) * 0.75
    h4 = (cV[2] - cV[0]) * 0.775
    v1 = (cV[3] - cV[1]) * 0.21
    v2 = (cV[3] - cV[1]) * 0.295

    im1 = ImageGrab.grab(bbox=(cV[0] + h1, cV[1] + v1, cV[0] + h2, cV[1] + v2))
    im2 = ImageGrab.grab(bbox=(cV[0] + h3, cV[1] + v1, cV[0] + h4, cV[1] + v2))

    bigimage1 = im1.resize((int((h2 - h1) * 10), int((v2 - v1) * 10)), Image.NEAREST)
    bigimage2 = im2.resize((int((h4 - h3) * 10), int((v2 - v1) * 10)), Image.NEAREST)

    bigimage1 = bigimage1.convert("RGB")
    bigimage1.save("pic17n.jpg", "JPEG")

    bigimage2 = bigimage2.convert("RGB")
    bigimage2.save("pic16n.jpg", "JPEG")

    image_string1 = pytesseract.image_to_string(bigimage1, config='-psm 10 -c tessedit_char_whitelist=0123456789')
    image_string2 = pytesseract.image_to_string(bigimage2, config='-psm 10 -c tessedit_char_whitelist=0123456789')


    score1 = -1
    score2 = -1

    if isnumber(image_string1) == True:
        score1 = int(image_string1)
    if isnumber(image_string2) == True:
        score2 = int(image_string2)

    scoreResult = [score1,score2]
    return scoreResult

def OCRattacks(cV, min, c, matchID):

    h1 = (cV[2] - cV[0]) * 0.52
    h2 = (cV[2] - cV[0]) * 0.99

    v1 = (cV[3] - cV[1]) * 0.50
    v2 = (cV[3] - cV[1]) * 0.59

    im1 = ImageGrab.grab(bbox=(cV[0] + h1, cV[1] + v1, cV[0] + h2, cV[1] + v2))

    bigimage1 = im1.resize((int((h2 - h1) * 5), int((v2 - v1) * 5)), Image.NEAREST)

    image_string1 = pytesseract.image_to_string(bigimage1, config='-psm 7 -c tessedit_char_whitelist=0123456789')

    savestring = "./pics/Attacks/attack_string.jpg"
    bigimage1 = bigimage1.convert("RGB")
    bigimage1.save(savestring, "JPEG")

    nums = get_all_numbers(image_string1)

    for i in range(0,len(nums)):
        if isnumber(nums[i]) == True:
            nums[i] = int(nums[i])
        else:
            nums[i] = -1

    ap = [-1, -1, -1, -1, -1, -1]

    if len(nums) == 6:
        for i in range(0,6):
            ap[i] = nums[i]

    elif len(nums) == 9:
        ap[0] = nums[0]
        ap[1] = nums[2]
        ap[2] = nums[3]
        ap[3] = nums[5]
        ap[4] = nums[6]
        ap[5] = nums[8]

    elif len(nums) == 7 or len(nums) == 8:

        ap[0] = nums[0]

        for i in range(1, 2):
            if test_number(nums[i], 3, min, c, matchID) > -1:
                ap[1] = nums[i]
        for i in range(2, 3):
            if test_number(nums[i], 4, min, c, matchID) > -1:
                ap[2] = nums[i]
        for i in range(3, 5):
            if test_number(nums[i], 5, min, c, matchID) > -1:
                ap[3] = nums[i]
        for i in range(4, 7):
            if len(nums) > i:
                if test_number(nums[i], 6, min, c, matchID) > -1:
                    ap[4] = nums[i]
        for i in range(5, 7):
            if len(nums) > i:
                if test_number(nums[i], 7, min, c, matchID) > -1:
                    ap[5] = nums[i]

    ap[0] = test_number(ap[0], 2, min, c, matchID)
    ap[1] = test_number(ap[1], 3, min, c, matchID)
    ap[2] = test_number(ap[2], 4, min, c, matchID)
    ap[3] = test_number(ap[3], 5, min, c, matchID)
    ap[4] = test_number(ap[4], 6, min, c, matchID)
    ap[5] = test_number(ap[5], 7, min, c, matchID)

    if ap[4] + ap[5] != 100:
        ap[4] = -1
        ap[5] = -1

    return ap


def get_number(cV,xV,yV,pc,c,min,matchID):

    def test_coords(x_diff):
        im1 = ImageGrab.grab(bbox=(cV[0] + xV[0]+x_diff, cV[1] + yV[0], cV[0] + xV[1]+x_diff, cV[1] + yV[1]))

        bigimage1 = im1.resize((int((xV[0] - xV[1]) * 2), int((yV[0] - yV[1]) * 2)), Image.NEAREST)
        bigimage2 = im1.resize((int((xV[0] - xV[1]) * 3), int((yV[0] - yV[1]) * 3)), Image.NEAREST)
        bigimage3 = im1.resize((int((xV[0] - xV[1]) * 5), int((yV[0] - yV[1]) * 5)), Image.NEAREST)

        image_string1 = pytesseract.image_to_string(bigimage1, config='-psm 7 -c tessedit_char_whitelist=0123456789')
        image_string2 = pytesseract.image_to_string(bigimage2, config='-psm 7 -c tessedit_char_whitelist=0123456789')
        image_string3 = pytesseract.image_to_string(bigimage3, config='-psm 7 -c tessedit_char_whitelist=0123456789')

        nm = -1

        if isnumber(image_string3):
            nm = int(image_string3)
        elif isnumber(image_string2):
            nm = int(image_string2)
        elif isnumber(image_string1):
            nm = int(image_string1)

        if pc in [2,3,4,5,6,7]:
            category = "Attacks"
        elif pc in [8,9,10,11]:
            category = "Shots"
        elif pc in [16,17]:
            category = "Corners"
        elif pc in [12, 13, 14, 15]:
            category = "Shots"

        if x_diff != 0:
            savestring = "./pics/" + category + "/" + str(matchID) + "-" + str(pc) + "-" + str(x_diff) + ".jpg"
            bigimage1 = bigimage1.convert("RGB")
            bigimage1.save(savestring, "JPEG")

        nm = test_number(nm,pc,min,c,matchID)

        return nm

    nm = test_coords(0)

    if nm > -1:
        pass
    else:
        print("Trying other coords")

        nm = test_coords(0.01)
        if nm > -1:
            pass
        else:
            nm = test_coords(-0.01)
            if nm > -1:
                pass
            else:
                nm = test_coords(0.015)
                if nm > -1:
                    pass
                else:
                    nm = test_coords(-0.015)
                    if nm > -1:
                        pass
                    else:
                        nm = test_coords(0.02)
                        if nm > -1:
                            pass
                        else:
                            nm = test_coords(-0.02)
                            if nm > -1:
                                pass
                            else:
                                nm = test_coords(-0.025)

    return nm

def get_time(cV):

    xV = [(cV[2] - cV[0]) * 0.27, (cV[2] - cV[0]) * 0.22]
    yV = [(cV[3] - cV[1]) * 0.30, (cV[3] - cV[1]) * 0.245]

    im1 = ImageGrab.grab(bbox=(cV[0] + xV[0], cV[1] + yV[0], cV[0] + xV[1], cV[1] + yV[1]))

    bigimage1 = im1.resize((int((xV[0] - xV[1]) * 2), int((yV[0] - yV[1]) * 2)), Image.NEAREST)
    bigimage2 = im1.resize((int((xV[0] - xV[1]) * 3), int((yV[0] - yV[1]) * 3)), Image.NEAREST)
    bigimage3 = im1.resize((int((xV[0] - xV[1]) * 5), int((yV[0] - yV[1]) * 5)), Image.NEAREST)

    image_string1 = pytesseract.image_to_string(bigimage1, config='-psm 7')
    image_string2 = pytesseract.image_to_string(bigimage2, config='-psm 7')
    image_string3 = pytesseract.image_to_string(bigimage3, config='-psm 7')

    bigimage3 = bigimage3.convert("RGB")
    bigimage3.save("pic1n.jpg", "JPEG")

    [min1, min2, min3] = ["-1", "-1", "-1"]
    [sec1, sec2, sec3] = ["-1", "-1", "-1"]


    if ":" in image_string1:
        i = image_string1.index(':')

        min1 = image_string1[0:i]
        sec1 = image_string1[i+1:len(image_string1)+1]

    elif len(image_string1) == 5:
        min1 = image_string1[0:2]
        sec1 = image_string1[3:5]


    if ":" in image_string2:
        i = image_string2.index(':')

        min2 = image_string2[0:i]
        sec2 = image_string2[i + 1:len(image_string2) + 1]

    elif len(image_string2) == 5:
        min2 = image_string2[0:2]
        sec2 = image_string2[3:5]


    if ":" in image_string3:
        i = image_string3.index(':')

        min3 = image_string3[0:i]
        sec3 = image_string3[i + 1:len(image_string3) + 1]

    elif len(image_string3) == 5:
        min3 = image_string3[0:2]
        sec3 = image_string3[3:5]

    min = -1
    sec = -1

    if min1 == min2 and min2 == min3:
        if isnumber(min1):
            min = int(min1)
    elif min1 == min2:
        if isnumber(min1):
            min = int(min1)
    elif min1 == min3:
        if isnumber(min1):
            min = int(min1)
    elif min2 == min3:
        if isnumber(min2):
            min = int(min2)

    if min > -1:
        if sec1 == sec2 and sec2 == sec3:
            if isnumber(sec1):
                sec = int(sec1)
        elif sec1 == sec2:
            if isnumber(sec1):
                sec = int(sec1)
        elif sec1 == sec3:
            if isnumber(sec1):
                sec = int(sec1)
        elif sec2 == sec3:
            if isnumber(sec2):
                sec = int(sec2)
        else:
            if isnumber(sec1):
                sec = int(sec1)
            elif isnumber(sec2):
                sec = int(sec2)
            elif isnumber(sec3):
                sec = int(sec3)

    return [min,sec]