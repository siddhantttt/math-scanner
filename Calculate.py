from pythonds.basic.stack import Stack 
from Project3 import operators, Solver
from Project4 import simplifier



precedence_dict = {'-':2, '+':2, '*':1, '/':1}
numbers = [str(i) for i in range(100000)]



def postfix_converter(exp):
	exp = ['('] + exp + [')']
	#print(exp)
	i = 0
	operator_stack = Stack()

	postfix_exp = []
	while(i < len(exp)):
		if (exp[i] in numbers):
			postfix_exp.append(exp[i])


		if (exp[i] == '('):
			operator_stack.push(exp[i])


		if (exp[i] == ')'):
			while (operator_stack.peek() != '('):
				postfix_exp.append(operator_stack.pop())
			operator_stack.pop()



		if (exp[i] in precedence_dict.keys()):
			if (operator_stack.peek() == '('):
				operator_stack.push(exp[i])


			elif (precedence_dict[exp[i]] < precedence_dict[operator_stack.peek()]):
				operator_stack.push(exp[i])

			else:
				postfix_exp.append(exp[i])
				postfix_exp.append(operator_stack.pop())



		i += 1
	return postfix_exp


exp = ['1','2','*', '2','2']

#print(exp)

simplified_exp  = simplifier(exp)
 
#print(simplified_exp)

postfix_exp = postfix_converter(simplified_exp)
#postfix_converter(exp)
print(Solver(postfix_exp))


















