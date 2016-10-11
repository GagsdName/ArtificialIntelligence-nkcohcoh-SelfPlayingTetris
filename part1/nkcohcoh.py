import sys
import numpy as np
import copy
import re
#reading arguments

if len(sys.argv) != 5:
    print "\n Use the following format: python nkcohcoh.py [value of n] [value of k] [board in row major format] [time-limit for move]"
    sys.exit()

n = int(sys.argv[1])
k = int(sys.argv[2])
board_state_string = str(sys.argv[3])
time_limit = int(sys.argv[4])
boardStates=set()
max_string='w'*k
min_string='b'*k
max_wins=0
min_wins=0
    
    
def CTM(state):
	global n
	mat=np.array(list(state))
	fin_mat=mat.reshape(n,n)
	for i in fin_mat.tolist():
		print i
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
	sum_w = 0
	sum_b = 0
	hw = {}
	for i in range(2,k):
		st = 'w'*i
		hw[st] = 0
		p = re.compile(r'\b'+st+r'\b')
		for each in li:
			hw[st] += len(p.findall(each))*len(st)
		sr = 'b'*i
		hw[sr] = 0
		p = re.compile(r'\b'+sr+r'\b')
		for each in li:
			hw[sr] += len(p.findall(each))*len(sr)
	for i in hw:
		if 'w' in i:
			sum_w += hw[i]
		else:
			sum_b += hw[i]
	print "dict",hw
	print "white:",sum_w
	print "black:",sum_b
	return sum_b - sum_w
	
	
def minimax(state,min_flag):
	if chkTerminal(state):
		print "Terminal\n"
		return eval(state), state
	if min_flag:
		return min(minimax(succ) for succ in successors(state,(min_flag+1)%2))
	else:
		return max(minimax(succ) for succ in successors(state,(min_flag+1)%2))

print eval(CTM(board_state_string))
