OPEN_LIST = ['(', '{', '['] 
CLOSE_LIST = [')', '}', ']']
OPEN_CORCHETE = '{'
CLOSED_CORCHETE = '}'
OPEN_PARENTESIS = '('
CLOSED_PARENTESIS = ')'
OPEN_CORCHETE_CERRADO = '['
CLOSED_ORCHETE_CERRADO = ']'
PLUS_OPERATOR = '+'


# Yalex comments 
# Ignore lines with comments
COMMENT_START1 = "(*"
COMMENT_END1 = "*)"
COMMENT_START2 = "{"
COMMENT_END2 = "}"
YALEX_REGEX = 'let'
YALEX_TOKEN = 'rule tokens'
TOKEN_RETURN = 'return'
# Yapar
IGNORE = 'IGNORE'
YAPAR_TOKEN = '%token'
YAPAR_COMMENT_END = '*/'
YAPAR_COMMENT_INIT = '/*'





ALPHABET = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
                        [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
                        [chr(i) for i in range(ord('0'), ord('9') + 1)] + \
                        ['\t', '\n',' '] 
# PATH
DIRECTORY = './generated/'
YALEX_DIRECTORY = './yalex/'
YALEX_TEST = './yalex_test/'
# OPERATORS                        
EPSILON = 'ε'
KLEENE = '*'
DOT = '•'
OPTIONAL= '?'
ALTERNATIVE= '|'
SYMBOLS = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
               '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\\', 'n', 't', '•'])