import sys
import numpy as np
import copy
import re
import math
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
D = 0

def print_state(state):
	for i in state:
		print i
    
def CTM(state):
	#print "I am in CTM"
	global n
	mat=np.array(list(state))
	fin_mat=mat.reshape(n,n)
	#print type(n)
	#print_state(state)
	return fin_mat.tolist()
	
def calc_depth(time_limit):
	global D
	brnch_factor=board_state_string.count('.')
	#D=math.log(time_limit+1,brnch_factor)
	
#returns all rotations of a board state    
def rot_states(state):
	#print "I am in rot_states"
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
	#print "I am in findUnique"
	boardStates=[]
	for state in succ:
		n1 = 0
		for rot in rot_states(state):
			if rot not in boardStates:
				n1 = n1+1
		if n1 == 4:
			boardStates.append(state)
	return boardStates
	
	
#check for terminal state
def chkTerminaldiag(state):
	#print "I am in ChkDiag"
	global max_wins
	global min_wins
	global n
	mat=np.array(state)
	a=mat.reshape(n,n)
	diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
	diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
	li=[]
	for n1 in diags:
		if not len(n1.tolist())<k:
			li.append(''.join(n1.tolist()))
	for each in li:
		if max_string in each:
			max_wins=1
			return True
		elif min_string in each:
			min_wins=1
			return True
	#print type(n)
	return False

def chkTerminalrow(state):
	#print "I am in Chk row"
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
	#print "I am in Chk Terminal"
	if '.' in str(state):
		return chkTerminalrow(state) or chkTerminalrow(np.transpose(state)) or chkTerminaldiag(state)
	else:
		return True

def successors(state,_min):
	#print "I am in succesors"
	count = 0
	succ = []
	if _min:
		c = 'b'
	else:
		c = 'w'
	#print "suc state",state
	succ=replace(state,c)
	
	return findUniqueStates(succ)

def replace(state,c):
	#print "I am in replace", state
	global n
	succlist=[]
	#print type(n)
	for i in range(n):
		for j in range(n):
			if state[i][j] == '.':
				temp=state[i][j]
				state[i][j] = c
				state1=copy.deepcopy(state)
				succlist.append(state1)
				state[i][j]=temp
	#print type(n)
	return succlist

def getall(state):
	#print "I am in getall"
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
	#print type(n)
	return li

def evaluate(state):
	#print "I am in eval"
	li = getall(state)
	print li
	sum_w = 0
	sum_b = 0
	hw = {}
	for i in range(2,k+1):
		st = 'w'*i
		hw[st] = 0
		p = re.compile(st+'+')
		for each in li:
			if p.findall(each) and len(p.findall(each)[0]) == len(st):
				hw[st] += len(p.findall(each))*len(st)
		sr = 'b'*i
		hw[sr] = 0
		p = re.compile(sr+'+')
		for each in li:
			if p.findall(each) and len(p.findall(each)[0]) == len(sr):
				hw[sr] += len(p.findall(each))*len(sr)
	for i in hw:
		if 'w' in i:
			sum_w += hw[i]
		else:
			sum_b += hw[i]
	print "sum_b:", sum_b
	print "sum_w:", sum_w
	print "hw:", hw
	return sum_b - sum_w
	
def max_depth_reached(state,depth):
	global D
	if depth>D:
		return True
	return False

def max_play(state, alpha, beta,depth):
	#print "I am in MAX_PLAY"
	#print "max_play:", state
	if chkTerminal(state):
		#print "Terminal: ", evaluate(state)
		return evaluate(state)
		
	if max_depth_reached(state,depth):
		return evaluate(state)
		
	max_score = -9999999
	for succ in successors(state,0):
		score = min_play(succ, alpha, beta,depth+1)
		if max_score < score:
			max_score = score
		if max_score >= beta:
			return max_score
		alpha = max(alpha, max_score)
	return max_score

def min_play(state,alpha,beta,depth):
	#print "I am in MIN_PLAY"
	#print "min_play:", state
	if chkTerminal(state):
		#print "Terminal: ", evaluate(state)
		return evaluate(state)
		
	if max_depth_reached(state,depth):
		return evaluate(state)
		
	min_score = 9999999
	for succ in successors(state,1):
		score = max_play(succ, alpha, beta,depth+1)
		if min_score > score:
			min_score = score
		if min_score <= alpha:
			return min_score
		beta=min(beta,score)
	return min_score

def minimax(state,depth=0):
	if chkTerminal(state):
		#print "Terminal: ", evaluate(state)
		return evaluate(state), state
		
	if max_depth_reached(state,depth):
		return evaluate(state),state
		
	alpha=-99999999
	beta=999999999
	max_score = -9999999
	state1 = 0
	for succ in successors(state,0):
		score = min_play(succ, alpha, beta,depth+1)
		if max_score < score:
			max_score = score
			state1 = succ
		if max_score >= beta:
			return max_score, succ
		alpha = max(alpha, max_score)
	return max_score, succ

#for s in successors(CTM(board_state_string),0):
#	print_state(s)
#	print
print minimax(CTM(board_state_string))
#calc_depth(time_limit)
#print evaluate(CTM(board_state_string))
#print successors(CTM(board_state_string),0)
