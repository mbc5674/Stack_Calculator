#HW3
#Due Date: 11/03/2019, 11:59PM 
'''
Team members: Michael Castell, Boyang Zhou

Collaboration Statement:             

'''

import re

class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          

#=============================================== Part I ==============================================

class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top = None
        self.count=0
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__

    def isEmpty(self):
        # YOUR CODE STARTS HERE
        return (self.top == None)

    def __len__(self): 
        # YOUR CODE STARTS HERE
        return self.count

    def push(self,value):
        # YOUR CODE STARTS HERE
        new_node = Node(value)
        temp = self.top
        self.top = new_node
        self.top.next = temp
        self.count += 1
             
    def pop(self):
        # YOUR CODE STARTS HERE
        if(self.top == None):
            return None
        else:
            temp = self.top.value
            self.top = self.top.next
            self.count -= 1
            return temp

    def peek(self):
        # YOUR CODE STARTS HERE
        return self.top.value

#=============================================== Part II ==============================================

class Calculator:
    def __init__(self):
        self.expr = None


    def isNumber(self, txt):
        # YOUR CODE STARTS HERE
        txt1 = re.sub('[^0-9.]', '', txt)
        if(len(txt1) > 0):
            if(txt1[0] == '.'):
                return False
        if txt1 == '':

            return False
        else:
            if txt1.count('.') <= 1:
                return True
            else:
                return False

    def postfix(self, txt):
        '''
            Required: postfix must create and use a Stack for expression processing
            >>> x=Calculator()
            >>> x.postfix(' 2 ^        4')
            '2.0 4.0 ^'
            >>> x.postfix('2')
            '2.0'
            >>> x.postfix('2.1*5+3^2+1+4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x.postfix('    2 *       5.34        +       3      ^ 2    + 1+4   ')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x.postfix(' 2.1 *      5   +   3    ^ 2+ 1  +     4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x.postfix('(2.5)')
            '2.5'
            >>> x.postfix ('((2))')
            '2.0'
            >>> x.postfix ('     -2 *  ((  5   +   3)    ^ 2+(1  +4))    ')
            '-2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x.postfix ('  (   2 *  ((  5   +   3)    ^ 2+(1  +4)))    ')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x.postfix ('  ((   2 *  ((  5   +   3)    ^ 2+(1  +4))))    ')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x.postfix('   2 *  (  5   +   3)    ^ 2+(1  +4)    ')
            '2.0 5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'
            >>> x.postfix('2 *    5   +   3    ^ -2       +1  +4')
            'error message'
            >>> x.postfix('2    5')
            'error message'
            >>> x.postfix('25 +')
            'error message'
            >>> x.postfix('   2 *  (  5   +   3)    ^ 2+(1  +4    ')
            'error message'
            >>> x.postfix('2*(5 +3)^ 2+)1  +4(    ')
            'error message'
        '''
        if not isinstance(txt, str) or len(txt) <= 0:
            print("Argument error in postfix")
            return None

        postStack = Stack()
        # YOUR CODE STARTS HERE

        # Parenthesis error (if left and right parenthesis are not equal)
        if (not (txt.count("(") == txt.count(")"))):
            return 'error message'

        # Variables
        nums = 0
        opers = 0
        p_test = 0
        temp_expr = ''
        i = 0
        length = len(txt)
        operators = "-*+/()^"

        # Special characters error
        while (i < length):
            if (not self.isNumber(txt[i]) and not (txt[i] in operators)
                    and not (txt[i] == ' ')):
                return 'error message'

            # Resetting variables
            temp_txt = ''
            end = i

            # Numbers
            if (self.isNumber(txt[i])):
                # Puts entire number into string, not just one character at a time
                while (end < length and (self.isNumber(txt[end]) or txt[end] == '.')):
                    end += 1
                temp_txt = txt[i: end]
                if (self.isNumber(temp_txt)):
                    if (len(temp_txt) < 2):
                        temp_expr += temp_txt + '.0 '
                    else:
                        temp_expr += temp_txt + ' '
                    nums += 1
                    end -= 1

            # Operators
            if (txt[i] in operators):
                # Parenthesis error (if right parenthesis comes before left parenthesis)
                if (p_test < 0):
                    return 'error message'

                # Special case for first operator
                if (len(postStack) == 0):
                    if(txt[i] == ')'):
                        return 'error message'

                    postStack.push(txt[i])
                    if (txt[i] not in '()'):
                        opers += 1
                else:
                    # Tracks ratio of left/right parenthesis
                    if (txt[i] == '('):
                        p_test += 1
                    if (txt[i] == ')'):
                        p_test -= 1
                        # Pops everything in the stack until '(', then pops '('
                        while (len(postStack) > 0 and postStack.peek() is not '('):
                            temp_expr += postStack.pop() + ' '
                        postStack.pop()
                    else:
                        # Determines if operator has higher precedence(pop), or lower precedence
                        if (txt[i] == '^'):
                            while (len(postStack) > 0 and postStack.peek() not in "/*+-("):
                                temp_expr += postStack.pop() + ' '
                        elif (txt[i] in "*/"):
                            while (len(postStack) > 0 and postStack.peek() not in "+-("):
                                temp_expr += postStack.pop() + ' '
                        elif (txt[i] in "+-"):
                            while (len(postStack) > 0 and postStack.peek() not in "("):
                                temp_expr += postStack.pop() + ' '
                        # Puts current operator onto stack
                        postStack.push(txt[i])
                        # Tracks operators
                    if (txt[i] not in '()'):
                        opers += 1

            # next loop
            i += (end - i + 1)

        # fencepost (last item in stack)
        while len(postStack) > 1:
            temp_expr += postStack.pop() + ' '

        if(len(postStack) > 0):
            temp_expr += postStack.pop()

        # operator error
        if (opers + 1 is not nums):
            return 'error message'

        temp_expr = temp_expr.strip()

        return temp_expr

    @property
    def calculate(self):
        '''
            Required: calculate must call postfix
                      calculate must create and use a Stack to compute the final result as shown in the video lecture
            >>> x=Calculator()
            >>> x.expr='    4  +      3 -2'
            >>> x.calculate
            5.0
            >>> x.expr='  -2  +3.5'
            >>> x.calculate
            1.5
            >>> x.expr='4+3.65-2 /2'
            >>> x.calculate
            6.65
            >>> x.expr=' 23 / 12 - 223 +      5.25 * 4    *      3423'
            >>> x.calculate
            71661.91666666667
            >>> x.expr='   2   - 3         *4'
            >>> x.calculate
            -10.0
            >>> x.expr=' 3 *   (        ( (10 - 2*3)))'
            >>> x.calculate
            12.0
            >>> x.expr=' 8 / 4  * (3 - 2.45      * (  4- 2 ^   3)) + 3'
            >>> x.calculate
            28.6
            >>> x.expr=' 2   *  ( 4 + 2 *   (5-3^2)+1)+4'
            >>> x.calculate
            -2.0
            >>> x.expr='2.5 + 3 * ( 2 +(3.0) *(5^2 - 2*3^(2) ) *(4) ) * ( 2 /8 + 2*( 3 - 1/ 3) ) - 2/ 3^2'
            >>> x.calculate
            1442.7777777777778
            >>> x.expr="4++ 3 +2"
            >>> x.calculate
            'error message'
            >>> x.expr="4    3 +2"
            >>> x.calculate
            'error message'
            >>> x.expr='(2)*10 - 3*(2 - 3*2)) '
            >>> x.calculate
            'error message'
            >>> x.expr='(2)*10 - 3*/(2 - 3*2) '
            >>> x.calculate
            'error message'
            >>> x.expr=')2(*10 - 3*(2 - 3*2) '
            >>> x.calculate
            'error message'
        '''

        if not isinstance(self.expr,str) or len(self.expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack=Stack()

        # YOUR CODE STARTS HERE

        # letting the expression to go through the postfix function so that further operation can be done
        a = self.postfix(self.expr)
        # end the entire process if a is None, in other words, self.expr is not in the correct format
        if a == 'error message':
            return 'error message'

        # establish a list of element that are seperated by space in the string after gone through postfix
        listt = a.split()


        # using a for loop to go through all the elements in the newly-created list
        for item in listt:
            # if the item is a operation sign, perform that operation
            if item in '+-*/^':
                num1 = calcStack.pop()
                num2 = calcStack.pop()
                if item == '+':
                    calcStack.push(num1+num2)
                elif item == '-':
                    calcStack.push(num2-num1)
                elif item == '*':
                    calcStack.push(num2*num1)
                elif item == '/':
                    calcStack.push(num2/num1)
                elif item == '^':
                    calcStack.push(num2**num1)
            # if the item is not an operation sign, in other words, it is a number, then just change it to float form
            # and push it into the stack
            else:
                calcStack.push(float(item))
        # return the only element in the stack
        return calcStack.pop()

