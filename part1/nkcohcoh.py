import sys
import numpy as np
import copy
#reading arguments

n = int(sys.argv[1])
k = int(sys.argv[2])
board_state_string = str(sys.argv[3])
time_limit = int(sys.argv[4])
boardStates=set()
max_string='w'*k
min_string='b'*k
max_wins=0
min_wins=0


if len(sys.argv) != 5:
    print "\n Use the following format: python nkcohcoh.py [value of n] [value of k] [board in row major format] [time-limit for move]"
    sys.exit()
    
    
def CTM(state):
	global n
	mat=np.array(list(state))
	fin_mat=mat.reshape(n,n)
	return fin_mat.tolist()


#returns all rotations of a board state    
def rot_states(state):
	state_set=[]
	state_set.append(state)
	k=np.rot90(state)
	state_set.append(k.tolist())
	l=np.rot90(k)
	state_set.append(l.tolist())
	n=np.rot90(l)
	state_set.append(n.tolist())
	return state_set

#returns unique board States
def findUniqueStates(succ):
	boardStates=[]
	for state in succ:
		n = 0
		for rot in rot_states(state):
			if rot not in boardStates:
				n = n+1
		if n == 4:
			boardStates.append(state)
	return boardStates
	
	
#check for terminal state
def chkTerminaldiag(state):
	global max_wins
	global min_wins
	global n
	mat=np.array(state)
	a=mat.reshape(n,n)
	diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
	diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
	li=[]
	for n in diags:
		if not len(n.tolist())<k:
			li.append(''.join(n.tolist()))
	for each in li:
		if max_string in each:
			max_wins=1
			return True
		elif min_string in each:
			min_wins=1
			return True
	
	return False

def chkTerminalrow(state):
	global max_wins
	global min_wins
	global n
	Rowli=[]
	for i in range(n):
		Rowli.append(''.join(state[i]))
	for each in Rowli:
		if ''.join(max_string) in each:
			max_wins=1
			return True
		elif ''.join(min_string) in Rowli:
			min_wins=1
			return True
	return False

def chkTerminal(state):
	return chkTerminalrow(state) or chkTerminalrow(np.transpose(state)) or chkTerminaldiag(state)
	
def successors(state,_min):
	global n
	count = 0
	succ = []
	if _min:
		c = 'b'
	else:
		c = 'w'
	succ=replace(state,c)
	
	return succ

def replace(state,c):
	global n
	succlist=[]
	for i in range(n):
		for j in range(n):
			if state[i][j] == '.':
				temp=state[i][j]
				state[i][j] = c
				state1=copy.deepcopy(state)
				succlist.append(state1)
				state[i][j]=temp
	return succlist

def getall(state):
	global n
	li = []
	mat=np.array(state)
	a=mat.reshape(n,n)
	diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
	diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
	for item in diags:
		li.append(''.join(item.tolist()))
	for i in range(n):
		li.append(''.join(state[i]))
	for i in np.transpose(state).tolist():
		li.append(''.join(i))
	return li
		
#print chkTerminal(CTM(board_state_string))
#print successors(CTM(board_state_string),0)
def eval(state):
	li = getall(state)
	ss = ''.join(li)
	

eval(CTM(board_state_string))


