import mathsExpression, treenodes, re, sys

class userInterface():

    def __init__(self):
        self.dictionary = {}
        self.menu()

    def differentialMenu(self):
        response = raw_input('\nwould you like to show full process? y/n: ')

        if response == 'y':

            inputString = mathsExpression.mathsExpression().getUserInputString()

            checkedString = mathsExpression.mathsExpression().impliedMultiplication(inputString)

            inputArray = mathsExpression.mathsExpression().getUserInputArray(checkedString)

            infix = mathsExpression.mathsExpression().getInfixAlgorithm(inputArray)

            print('Infix = ' + str(infix))

            postfix = mathsExpression.mathsExpression().postfixAlgorithm(infix)

            print('Postfix = ' + str(postfix))

            self.expressionTree = mathsExpression.mathsExpression().getTree(postfix)

            print('simplify the following tree : ' + self.expressionTree.treeToText() + ' to: ')

            # naryExpressionTree = self.expressionTree.binaryToNaryTree()

            # print(naryExpressionTree.treeToText())

            self.simplifiedExpressionTree = self.expressionTree.simplifyTree()

            print('simplified input is : ' + self.simplifiedExpressionTree.treeToText())
            # print('here we go: ' + simplifiedExpressionTree.treeToText())

            isNumerical = self.expressionTree.isNumericalNode()
            # isNumerical = self.simplifiedExpressionTree.isNumericalNode()

            print('Is numerical is ' + str(isNumerical))

            print('Input value = ' + self.expressionTree.treeToText())

            self.derivativeTree = self.simplifiedExpressionTree.differentiate()
            # self.derivativeTree = self.expressionTree.differentiate()

            print('Output value = ' + self.derivativeTree.treeToText())

            self.simplifiedTree = self.derivativeTree.simplifyTree()

            self.checkedDerivativeTree = self.simplifiedTree.binaryToNaryTree()
            # self.derivativeTree.binaryToNaryTree()
            self.finalDerivativeTree = self.checkedDerivativeTree.simplifyTree()

            print('Simplified output: ' + self.finalDerivativeTree.treeToText())

            outputString = self.finalDerivativeTree.treeToText()

            self.storeDictionary(inputString, outputString)

            self.finalMenu()

            # self.finalTree = self.simplifiedTree.binaryToNary.treeToText()

            # print(self.finalTree)

            # self.compareAnswers()

            # self.tidyExpression(preSimplifiedText)

        elif response == 'n':

            inputString = mathsExpression.mathsExpression().getUserInputString()

            checkedString = mathsExpression.mathsExpression().impliedMultiplication(inputString)

            inputArray = mathsExpression.mathsExpression().getUserInputArray(checkedString)

            infix = mathsExpression.mathsExpression().getInfixAlgorithm(inputArray)

            postfix = mathsExpression.mathsExpression().postfixAlgorithm(infix)

            self.expressionTree = mathsExpression.mathsExpression().getTree(postfix)

            self.simplifiedExpressionTree = self.expressionTree.simplifyTree()

            isNumerical = self.expressionTree.isNumericalNode()

            self.derivativeTree = self.simplifiedExpressionTree.differentiate()

            self.simplifiedTree = self.derivativeTree.simplifyTree()

            self.checkedDerivativeTree = self.simplifiedTree.binaryToNaryTree()

            self.finalDerivativeTree = self.checkedDerivativeTree.simplifyTree()

            print('derivative : ' + self.finalDerivativeTree.treeToText())

            outputString = self.finalDerivativeTree.treeToText()

            self.storeDictionary(inputString, outputString)

            self.finalMenu()

            # self.finalTree = self.simplifiedTree.binaryToNary.treeToText()

            # print(self.finalTree)

            # self.compareAnswers()

            # self.tidyExpression(preSimplifiedText)

        else:
            print('This is not a valid input')
            self.differentialMenu()

    def menu(self):

        print('\nMenu options')
        print('1. Differentiate expression')
        print('2. View previous entries')
        print('3. Exit program')

        option = raw_input('Enter menu option: ')

        if option == '1':
            self.differentialMenu()
        elif option == '2':
            self.printDictionary()
        elif option == '3':
            sys.exit()
        else:
            print('This is not a valid option')
            self.menu()

    def finalMenu(self):
        print('\nWould you like to: ')
        print('1. Enter another expression. ')
        print('2. Return to main menu ')
        print('3. Exit the program')

        option = raw_input('Enter menu option: ')

        if option == '1':
            self.differentialMenu()
        elif option == '2':
            self.menu()
        elif option == '3':
            sys.exit()

    def storeDictionary(self, inputString, outputString):
        self.dictionary.update({inputString:outputString})
        print('Expression Saved.')

    def printDictionary(self):
        print('\nRecent History: ')
        for expression in self.dictionary:
                print(expression + ' Differentiated to: ' + self.dictionary[expression])
        self.menu()




runProgram = userInterface()
