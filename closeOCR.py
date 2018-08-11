import pyscreenshot as ImageGrab
import pytesseract
from PIL import Image
from functions import isnumber
from functions import get_all_numbers
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

def OCRcorner(cV):
    h1 = (cV[2] - cV[0]) * 0.05
    h2 = (cV[2] - cV[0]) * 0.26
    h3 = (cV[2] - cV[0]) * 0.74
    h4 = (cV[2] - cV[0]) * 0.95

    v1 = (cV[3] - cV[1]) * 0.905
    v2 = (cV[3] - cV[1]) * 0.955

    im1 = ImageGrab.grab(bbox=(cV[0] + h1, cV[1] + v1, cV[0] + h2, cV[1] + v2))
    im2 = ImageGrab.grab(bbox=(cV[0] + h3, cV[1] + v1, cV[0] + h4, cV[1] + v2))

    bigimage1 = im1.resize((int((h2 - h1) * 5), int((v2 - v1) * 5)), Image.NEAREST)
    bigimage2 = im2.resize((int((h4 - h3) * 5), int((v2 - v1) * 5)), Image.NEAREST)

    #bigimage1 = bigimage1.convert("RGB")
    #bigimage1.save("test.jpg","JPEG")

    image_string1 = pytesseract.image_to_string(bigimage1, config='-psm 7 -c tessedit_char_whitelist=0123456789')
    image_string2 = pytesseract.image_to_string(bigimage2, config='-psm 7 -c tessedit_char_whitelist=0123456789')

    r = [-1,-1,-1,-1,-1,-1]

    image_string1 = image_string1.replace(" ", "")
    image_string2 = image_string2.replace(" ", "")

    if len(image_string1) == 3 and isnumber(image_string1) == True:
        r[0] = int(image_string1[0])
        r[1] = int(image_string1[1])
        r[2] = int(image_string1[2])
    elif len(image_string1) == 4 and isnumber(image_string1) == True:
        r[0] = int(image_string1[0:2])
        r[1] = int(image_string1[2])
        r[2] = int(image_string1[3])

    if len(image_string2) == 3 and isnumber(image_string2) == True:
        r[3] = int(image_string2[0])
        r[4] = int(image_string2[1])
        r[5] = int(image_string2[2])
    elif len(image_string2) == 4 and isnumber(image_string2) == True:
        r[3] = int(image_string2[1])
        r[4] = int(image_string2[2])
        r[5] = int(image_string2[3:5])

    return r


def ShotsOn(cV):
    h1 = (cV[2] - cV[0]) * 0.26
    h2 = (cV[2] - cV[0]) * 0.33
    h3 = (cV[2] - cV[0]) * 0.67
    h4 = (cV[2] - cV[0]) * 0.74

    v1 = (cV[3] - cV[1]) * 0.855
    v2 = (cV[3] - cV[1]) * 0.905

    im1 = ImageGrab.grab(bbox=(cV[0] + h1, cV[1] + v1, cV[0] + h2, cV[1] + v2))
    im2 = ImageGrab.grab(bbox=(cV[0] + h3, cV[1] + v1, cV[0] + h4, cV[1] + v2))

    bigimage1 = im1.resize((int((h2 - h1) * 5), int((v2 - v1) * 5)), Image.NEAREST)
    bigimage2 = im2.resize((int((h4 - h3) * 5), int((v2 - v1) * 5)), Image.NEAREST)

    bigimage1 = bigimage1.convert("RGB")
    bigimage1.save("testOn1.jpg", "JPEG")
    bigimage2 = bigimage2.convert("RGB")
    bigimage2.save("testOn2.jpg", "JPEG")

    image_string1 = pytesseract.image_to_string(bigimage1, config='-psm 7 -c tessedit_char_whitelist=0123456789')

    image_string2 = pytesseract.image_to_string(bigimage2, config='-psm 7 -c tessedit_char_whitelist=0123456789')

    s = [-1,-1]

    if isnumber(image_string1):
        s[0] = int(image_string1)

    if isnumber(image_string2):
        s[1] = int(image_string2)

    return s


def ShotsOff(cV):
    h1 = (cV[2] - cV[0]) * 0.26
    h2 = (cV[2] - cV[0]) * 0.33
    h3 = (cV[2] - cV[0]) * 0.67
    h4 = (cV[2] - cV[0]) * 0.74

    v1 = (cV[3] - cV[1]) * 0.905
    v2 = (cV[3] - cV[1]) * 0.995

    im1 = ImageGrab.grab(bbox=(cV[0] + h1, cV[1] + v1, cV[0] + h2, cV[1] + v2))
    im2 = ImageGrab.grab(bbox=(cV[0] + h3, cV[1] + v1, cV[0] + h4, cV[1] + v2))

    bigimage1 = im1.resize((int((h2 - h1) * 5), int((v2 - v1) * 5)), Image.NEAREST)
    bigimage2 = im2.resize((int((h4 - h3) * 5), int((v2 - v1) * 5)), Image.NEAREST)

    bigimage1 = bigimage1.convert("RGB")
    bigimage1.save("testOff1.jpg","JPEG")
    bigimage2 = bigimage2.convert("RGB")
    bigimage2.save("testOff2.jpg", "JPEG")

    image_string1 = pytesseract.image_to_string(bigimage1, config='-psm 7 -c tessedit_char_whitelist=0123456789')

    image_string2 = pytesseract.image_to_string(bigimage2, config='-psm 7 -c tessedit_char_whitelist=0123456789')

    s = [-1, -1]

    if isnumber(image_string1):
        s[0] = int(image_string1)

    if isnumber(image_string2):
        s[1] = int(image_string2)

    return s



