# Simple tetris program! v0.1
# D. Crandall, Sept 2016
# Problem abstraction and analysis in a file called Assignment 2 - Report in master branch
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
   
	commands = [ "b", "n", "m"]
	#chance node
        def chance_layer(self,piece,actions, board):
		original_piece_tuple = tetris.get_piece() #original piece value and position	
		result_tuple = self.result(piece,board,actions)	#successor piece value and position
		eval_val = self.evaluation(result_tuple[0],(result_tuple[1],result_tuple[2]), board) # heuristic evaluation
		#temp_board_score = tetris.place_piece(tetris.state,piece,original_piece_tuple[1],original_piece_tuple[2]) #just checking to see placement of piece 
		#and resulting score
		return eval_val
	#max node value
        def max_layer(self,piece,board):
		piece_tuple = tetris.get_piece()
		max_val = self.evaluation(piece_tuple[0],(piece_tuple[1],piece_tuple[2]), board)
		action_string = "bbb" #default action if no favorable action could be calculated - meaning the piece is already at it's best position
		#could not specify a " " as the default action as the program throws an error always with that.
		generated = [] #so that there are no repeated actions if we added the middle random layer to possible combination of actions 
		for action1 in self.commands:
			for action2 in self.commands:
				for action3 in self.commands:
					count = 1
					for i in range(1,100): #depth value is 100
						#random number multiplied with the combination of "bnm" generated to allow for multiple actions across the
						# complete length of the board
						action = random.choice(action1+action2+action3) * random.randint(1,10)
						if action not in generated:
							generated.append(action)
					chance_eval = self.chance_layer(piece,(action1,action2,action3), board)#sent for evaluation		
					if chance_eval > max_val: #keeping a track of the action which evaluates as max
						max_val = chance_eval
						action_string = action1+action2+action3
		return action_string
	#ExpectiMiniMax
	def get_choice(self,piece,board):
		desired_action = self.max_layer(piece,board)
		return desired_action 

	#checks piece type for multiplying with corresponding probability values to obtain expected values
	#piece names have been assigned based on their similarity of shape to an alphabet or a number
	def check_type(self,piece):
		string  = str(piece).strip("[]")
                if string  == "'x', 'x', 'x', 'x'" or string == "'xxxx'":
                        return "line"
                if string == "'xx', 'xx'":
                        return "brick"
                if string == "'xx ', ' xx'" or string == "' x', 'xx', 'x '" or string == "' xx', 'xx '"\
                 or string == "'x ', 'xx',', ' x'" or string == "' xx', 'xx '":
                        return "n"
                if string == "'xxx', ' x '" or string == "'x ', 'xx', 'x '" or string == "' x ', 'xxx'" or string == "' x', 'xx', ' x'":
                        return "t"
                if string == "'xxx', '  x'" or string == "' x', ' x', 'xx'" or string == "'xx', 'x ', 'x '":
                        return "7"
		
		return None 
	#check r ws above a prospective match for a column position to validate heuristic and make it stronger or weaker
	def check_rows_above(self,col,row,board):
		minus_factor = 0
		for r in range(0,20):
			if r == row:
				return minus_factor
			if board[r][col] == "x":
				minus_factor =  1 #indicating there is indeed another piece obstructing it's new column position
				return minus_factor
			if board[r][col] == " ":
				minus_factor = -1 # nothing is obstructing the piece's way
		return minus_factor 
			
	#find number of non-space character in the last row (or lower part)  of the successor - piece
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
			else:
				c+=1
		return (chunk_positions, chunk_lengths)	
				
	#evaluation function for a given state
	def evaluation(self,successor_piece,new_position, board):
		constant_multiplier = -1
		eval_points = -9999999999999
		line_prob =  0.428571428571
		brick_prob =  0.0
		n_prob =  0.238095238095
		t_prob =  0.0952380952381
		seven_prob  =  0.190476190476
		constant_multiplier = -1
		non_space_chars = self.find_non_space_chars(successor_piece)
		for row in range(19,-1,-1):
			flag = False
			chunk_tuple = self.get_space_chunks(board[row])
			max_for_row = -99999999999999
			for i in chunk_tuple[0]:
				if i <= new_position[1] and new_position[1] <= i + chunk_tuple[1][chunk_tuple[0].index(i)] - 1:
					index = chunk_tuple[0].index(i)
					if chunk_tuple[1][index] >= non_space_chars:
						#Column heuristic - checking to see if the column the successor piece ends being in doesn't have any pieces 
						#in the same column but rows above it - basically if anything else is in it's way 
						minus_factor = self.check_rows_above(new_position[1],row,board)
						#Row-heuristic
						eval_points = constant_multiplier * (chunk_tuple[1][index] - non_space_chars) - minus_factor
						#checking piece type , descriptions of piece names i.e line, brick etc can be found in check_type function
						type_of_piece = self.check_type(successor_piece)
						#applying weighted probablility distributions to the heuristic to calculate expectation values.
						#still keeping the heuristic as negative values as initially it is calculated as the difference 
						#between the space chunk  and the solid parts in the lowest part of the successor piece - which
						#means - the lesser the difference the mostly likely the position is for the piece.
						if type_of_piece == "line":
							eval_points = eval_points * line_prob
						if type_of_piece == "brick":
							eval_points = eval_points * brick_prob
						if type_of_piece == "n":
							eval_points = eval_points * n_prob
						if type_of_piece == "t":
							eval_points = eval_points * t_prob
						if type_of_piece == "7":
							eval_points = eval_points * seven_prob
						flag = True #once a favorable position is found, the rest of the space chunks in the row are pruned from evaluation
						break
			if flag == True:
				break
		return eval_points	
	#calculates the result of an action on a piece and returns a successor piece and position 
	def result(self,piece,board,actions):
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
		#writing pieces to an external file for probability value calculation, this can be removed as well.
	 	target.write(str(piece).strip("[]"))
		target.write("\n")	
		#optimal action string
		move_string = ""
		move_string = move_string + self.get_choice(piece, board)
		print "\nmove_string = ", move_string + " for piece = ", piece	
        	return move_string
		#random.choice("mnb") * random.randint(1, 10)
       
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

            		piece = tetris.get_piece()
            		board = tetris.get_board()
            		#column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
					#index = column_heights.index(max(column_heights))
            		moves = player.get_moves(piece,board)
            		for c in moves:
            			if c == 'b':
            				tetris.left()
            			elif c == 'm':
            				tetris.right()
            			elif c == 'n':
            				tetris.rotate()
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
    
    #file IO variable
    global target 
    target = open("pieces_print.txt", 'w')
    
    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s
