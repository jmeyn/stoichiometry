import symbol
class Info:
    '''Holds information of Elements and Compounds'''

    def __init__(self):
        #Real names (in order): symbol, mass, name, number, amount
        self.data = ['', 0.0, '', 0, 0]
    
    def change(self, name, value):
        i = 0
        if name in [0, 'symbol']:
            i = 0
        elif name in [1, 'mass']:
            i = 1
        elif name in [2, 'name']:
            i = 2
        elif name in [3, 'number']:
            i = 3
        elif name in [4, 'amount']:
            i = 4
        self.data[i] = value

    def symbol(self):
        return self.data[0]
    def mass(self):
        return self.data[1]
    def name(self):
        return self.data[2]
    def number(self):
        return self.data[3]
    def amount(self):
        return self.data[4]

class Element:
    '''A class to hold element information'''

    def amount(self):
        for i in range(len(self.stat.symbol()) ):
            if not self.stat.symbol()[i].isalpha():
                temp = int(self.stat.symbol()[i:])
                self.stat.change('symbol', self.stat.symbol()[:i])
                return temp
        else:   #if self.stat.symbol has no amount attached, defaults to 1
            return 1

    def find(self): #Might revert back to single data return
        '''Finds element in table.bin, returns element mass'''

        with open('table.bin', 'rb') as f:
            for line in f:

                if line.split()[0] == self.stat.symbol(): #line.split()[0] is symbol location

                    for term in range( len(line.split()) ):
                        self.stat.change(term, type(self.stat.data[term])(line.split()[term]))
                    break

            else:
                print 'ERROR: unknown element %s. Exiting program' % self.stat.symbol()
                f.close()
                exit(1)

    def __init__(self, symbol, compoundAmount):
        self.stat = Info()
        self.stat.change('symbol', symbol)
        self.stat.change('amount', compoundAmount * self.amount())
        
        print '  Element<__init__> symbol:', symbol
        print '  Element<__init__> self.stat.symbol:', self.stat.symbol(), self.stat.amount()

        self.find()

class Compound:
    '''A class to hold compounds, which hold class(Element)'''

    def analyze(self):
        '''Determines interior elements and puts them in array(inside)'''

        j = len( str( self.stat.amount() ) )
        brackets = ()
        
        for i in range( len( str( self.stat.amount()) ), len(self.stat.symbol()) ):
            print 'Compound<analyze>for;start;:', j, i
            
            if self.stat.symbol()[i].isupper() and (i != len( str( self.stat.amount()))): #P4
                print 'Compound<analyze>for;if1:', i, j
                self.inside.append(
                    Element(
                        self.stat.symbol()[j:i],
                        self.stat.amount() ) )
                j = i

            elif self.stat.symbol()[i] == '(':  #P1
                if not j == i: #If not first char after total amount is '(', append another compound
                    self.inside.append(
                        Element(
                            self.stat.symbol()[j:i-1],
                            self.stat.amount() ) )
                    j = i + 1

                if not len(brackets) == 0:
                    print 'Too many \'\(\' brackets in userInput. Exiting program',
                    print 'If you believe this is wrong, report this in the GitHub repo.'
                    exit(1)
                else:
                    brackets += (i,)

            elif self.stat.symbol()[i] == ')':  #P1
                if not len(brackets) == 1:
                    print 'Missing brackets in userInput. Exiting program',
                    print 'If you believe this is wrong, report this in the GitHub repo.'
                    exit(1)
                else:
                    brackets += (i, int( self.stat.symbol()[i+1:]), )

        else:
            self.inside.append(
                Element(
                    self.stat.symbol()[j:],
                    self.stat.amount() ) )

    def coef(self):
        for i in range( len(self.stat.symbol()) ):
            currentChar = self.stat.symbol()[i]

            if not currentChar.isdigit():
                break

        #if Compound has no coefficient, amount defaults to 1
        if not self.stat.symbol()[0].isdigit():
            self.stat.change('symbol', '1' + self.stat.symbol())

            return 1

        else:
            return int( self.stat.symbol()[0:i] )

    def mass(self):
        for i in self.inside:
            self.stat.change('mass', self.stat.mass() + i.stat.mass())

    def __init__(self, symbol):
        self.stat = Info()
        self.inside = []
        self.massInput = 0.0 #Will be used later
                
        self.stat.change('symbol', symbol)
        self.stat.change('amount', self.coef())

        self.analyze()
        self.mass()