def OCRattacks(cV, possession):

    h1 = (cV[2] - cV[0]) * 0.04
    h2 = (cV[2] - cV[0]) * 0.94

    v1 = (cV[3] - cV[1]) * 0.75
    v2 = (cV[3] - cV[1]) * 0.82

    im1 = ImageGrab.grab(bbox=(cV[0] + h1, cV[1] + v1, cV[0] + h2, cV[1] + v2))

    bigimage1 = im1.resize((int((h2 - h1) * 5), int((v2 - v1) * 5)), Image.NEAREST)

    #bigimage1 = bigimage1.convert("RGB")
    #bigimage1.save("test.jpg", "JPEG")

    image_string1 = pytesseract.image_to_string(bigimage1, config='-psm 7 -c tessedit_char_whitelist=0123456789')

    nums = get_all_numbers(image_string1)

    for i in range(0,len(nums)):
        if isnumber(nums[i]) == True:
            nums[i] = int(nums[i])
        else:
            nums[i] = -1

    ap = [-1, -1, -1, -1, -1, -1]

    if possession == 0 and len(nums) == 4:
        for i in range(0, 3):
            ap[i] = nums[i]

    elif possession == 0 and len(nums) == 6:
        ap[0] = nums[0]
        ap[1] = nums[2]
        ap[2] = nums[3]
        ap[3] = nums[5]

    elif possession == 1 and len(nums) == 6:
        for i in range(0,5):
            ap[i] = nums[i]

    elif possession == 1 and len(nums) == 9:
        ap[0] = nums[0]
        ap[1] = nums[2]
        ap[2] = nums[3]
        ap[3] = nums[5]
        ap[4] = nums[6]
        ap[5] = nums[8]


    if ap[4] == -1 or ap[5] == -1:

        pos1 = float(int(ap[0])) * 1.5
        pos2 = float(int(ap[1])) * 1.5
        pos3 = float(int(ap[2]))
        pos4 = float(int(ap[3]))

        if (pos1 + pos2 + pos3 + pos4) != 0:
            ep1 = 100 * (pos1 + pos3) / (pos1 + pos2 + pos3 + pos4)
            ep2 = 100 - ep1

            est_pos1 = str(round(ep1))
            est_pos2 = str(round(ep2))

            ap[4] = int(est_pos1)
            ap[5] = int(est_pos2)

        else:
            ap[4] = 50
            ap[5] = 50

    return ap


def check_possession(cV):

    h1 = (cV[2] - cV[0]) * 0.04
    h2 = (cV[2] - cV[0]) * 0.94

    v1 = (cV[3] - cV[1]) * 0.70
    v2 = (cV[3] - cV[1]) * 0.75

    im1 = ImageGrab.grab(bbox=(cV[0] + h1, cV[1] + v1, cV[0] + h2, cV[1] + v2))

    bigimage1 = im1.resize((int((h2 - h1) * 5), int((v2 - v1) * 5)), Image.NEAREST)

    #bigimage1 = bigimage1.convert("RGB")
    #bigimage1.save("test.jpg", "JPEG")

    image_string1 = pytesseract.image_to_string(bigimage1, config='-psm 7')

    nums = get_all_numbers(image_string1)

    possession = 0

    if "oss" in image_string1 or "ssi" in image_string1 or "ion" in image_string1:
        possession=1

    return possession


def get_number(cV,xV,yV,pc):

    im1 = ImageGrab.grab(bbox=(cV[0] + xV[0], cV[1] + yV[0], cV[0] + xV[1], cV[1] + yV[1]))

    bigimage1 = im1.resize((int((xV[0] - xV[1]) * 2), int((yV[0] - yV[1]) * 2)), Image.NEAREST)
    bigimage2 = im1.resize((int((xV[0] - xV[1]) * 3), int((yV[0] - yV[1]) * 3)), Image.NEAREST)
    bigimage3 = im1.resize((int((xV[0] - xV[1]) * 5), int((yV[0] - yV[1]) * 5)), Image.NEAREST)

    image_string1 = pytesseract.image_to_string(bigimage1, config='-psm 7 -c tessedit_char_whitelist=0123456789')
    image_string2 = pytesseract.image_to_string(bigimage1, config='-psm 7 -c tessedit_char_whitelist=0123456789')
    image_string3 = pytesseract.image_to_string(bigimage1, config='-psm 7 -c tessedit_char_whitelist=0123456789')

    nm = -1

    if isnumber(image_string3):
        nm = int(image_string3)
    elif isnumber(image_string2):
        nm = int(image_string2)
    elif isnumber(image_string1):
        nm = int(image_string1)

    savestring = "pic" + str(pc) + ".jpg"

    bigimage1 = bigimage1.convert("RGB")
    bigimage1.save(savestring, "JPEG")

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

    bigimage1 = bigimage1.convert("RGB")
    bigimage1.save("pic1n.jpg", "JPEG")

    [min1, min2, min3] = ["-1","-1","-1"]

    if ":" in image_string1:
        i = image_string1.index(':')

        min1 = image_string1[0:i]
        sec1 = image_string1[i+1:len(image_string1)+1]

    if ":" in image_string2:
        i = image_string2.index(':')

        min2 = image_string2[0:i]
        sec2 = image_string2[i + 1:len(image_string2) + 1]

    if ":" in image_string3:
        i = image_string3.index(':')

        min3 = image_string3[0:i]
        sec3 = image_string3[i + 1:len(image_string3) + 1]

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
            if isnumber(sec1):
                sec = int(sec2)
        else:
            if isnumber(sec1):
                sec = int(sec1)
            elif isnumber(sec2):
                sec = int(sec2)
            elif isnumber(sec3):
                sec = int(sec3)

    return [min,sec]