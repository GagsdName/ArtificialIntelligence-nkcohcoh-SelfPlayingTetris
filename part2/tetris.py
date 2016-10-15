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
		original_piece_tuple = tetris.get_piece()		
		#print "\n\n\n\n original piece = ", piece
		#print "\n original piece and position = ", original_piece_tuple
		result_tuple = self.result(piece,board,actions)	
		#print "\nresult_tuple = ", result_tuple
		#print "\nactions = ", actions	
		#@print "\nsuccessor_piece = ", result_tuple[0]
		eval_val = self.evaluation(result_tuple[0],(result_tuple[1],result_tuple[2]), board)
		#print "\nnew_position = ", result_tuple[1], result_tuple[2]	
		#print "\n eval_val in chance layer = ",eval_val
		
		#place piece back at it's original location	
		temp_board_score = tetris.place_piece(tetris.state,piece,original_piece_tuple[1],original_piece_tuple[2])
		return eval_val
	#max node value
        def max_layer(self,piece,board):
		piece_tuple = tetris.get_piece()
		max_val = self.evaluation(piece_tuple[0],(piece_tuple[1],piece_tuple[2]), board)
		action_string = " "
		generated = []
		for action1 in self.commands:
			for action2 in self.commands:
				for action3 in self.commands:
					count = 1
					for i in range(1,100):
						action = random.choice(action1+action2+action3) * random.randint(1,10)
						if action not in generated:
							generated.append(action)
							chance_eval = self.chance_layer(piece,action, board)
							#print "\n chance eval = ", chance_eval
							if chance_eval > max_val:
								max_val = chance_eval
								action_string = action1+action2+action3
                #print "\naction_string for piece -  ", piece, " is - ",action_string
		return action_string
	#ExpectiMiniMax
	def get_choice(self,piece,board):
		desired_action = self.max_layer(piece,board)
		return desired_action 

	#find number of non-space character in the last row of the piece
	def find_non_space_chars(self, piece):
		count = 0
		for row in piece[::-1]:
			for c in row:
				if not c == " ":
			 		count+=1
			break
		return count	

	#get chunks of space, which need to be filled, in a given row and their locations	
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
		eval_points = -9999999999999
		constant_multiplier = -1
		non_space_chars = self.find_non_space_chars(successor_piece)
		for row in board[::-1]:
			flag = False
			chunk_tuple = self.get_space_chunks(row)
			max_for_row = -99999999999999
			for i in chunk_tuple[0]:
				if i <= new_position[1] and new_position[1] <= i + chunk_tuple[1][chunk_tuple[0].index(i)]:
					index = chunk_tuple[0].index(i)
					if chunk_tuple[1][index] >= non_space_chars and\
					 not(tetris.check_collision(tetris.state,successor_piece, board[::-1].index(row), new_position[1] )):
						eval_points = constant_multiplier * (chunk_tuple[1][index] - non_space_chars)
						flag = True
						break
				

				#if not(tetris.check_collision(tetris.state,successor_piece, new_position[0], new_position[1])) and\
				 #(non_space_chars <= i):
				#	eval_points = constant_multiplier * (i - non_space_chars)
				#	flag = True
				#	break
					#print "\ni = ", i, " successor_piece = " ,successor_piece, " elligible for row =  ", row, " eval points = ", eval_points
			if flag == True:
				break
		return eval_points	
			 
	def result(self,piece,board,actions):
		'''commands_map = { "b": tetris.left, "n": tetris.rotate, "m": tetris.right }
		for action in actions:
			commands_map[action]()
		print "\npiece after action = ", piece
		return tetris.get_piece()'''
		piece_pos_tuple = tetris.get_piece()
		new_piece= piece_pos_tuple[0]
		new_row = piece_pos_tuple[1]
		new_col = piece_pos_tuple[2]
		for action in actions:
			if action == 'b':
				if new_col > 0 :
					new_col = new_col - 1
			if action == 'm':
				if new_col < len(board[0]) - 1 :
					new_col = new_col + 1
			if action == 'n':
				new_piece = tetris.rotate_piece(new_piece,90)
		return (new_piece,new_row,new_col)

	# Given a new piece (encoded as a list of strings) and a board (also list of strings), 
    	# this function should generate a series of commands to move the piece into the "optimal"
    	# position. The commands are a string of letters, where b and m represent left and right, respectively,
    	# and n rotates. 
    	#
    	def get_moves(self, piece, board):
        	move_string = ""
		move_string = move_string + self.get_choice(piece, board)

		print "\nmove_string = ", move_string + " for piece = ", piece
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



