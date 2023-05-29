from constants import *

class Parser:
    def __init__(self, file):
        self.file = file
        self.grammar = {}
        self.tokens = []
        self.ignore_tokens = []
        self.children = []
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
                    production_name = line.split(':')[0]
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
                        self.grammar[production_name].append(line)
                        #print(repr(line),production_name)
                        
    def replace_tokens(self):
        pass
    
    # export grammar, tokens and ignore
    def export(self):
        return self.grammar,self.tokens,self.ignore_tokens
    
    