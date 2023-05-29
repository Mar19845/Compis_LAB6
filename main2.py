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


yalexFile = "slr-3.yalp"
a = Parser(yalexFile)

lr0 = LR0(*a.export())
#lr0.expand_grammar()
lr0.write_txt()
lr0.graph_LR0()

