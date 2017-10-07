#########################
###Math Game
###By: Juan Barrero, Jashan Thind, Vladimir Bereznyakov
###Last Revision: Monday, November 24th
###Hours Spent on Project: 12
#########################
###This game lets you guess a formula and evaluate it
###When the game is over, it displays some statistics
###regarding the user's play of the game and 2 lucky numbers
###based on the last used formula
#########################

##########
#TopLevel
##########
import random

def read(the_file):
#Function Courtesy of Diana Cukierman
    fileRef = open(the_file,"r") # opening file to be read
    localList=[]
    for line in fileRef:
        string = line[0:len(line)-1]  # eliminates trailing '\n'
                                      # of each line     
        localList.append(string)  # adds string to list
    fileRef.close()  
    return localList

def chooseFrmla(theList):
#chooses random formula
    index = random.randrange(1,10)
    formula = theList[index]
    return formula

def expand (condensed):
#expands formula
    st = ''
    op1 = condensed[0]
    op2 = condensed[1]
    for i in range(2, len(condensed)):
        if i % 2 == 0:
            st += condensed[i] + op1
        if i % 2 == 1:
            st += condensed[i] + op2
    return st[0:len(st) - 1]

def evaluate(frmla):
#puts formula into a list
    result=[]
    for i in range(len(frmla)):
        result.append(frmla[i])
    return result

def evaluateTwo(ListA):
#evaluates formula but getting rid of multiplication
#and replacing all + and * symbols with 0's
#to be added together after all multiplying is done
    result = 0
    iResult = 0
    order = ListA
    for a in range(len(order)):
        if (order[a] == "*"):
            iResult = (int(order[a-1]) * int(order[a+1]))
            order[a] = "0"
            order[a+1] = str(iResult)
            order[a-1] = "0"
        elif (order[a] == "+"):
            order[a] = "0"
    for s in range(len(order)):
        result = result + int(order[s])
    return result

def guessChecker():
#This checks the users guess for validity
    while(1):
        guesses = raw_input("Provide the maximum number of wrong guesses you wish to allow: ")
        if(guesses.isdigit()):
            if (int(guesses) > 100):
                print "Too many guesses, retry"
            elif (int(guesses) < 1):
                print "Too few guesses, retry"
            else:
                guesses = int(guesses)
                break
        else:
            print "Invalid entry, retry"
    return guesses

def symbolCheck():
#Checks the users choice of symbol
    while(1):
        symbol = raw_input("Please enter an operations symbol or digit: ")
        if(len(symbol) == 1):
            if(symbol.isalpha()):
                print "Invalid entry, retry. (Does not count as incorrect guess)"
            else:
                if(symbol.isdigit() == False):
                    if(symbol == "+" or symbol == "*"):
                        break
                    else:
                        print "Invalid entry, retry. (Does not count as incorrect guess)"
                else:
                    break
        else:
            print "Invalid entry, retry. (Does not count as incorrect guess)"
    return symbol

def generateNext(complete, partial, symbol):
#creates a new string to replace a symbol in the partial Formula
    newSt = ""
    for i in range(len(complete)):
        if(complete[i] == symbol and partial[i] != symbol):
            newSt = newSt + symbol
        else:
            newSt = newSt + partial[i]
    return newSt

def convertBin(formula):
#creats binary list for lucky number 1
    counter = 2
    binList = []
    while(counter < len(formula)):
        if(int(formula[counter]) % 2 == 0):
           binList.append(0)
        else:
           binList.append(1)
        counter += 1
    return binList

def convertBin2(binList):
#converts binary list into base 10
    return int(''.join(str(e) for e in binList),2)

def lucky2(formula):
#creates a list for lucky number 2
    order = []
    form = formula[2:]
    newSt = ""
    for q in range (len(form)):
        for i in range (len(form)):
            newSt = newSt + form[i] + "+"
        newSt = newSt[:-1]
        order.append(newSt)
        form = form[1:]
        newSt = ""
    return order

def lucky2Count(luckyN):
#adds up the values in luckyN
    st = ""
    newSt = ""
    result = 0
    luckyN2 = []
    for i in range (len(luckyN)):
        result = 0
        newSt = ""
        st = luckyN[i]
        for s in range(len(st)):
            if(st[s] == "+"):
                newSt = newSt + "0"
            else:
                newSt = newSt + st[s]
        for q in range(len(newSt)):
            result = result + int(newSt[q])
        luckyN2.append(result)
    return luckyN2

#################
#Game
#################

#Variables#

points = 0
gamesPlayed = 0
currentGame = 1
guesses = 0
playing = True
wish = ""
globalList = read("fmlas.txt")
formula = ""
expFormula = ""
evalFormula = 0
pointCheck = 0
listB = []
lengthF = 0
partialF = ""
symbol = ""
newPartial = ""
visualGuess = ""
wrongGuess = 0
interFrmla = ""
userEval = ""
finalGamePoints = 0
uGuess = []
wholeGuess = False
correctEval = False
playing2 = True

