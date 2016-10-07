import sys
import numpy as np

#reading arguments

n = int(sys.argv[1])
k = int(sys.argv[2])
board_state_string = str(sys.argv[3])
time_limit = int(sys.argv[4])
boardStates=set()
max_string=[]
min_string=[]
max_wins=0
min_wins=0

for i in range(k):
	max_string.append("w")
	min_string.append("b")


if len(sys.argv) != 5:
    print "\n Use the following format: python nkcohcoh.py [value of n] [value of k] [board in row major format] [time-limit for move]"
    sys.exit()
    
    
def CTM(state):
	mat=np.array(list(state))
	fin_mat=mat.reshape(3,3)
	return fin_mat


#returns all rotations of a board state    
def rot_states(state):
	state_set=[]
	state_set.append(state)
	k=np.rot90(m)
	state_set.append(k)
	l=np.rot90(k)
	state_set.append(l)
	n=np.rot90(l)
	state_set.append(n)
	return state_set

#returns unique board States
def findUniqueStates(succ):
	boardStates=set()
	for state in succ:
		if rot_states(state) not in boardStates:
			boardStates.add(state)
	return boardStates
	
	
#check for terminal state
def chkTerminaldiag(state):
	global max_wins
	global min_wins
	mat=np.array(list(string))
	a=mat.reshape(3,3)
	print a
	print
	diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
	diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
	li=[]
	for n in diags:
		if not len(n.tolist())<k:
			li.append(n.tolist())
	if max_string in li:
		max_wins=1
		return True
	elif min_string in li:
		min_wins=1
		return True
	
	return False

def chkTerminalcol(state):
	global max_wins
	global min_wins
	Rowli=[]
    for i in range(N):
    	Rowli.append(str(state[i])
	if str(max_string) in Rowli:
		max_wins=1
		return True
	elif str(min_string) in Rowli:
		min_wins=1
		return True
	
	return False
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
