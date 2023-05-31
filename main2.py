from utils import Utils,Grapher
import re
from models import *
from constants import *
from NFA import *
from DFA import *
from DFA_DIRECT import *
from LEXER import *
from lexer2 import *
import uuid
import sys
from create_scanner import *
import json
from lr0 import *


file_numer = input('Ingrese que archivo desea utilizar: ')
#file_numer = '3'
yalFile =  f"slr-{file_numer}.yal"
yalex = Lexer(yalFile)
rules = yalex.getIndividualRules()
operators = yalex.getOperators()

#print(operators)
#print(individualRules)


yalexFile = f"slr-{file_numer}.yalp"
yalp = Parser(yalexFile)
yalp.replace_tokens(operators)
lr0 = LR0(*yalp.export())
lr0.build_slr1_table()
lr0.write_txt()
lr0.graph_LR0()
lr0.create_slr1_table_png()


#print(lr0.grammar)
#str_input = 'NUMBER + ID * ID'



input_file_test = input('Ingrese que archivo desea simular: ')
#input_file_test = '2.1'
file = f'./yalex_test/slr-{input_file_test}.yal.run'
with open(file, "r") as f:
    lines = f.readlines()
    

inputs = Utils.tokenize(lines)

for line in inputs:
    input_to_parse = []
    if len(line) > 0:
        for char in line:
            if char in operators:
                input_to_parse.append(char)
            else:      
                #print(repr(char))
                for key in operators:
                    if key in rules:
                        key = 'digits' if key == 'number' else key
                        regex = rules[key]
                        postfixExp = Convert_Infix_Postfix(regex)
                        postfixExp.toPostfix()
                        try:
                            thompson = build_thompson(postfixExp.postfix)
                            dfa = DFASubsets(thompson)
                            newAFD = dfa.create_DFASubset()
                            if key == 'digits':
                                char = char.replace('E-','')
                                char = char.replace('E+','')
                                char = char.replace('.','')
                                #print(char)
                            simulated = newAFD.simulate(char)
                            if simulated:
                                if key == 'digits':
                                    input_to_parse.append('number')
                                else:
                                    input_to_parse.append(key)#print(char,' ',operators[key])
                            else:
                               pass
                               #print(char,' not found :(')
                        except:
                           pass
                        #print(key,)
                        pass
        print(input_to_parse)
        #print(line)


    
input_to_parse = ['number','+','id','*','id']

def slr1_parse(input_to_parse):
    stack = [0]
    input_to_parse.append('$')
    index = 0
    while True:
        state = stack[-1]
        symbol = input_to_parse[index]
        action = lr0.slr1_table.loc[state,symbol]
        
        #print(action,type(action),state,symbol)
        if action.startswith('S'):  # Shift
            val = action.split(':')[1].lstrip().rstrip()
            stack.append(int(val))
            index += 1
            #print(val)
        elif action.startswith('R'): # reduce
            reduce,prods = action.split(':')
            print(reduce,prods,type(prods))
            #stack.pop()
            break
            #pass
        elif action.startswith('ACCEPT'): # ACCEPT
            print('Valid input!!!!')
            return 
        else:
            print('Invalid input!!!')
            return False
              
    
#slr1_parse(input_to_parse)