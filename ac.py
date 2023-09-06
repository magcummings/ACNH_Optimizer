import sqlite3
from sqlite3 import Error

times = ['t1','t2','t3','t4','t5','t6','t7','t8','t9','t10','t11','t12','t13','t14','t15','t16','t17','t18','t19','t20','t21','t22','t23','t24']
months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_all_creatures(conn,creature,month):

    cur = conn.cursor()
    cur.execute("SELECT "+ creature +"_name FROM "+ creature +" WHERE "+ month +" = 1")

    rows = cur.fetchall()

    count = 0
    for row in rows:
        print(row[0])
        count += 1


def select_all_creatures_time(conn,creature,month,time):

    cur = conn.cursor()
    cur.execute("SELECT "+ creature +"_name FROM "+ creature +" WHERE "+ month +" = 1 AND t"+time+" = 1")

    rows = cur.fetchall()
    count = 0
    for row in rows:
        print(row[0])
        count += 1


def best_time(conn,month,animal):
    cur = conn.cursor()
    mostMoney = 0
    listofall = []
    listofbest = []
    #find sums for all 24 hours in a specific month
    for t in range(24):
        cur.execute("SELECT SUM(price) FROM "+animal+" WHERE "+times[t]+" = 1 AND "+month+" = 1")
        rows = cur.fetchall()
        for row in rows:
             print(t+1)
             listofall.append([row[0],t+1])
             if(row[0]>mostMoney):
                 mostMoney = row[0]
    #changing times to am and pm since acnh is on the 12 hour clock
    for x in listofall:
         if x[0] == mostMoney:
            if(x[1] < 12):
                listofbest.append(str(x[1]) + "am")
            elif(x[1] == 12):
                listofbest.append("12pm")
            elif(x[1]%12 == 0):
                listofbest.append("12am")
            else:
                listofbest.append(str(x[1]%12) + "pm")    
    print(listofbest)



def find_creature(conn,month,animal,type):
    cur = conn.cursor()
    creature_av = []
    creature_amounts = []
    listOfLowest = []
    #80 is chosen as there are a max of 80 bugs,fish,sea creatures in the game
    lowestCreatureCount = 80
    #find sums for all 24 hours in a specific month
    cur.execute("SELECT t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24 FROM "+animal+" WHERE "+animal+"_name = '"+type+"' AND "+month+" = 1")
    rows = cur.fetchall()
    print(rows)
    for hour in range(24):
        if(rows[0][hour] == 1):
            creature_av.append(hour+1)
    for times in creature_av:
        cur.execute("SELECT COUNT("+animal+"_name) FROM "+animal+" WHERE t"+str(times)+" = 1 AND "+month+" = 1")
        rows = cur.fetchall()
        for row in rows:
             creature_amounts.append([row[0],times])
             if(row[0]<lowestCreatureCount):
                 lowestCreatureCount = row[0]
    for amount in creature_amounts:
         if amount[0] == lowestCreatureCount:
            if(amount[1] < 12):
                listOfLowest.append(str(amount[1]) + "am")
            elif(amount[1] == 12):
                listOfLowest.append("12pm")
            elif(amount[1]%12 == 0):
                listOfLowest.append("12am")
            else:
                listOfLowest.append(str(amount[1]%12) + "pm")
    print("----------------------------")
    print("Available during:")   
    print(creature_av)
    print("----------------------------")
    print("Best times:")    
    print(listOfLowest)
    


def main():
    #database = r"C:/Users/margauxcummings/Desktop/csds395.db" 

    # create a database connection
    conn = create_connection('acnh.db')
    with conn:
        print("---------------------------------------")
        #select_all_bugs(conn)
        #select_all_fish(conn)
        #best_time_to_fish(conn,'sep')
        name = input("Please select a number: 1:max profit 2:find creature 3:find all creatures ")
        if name == "1":
            correct = False;
            while correct == False:
                mon = input("Please enter the month (ex: jan,feb,...)")
                if mon.strip() in ("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"): 
                    correct = True
                else:
                
                    print("Please use the three letter format")
            print("fish:")
            best_time(conn,mon,"fish")
            print("sea:")
            best_time(conn,mon,"sea")
            print("bug:")
            best_time(conn,mon,"bug")
        elif name == "2":
            print("---------------------------------------")
            correct = False
            while correct == False:
                creaturePrint = input("Do you want to look up a bug, sea creature, or fish? ")
                if creaturePrint in ("bug","sea creature","fish"):
                    creature = creaturePrint
                    correct = True
            correct = False
            while correct == False:
                mon = input("Please enter the month (ex: jan,feb,...)")
                if mon.strip() in ("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"): 
                    correct = True
                else:
                    print("Please use the three letter format")
            if(creature == "sea creature"):
                creature = "sea"
            #print all of creatures so users have a nice list
            select_all_creatures(conn,creature,mon)
            cr = input("What is the " + creaturePrint + " you want to look up? ")
            #need to add check to safe guard a misspelled creature
            find_creature(conn,mon,creature,cr.strip())
        elif name == "3":
            print("---------------------------------------")
            correct = False
            time = False
            while correct == False:
                creaturePrint = input("Do you want to look up a bug, sea creature, or fish? ")
                if creaturePrint in ("bug","sea creature","fish"):
                    creature = creaturePrint
                    correct = True
            correct = False
            while correct == False:
                mon = input("Please enter the month (ex: jan,feb,...)")
                if mon.strip() in ("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"): 
                    correct = True
                else:
                    print("Please use the three letter format")
            correct = False
            while correct == False:
                timeQuestion = input("Do you want them at a certain time? ")
                if timeQuestion.strip() in ("Yes", "No", "yes", "no", "y", "n"): 
                    correct = True
                    if timeQuestion.strip() in ("Yes", "yes", "y"):
                        time = True
                else:
                    print("Please enter either (yes/no)")
            if(creature == "sea creature"):
                creature = "sea"
            if(time):
                correct = False
                while correct == False:
                    timeQuestion = input("Please enter a time (ex: 12pm, 4am)")
                    if timeQuestion.strip() in ("1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am","12pm"): 
                        correct = True
                        timeStr = timeQuestion.strip()[0:-2]
                    elif timeQuestion.strip() in ("1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm", "12am"):
                        correct = True
                        timeStr = str(int(timeQuestion.strip()[0:-2]) + 12)
                    else:
                        print("Please use the correct format")
                select_all_creatures_time(conn,creature,mon,timeStr)
            else:
                select_all_creatures(conn,creature,mon)
        else:
            print("Please select options 1, 2, or 3")
            main()
        


if __name__ == '__main__':
    main()
