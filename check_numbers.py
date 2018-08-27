from functions import isnumber
import datetime

def check_time(pre_val, pre_sec, start_time, start_min, c, matchID):

    if isnumber(pre_val):

        mins = []

        c.execute("SELECT time as dayTime FROM tradedata where ID = ?", [str(matchID)])
        dayTime = c.fetchall()
        if len(dayTime) > 0:
            currTime = max(dayTime)[0]
            c.execute("SELECT timeMin as times FROM tradedata where ID = ? and time = ?", [str(matchID),currTime])
            mins = c.fetchall()

        if len(mins) > 0:
            start_time = str(max(dayTime)[0])
            start_min = max(mins)[0]

        check_number = 1

        # Check if time numbers are reasonable
        if pre_val < 0 or pre_val > 120:
            check_number = 0

        d1 = datetime.datetime.strptime((start_time)[0:19], '%Y-%m-%d %H:%M:%S')
        d2 = datetime.datetime.strptime(str(datetime.datetime.now())[0:19], '%Y-%m-%d %H:%M:%S')

        diff = (d2 - d1).total_seconds() / 60
        exp_min = start_min + diff

        if len(mins) == 0 and pre_val in [0,1]:
            exp_min = 0

        if pre_val == 45 and pre_sec == 0:
            if start_min > 45:
                pass
        else:
            if abs(exp_min - pre_val) > 2:
                pre_val = -1
            else:
                print("Expected time " + str(round(exp_min, 1)) + " actual " + str(pre_val) + " time accepted")

    return pre_val

def test_number(nm,pc,min,c,matchID):

    val = 0

    t=0
    r=0

    pc_vect = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    var_vect = ["att1","att2","dng1","dng2","blank","blank","onT1","onT2","offT1","offT2","yel1","yel2","red1","red2","corn1","corn2"]
    t_vect = [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
    r_vect = [15,15,12,12,100,100,2,2,2,2,4,4,2,2,3,3]

    name = ""

    for i in range(0,len(pc_vect)):

        if pc == pc_vect[i]:

            name = var_vect[i]
            met = []

            if name != "blank":
                ex_string = "SELECT " + var_vect[i] + " as " + var_vect[i] + " FROM tradedata where ID = " + str(matchID) + " and timeMin > " + str(min-4) + " and " + var_vect[i] + " > -1"

                c.execute(ex_string)
                met = c.fetchall()

            if len(met) > 0:

                a=0
                for j in range(0,len(met)):
                    a += met[j][0]

                b = len(met)

                val = float(a)/b

            else:
                val = 0

            t = t_vect[i]
            r = r_vect[i]

    c.execute("SELECT timeMin as timeMin FROM tradedata where ID = ?", [str(matchID)])
    minl = c.fetchall()

    if len(minl) > 0:
        min_last = max(minl)[0]
    else:
        min_last = 0

    min_diff = min - min_last

    if val > 0:
        if nm >= val-1 and nm <= val+t*min_diff+r:
            pass
        else:
            print("Value is incorrect. Min val is " + str(val - 1) + ". Max val is " + str(val + t * min_diff + r) + ". Real val is " + str(nm))
            print("Expected value for " + name + " was " + str(val) + "")
            nm = -1
    else:
        if min <= 15:
            if nm <= min*t+r and nm >= min*t-r:
                pass
            else:
                print("Value is incorrect. Min val is " + str(min*t-r) + ". Max val is " + str(min*t+r) + ". Real val is " + str(nm))
                print("Expected value for " + name + " was " + str(val) + "")
                nm = -1

    return nm


















