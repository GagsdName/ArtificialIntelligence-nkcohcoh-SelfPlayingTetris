
PIECES = [ [ "xxxx" ], [ "xx ", " xx" ], [ "xx", "xx" ], [ "xxx", "  x"], [ "xxx", " x " ] ]
total_count = 0
line_count = 0
brick_count = 0
n_count = 0
t_count = 0
seven_count = 0
with open('pieces_print.txt') as fin:
	
	for line in fin:
		print "\n line = ", str(line)
		if str(line) == "'x', 'x', 'x', 'x'\n" or str(line) == "'xxxx'\n":
			line_count += 1
		if str(line) == "'xx', 'xx'\n":
			brick_count+=1
		if str(line) == "'xx ', ' xx'\n" or str(line) == "' x', 'xx', 'x '\n" or str(line) == "' xx', 'xx '\n"\
		 or str(line) == "'x ', 'xx',', ' x'\n" or str(line) == "' xx', 'xx '\n":
			n_count+=1
		if str(line) == "'xxx', ' x '\n" or str(line) == "'x ', 'xx', 'x '\n" or str(line) == "' x ', 'xxx'\n" or str(line) == "' x', 'xx', ' x'\n":
			t_count+=1
		if str(line) == "'xxx', '  x'\n" or str(line) == "' x', ' x', 'xx'\n" or str(line) == "'xx', 'x ', 'x '\n":
			seven_count+=1
		
		total_count+=1
				

print "\ntotal = ", total_count
float(line_count)/float(total_count)
print "\nline count = ", line_count," probability of line = ", float(line_count)/float(total_count)
print "\nbrick count = ", brick_count," probability of brick = ", float(brick_count)/float(total_count)
print "\nn count = ", n_count," probability of n = ", float(n_count)/float(total_count)
print "\nt count = ", t_count," probability of t = ", float(t_count)/float(total_count)
print "\nseven count = ", seven_count," probability of seven = ",float(seven_count)/float(total_count)


