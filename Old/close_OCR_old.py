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