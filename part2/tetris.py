# Simple tetris program! v0.1
# D. Crandall, Sept 2016

from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys
import numpy as np

class HumanPlayer:
    def get_moves(self, piece, board):
        print "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
   
	#depth = 0
	#desired_depth = 6
	commands = [ "b", "n", "m"]
	#chance node
        def chance_layer(self,piece,actions, board):
		result_tuple = self.result(piece,board,actions)
		self.evaluation(result_tuple[0],(result_tuple[1],result_tuple[2]), board)
		#print "\nresult_tuple = ", result_tuple
		#print "\npiece = ", piece
		#print "\nactions = ", actions
		#print "\nsuccessor_piece = ", result_tuple[0]
		#print "\nnew_position = ", result_tuple[1], result_tuple[2]	
		return True
	#max node value
        def max_layer(self,piece,board):
		max_val = 0
		for action1 in self.commands:
			for action2 in self.commands:
				for action3 in self.commands:
					print (action1,action2,action3)
					chance_eval = self.chance_layer(piece,(action1,action2,action3), board)
					if chance_eval > max_val:
						max_val = chance_eval
                	
		print max_val
		return True
	#ExpectiMiniMax
	def get_choice(self,piece,board):
		desired_action = self.max_layer(piece,board)
		return desired_action 
	
	def get_space_chunks(self,row):
		c = 0
		chunk_positions = [] 
		chunk_lengths = []
		length = 0
		while c < len(row):
			if row[c] == " ":
				d = c
				length = 0
				chunk_positions.append(c)
				while d < len(row) and row[d] == " ":
					length+=1
					d+=1
				chunk_lengths.append(length)
				c = c+length+1
				#print "\n for row = ", row, " chunk length = ", length
			else:
				c+=1
		return (chunk_positions, chunk_lengths)	
				
	#evaluation function for a given state
	def evaluation(self,successor_piece,new_position, board):
		#evaluate piece
        	#board = tetris.get_board()
		#print "\nboard = ", boarid
		eval_points = 0
		constant_multiplier = 10	
		for row in board:
			chunk_tuple = self.get_space_chunks(row)
			for i in chunk_tuple[1]:
				if (tetris.check_collision((board,0),successor_piece, new_position[0], new_position[1])) and\
				 (len(successor_piece[len(successor_piece) - 1]) <= i):
					eval_points = constant_multiplier * (i - len(successor_piece[len(successor_piece) - 1]))
					print "\ni = ", i, " successor_piece = " ,successor_piece, " elligible for row =  ", row, " eval points = ", eval_points
			
			 
	def result(self,piece,board,actions):
		#print "\nactions:",actions
		#print "\nBefore Actions:", tetris.get_piece()
		commands_map = { "b": tetris.left, "n": tetris.rotate, "m": tetris.right }
		for action in actions:
			commands_map[action]()
			#self.evaluation(tetris.get_piece(), board)			
		return tetris.get_piece()

	# Given a new piece (encoded as a list of strings) and a board (also list of strings), 
    	# this function should generate a series of commands to move the piece into the "optimal"
    	# position. The commands are a string of letters, where b and m represent left and right, respectively,
    	# and n rotates. 
    	#
    	def get_moves(self, piece, board):
        	move_string = self.get_choice(piece, board)
		#for row in board:
		#	print "\column = ", row[0]
		# super simple current algorithm: just randomly move left, right, and rotate a few times
        	return random.choice("mnb") * random.randint(1, 10)
       
    	# This is the version that's used by the animted version. This is really similar to get_moves,
    	# except that it runs as a separate thread and you should access various methods and data in
    	# the "tetris" object to control the movement. In particular:
    	#   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    	#     falling piece
    	#   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    	#   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    	#     issue game commands
    	#   - tetris.get_board() returns the current state of the board, as a list of strings.
    	#
    	def control_game(self, tetris):
        	# another super simple algorithm: just move piece to the least-full column
        	while 1:
            		time.sleep(0.1)

            		board = tetris.get_board()
            		column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            		index = column_heights.index(max(column_heights))

            		if(index < tetris.col):
                		tetris.left()
            		elif(index > tetris.col):
                		tetris.right()
            		else:
                		tetris.down()
    

###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]
try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print "unknown player!"

    if interface_opt == "simple":
        tetris = SimpleTetris()
    elif interface_opt == "animated":
        tetris = AnimatedTetris()
    else:
        print "unknown interface!"
    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s



