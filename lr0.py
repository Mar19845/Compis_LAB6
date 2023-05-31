from typing import Any
from constants import *
from utils import Utils,Grapher
from graphviz import Digraph
from collections import defaultdict
import dataframe_image as dfi
import pandas as pd

class ITEM:
    def __init__(self, label,production, dot_position,derived=False):
        self.label = label
        self.production = production
        self.dot_position = dot_position
        self.derived = derived
        
    def __eq__(self, other):
        return self.label == other.label and self.production == other.production and self.dot_position == other.dot_position

    def __hash__(self):
        production = ''.join(self.production)
        return hash((self.label,production, self.dot_position))
    
    def __repr__(self):
        return f'{self.label} -> {" ".join(self.production[:self.dot_position]) + "." + " ".join(self.production[self.dot_position:])}'

    def get_item(self):
        return self.label,self.production,self.dot_position,self.derived
    

class LR0:
    def __init__(self,grammar,tokens,ignore_tokens):
        self.grammar = grammar
        self.tokens = tokens
        self.ignore_tokens = ignore_tokens
        self.terminals = []
        self.not_terminals = []
        self.states = None
        self.transitions = None
        self.start_symbol = None
        self.FIRST = {}
        self.FOLLOW = {}
        self.action_table = None
        self.goto_table = None
        self.slr1_table = None
        self.file_name = 'LR0_' + Utils.create_filename() 
        self.obtain_terminals_and_not_terminals()
        self.get_first_and_follow()
        self.calculate_collections()
    
    def obtain_terminals_and_not_terminals(self):
        terminals = []
        for symbol in self.grammar:
            self.not_terminals.append(symbol)
            for production in self.grammar[symbol]:
                terminals.extend(production)
            
                
        terminals = list(set(terminals))
        for symbol in  self.not_terminals:
            if symbol in terminals:
                terminals.remove(symbol)
        self.terminals = terminals
        
    def get_terminals_and_not_terminals(self):
        return self.terminals,self.not_terminals
        
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
    
    def expand_grammar(self):
        
        first_key = list(self.grammar.keys())[0]
        grammar = {
            'S': [['.',first_key]]
        }
        self.grammar =  grammar | self.grammar
    
    def calculate_collections(self):
        extend_grammar_label = list(self.grammar.keys())[0] +'\''
        self.start_symbol = extend_grammar_label
        items = ITEM(label= extend_grammar_label,production=[list(self.grammar.keys())[0]],dot_position=0)
        states = [self.closure({items}, self.grammar)]
        stack = [states[0]]
        transitions = []
        while stack:
            state = stack.pop()
            for symbol in set(sym for item in state for sym in item.production[item.dot_position:item.dot_position + 1]):
                next_state = self.goto(state, symbol, self.grammar)
                if not next_state:
                    continue
                if next_state not in states:
                    states.append(next_state)
                    stack.append(next_state)
                transitions.append((states.index(state), symbol, states.index(next_state)))
        
        accept_state = len(states)
        for i,state in enumerate(states):
            for item in state:
                if item.label == extend_grammar_label and item.dot_position == len(item.production) and item.derived == False:
                    transitions.append((i,'$',accept_state))
                    break
                
        states.append(set())
        
        self.states = states
        self.transitions = transitions
        
    def goto(self,items,symbol,productions):
        next_items = set()
        for item in items:
            if item.dot_position < len(item.production) and item.production[item.dot_position] == symbol:
                next_items.add(ITEM(label=item.label,production=item.production, dot_position= item.dot_position + 1))
        return self.closure(next_items, productions)
        
    
    def closure(self,item,grammar):
        new_items = set(item)
        changed = True
        while changed:
            changed = False
            for item in list(new_items):
                if item.dot_position < len(item.production) and item.production[item.dot_position] in grammar:
                    non_terminal = item.production[item.dot_position]
                    for production in grammar[non_terminal]:
                        new_item = ITEM(label=non_terminal,production=production,dot_position=0,derived=True)
                        if new_item not in new_items:
                            new_items.add(new_item)
                            changed = True
        return new_items
    
    def write_txt(self):
        file_path = Utils.create_file_path(self.file_name)
        f = open(file_path + '.txt', 'w+', encoding="utf-8")
        f.write("---------------LR0---------------\n")
        f.write(f"NOT TERMINALS: {self.not_terminals}\n")
        f.write(f"TERMINALS: {self.terminals}\n")
        f.write("\nFIRST: \n")
        for key,value in self.FIRST.items():
            f.write(f"{key}: {value}\n")
        f.write("\nFOLLOW: \n")
        for key,value in self.FOLLOW.items():
            f.write(f"{key}: {value}\n")
        f.write("\nSTATES: \n")
        for i, state in enumerate(self.states):
            f.write(f'{i}: {state}\n')
        f.write("\nTRANSITION: \n")
        for transition in self.transitions:
            #print(type(transition))
            f.write(repr(transition)+'\n')
    
    def graph_LR0(self):
        dot = Digraph("LR0", format='png')
        dot.attr(rankdir="LR")
        dot.attr('node', shape='hexagon')
        for i, state in enumerate(self.states):
            if i == len(self.states) - 1:  # Estado de aceptación
                label = 'ACCEPTED'
            else:
                non_derived = []
                derived = []
                for item in state:
                    if item.derived:
                        derived.append(str(item))
                    else:
                        non_derived.append(str(item))

                label = 'I' + str(i) + '\n-----------\n'
                label += '\n'.join(non_derived) + '\n-----------\n' + '\n'.join(derived)

            dot.node(str(i), label=label)

        for t in self.transitions:
            dot.edge(str(t[0]), str(t[2]), label=t[1])

            # Generar y guardar el gráfico como imagen PNG
        file_path = Utils.create_file_path(self.file_name)
        dot.render(file_path, cleanup=True)
    
    def get_next_state(self,old_state,symbol):
        for i,state in enumerate(self.transitions):
            if state[0] == old_state and state[1] == symbol:
                return self.transitions[i]
        
        return None

    def build_slr1_table(self):
        action_table = defaultdict(dict)
        goto_table = defaultdict(dict)
        for i,state in enumerate(self.states):
            for item in state:
                label,production,dot_position,derived = item.get_item()
                
                if dot_position != len(production):
                    next_symbol = production[dot_position]
                    #print(next_symbol,type(next_symbol))
                    
                    
                    if next_symbol in self.terminals:
                        next_state = self.get_next_state(i,next_symbol)
                        if next_state is not None:
                            action_table[i][next_symbol] = ('S', next_state[2])
                            pass
                        
                    
                    elif next_symbol in self.not_terminals:
                        next_state = self.get_next_state(i,next_symbol)
                        if next_state is not None:
                            goto_table[i][next_symbol] = next_state[2]
                
                elif label != self.start_symbol:
                    if label in self.not_terminals: # compute only the not_terminals
                        for symbol in self.FOLLOW[label]:
                            #print(i,symbol,label,production) # print
                            action_table[i][symbol] = ('R', (label, production))
                            #next_state = self.get_next_state(i,symbol)
                            #if next_state is not None:
                                #action_table[i][symbol] = ('R', next_state[2])
                            pass
                            
                elif label == self.start_symbol and dot_position == len(production):
                    action_table[i]['$'] = ('ACCEPT', 'None')
                    pass
        self.action_table = action_table
        self.goto_table = goto_table
    
    def create_slr1_table_png(self):
        #print(self.terminals.sort())
        
        
        def custom_sort(elem):
            order = {'+': 0, '-': 1, '*': 2, '/': 3, '(': 4, ')': 5, 'id': 6, 'number': 7}
            return order.get(elem, float('inf'))

        sorted_a = sorted(self.terminals, key=custom_sort)
        columns = sorted_a
        columns.extend('$')
        columns.extend(self.not_terminals)

        df = pd.DataFrame(columns=columns)
        #df = pd.DataFrame(columns=self.terminals)
        # Llenar el dataframe con los valores de action_table
        for estado, acciones in self.action_table.items():
            for terminal, accion in acciones.items():
                accion_tipo, accion_valor = accion
                #print(estado, terminal)
                df.loc[estado, terminal] = f"{accion_tipo}: {accion_valor}"

        # Llenar el dataframe con los valores de goto_table
        for estado, gotos in self.goto_table.items():
            for not_terminal, goto in gotos.items():
                #print(estado, not_terminal)
                df.loc[estado, not_terminal] = goto

        # Rellenar celdas vacías con NaN en lugar de None
        df = df.fillna(pd.NA)

        # Mostrar el dataframe resultante
        #print(df.head(100))
        self.slr1_table = df
        df_styled = df.style.background_gradient() 
        file_name = self.file_name + '_SLR1_TABLE.png'
        file_path = Utils.create_file_path(file_name)
        dfi.export(df_styled,file_path)
        
        
                    
        
        
        