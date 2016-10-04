import sys
n = int(sys.argv[1])
k = int(sys.argv[2])
board_state_string = ""
time_limit = 0

################ Function to read user-input ########################## 
def readInput():
    global n
    global k
    global board_state_string
    global time_limit
    
    n = int(sys.argv[1]) 
    k = int(sys.argv[2])
    board_state_string = str(sys.argv[3])
    time_limit = int(sys.argv[4])

if len(sys.argv) != 5:
    print "\n Use the following format: python nkcohcoh.py [value of n] [value of k] [board in row major format] [time-limit for move]"
else:
    readInput()
    print "\nn = ",n, "\nk = ", k, "\nboard_state = ", board_state_string, "\ntime_limit = ", time_limit


