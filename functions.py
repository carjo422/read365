from itertools import combinations
import math


########### Compare strings and give out a specifc percent based on how similar they are #########


def compare(string1, string2): #String 1&2 strings to compare

    ############################# HELP FUNCTIONS #################################

    ### Generate new binary combos when trying different movement combinations ###

    def add_iteration(test_combos, at_point, ref_data):

        if ref_data[at_point] > -1:

            test_combos[at_point] = test_combos[at_point] + 1

            if test_combos[at_point] > 1:
                test_combos[at_point] = 0

                if at_point > 0:
                    add_iteration(test_combos, at_point - 1, ref_data)

        else:
            if at_point > 0:
                add_iteration(test_combos, at_point - 1, ref_data)

        return test_combos

    ### From binary vector create movement vector for how characters moves ###

    def calc_iteration(binary, numbers):

        result = [0 for i in range(len(binary))]

        if binary[0] == 0:
            result[0] = 0
        else:
            result[0] = numbers[0]

        for i in range(1,len(binary)):
            if binary[i] == 0:
                result[i] = result[i-1]
            else:
                if numbers[i] > result[i-1]:
                    result[i] = numbers[i]
                else:
                    result[i] = result[i - 1]

        return result

    ### From movement vector get the new string ###

    def string_from_nums(numbers, match, ref):

        numbers_add = [0 for i in range(len(numbers))]

        numbers_add[0] = numbers[0]

        for i in range(1,len(numbers)):
            numbers_add[i] = numbers[i]-numbers[i-1]

        for i in range(0,len(numbers_add)):
            if numbers_add[i] > 0:
                if i == 0:
                    match = ref[0:numbers_add[i]] + match
                else:
                    match = match[0:i]+ref[i:i+numbers_add[i]]+ match[i:len(match)]


        return match

    ### Function that compare number of matches in string ###

    def compare_strings(new_string, ref):

        matches = 0

        for i in range(0, len(new_string)):
            if new_string[i] == ref[i]:
                matches += 1

        return matches


    ########################### ALGORITHM START ###############################

    ### Set all characters lower_case to simplify algorithm (i.e. A = a) ###

    string1 = string1.lower()
    string2 = string2.lower()

    ### If one of strings is empty return nothing ###

    lengths = [len(string1), len(string2)]

    if lengths[0] == 0 or lengths[1] == 0:
        return 0
    else:

        ### Set which string is compared to the other how, based on lenght ###

        if lengths[0] < lengths[1]:
            ref = string2
            match = string1
        else:
            ref = string1
            match = string2


        total_characters = len(ref)

        ### Step 1: Delete all characters with exact match at start of string ###

        cut_point = -1

        for i in range(0,len(match)):
            if ref[i] != match[i] and cut_point == -1:
                cut_point = i

        ref = ref[cut_point:len(ref)]
        match = match[cut_point:len(match)]

        matching_start = total_characters-len(ref)

        # Numbers of characters removed = cut_point

        ref_save = ref
        match_save = match



        ### Step 2: Add characters to string match to get more matches ###

        # Number of characters to add
        add_characters = len(ref)-len(match)

        if add_characters > 0:

            ### Array for where movements should take place in the string to minimize move for maximum match ###
            movements = [[-1 for i in range(add_characters+1)] for j in range(len(match))]

            ### Calculate how many steps each character can move to match with a similar character ###
            a = [0 for i in range(len(match))]


            for i in range(0,len(match)):
                for j in range(i,len(ref)):
                    if match[i] == ref[j]:
                        if (j-i) <= add_characters:

                            movements[i][a[i]] = (j-i)
                            a[i]=a[i]+1

            n_combos = 1

            for i in range(0,len(match)):
                if a[i] == 0:
                    a[i] = 1

                n_combos = n_combos*(a[i])

            ### What are the types of movements that can be done on each position which gives benefits to the algorithm ###

            char_movements = [[-1 for i in range(len(match))] for j in range(n_combos)]

            nl = 1
            ni = n_combos

            for i in range(0,len(match)):
                if a[i] == 1:
                    for j in range(0,n_combos):
                        char_movements[j][i] = movements[i][0]
                else:
                    nl=nl*a[i]
                    ni = int(ni/a[i])

                    for j in range(1,nl+1):

                        for k in range(1,ni+1):

                            index_n = (j-1)*ni+k

                            char_movements[index_n-1][i] = movements[i][(j-1) % (a[i])]


            ### Create variables for testing different solutions ###

            n_min = 0
            for i in range(0, len(match)):
                if char_movements[0][i] == -1:
                    n_min = n_min + 1

            test_iterations = int(math.pow(2, len(match)-n_min))

            test_combos = [0 for i in range(len(match))]
            test_number = [0 for i in range(len(match))]

            at_point = len(test_combos) - 1

            best_match = 0
            best_string = ""

            ### Find best matching string with the least moves ###

            for i in range(0,n_combos):

                for j in range(0,test_iterations):

                    add_iteration(test_combos, at_point, char_movements[:][i])
                    result = calc_iteration(test_combos, char_movements[:][i])
                    new_string = string_from_nums(result,match,ref)

                    matches = compare_strings(new_string,ref) # HÄR FUCKAR DET UPP ORDENTLIGT

                    if matches >= best_match:
                        best_match = matches
                        best_string = new_string

                    #Create 1/0 on each observation j


            ### Delete all matching characters ###

            match_comp = ""
            ref_comp = ""

            match = best_string
            ref = ref

            for i in range(0,len(match)-1):
                if match[i] != ref[i]:
                    match_comp = match_comp + match[i]
                    ref_comp = ref_comp + ref[i]

            match = match_comp
            ref = ref_comp

        matches_after_adds = total_characters-matching_start-len(ref)

        ### How many matches can be found but on different positions ###

        matches = 0
        comp_array = [0]*len(match)

        for i in range(0,len(match)-1):
            for j in range(0,len(ref)-1):
                if match[i] == ref[j] and comp_array[j] == 0:
                    comp_array[j] = 1
                    matches = matches + 1

        mixed_matches = matches


        no_match = total_characters - matching_start-matches_after_adds-mixed_matches

        #print(total_characters)
        #print(matching_start)
        #print(matches_after_adds)
        #print(add_characters)
        #print(mixed_matches)
        #print(no_match)

        match_score = (matching_start + (matches_after_adds-add_characters) + mixed_matches/2)/total_characters
        ##print(match_score)
        return match_score



