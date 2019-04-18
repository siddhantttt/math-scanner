from pythonds.basic.stack import Stack


numbers = [str(i) for i in range(10000)]


operators = ['*', '/', '-', '+']


def Solver(postfix_exp):
    solver_stack = Stack()

    for i in range(len(postfix_exp)):
        if postfix_exp[i] in numbers:
            solver_stack.push(int(postfix_exp[i]))
        if postfix_exp[i] in operators:
            first = solver_stack.pop()
            second = solver_stack.pop()
            if postfix_exp[i] == '+':
                solver_stack.push(first + second)
            elif postfix_exp[i] == '-':
                solver_stack.push(second - first)
            elif postfix_exp[i] == '*':
                solver_stack.push(first * second)
            elif postfix_exp[i] == '/':
                solver_stack.push(first / second)

    return solver_stack.pop()


postfix_exp = ['2', '3', '4', '*', '+']

Solver(postfix_exp)