###########

while(pointCheck == 0):
    points = raw_input("Provide points to start the games: ")
    if(points.isdigit()):
        if(int(points)<2):
            print "Must have at least 2 points to play"
        else:
            pointCheck = 1
            points = int(points)
    else:
        print "Invalid entry, retry"
        
while(playing):
    wish = raw_input("Do you wish to play ? y - yes, n - no: ")
    if(wish == "y" or wish == "Y"):
        playing2 = True
        wholeGuess = False
        correctEval = False
        uGuess = []
        partialF= ""
        print "Playing Game Number:", currentGame
        print"-----------------------------"
        print "You have this many points so far: ", points
        finalGamePoints = points
        guesses = guessChecker()
        wrongGuess = 0
        visualGuess = ""
        
        ##Make visual of guesses
        for s in range(guesses):
            visualGuess += "#"
        ##program selects formula
        formula = chooseFrmla(globalList)
        print "TRACE: computer chose this formula: ", formula
        lengthF = len(formula)
        
        ##formula expands
        expFormula = expand(formula)
        print "TRACE: expanded formula is: ", expFormula

        
        ##formula evaluates
        listB = evaluate(expFormula)
        evalFormula = evaluateTwo(listB)
        print "TRACE: evauluated formula is: ", evalFormula

        ##Partial Formula
        for i in range (lengthF):
            partialF += "-"
        print "The formula you will have to guess has", lengthF, "symbols ", partialF
        print "You can only use digits 0 to 9 and symbols + and *"
        
        while(1):
            ##Check if Valid entry and return if it is
            symbol = symbolCheck()
            uGuess.append(symbol)
            ##Check if symbol is in the string
            newPartial = generateNext(formula, partialF, symbol)
            if(newPartial == partialF):
                visualGuess = visualGuess.replace("#", "/", 1)
                print "Wrong guess (#-represents unused wrong guesses) ", visualGuess
                wrongGuess += 1
            elif(newPartial == formula):
                print "You have guessed the formula ", newPartial
                print "You receive 2 points"
                points += 2
                print "Point Total so far is: ", points
                print "The expanded formula is: ", expFormula
                wholeGuess = True
                break
            else:
                print "You have guessed a correct symbol ", newPartial
                partialF = newPartial
            if(wrongGuess == guesses):
                print "You have used up all of your guesses, game is over"
                points = points - 2
                gamesPlayed +=1
                print "You have lost 2 points, new point total is: ", points
                playing2 = False
                if(points <2):
                    playing = False
                    print "You do not have enoguh points to start a new game "
                break
        ##User calculate formula
        if (playing2):
            while(1):
                userEval =  raw_input("Please evauate the formula (answer is an integer): ")
                if(userEval.isdigit() == False):
                    print "Invalid evaluation, must be an integer, retry"
                else:
                    break
            ##Check wether user is right or wrong
            if(int(userEval)== evalFormula):
                points += 10
                print "You have correctly guessed and evaluated the formula."
                print "you have earned 12 points and your new total is: ", points
                correctEval = True
                gamesPlayed +=1
            else:
                points = points - 2
                print "Your evaluation is incorrect, the correct answer was: ", evalFormula
                print "You lost 2 points and your new total is: ", points
                gamesPlayed +=1
                if(points <2):
                    playing = False
                    print "You do not have enoguh points to start a new game "
                
    elif(wish == "n" or wish =="N"):        
        playing = False
    else:
        print "Invalid entry,retry"
    
print "-----------------------------------------------------------------------------"
print "All games are now over"
print "You have played ", gamesPlayed, " games and your point total is: ", points
print "The history of the last game you played is: "

print "You started with this many points: ", finalGamePoints
print "Mystery Formula was: ", formula

for q in range (len(uGuess)):
    print "user guessed: ", uGuess[q]
if(wholeGuess):
    print "You guessed the correct formula", formula
    if(correctEval):
        print "You evaluated correctly, the result was: ", evalFormula
    else:
        print "You evauluated incorrectly, the correct result was: ", evalFormula
else:
    print "You did not guess the correct formula", formula

print "Your final point total is: ", points

##Lucky Number Juan
firstL = convertBin(formula)
print "Based on the binary list: ", firstL
firstNum = convertBin2(firstL)
print "Your first lucky number is: :", firstNum

##Lucky Number Two
luckyN = lucky2(formula)
print "Based on the list of expressions", luckyN

luckyN2 = lucky2Count(luckyN)

    
print "and on the list of added values", luckyN2

luckyNum2 = 0
for z in range (len(luckyN2)):
    luckyNum2 = luckyNum2 + luckyN2[z]

print "Your second lucky number is: ", luckyNum2

print "Game over"