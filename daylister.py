def parse_schedule(schedule):
    if (not schedule[1].isupper()):
        return [schedule[0:2] , schedule[2:len(schedule)]]
    else:
        return [schedule[0] , schedule[1:len(schedule)]]
    
    
days = ["M" , "T" , "W" , "Th" ,"F", "S"]
for i in range(len(days)):
    for j in range(len(days)):
        if (i < j):
            print(parse_schedule(days[i] + days[j]))