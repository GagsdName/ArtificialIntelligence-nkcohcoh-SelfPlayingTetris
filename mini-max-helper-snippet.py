#min node value
    def min_value(state,alpha,beta):
                if terminal_test(state):
                    return utility(state)
                v = 99999999
                for c in commands: # commands = list of actions 
                    v = min(v,max_value(result(state,c),alpha,beta))
                    if v <= alpha:
                        return v
					beta = min(beta,v)
				return v


#max node value
    def max_value(state,alpha,beta):
        if terminal_test(state):
            return utility(state)
        v = -99999999
        for c in self.commands:
			v = max(v, min_value(result(state,c), alpha, beta))
            if v >= beta:
                return v
			alpha = max(alpha,v)
        return v

#MiniMax
	def alpha_beta_search(self,state):
		v = max_value(state, -99999999, 99999999)
		return action #returns the next best action with value v

#transition model - result of an action on the current state
	def result(state,command):
		#calculates a successor for 'state' with the application of action - 'command'
		#returns resulting state
		
#terminal test
	def terminal_test(self,state):
		#returns true or false 

#utility function
	def utility(state):
		#returns utility values
		
