from functions import get_all_numbers
from functions import most_common

def re_check_numbers(input_text,firstwrite,matchID,c,fV,n_iter, possession):
    all_numbers = []

    # If time is missing

    for i in range(0, n_iter):
        all_numbers.append(get_all_numbers(input_text[i]))

    if firstwrite == 0 and fV[0] == -1:
        c.execute("SELECT timeMin as mins FROM footballdata where ID = ?", [str(matchID)])
        mins = c.fetchall()
        c.execute("SELECT timeSec as secs FROM footballdata where ID = ?", [str(matchID)])
        secs = c.fetchall()

        last_time = max(mins)
        last_secs = max(secs)

        last_match = 0
        last_within_one = 0

        for i in range(0, n_iter):

            if len(all_numbers) > 0 and len(last_time) > 0:

                if all_numbers[i][0] == last_time[0]:
                    last_match += 1
                    last_within_one += 1
                elif all_numbers[i][0] - last_time[0] < 2:
                    last_within_one += 1

                if last_match > 1:
                    fV[0] = all_numbers[i][0]
                    fV[1] = min(59, last_secs + 7)
                elif last_within_one > 2:
                    fV[0] = all_numbers[i][0]
                    fV[1] = 0

    anums = []

    # if attacks/possesion is missing

    if fV[2] == -1 or fV[3] == -1 or fV[4] == -1 or fV[5] == -1 or fV[6] == -1 or fV[7] == -1:
        tot_cells = 0
        n = 0
        for i in range(0, n_iter):
            text_list = input_text[i].splitlines()

            for j in range(0, len(text_list)):
                if "Attacks" in text_list[j] or "Danger" in text_list[j]:

                    if len(text_list[j + 1]) > 10:
                        anums.append(get_all_numbers(text_list[j + 1]))
                    elif len(text_list[j + 2]) > 10:
                        anums.append(get_all_numbers(text_list[j + 2]))
                    elif len(text_list[j + 3]) > 10:
                        anums.append(get_all_numbers(text_list[j + 3]))
                    elif len(text_list[j + 4]) > 10:
                        anums.append(get_all_numbers(text_list[j + 4]))


        obs1 = []
        obs2 = []
        obs3 = []
        obs4 = []
        obs5 = []
        obs6 = []

        # print(ave_cells)

        if possession == 0:
            for i in range(0, len(anums)):
                if len(anums[i]) == 4:
                    obs1.append(anums[i][0])
                    obs2.append(anums[i][1])
                    obs3.append(anums[i][2])
                    obs4.append(anums[i][3])

            if len(obs1) > 0:
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

                fV[6] = int(est_pos1)
                fV[7] = int(est_pos2)


        else:
            for i in range(0, len(anums)):
                if len(anums[i]) == 6:
                    obs1.append(anums[i][0])
                    obs2.append(anums[i][1])
                    obs3.append(anums[i][2])
                    obs4.append(anums[i][3])
                    obs5.append(anums[i][4])
                    obs6.append(anums[i][5])

            if len(obs1) > 0:
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

    if fV[8] == -1 or fV[9] == -1:
        for i in range(0, n_iter):
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
            for i in range(0, len(anums)):
                obs1.append(anums[i][0])
                obs2.append(anums[i][1])

            fV[8] = most_common(obs1)
            fV[9] = most_common(obs2)

    # if shots off target is missing

    if fV[10] == -1 or fV[11] == -1 or fV[12] == -1 or fV[13] == -1 or fV[14] == -1 or fV[15] == -1 or fV[16] == -1 or fV[
        17] == -1:
        for i in range(0, n_iter):
            text_list = input_text[i].splitlines()

            for j in range(0, len(text_list)):
                if "Off " in text_list[j] or "f Ta" in text_list[j]:
                    pass

    # If goals are missing

    if fV[18] == -1 or fV[19] == -1:
        for i in range(0, n_iter):
            text_list = input_text[i].splitlines()


    return fV