def empirical():
    storage = [ ]

    while True:
        print 'Enter your list of percent amounts of elements (type \'help\' for help)'
        userInput = raw_input(">>> ")

        if userInput == 'help':
            print '\nWelcome to the stoichiometry.py help page!'
            print '* The expected input for this program is as follows:'
            print '\tMASS SYMBOL, MASS SYMBOL, ...'
            print '* Where \'MASS\' is AT MOST in the thousandths place.'
            print '\nAny bugs, issues, requests? Put them in the GitHub repo.\n'
        elif userInput == 'quit':
            exit(0)
        else:
            break

    #TODO: finish stuff!
    for i in userInput.split(','):
        try:
            storage.append(
                (Compound(
                    i.split()[0] ),
                int( i.split()[1] )) )

        except:
            print 'Incorrect syntax in userInput. Exiting program.',
            print 'If you believe this is wrong, report this in the GitHub repo.'
            exit(0)

def limiting():
    reactants = [ ]
    products  = [ ]
    switch    = False

    #Phase 1: read input and check for commands
    while True:
        print 'Enter your BALANCED chemical equation (type \'help\' for help)'
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
            exit(0)
        else:
            break

    #Phase 2: read input and put compounds into list(reactants) or list(products)
    for i in userInput.split():

        if i == '->':
            if switch is True:
                print 'Repeated syntax %s in userInput.' % i,
                print 'If you believe this is wrong, report this in the GitHub repo.'
                exit(1)

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
                exit(1)
        else:
            if switch is True:
                products.append( Compound(i) )
                switch = False

            else:
                reactants.append( Compound(i) )

    #Phase 3: userInput of each compound's mass
    for i in reactants + products:
        print i
        print 'How many grams of %s are in the reaction? (Type \'?\' if value is unknown' % i.stat.symbol

        if userInput == '?':
            continue

        else:
            i.massInput = float( raw_input(">>>") ) #Would like to rename variable

    #debug
    for i in reactants:
        print 'reactants:'
        print '%10f' % i.massInput
        for j in i.inside:
            print 'r:'
            print '%10s' % j.stat.data[0]
            print '%10f' % j.stat.data[1]
            print '%10s' % j.stat.data[2]
            print '%10d' % j.stat.data[3]
    for i in products:
        print i.massInput
        print 'products:'
        for j in i.inside:
            print 'p:'
            print '%10s' % j.stat.data[0]
            print '%10f' % j.stat.data[1]
            print '%10s' % j.stat.data[2]
            print '%10d' % j.stat.data[3]

def main():
    #Phase 1: read input and check for commands
    while True:
        print 'What mode of stoichiometry would you like to do? (type \'help\' for help)'
        userInput = raw_input(">>> ")

        if userInput.lower() == 'help':
            print '\nWelcome to the stoichiometry.py help page!\n'
            print 'For empirical/molecular formula, type \'empirical\' or \'molecular\''
            print 'For limiting reactant solver, type \'limiting\''
            print '\nAny bugs, issues, requests? Put them in the GitHub repo.\n'

        elif userInput.lower() == 'quit':
            exit(0)

        elif userInput.lower() in ['empirical', 'emp', 'molecular', 'mol']:
            empirical()
            break

        elif userInput.lower() in ['limiting', 'lim']:
            limiting()
            break

if __name__ == '__main__':
    test = Compound( raw_input("Compound: ") )
    print test.stat.data

    #main() *need to work on Compound.analyze() more

    exit(0)
