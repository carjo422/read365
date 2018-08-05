from functions import isnumber

def check_numbers(fV, matchID,c,firstwrite):

    # Check if time makes sense
    if isnumber(fV[0]) and isnumber(fV[1]):
        c.execute("SELECT timeMin*100+timeSec as times FROM footballdata where ID = ?", [str(matchID)])
        times = c.fetchall()
        c.execute("SELECT timeMin as mins FROM footballdata where ID = ?", [str(matchID)])
        mins = c.fetchall()

        check_number = 1

        # Check if time numbers are reasonable
        if fV[0] < 0 or fV[0] > 100:
            check_number = 0
        if fV[1] < 0 or fV[1] > 59:
            check_number = 0

        if len(times) > 0:
            if fV[0] < max(mins)[0] and (fV[0] > 55 or fV[0] < 45):
                check_number = 0
            if fV[0] > max(mins)[0] + 2 and firstwrite == 0:
                check_number = 0

        if check_number == 0:
            fV[0] = -1
            fV[1] = -1

    # Check if attacks makes sense
    if isnumber(fV[2]) & isnumber(fV[3]):

        c.execute("SELECT att1 as mins FROM footballdata where ID = ?", [str(matchID)])
        att1 = c.fetchall()
        c.execute("SELECT att2 as mins FROM footballdata where ID = ?", [str(matchID)])
        att2 = c.fetchall()

        check_number = 1

        if fV[0] >= 0:
            if fV[2] > fV[0] * 3 + 20 or fV[3] > fV[0] * 3 + 20:
                check_number = 0
            if fV[2] + fV[3] + 10 < fV[0] * 0.7:
                check_number = 0

        if len(att1) > 0:
            if fV[2] < max(att1)[0]:
                check_number = 0
            if fV[3] < max(att2)[0]:
                check_number = 0

        if check_number == 0:
            fV[2] = -1
            fV[3] = -1

    # Check if dangerous attacks makes sense
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

        if len(dng1) > 0:
            if fV[2] < max(dng1)[0]:
                check_number = 0
            if fV[3] < max(dng2)[0]:
                check_number = 0

        if fV[2] > 0 & fV[3] > 0:
            if fV[4] > fV[2]:
                check_number = 0
            if fV[5] > fV[3]:
                check_number = 0

        if check_number == 0:
            fV[4] = -1
            fV[5] = -1

    # Check if possesion makes sense
    if isnumber(fV[6]) & isnumber(fV[7]):

        check_number = 1

        if fV[6] + fV[7] != 100:
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

        if len(onT1) > 0 and len(onT2) > 0:
            if fV[8] < max(onT1)[0]:
                check_number = 0
            if fV[9] < max(onT2)[0]:
                check_number = 0

                if fV[0] > 0:
                    if (fV[8] - max(onT1)[0]) > (fV[0] - max(mins)[0]) + 2:
                        check_number = 0
                    if (fV[9] - max(onT2)[0]) > (fV[0] - max(mins)[0]) + 2:
                        check_number = 0

        if fV[8] > fV[0] / 3 + 5 or fV[9] > fV[0] / 3 + 5:
            check_number = 0

        if check_number == 0:
            fV[8] = -1
            fV[9] = -1

    # Check if shots off target makes sense
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

    # Check if yellow cards makes sense
    if isnumber(fV[12]) & isnumber(fV[13]):

        c.execute("SELECT yel1 as mins FROM footballdata where ID = ?", [str(matchID)])
        yel1 = c.fetchall()
        c.execute("SELECT yel2 as mins FROM footballdata where ID = ?", [str(matchID)])
        yel2 = c.fetchall()

        check_number = 1

        if len(yel1) > 0 and len(yel2) > 0:
            if fV[12] < max(yel1)[0]:
                check_number = 0
            if fV[13] < max(yel2)[0]:
                check_number = 0

            if fV[0] > 0:
                if (fV[12] - max(yel1)[0]) > (fV[0] - max(mins)[0]) / 10 + 3:
                    check_number = 0
                if (fV[13] - max(yel2)[0]) > (fV[0] - max(mins)[0]) / 10 + 3:
                    check_number = 0

            if fV[12] > 10 or fV[13] > 10:
                check_number = 0

        if check_number == 0:
            fV[12] = -1
            fV[13] = -1

    # Check if red cards makes sense
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

    # Check if corners makes sense
    if isnumber(fV[16]) & isnumber(fV[17]):

        c.execute("SELECT corn1 as mins FROM footballdata where ID = ?", [str(matchID)])
        corn1 = c.fetchall()
        c.execute("SELECT corn2 as mins FROM footballdata where ID = ?", [str(matchID)])
        corn2 = c.fetchall()

        check_number = 1

        if len(corn1) > 0 and len(corn2) > 0:
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

    # Check if score makes sense
    if isnumber(fV[18]) & isnumber(fV[19]):

        c.execute("SELECT score1 as mins FROM footballdata where ID = ?", [str(matchID)])
        score1 = c.fetchall()
        c.execute("SELECT score2 as mins FROM footballdata where ID = ?", [str(matchID)])
        score2 = c.fetchall()

        check_number = 1

        if len(score1) > 0 and len(score2) > 0:
            if fV[18] < max(score1)[0]:
                check_number = 0
            if fV[19] < max(score2)[0]:
                check_number = 0

            if fV[0] > 0:
                if (fV[18] - max(score1)[0]) > (fV[0] - max(mins)[0]) / 20 + 2:
                    check_number = 0
                if (fV[19] - max(score2)[0]) > (fV[0] - max(mins)[0]) / 20 + 2:
                    check_number = 0

        if fV[18] > 20 or fV[19] > 20:
            check_number = 0

        if check_number == 0:
            fV[18] = -1
            fV[19] = -1

    return fV