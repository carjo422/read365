def import_base_data(pV,input_text,t):
    from functions import contains
    from functions import get_isolated_number
    from functions import isnumber
    import re

    # Variables to get

    # Split up text in lines and delete empty lines
    text_list = input_text[t].splitlines()
    #print(text_list)


    if len(text_list) > 0:
        #print(text_list)

        for k in range(0, len(text_list)):
            if len(text_list[k]) < 4:
                text_list[k] = ""


        for k in range(0,len(text_list)):

            text_list[k] = text_list[k].replace("O", "0")
            text_list[k] = text_list[k].upper()

            if k > 0 and k < len(text_list):
                if text_list[k - 1] == " " or text_list[k-1].isdigit():
                    if text_list[k + 1] == " " or text_list[k+1].isdigit():

                        text_list[k] = text_list[k].replace("I", "1")
                        text_list[k] = text_list[k].replace("'I", "1")
                        text_list[k] = text_list[k].replace("I", "1")

        #Get time:
        time_row = len(text_list)
        for i in range(1,len(text_list)):
            if ":" in text_list[i]:
                if len(text_list[i]) == 5:
                    pV[0].append(text_list[i])
                    time_row = i
                elif len(text_list[i]) > 5:
                    p = text_list[i].find(":")

                    if isnumber(text_list[i][p-2:p]):
                        pV[0].append(text_list[i][p-2:p+3])
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
        if len(text_list[i]) > 10 and contains(text_list[i], "OFF TARGET", 4) == True:
            for k in range(0,len(text_list[i])):
                text_list[i] = text_list[i].replace("l", "1")
                text_list[i] = text_list[i].replace("'", "")
                text_list[i] = text_list[i].replace("´", "")
                text_list[i] = text_list[i].replace("‘", "")
                text_list[i] = text_list[i].replace(">", "")
                text_list[i] = text_list[i].replace(")", "")
                text_list[i] = text_list[i].replace("(", "")
                text_list[i] = text_list[i].replace("C", "")

                list = get_isolated_number(text_list[-1])
                #print(list)

                if len(list) == 8:
                    pV[9].append(list[3])
                    pV[10].append(list[4])
                    pV[11].append(list[2])
                    pV[12].append(list[5])
                    pV[13].append(list[1])
                    pV[14].append(list[6])
                    pV[15].append(list[0])
                    pV[16].append(list[7])

        for i in range(0, len(text_list)):
            if len(text_list[i]) > 8 and contains(text_list[i], "ON TARGET", 4) == True and "OF" not in text_list[i] and "FF" not in text_list[i]:
                #print(text_list[i])
                list = get_isolated_number(text_list[i])

                if len(list) == 2:
                    pV[7].append(list[0])
                    pV[8].append(list[1])

                if len(list) == 3:
                    if list[1] == "0N":
                        pV[7].append(list[0])
                        pV[8].append(list[2])

        #Get score
        for i in range(0, time_row):
            #print(text_list[i])
            if len(get_isolated_number(text_list[i])) > 1:
                pV[17].append(get_isolated_number(text_list[i])[0])
                pV[18].append(get_isolated_number(text_list[i])[1])


    return pV