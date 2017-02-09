class Info:
    '''Holds information of Elements and Compounds'''

    def __init__(self):
        #Real names (in order): symbol, number, mass, name, amount
        self.data = ['', 0, 0.0, '', 0]

    def index(self, value):
        '''Returns index value of corresponding real name'''
        try:
            value.isalpha()
        except:
            return value

        j = 0
        for i in ['symbol', 'number', 'mass', 'name', 'amount']:
            if i == value:
                return j
            j += 1

    def symbol(self):
        return self.data[0]
    def number(self):
        return self.data[1]
    def mass(self):
        return self.data[2]
    def name(self):
		return self.data[3]
    def amount(self):
        return self.data[4]

class Element:
    '''A class to hold element information'''

    def amount(self):
        j = 0
        temp = []

        for i in range( len(self.stat.symbol) ):

            if self.stat.symbol[i].isdecimal():
                temp = self.stat.symbol[i:]
                self.stat.symbol = self.stat.symbol[:i]
                return int(temp)
        else:
            self.stat.symbol = self.stat.symbol[:i+1]
            return 1

    def find(self, value):
        '''Finds element in periodictable.txt, returns element mass'''
        f = open('periodictable.txt', 'r')

        value = self.stat.index(value)
        maxSearch = self.stat.index(value)

        for line in f:

            for i in range( maxSearch + 1 ):

                if line.split()[i] == self.stat.symbol():
                    f.close()
                    return line.split()[maxSearch]
        else:
            print 'ERROR: unknown element %s. Exiting program' % self.stat.symbol
            f.close()
            exit(-1)

    def __init__(self, symbol, totalAmount):
        self.stat = Info()
        self.stat.symbol = symbol
        self.stat.amount = totalAmount * self.amount()

class Compound:
    '''A class to hold compounds, which hold class(Element)'''

    def analyze(self):
        '''Determines interior elements and puts them in array(inside)'''
        j = 0
        bracketAmount  = 1

		#index slice of what's inside the brackets
        bracketLocation= ()

        #Finds where the brackets are located and what amount is assigned to them
        for i in range( len(str(self.stat.amount)), len(self.stat.symbol) ):

            if self.stat.symbol[i] == '(':
				bracketLocation = (i,)

            elif self.stat.symbol[i] == ')':
                bracketLocation = bracketLocation + (i-1,)

            	#Checking if there are not enough/too many extra brackets
                if len(bracketLocation) is not 2:
					print 'Missing or too many brackets in userInput.',
					print 'If you believe this is wrong, report this in the GitHub repo.'
					exit(-1)

                for j in range( i + 1, len(self.stat.symbol) ):

                    if not self.stat.symbol[j].isdecimal():
                        bracketAmount = int( self.stat.symbol[ bracketLocation[1] + 1:j ] )
                        j = 1

                        break
                else:
                    try:
                        bracketAmount = int( self.stat.symbol[i+1:] )
                    except:
                        bracketAmount = 1

                    j = 1
                    break

        for i in range( len(str(self.stat.amount)), len(self.stat.symbol) ):

            #If i.isupper(): insideAmount.append(self.stat.symbol[slice])
            if self.stat.symbol[i].isupper() and not i == len(str(self.stat.amount)):

                if len( bracketLocation ) > 0:

                    if i >= bracketLocation[0] and i <= bracketLocation[1]:

                        if j < bracketLocation[0]:

                            for k in range(j, i):

                                if k == bracketLocation[0]:
                                    self.inside.append(
                                        Element(
                                            self.stat.symbol[ j:k ],
                                            self.stat.amount ) )

                                    j = i
                                    break

                        elif i > bracketLocation[1]:
                            self.inside.append(
                                Element(
                                    self.stat.symbol[ j:bracketLocation[1] - 1 ],
                                    self.stat.symbol * bracketAmount ) )

                            j = i

                        else:
                            self.inside.append(
                                Element(
                                    self.stat.symbol[ j:i ],
                                    self.stat.amount * bracketAmount ) )

                            j = i

        else:
            if len( bracketLocation ) > 0:

                if j <= bracketLocation[1]:
                    self.inside.append(
                        Element(
                            self.stat.symbol[ j:bracketLocation[1]+1 ],
                            self.stat.amount * bracketAmount ) )

            else:
                self.inside.append(
                    Element(
                        self.stat.symbol[ j: ],
                        self.stat.amount ) )

    def coef(self):
        for i in range( len(self.stat.symbol) ):
            currentChar = self.stat.symbol[i]

            if not currentChar.isdigit():
                break

        #if Compound has no coefficent, amount defaults to 1
        if not self.stat.symbol[0].isdigit():
            change = '1' + self.stat.symbol
            self.stat.symbol = change

            return 1

        else:
            return int( self.stat.symbol[0:i] )

    def elementLen(self):
        j = 0

        for i in self.stat.symbol:
            if i.isupper():
                j += 1

        return j

    def __init__(self, symbol):
        self.stat = Info()
        self.stat.symbol = symbol
        self.stat.amount = self.coef()

        self.inside = []
        self.analyze()

if __name__ == '__main__':
    reactants = [ ]
    products  = [ ]
    switch    = False

    while True:
        print 'Input your BALANCED chemical equation (type \'help\' for help)'
        userInput = raw_input(">>> ")

        if userInput == 'help':
            print '\nWelcome to the stoichiometry.py help page!\n'
            print 'The expected input for this program is as follows:'
            print '\tR + R... -> P + P...'
            print '* R: Reactants (any order, seperated by the syntax, \' + \'(space plus space)'
            print '* ->: yields symbol, please put a space before and after it'
            print '* P: Products (any order, separated by the syntax, \' +  \'(space plus space)'
            print '\nAny bugs, issues, requests? Put them in the GitHub repo.\n'
        elif userInput == 'quit':
            exit(1)
        else:
            break

    for i in userInput.split():
        if i == '->':
           if switch is True:
              print 'Repeated syntax %s in userInput.' % i,
              print 'If you believe this is wrong, report this in the GitHub repo.'
              exit(-1)

           switch = True
           continue

        for j in i:
            if j.isalnum() or j in [')', '(']:
                continue
            elif j == '+':
                 break
            else:
                print 'Unknown character %c in userInput.' % j,
                print 'If you believe this is wrong, report this in the GitHub repo.'
                exit(-1)
        else:
             if switch is True:
                 products.append( Compound(i) )
                 switch = False
             else:
                 reactants.append( Compound(i) )

    #debug
    for i in reactants:
        print 'reactants:'
        for j in i.inside:
            print '%5s, %5d' % (j.stat.symbol, j.stat.amount)
    for i in products:
        print 'products:'
        for j in i.inside:
            print '%10s, %04d' % (j.stat.symbol, j.stat.amount)
