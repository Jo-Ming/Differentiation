import re, math

class treeNode(object):
    def __init__(self):
        self.children = [] # list of child nodes

    def addChild(self,Node):
        self.children.append(Node)

    def insertChild(self,node, index):
        self.children.insert(index, node)

    def isNumericalNode(self):

        if type(self) == numberNode:
            return True

        elif type(self) == variableNode:
            return False

        elif type(self) in [operatorNode, minusNode]:
            temp = True  # assume True

            for child in self.children:

                temp = temp and child.isNumericalNode()
            return temp

        else:
            return False


    def simplifyTree(self):
        root = self.copy()

        for child in self.children:
            # recursively simplifies all children in the tree
            root.addChild(child.simplifyTree())

        #print('we are going to simplify: ' + self.treeToText() + ' to ' + root.treeToText())
        return root

    def binaryToNaryTree(self):
        root = self.copy()

        for child in self.children:
            # recursively checks children
            root.addChild(child.binaryToNaryTree())

        return root

    def equalTree(self):
        # assume trees are equal
        isEqual = True
        index = 0

        while isEqual and index in range(len(self.children)):
            self.children[index].equalTree()

        return isEqual



    def copy(self):
        raise Exception('This is an abstract method and should not have been called')

class variableNode(treeNode):
    def __init__(self, variable ):
        self.variable = variable
        super(variableNode, self).__init__()

    def differentiate(self):

        if self.variable == 'x':
            return numberNode(1.0)

    def treeToText(self):
        return self.variable

    def evaluate(self):
        # this lets me know there is a problem in my code as variables should not be evaluated
        raise Exception('Cannot evaluate a variable node - replace the variables with their values first in code somewhere')

    def copy(self):
        return variableNode('x')


class functionNode(treeNode):

    def __init__(self, function):
        self.function = function
        super(functionNode, self).__init__()

    def differentiate(self):
        child = self.children[0]
        diffChild = child.differentiate()

        if self.function == 'sin':
            diffSin = functionNode('cos')
            root = operatorNode('*')

            root.addChild(diffSin)
            diffSin.addChild(child)

            root.addChild(diffChild)

        elif self.function == 'cos':
            """diffCos = functionNode('-sin')
            root = operatorNode('*')

            root.addChild(diffCos)
            diffCos.addChild(child)

            root.addChild(diffChild)"""

            sin = functionNode('sin')
            root = operatorNode('*')
            minus = operatorNode('-')

            sin.addChild(child)
            minus.addChild(sin)

            root.addChild(minus)
            root.addChild(diffChild)



        elif self.function == 'tan':
            sec = functionNode('sec')
            subRoot = operatorNode('^')

            sec.addChild(child)

            subRoot.addChild(sec)
            subRoot.addChild(numberNode(2.0))

            root = operatorNode('*')

            root.addChild(subRoot)
            root.addChild(diffChild)


        else:
            raise Exception('Have not differentiated %s' %self.function)
        return root

    def copy(self):
        return functionNode(self.function)


    def evaluate(self):
        if self.function == 'sin':
            return math.sin(self.children[0].evauate())
        elif self.function == 'cos':
            return math.cos(self.children[0].evaluate())
        elif self.function == 'tan':
            return math.tan(self.children[0].evaluate())

    def treeToText(self):
        return self.function + '(' + self.children[0].treeToText() + ')'


class numberNode(treeNode):
    def __init__(self, value):
        if not type(value) in [int,float]:
            raise Exception('number nodes must be integers or floating point numbers')

        self.value = value
        super(numberNode,self).__init__()

    def evaluate(self):
        return self.value

    def differentiate(self):
        # differentiate a constant and you get 0 so return a tree with zero in it
        return numberNode(0)

    def treeToText(self):
        return str(self.value)

    def copy(self):
        return numberNode(self.value)