#print(compare("Carl Jonsson","Kal Johnsson"))


import numpy as np

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #print (matrix)
    return (matrix[size_x - 1, size_y - 1])


import itertools
import operator

def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]

def get_all_numbers(string):

    list = []

    string = string.replace("\n","")
    string = string.replace(".","")
    string = string.upper()
    string = string.replace("I", "1")
    string = string.replace("'I", "1")
    string = string.replace("I", "1")

    maxcalc=-1

    for i in range(0,len(string)):
        if i > maxcalc:
            if i == 0:
                if isnumber(string[i]) and isnumber(string[i+1]) == False:
                    list.append(int(string[i]))
                    maxcalc = i
                elif isnumber(string[i:i+2]) and isnumber(string[i+2]) == False:
                    list.append(int(string[i:i+2]))
                    maxcalc = i+1
                elif isnumber(string[i:i + 3]) and isnumber(string[i+3]) == False:
                    list.append(int(string[i:i + 3]))
                    maxcalc = i+2

            if i > 0 and i < len(string)-3:
                if isnumber(string[i]) and isnumber(string[i+1]) == False and isnumber(string[i-1]) == False:
                    list.append(int(string[i]))
                    maxcalc = i
                elif isnumber(string[i:i + 2]) and isnumber(string[i+2]) == False and isnumber(string[i - 1]) == False:
                    list.append(int(string[i:i + 2]))
                    maxcalc = i+1
                elif isnumber(string[i:i + 3]) and isnumber(string[i+3]) == False and isnumber(string[i - 1]) == False:
                    list.append(int(string[i:i + 3]))
                    maxcalc = i+2

            if i == len(string)-2:
                if isnumber(string[i]) and isnumber(string[i + 1]) == False and isnumber(string[i - 1]) == False:
                    list.append(int(string[i]))
                    maxcalc = i
                elif isnumber(string[i:i + 2]) and isnumber(string[i - 1]) == False:
                    list.append(int(string[i:i + 2]))
                    maxcalc = i + 1

            if i == len(string) - 1:
                if isnumber(string[i]) and isnumber(string[i - 1]) == False:
                    list.append(int(string[i]))
                    maxcalc = i

            if i == len(string):
                if isnumber(string[i]) and isnumber(string[i - 1]) == False:
                    list.append(int(string[i]))
                    maxcalc = i

    return list

