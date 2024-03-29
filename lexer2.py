from constants import *

class Parser:
    def __init__(self, file):
        self.file = file
        self.grammar = {}
        self.tokens = []
        self.ignore_tokens = []
        self.ERROR = False
        self.read()

        
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
                    production_name = line.split(':')[0].upper()[0]
                    if production:
                        self.grammar[production_name] = []
                        #print(repr(production_name),production)
                    else:
                        print('Revisar el archivo .yalp')
                        self.ERROR = not self.ERROR
                        raise Exception("No productions separator '%%' found")
                        break
                elif line.startswith(';'):
                    production = not production
                else:
                    if len(line) > 0:
                        line = line.replace('|', '',1).lstrip().rstrip()
                        line = line.split()
                        new_line = []
                        # replace not terminals to only first char
                        for prod in line:
                            if prod not in self.tokens:
                                new_line.append(prod.upper()[0])
                            else:
                                new_line.append(prod)
                        
                        self.grammar[production_name].append(new_line)
                        #print(repr(line),production_name)
                        
    def replace_tokens(self,operators):
        inverted = {}
        for k,v in operators.items():
            if v in self.tokens:
                #print(v,self.tokens)
                index = self.tokens.index(v)
                self.tokens[index] = k
            if v in self.ignore_tokens:
                index = self.ignore_tokens.index(v)
                self.ignore_tokens[index] = k
            
            inverted[v] = k
        for k in self.grammar:
            for prod in self.grammar[k]:
                for i in prod:
                    if i in inverted:
                        index = prod.index(i)
                        prod[index] = inverted[i]
                        #print(inverted[i],i,prod)
                #print(prod)

                    
        #print(inverted)      
        #print(self.grammar)
        #inverted = {}
        #for key, value in operators.items():
            #inverted[value] = key
            
        
    
    # export grammar, tokens and ignore
    def export(self):
        return self.grammar,self.tokens,self.ignore_tokens
    
    