import datetime
from prettytable import PrettyTable
file = open('human_in.txt', 'r')

mlist = dict()
mlist['jan']=1
mlist['feb']=2
mlist['mar']=3
mlist['apr']=4
mlist['may']=5
mlist['jun']=6
mlist['jul']=7
mlist['aug']=8
mlist['sep']=9
mlist['oct']=10
mlist['nov']=11
mlist['dec']=12

#YEAR MON d 2:00 pm
def convert_from_human(raw, start_time, end_time):
    year = int(raw[2])
    mon = mlist[raw[1]]
    d = int(raw[0])
    date = datetime.date(year, mon, d)
    
    t = raw[3].split(':')
    h = int(t[0])
    m = int(t[1])
    twelve = raw[4]

    if twelve == "pm" and h != 12:
        h = (h+12)%24
    if twelve == "am" and h == 12:
        h = 0
    time = datetime.time(h,m)
    if time < start_time:
        time = start_time
    elif time > end_time:
        time = end_time
    
    return datetime.datetime.combine(date, time)

def debug(main):
    for x in main:
        print (x[0], " -- ", x[1])

#Initialising Start and End Dates and Times---------
while True:
    raw = file.readline().split()
    if raw != []:
        break
start = convert_from_human(raw[:5], datetime.time(0,0), datetime.time(23,59,59))
end =  convert_from_human(raw[5:], datetime.time(0,0), datetime.time(23,59,59))

#Start and end of period possible for event
start_day = start.date()
end_day = end.date()

#Earliest and latest the event can last for
start_time = start.time()
end_time = end.time()

start_datetime = datetime.datetime.combine(start_day, start_time)
end_datetime = datetime.datetime.combine(end_day, end_time)

main = [(start_datetime, 0)]

#blocks------------------------------------
weeklist = dict()
weeklist['sun'] = 6
weeklist['sat'] = 5
weeklist['fri'] = 4
weeklist['thurs'] = 3
weeklist['thur'] = 3
weeklist['thu'] = 3
weeklist['wed'] = 2
weeklist['tue'] = 1
weeklist['mon'] = 0

raw = file.readline().split()

blocked_days = set()
for day in raw:
    try:
        blocked_days.add(weeklist[day])
    
    except:
        print ("Error with", day, "ignoring that day...")
        continue
        
    
start_date = start_datetime.date()
end_date= end_datetime.date()

for single_date in (start_date + datetime.timedelta(n) for n in range(1000)):
    if single_date > end_date:
        break
    if single_date.weekday() in blocked_days:
        elements = (datetime.datetime.combine(single_date, start_time), 100)
        elemente = (datetime.datetime.combine(single_date, end_time), 0)
        main.append(elements)
        main.append(elemente)

#Building linked list------------------------------------
main.append((end_datetime, 0))

while True:
    raw = file.readline().split()
    if raw == []:
        continue
    if raw[0] == "break":
        break

    start = convert_from_human(raw[:5], start_time, end_time)
    end =  convert_from_human(raw[5:], start_time, end_time)
    
    start_in = end_in = False
    for index, dt in enumerate(main):
        if dt[0] == start:
            start_in = True
        elif dt[0] == start:
            end_in = True

    if not start_in:
        for index, element in enumerate(main):
            if element[0] < start and main[index+1][0] > start:
                main.insert(index+1, (start, element[1]))
    if not end_in:
        for index, element in enumerate(main):
            if element[0] < end and main[index+1][0] > end:
                main.insert(index+1,(end, element[1]))
        
    for index,element in enumerate(main):
        if index ==len(main) -1:
            break
        if ((element[0] > start or element[0] == start) and (element[0] < end)):
            new_element = (element[0], element[1]+1)
            main[index] = new_element

#debug(main)


#Analysis--------------------------------
datetimes = []
for i in range(100):
    datetimes.clear()
    for index, cur in enumerate(main):
        if cur[1] != i:
            continue
        if index == len(main) -1:
            break
        if main[index+1][0].date() > cur[0].date():
            #cur time to end of cur day

            start = cur[0]
            end = datetime.datetime.combine(cur[0].date(), end_time)
                
            if end > start and not (start.time() ==  start_time and end.time() == end_time):
                datetimes.append((end-start, start, end, "Half Day"))

                
                       
            #Full days
            start_day = main[index][0].date() + datetime.timedelta(days = 1)
            if start.time() ==  start_time and end.time() == end_time:
                start_day -= datetime.timedelta(days = 1)
            end_day = main[index+1][0].date() - datetime.timedelta(days = 1)
            if main[index+1][0].time() == end_time:
                end_day += datetime.timedelta(days = 1)
            if end_day > start_day or end_day == start_day:
                datetimes.append((end_day-start_day+datetime.timedelta(1), start_day, end_day, "Full Day"))

            #start of main[index+1][0].date() to main[index+1][0]
            start_day = main[index+1][0].date()
            start = datetime.datetime.combine(start_day, start_time)
            end = main[index+1][0]
            if end > start and not main[index+1][0].time() == end_time:
                datetimes.append((end-start, start,end, "Half Day"))
            
        else:
            start = cur[0]
            end = main[index+1][0]
            
            if end > start:
                if start.time() ==  start_time and end.time() == end_time:
                    datetimes.append ((end- start, start,end, "Full Day"))
                else:
                    datetimes.append ((end- start, start,end, "Half Day"))


    if len(datetimes)  == 0:
        break
    #datetimes.sort(reverse = True)
    print ("Possible Timings with", i, "people unavailable:")
    table = PrettyTable()
    table.field_names = ["Type", "Duration", "Start", "End"]
    for dt, s, e, r in datetimes:
        '''
        if isinstance == "<class 'datetime.datetime'>":
            print ("ho")
            '''
        table.add_row([r, dt, s.strftime('%d of %b %y, %I %M %p'), e.strftime('%d of %b %Y, %I %M %p')])
    print (table)
    

    

'''
Input Format
n
y m d h m       y m d h m


'''