class operatorNode(treeNode):
    def __init__(self, operatorValue):
        self.operatorValue = operatorValue

        if self.operatorValue == '+':
            self.precedence = 5
        elif self.operatorValue == '-':
            self.precedence = 6
        elif self.operatorValue == '*':
            self.precedence = 7
        elif self.operatorValue == '/':
            self.precedence = 8
        elif self.operatorValue == '^':
            self.precedence = 9
        elif self.operatorValue in self.functions:
            self.precedence = 11
        else:
            self.precedence = 1
        super(operatorNode,self).__init__()


    def treeToText(self):
        text = ""

        if self.operatorValue == '+':

            if len(self.children)>0:
                text = self.children[0].treeToText()

            for i in range(1, len(self.children)):
                child = self.children[i]
                if type(child) == operatorNode and child.precedence > self.precedence :
                    text = text + '+' + '(' + self.children[i].treeToText() + ')'

                else:
                    text = text + '+' + child.treeToText()

            return text

        elif self.operatorValue == '*':

            if len(self.children) > 0:
                text = self.children[0].treeToText()

                for i in range(1, len(self.children)):
                    child = self.children[i]
                    if type(child) == operatorNode and child.precedence < self.precedence :
                        text = text + '*' + '(' + self.children[i].treeToText() + ')'

                    else:
                        text = text + '*' + child.treeToText()

                return text

            # else:
            #             left = self.children[0]
            #
            # right = self.children[1]
            #
            # leftText = self.children[0].treeToText()
            #
            # rightText = self.children[1].treeToText()
            #
            # # decide if the numerator needs brackets
            #
            # if type(left) == operatorNode and left.operatorValue in ['+', '-', '*']:
            #
            #     text = text + '(' + leftText + ')*'
            #
            # else:
            #
            #     text = text + leftText + '*'
            #
            # # decide if the denominator needs brackets
            #
            # if type(right) == operatorNode and right.operatorValue in ['+', '-', '*']:
            #
            #     text = text + '(' + rightText + ')'
            #
            # else:
            #
            #     text = text + rightText
            #
            # return text

        elif self.operatorValue == '-':


            if type(self.children[0]) == functionNode:
                return self.operatorValue + '(' + self.children[0].treeToText() + ')'

            else:

                left = self.children[0]
                right = self.children[1]

                leftText = self.children[0].treeToText()
                rightText = self.children[1].treeToText()

                # decide if the numerator needs brackets
                if type(left) == operatorNode and left.operatorValue in [ '-', '/']:
                    text = text + '(' + leftText + ')-'
                else:
                    text = text + leftText + '-'

                # decide if the denominator needs brackets
                if type(right) == operatorNode and right.operatorValue in ['+', '-', '/']:
                    text = text + '(' + rightText + ')'
                else:
                    text = text + rightText

                return text

        elif self.operatorValue == '/':

            den = self.children[1]
            num = self.children[0]

            denText = self.children[1].treeToText()
            numText = self.children[0].treeToText()

            # decide if the numerator needs brackets
            if type(num) == operatorNode and num.operatorValue in ['+', '-', '/', '*']:
                text = text + '(' + numText + ')/'
            else:
                text = text + numText + '/'

            # decide if the denominator needs brackets
            if type(den) == operatorNode and den.operatorValue in ['+', '-', '/','*']:
                text = text + '(' + denText + ')'
            else:

                text = text + denText

            return text

        elif self.operatorValue == '^':

            left = self.children[0]
            right = self.children[1]

            leftText = self.children[0].treeToText()
            rightText = self.children[1].treeToText()

            # decide if the numerator needs brackets
            if type(left) == operatorNode and left.operatorValue in [ '^','+','-', '/']:
                text = text + '(' + leftText + ')^'
            else:
                text = text + leftText + '^'

            # decide if the denominator needs brackets
            if type(right) == operatorNode and right.operatorValue in ['^','+', '-', '/']:
                text = text + '(' + rightText + ')'
            else:
                text = text + rightText

            return text

    def copy(self):
        if type(self) == operatorNode:
            return operatorNode(self.operatorValue)



    def differentiate(self):

        if self.operatorValue in ['+']:
            # create a root note as a + since the D(sum)=sum(derivatives)
            root = operatorNode('+')
            for i in range(len(self.children)):
                child = self.children[i]
                childDiff = child.differentiate()
                root.addChild(childDiff)


            return root

        elif self.operatorValue in ['-']:
            # create a root note as a + since the D(sum)=sum(derivatives)
            root = operatorNode('-')

            left = self.children[0]
            right = self.children[1]

            root.addChild(left.differentiate())
            root.addChild(right.differentiate())

            return root


        elif self.operatorValue =='*':
            # We differentiate prod(T1,T2,T3....Tn) as T1*Diff(prod(T2....Tn))+prod(T2..Tn)*Diff(T1)
            root = operatorNode('+')
            u = self.children[0]
            if len(self.children) > 2:

                v = operatorNode('*')
                for i in range(1, len(self.children)):
                    v.addChild(self.children[i])

            else:
                v= self.children[1]

            du = u.differentiate()
            dv = v.differentiate()

            left = operatorNode('*')
            left.addChild(u)
            left.addChild(dv)

            right = operatorNode('*')
            right.addChild(v)
            right.addChild(du)

            root.addChild(left)
            root.addChild(right)

            return root

        elif self.operatorValue in ['/']:
            # use quotient rule: [(v*du)-(u*dv)] /(v^2)

            root = operatorNode('/')
            numerator = operatorNode('-')
            u = self.children[0]
            v = self.children[1]
            du = u.differentiate()
            dv = v.differentiate()

            left = operatorNode('*')
            left.addChild(v)
            left.addChild(du)

            right = operatorNode('*')
            right.addChild(u)
            right.addChild(dv)

            numerator.addChild(left)
            numerator.addChild(right)

            denominator = operatorNode('^')
            denominator.addChild(v)
            denominator.addChild(numberNode(2.0))

            root.addChild(numerator)
            root.addChild(denominator)

            return root

        elif self.operatorValue in ['^']:

            u = self.children[0]
            du = u.differentiate()
            n = self.children[1]

            root = operatorNode('*')
            powerNode = operatorNode('^')
            powerNode.addChild(u)

            nMinus1 = operatorNode('-')
            nMinus1.addChild(n)
            nMinus1.addChild(numberNode(1.0))

            powerNode.addChild(nMinus1)

            nTimesdu = operatorNode('*')
            nTimesdu.addChild(n)
            nTimesdu.addChild(du)

            root.addChild(nTimesdu)
            root.addChild(powerNode)

            return root

    def evaluate(self):
        operators = ['+', '-', '*', '/', '^']
        functions = ['sin', 'tan', 'cos']

        if self.operatorValue in operators :


            if self.operatorValue == '+':
                temp = 0.0
                for child in self.children:
                    temp = temp + child.evaluate()

                return temp

            elif self.operatorValue == '*':
                temp = 1.0
                for child in self.children:
                    if child == 0:
                        return 0
                    else:
                        temp = temp * child.evaluate()



                return temp

            elif self.operatorValue == '-':
                return self.children[0].evaluate() - self.children[1].evaluate()

            elif self.operatorValue == '/':
                return self.children[0].evaluate() / float(self.children[1].evaluate())

            elif self.operatorValue == '^':
                # if self.children[1] == 1:
                #     return numberNode(1)
                return self.children[0].evaluate() ** self.children[1].evaluate()

            else:
                raise Exception('I have not implemented %s evaluate yet',self.operatorValue)

        else:
            return self.value

    def evaluateVariables(self):

        if self.operatorValue == '*':
            for child in self.children:
                if child == numberNode(0):
                    return 0

        else:
            return self

    def copy(self):
        return operatorNode(self.operatorValue)

    def binaryToNaryTree(self):
        #check if operator is commutative
        if self.operatorValue in ['*', '+']:
            # create a temporary list to hold grandchildren
            naryChildList = []

            for child in self.children:

                if type(child) == operatorNode and child.operatorValue == self.operatorValue:

                    for grandchild in child.children:
                        naryChildList.append(grandchild)
                    self.children.remove(child)

            # add each element in list of grandchildren to self
            for element in naryChildList:
                self.addChild(element)

        return self


    def simplifyTree(self):
        #first simplify children
        presimplifytext = self.treeToText()

        #print('we are going to simplify: ' + self.treeToText())
        self = super(operatorNode, self).simplifyTree()

        if self.isNumericalNode():
            return numberNode(self.evaluate())


        elif self.operatorValue in ['+']:
            # go through all the children and replace the numerical nodes with a single node
            root = operatorNode('+')
            # temp holds onto a sum of all the nodes that are numerical
            temp = 0
            for child in self.children:

                if child.isNumericalNode():
                    temp = temp + child.evaluate()
                # if child is not numerical add straight to root

                else:
                    #if not numerical add to tree
                    root.addChild(child)

            if temp != 0:
                root.addChild(numberNode(temp))

            if len(root.children) == 1:
                # +x makes no sense so just return child
                #print(' to ' + root.children[0].treeToText())
                return root.children[0]
            #print(' to ' + root.treeToText())
            return root

        if self.operatorValue in ['*']:
            root = operatorNode('*')
            temp = 1.0


            for child in self.children:

                if child.isNumericalNode():
                    childValue = child.evaluate()

                    if childValue == 0:
                        return numberNode(0)

                    else:
                        temp = temp * childValue

                else:
                    root.addChild(child)

            # e.g instead of x*2 we write 2*x
            if temp != 1:
                root.insertChild(numberNode(temp), 0)

            if len(root.children)==1:
                #print(' to ' + root.children[0].treeToText())
                return root.children[0]
            #print(' to ' + root.treeToText())
            return root




        if self.operatorValue in ['/']:

            # there should never be more than two children for a quotient
            if self.isNumericalNode():
                return numberNode(self.children[0]/self.children[1])
            else:
                return self

        if self.operatorValue in ['-']:

            # there should never be more than two children for a subtraction
            if self.isNumericalNode():
                return numberNode(self.children[0]-self.children[1])
            else:
                return self

        if self.operatorValue in ['^']:

            # there should never be more than two children for a power
            base = self.children[0]
            power = self.children[1]

            if self.isNumericalNode():

                return numberNode(math.pow(base.evaluate(), power.evaluate()))
            else:

                if power.isNumericalNode():
                    powerVal = power.evaluate()

                    #base to the power of 1 is the base
                    if powerVal == 1.0:
                        return base

                    # anything to the power of 0 is 1
                    elif powerVal == 0.0:
                        return numberNode(1)

                else:
                    if base.isNumericalNode():

                        baseVal= base.evaluate()
                        # 0 to the power of anything is 0
                        if baseVal == 0.0:
                            return numberNode(0)
                        # 1 to the power of anything is 1
                        elif baseVal == 1.0:
                            return numberNode(1)

                return  self



        def isNumber(self, currentSymbol):

            number = (re.search('^\d*.{0,1}\d+$', currentSymbol))
            return number != None


class minusNode(treeNode):
    def __init__(self, unaryMinus):
        self.unaryMinus = unaryMinus
        super(minusNode, self).__init__()



    def differentiate(self):

        root = minusNode('%')
        child = self.children[0]
        diffChild = child.differentiate()
        root.addChild(diffChild)

        return root

    def copy(self):
        return minusNode(self.unaryMinus)

    def treeToText(self):
        text = "-"
        child = self.children[0]
        if type(child) == operatorNode:
            text =  text + '(' + child.treeToText() + ')'
        else:
            text = text + child.treeToText()

        return text

    def evaluate(self):
        return -self.children[0].evaluate()


    def simplifyTree(self):

        return self