def get_isolated_number(string):

    list = []
    if len(string) > 6:
        for i in range(0, len(string)):

            if i == 0:
                if string[i].isdigit() and string[i + 1] == " ":
                    list.append(string[i])
                if string[i:i + 1].isdigit() and string[i + 2] == " ":
                    list.append(string[i:i + 2])
                if string[i:i + 2].isdigit() and string[i + 3] == " ":
                    list.append(string[i:i + 3])

                #if string[i].isdigit() and string[i+1].isdigit() == False and string[i+2] == " ":
                #    list.append(string[i])
                #if string[i].isdigit() and string[i + 2].isdigit() == False and string[i + 3] == " ":
                #    list.append(string[i:i+2])
                #if string[i].isdigit() and string[i + 3].isdigit() == False and string[i + 4] == " ":
                #    list.append(string[i:i+3])


            elif i == len(string)-1:
                if string[i].isdigit() and string[i-1] == " ":
                    list.append(string[i])

            elif i == len(string)-2:
                if string[i].isdigit() and string[i - 1] == " " and string[i + 1] == " ":
                    list.append(string[i+1])
                if string[i:i+2].isdigit() and string[i - 1] == " ":
                    list.append(string[i:i+2])

            elif i == len(string) - 3:
                if string[i].isdigit() and string[i - 1] == " " and string[i + 1] == " ":
                    list.append(string[i:i+1])
                if string[i:i + 2].isdigit() and string[i - 1] == " " and string[i + 2] == " ":
                    list.append(string[i:i + 2])
                if string[i:i + 3].isdigit() and string[i - 1] == " ":
                    list.append(string[i:i + 3])



            else:
                if string[i].isdigit():
                    if string[i-1] == " " and string[i+1] == " ":
                        list.append(string[i:i+1])
                    elif string[i - 1] == " " and string[i:i + 1].isdigit() and string[i + 2] == " ":
                        list.append(string[i:i+2])
                    elif string[i - 1] == " " and string[i:i + 2].isdigit() and string[i + 3] == " ":
                        list.append(string[i:i+3])

                    #if string[i - 1] == " " and string[i + 2].isdigit() == False and string[i+3] == " ":
                    #    list.append(string[i:i + 1])
                    #elif string[i - 1] == " " and string[i + 3].isdigit() == False and string[i + 4] == " ":
                    #    list.append(string[i:i + 2])
                    #elif string[i - 1] == " " and string[i + 4].isdigit() == False and string[i + 5] == " ":
                    #    list.append(string[i:i + 3])

    for i in range(0,len(list)):
        list[i] = list[i].replace("c", "")
        list[i] = list[i].replace("C", "")
        list[i] = list[i].replace("/", "")
        list[i] = list[i].replace("\.", "")
        list[i] = list[i].replace("<", "")
        list[i] = list[i].replace(">", "")
        list[i] = list[i].replace("(", "")
        list[i] = list[i].replace(")", "")

    return list



def normalize(odds):

    norm_total = 0

    for i in range(len(odds)):
        odds[i] = 1/odds[i]
        norm_total += odds[i]

    for i in range(len(odds)):
        odds[i] = round(odds[i] / norm_total,2)

    return odds

def contains(in_string, ref, p):

    true_return = 0

    if len(in_string) > len(ref):
        for i in range(0,len(in_string)-len(ref)):
            match = levenshtein(in_string[i:i+len(ref)],ref)

            if match < p:
                true_return = 1

        if true_return == 1:
            return True
        else:
            return False

    else:
        return False



def isnumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

