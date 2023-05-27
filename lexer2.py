from constants import *

class Parser:
    def __init__(self, file):
        self.file = file
        self.grammar = {}
        #self.tokens = {}
        self.tokens = []
        #self.ignore_tokens = {}
        self.ignore_tokens = []
        self.children = []
        self.FIRST = {}
        self.FOLLOW = {}
        self.ERROR = False
        self.read()
        self.get_first_and_follow()
        
    def read(self):   
        with open(YALEX_DIRECTORY + self.file, "r") as file:
            lines = file.readlines()
            production = False
            production_name = ''
            for line in lines:
                line = line.rstrip().lstrip().replace("\n",'')
                #print(repr(line),production)
                # comment lines
                if line.startswith(YAPAR_COMMENT_INIT) and line.endswith(YAPAR_COMMENT_END):
                    if '->' in line:
                        pass
                        #print(repr(line))
                elif line.startswith(YAPAR_TOKEN):
                    line = line.replace(YAPAR_TOKEN,'',1).lstrip().rstrip()
                    line = line.split()
                    self.tokens.extend(line)
                    
                elif line.startswith(IGNORE):
                    line = line.replace(IGNORE,'',1).lstrip().rstrip()
                    line = line.split()
                    self.ignore_tokens.extend(line)
                elif line.endswith(':'):
                    production = not production
                    production_name = line.split(':')[0]
                    if production:
                        self.grammar[production_name] = []
                        #print(repr(production_name),production)
                    else:
                        print('Revisar el archivo .yalp')
                        self.ERROR = not self.ERROR
                        break
                elif line.startswith(';'):
                    production = not production
                else:
                    if len(line) > 0:
                        line = line.replace('|', '',1).lstrip().rstrip()
                        line = line.split()
                        self.grammar[production_name].append(line)
                        #print(repr(line),production_name)
                        
    def replace_tokens(self):
        pass
    
    def get_first_and_follow(self):
        for symbol in self.grammar:
            first = list(self.calculate_first(symbol))
            follow = list(self.calculate_follow(symbol))
            self.FIRST[symbol] = first
            self.FOLLOW[symbol] = follow
            
    # Calculate FIRST sets for all non-terminal symbols
    def calculate_first(self,symbol):
        if symbol in self.FIRST:
            return self.FIRST[symbol]

        self.FIRST[symbol] = set()

        for production in self.grammar[symbol]:
            if production[0] not in self.grammar:
                self.FIRST[symbol].add(production[0])

            elif production[0] == symbol:
                continue

            else:
                first_of_production = self.calculate_first(production[0])
                self.FIRST[symbol].update(first_of_production)

                i = 1
                while 'epsilon' in first_of_production and i < len(production):
                    first_of_production = self.calculate_first(production[i])
                    self.FIRST[symbol].update(first_of_production - set(['epsilon']))
                    i += 1

                if 'epsilon' in first_of_production and i == len(production):
                    self.FIRST[symbol].add('epsilon')

        return self.FIRST[symbol]
    
    # Calculate FOLLOW sets for all non-terminal symbols
    def calculate_follow(self,symbol):
        if symbol in self.FOLLOW:
            return self.FOLLOW[symbol]

        self.FOLLOW[symbol] = set()

        if symbol == list(self.grammar.keys())[0]:
            self.FOLLOW[symbol].add('$')

        for non_terminal in self.grammar:
            for production in self.grammar[non_terminal]:
                if symbol in production:
                    symbol_index = production.index(symbol)
                    if symbol_index == len(production) - 1:
                        self.FOLLOW[symbol].update(self.calculate_follow(non_terminal))
                    else:
                        next_symbol = production[symbol_index + 1]
                        if next_symbol not in self.grammar:
                            self.FOLLOW[symbol].add(next_symbol)
                        else:
                            first_of_next_symbol = self.calculate_first(next_symbol)
                            self.FOLLOW[symbol].update(first_of_next_symbol - set(['epsilon']))
                            if 'epsilon' in first_of_next_symbol:
                                self.FOLLOW[symbol].update(self.calculate_follow(non_terminal))

        return self.FOLLOW[symbol]
    
    # expand the grammar by adding the S' at the beginning of the grammar
    def expand_grammar(self):
        first_non_terminal = list(self.grammar.keys())[0]
        new_grammar = {
            "S'": [['.',first_non_terminal]]
        }
        new_grammar.update(self.grammar)
        self.grammar = new_grammar
        #print(first_non_terminal)
        
    def shift_closure(self):
        for non_terminal in self.grammar:
            for production in self.grammar[non_terminal]:
                if '.' not in production:
                    production.insert(0, '.')
                else:
                    index = production.index('.')
                    del production[index]
                    production.insert(index+1, '.')
    
    def goto_closure(self,production):
        new_production = production
        if '.' not in new_production:
            new_production.insert(0, '.')
            return new_production

        index = new_production.index('.')
        del new_production[index]
        new_production.insert(index+1, '.')
        return new_production
        
    def closure2(self,grammar):
        self.expand_grammar()
        self.shift_closure()
        done = []
        edges = []
        #closure = set()
        closure = {}
        new_items_added = True
        
        while new_items_added:
            new_items_added = False
            for non_teminal in grammar:
                for production in grammar[non_teminal]:
                    if '.' in production:
                        index = production.index('.')
                        if index + 1 < len(production) and production[index + 1] == non_teminal:
                            next_symbol = production[index + 2] if index + 2 < len(production) else None
                            
                            if next_symbol in grammar:
                                for r_production in grammar[next_symbol]:
                                    new_item = self.goto_closure(r_production)
                                    if ''.join(new_item) not in closure:
                                        closure[''.join(new_item)] = new_item
                                        new_items_added = True 
                                pass
                            elif next_symbol:
                                #print(production[:index],next_symbol,'.',production[index + 3:][0],production)
                                #new_item = production[:index] + next_symbol + '.' + production[index + 3:]
                                new_item = [next_symbol,'.',production[index + 3:][0]]
                                if ''.join(new_item) not in closure:
                                    closure[''.join(new_item)] = new_item
                                    new_items_added = True
                            #print(production,next_symbol)
            #new_items_added = False
        return closure
    def closure(self):
        self.expand_grammar()
        self.shift_closure()
        done = []
        for non_terminal in self.grammar:
            for production in self.grammar[non_terminal]:
                
                if '.' in production:
                    index = production.index('.')
                    if index == len(production) - 1:
                        pass
                    else:
                        edge = production[index + 1]
                        
                        if edge not in done:
                            done.append(edge)
                        
                        for non_terminal in self.grammar:
                            for production in self.grammar[non_terminal]:
                                
                                if edge in production:
                                    new_production = self.goto_closure(production)
                                    production = new_production
                                    for non_terminal in self.grammar:
                                        for production in self.grammar[non_terminal]:
                                            
                                            if '.' in production:
                                                index = production.index('.')
                                                if (production[-1] != '.') and production[index + 1] in list(self.grammar.keys()):
                                                    new_edge = production[index + 1]
                                                    
                                                if production[-1] != '.':
                                                    self.closure()
                                                    
                                                    
                                    #print(production,new_production)
    
    
    
    
    
                
            
            
        
                        
                    
                    
yalexFile = "slr-2.yalp"
a = Parser(yalexFile)
#a.expand_grammar()
#print(repr(a.grammar))
#c =  a.closure2(a.grammar)
#print(c)

#print(repr(a.grammar))
#print(a.tokens)
print(a.FIRST)
print(a.FOLLOW)
#for k in a.grammar.keys():
    #for v in a.grammar[k]:
        #print(k,v)
        #print(k,repr(a.grammar[k]))
#print(a.grammar)