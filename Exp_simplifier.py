operators = ['*', '/', '-', '+']

numbers = [str(i) for i in range(10000)]



def simplifier(exp):
	simplified_exp = []
	buff = 0
	for i in range(len(exp)):
		if exp[i] in numbers:
			#print('yes')
			buff = buff  * 10 + int(exp[i])

		elif exp[i] in operators:
			simplified_exp.append(str(buff))
			buff = 0
			simplified_exp.append(exp[i])

	simplified_exp.append(str(buff))


	return simplified_exp




#exp = ['2', '3', '+', '3', '4']

#simplifier(exp)