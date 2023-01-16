import re
import sys
from treenodes import *

class mathsExpression(object):
    operators = ['+', '-', '*', '/', '^','%']
    functions = ['sin', 'tan', 'cos']
    terminalToken = '&'


    def getDerivativeText(self):
        if self.finalDerivativeTree == None:
            return 'error in differentiating expression %s'%self.expressionString
        else:
            return self.finalDerivativeTree.treeToText()

    def getUserInputString(self):
        # This function takes in an input string and converts it into an array of atomic elements

        userStringInput = raw_input(str("Please Enter expression: "))

        if userStringInput == '':
            userStringInput = '-2+(4-3)'

        return userStringInput

    def getUserInputArray(self, inputString):

        inputArray = []
        inputLength = len(inputString)
        index = 0
        # This for loop adds the characters into our inputList, which gives me an array which will allow me
        # to change the order of the character for RPN
        for index in range(int(inputLength)):
            inputArray.append(inputString[index])
            index = index + 1

        return inputArray

    def getInfixAlgorithm(self, inputArray):
        # token string is used so that I can add strings as an element of the array this means that I can use
        # numbers larger than a single digit and decimal numbers
        userInput = inputArray
        inputLength = len(userInput)
        bracketCount = 0
        counter = 0
        token = ""
        infix = []

        while counter < inputLength:
            # this loop collects token a token string and adds the string to the array as an element
            # so larger numbers and decimals can be used

            character = userInput[counter]

            # This if statement skips the code past any spaces in the user input
            if character == ' ':
                counter = counter + 1

            # checks that parenthesise are matching else input is invalid
            elif character == '(':
                bracketCount = bracketCount + 1

                if len(token) > 0:
                    infix.append(token)
                    token = ""

                infix.append(character)
                counter = counter + 1

            elif character == ')':
                bracketCount = bracketCount - 1

                if len(token)>0:
                    infix.append(token)
                    token = ""

                infix.append(character)
                counter = counter + 1

            elif character in self.operators:
                if character in ['-']:

                    nextCharacter = userInput[counter + 1]
                    lastCharacter = userInput[counter - 1]

                    if counter == 0 or nextCharacter in ['('] or lastCharacter in ['('] or lastCharacter in self.operators \
                        or nextCharacter in self.functions:

                        character = '%'

                if len(token) > 0:
                    infix.append(token)
                    token = ""

                infix.append(character)
                counter = counter + 1
                token = ""



            else:
                token = token + character
                counter = counter + 1

            """elif character == 'x':

                # our counter is where the "x" is so infix[index] is character before
                index = counter - 1
                pointer = userInput[index]

                if self.isNumber(pointer):

                    infix.append(token)
                    infix.append('*')
                    token = character

                else:
                    token = token + character
                    counter = counter + 1

                counter = counter + 1  """


        if len(token)>0:
            infix.append(token)

        if bracketCount != 0:
            print('Error, mismatching parenthesise')
            sys.exit()

        else:
            return infix

    def postfixAlgorithm(self, infix):
        # conversion from infix to reverse polish notation

        leftAssociativeOperators = ['*', '-', '+', '/']
        rightAssociativeOperators = ['^']
        unaryMinus = '%'
        functions = ['sin', 'tan', 'cos']
        leftParentheses = '('
        rightParentheses = ')'
        brackets = [leftParentheses, rightParentheses]
        inputLength = len(infix)
        tokenStack = []
        postfixArray = []
        bracketCount = 0
        counter = 0


        while counter < inputLength:

            currentSymbol = infix[counter]

            if self.isNumber(currentSymbol) :
                postfixArray.append(currentSymbol)
                counter = counter + 1


            elif currentSymbol in functions:
                tokenStack.append(currentSymbol)
                counter = counter + 1

            elif currentSymbol == unaryMinus:
                tokenStack.append(currentSymbol)
                counter = counter + 1

            elif currentSymbol in self.operators:
                counter = counter + 1

                # using bidmas to check precedence of operators to know order of operations
                if currentSymbol in leftAssociativeOperators:
                    while len(tokenStack)>0 and tokenStack[-1] in self.operators and \
                    self.getTokenPrecedence(tokenStack[-1]) >= self.getTokenPrecedence(currentSymbol):
                        postfixArray.append(tokenStack.pop())
                    tokenStack.append(currentSymbol)

                else:
                    while len(tokenStack) > 0 and tokenStack[-1] in self.operators and \
                                    self.getTokenPrecedence(tokenStack[-1]) > self.getTokenPrecedence(
                                currentSymbol):
                        postfixArray.append(tokenStack.pop())
                    tokenStack.append(currentSymbol)

                """                if len(tokenStack) > 0 and tokenStack[-1] != leftParentheses:

                    op1 = currentSymbol
                    op2 = tokenStack[-1]

                    while len(tokenStack) > 0 and op1 in leftAssociativeOperators and \
                        self.getOperatorPrecedence(op1) <= self.getOperatorPrecedence(op2)\
                        or op1 in rightAssociativeOperators and self.getOperatorPrecedence(op1) >= \
                            self.getOperatorPrecedence(op2):

                            postfixArray.append(tokenStack.pop())
                            tokenStack.append(op1)
                            """
            elif currentSymbol == leftParentheses:
                counter = counter + 1
                if len(tokenStack) > 0 and tokenStack[-1] in self.functions:
                    postfixArray.append(self.terminalToken)
                tokenStack.append(currentSymbol)

            elif currentSymbol == rightParentheses:
                counter = counter + 1

                while len(tokenStack) > 0 and tokenStack[-1] != leftParentheses:
                    postfixArray.append(tokenStack.pop())

                if len(tokenStack) > 0 and tokenStack[-1] != leftParentheses:
                    print ('Error occurred, mismatch of parentheses')

                else:
                    tokenStack.pop()

                if len(tokenStack) > 0 and tokenStack[-1] in self.functions:
                    postfixArray.append(tokenStack.pop())

            else:
                # Its none of the others therefore it must be a variable
                postfixArray.append(currentSymbol)
                counter = counter + 1


        while len(tokenStack) > 0:
            operator = tokenStack.pop()
            postfixArray.append(operator)

        return postfixArray

    def getTokenPrecedence(self, token):

        if token in ['+']:
            return 5
        elif token in ['-']:
            return 6
        elif token in ['*']:
            return 7
        elif token in ['/']:
            return 8
        elif token in ['%']:
            return 9
        elif token in ['^']:
            return 10
        elif token in self.functions:
            return 11
        else:
        # 1 is for an operand such as variables or numbers return a precedence of 1
            return 1

        # +,- = 5   */=6  ^=7  unary - = 10 function =11 any other operator = 5 other variables = 1


    def isNumber(self,currentSymbol):

        """try:
            float(currentSymbol)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(currentSymbol)
            return True
        except (TypeError, ValueError):
            pass

        return False"""



        number = (re.search('^\d*.{0,1}\d+$', currentSymbol))
        return number != None


    def evaluateExpression(self, inputArray, variableValue):

        arrayLength = len(inputArray)
        stack = []

        counter = 0

        for counter in range(arrayLength):

            currentSymbol = inputArray[counter]
            # todo add functions into my evaluate expression function

            if currentSymbol =='x':
                currentSymbol = str(variableValue)

            if self.isNumber(currentSymbol):
                stack.append(currentSymbol)
                counter = counter + 1

            elif currentSymbol in self.operators:
                value2 = float(stack.pop())
                value1 = float(stack.pop())

                if currentSymbol == '+' :
                    output = value1 + value2

                elif currentSymbol == '-':
                    output = value1 - value2

                elif currentSymbol == '*':
                    output = value1 * value2

                elif currentSymbol == '/':
                    output = value1 / value2

                elif currentSymbol == '^':
                    output = value1 ^ value2

                stack.append(output)

        output = stack[-1]

        print('Expression output value =' + str(stack[-1]))
        return (output)

    def compareAnswers(self, trueAnswer, userAnswer, domainStart, domainEnd, numPoints, failureRate):

        validCount = 0
        invalidCount = 0
        step = (domainEnd-domainStart)/numPoints
        x = domainStart

        for x in range(0, numPoints):

            if self.evaluateExpression(trueAnswer, x) == self.evaluateExpression(userAnswer, x):
                validCount = validCount + 1
                x = x + step

            else:
                invalidCount = invalidCount + 1
                x = x + step

        if invalidCount > 5:
            print('Sorry, this answer is incorrect. Would you like to see the solution?')

        else:
            print('This answer is correct! :)')

        return not invalidCount > failureRate


    def variableCheck(self, inputArray):

        index = 0

        for index in range(inputArray):
            if inputArray[index] in self.operators:
                return True
            else:
                return False

        return

    def getTree(self, postfix):

        length = len(postfix)
        index = 0
        stack = []

        for token in postfix:

            if token == 'x':
                stack.append(variableNode(token))

            elif token == self.terminalToken:
                stack.append(token)

            elif self.isNumber(token):
                stack.append(numberNode(float(token)))


            elif token in self.functions:
                root = functionNode(token)
                while len(stack) > 0 and stack[-1] != self.terminalToken:
                    root.addChild(stack.pop())
                #to remove the terminal node
                stack.pop()

                stack.append(root)

            elif token == '%':

                root = minusNode(token)
                root.addChild(stack.pop())

                stack.append(root)

            elif token in self.operators:

                root = operatorNode(token)

                right = stack.pop()
                left = stack.pop()

                if token in ['*','+']: # check if operator is commutative

                    if type(left) == operatorNode and left.operatorValue == token:
                        for child in left.children:
                            root.addChild(child)

                    else:
                        root.addChild(left)

                    if type(right) == operatorNode and right.operatorValue == token:
                        for child in right.children:
                            root.addChild(child)

                    else:
                        root.addChild(right)

                else:
                    root.addChild(left)
                    root.addChild(right)


                stack.append(root)

                """elif token == '%':

                    root = minusNode(token)
                    root.addChild(stack.pop)"""

                """root = operatorNode(token)

                while (len(stack)>0) and (not type(stack[-1]) == operatorNode):

                    child = stack.pop()
                    root.insertChild(child, 0)

                stack.append(root)"""
            else:
                print('sorry "'+ token + '" is not a valid input, please try again. ')
                sys.exit()


        return stack.pop()

    """def binaryToNaryTree(self):
        for child in self.children:
            child.checkCommutativeTree

        if self.operatorValue in ['*', '+']:

            for child in self.children:
                if child == self.operatorValue:
                    grandchild = child
                    for

        else:
            for child in self.children:
                child.checkCommutativeTree"""



            #todo add functions in later

    def tidyExpression(self, preSimplifiedText):

        expressionArray =list(preSimplifiedText)
        index = 0
        stack = []
        stackTop = [-1]
        operatorStack =[]
        token = ""

        while index in range(len(expressionArray)):

            currentSymbol = expressionArray[index]

            if currentSymbol in self.operators:

                operatorStack.append(currentSymbol)
                token = ""


           # if self.isNumber(currentSymbol):


    def impliedMultiplication(self, inputString):

        result = inputString;

        result = re.sub('([a-zA-Z]+)([0-9]*\.?[0-9]+)', '\g<1>*\g<2>', result)  # e.g. x6->x*6

        result = re.sub('([0-9]*\.?[0-9]+)([a-zA-Z]+)', '\g<1>*\g<2>', result)  # e.g. 6x->6*x
        #result = re.sub('([0-9]*\.?[0-9]+)([a-zA-Z]+)', '\g<1>\u2062\g<2>', result)

        result = re.sub('([0-9]*\.?[0-9]+)(\()', '\g<1>*\g<2>', result)  # e.g. // 6( -> 6*(

        result = re.sub('(\))([0-9]*\.?[0-9]+)', '\g<1>*\g<2>', result)  # e.g. )6( -> )*6

        return result;


mainModel = mathsExpression()
print(mainModel.isNumber('2'))
