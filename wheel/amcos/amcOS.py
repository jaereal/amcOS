from sly import Lexer, Parser
from time import sleep

class CalcLexer(Lexer):
    # Set of token names (required)
    tokens = { NAME, NUMBER, PLUS, MINUS, TIMES, DIVIDE, POWER, ASSIGN }
    ignore = ' \t'

    # Tokens as regular expressions
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    POWER   = r'\^' 
    ASSIGN  = r'='
    NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value) # Convert string to integer
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    # Define operator precedence (low to high)
    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', POWER),
    )

    def __init__(self):
        self.variables = { }

    # Grammar rules
    @_('NAME ASSIGN expr')
    def statement(self, p):
        self.variables[p.NAME] = p.expr

    @_( 'expr')
    def statement(self, p):
        print(p.expr)

    @_('expr PLUS expr',
       'expr MINUS expr',
       'expr TIMES expr',
       'expr DIVIDE expr',
       'expr POWER expr')
    def expr(self, p):
        if p[1] == '+': return p.expr0 + p.expr1
        elif p[1] == '-': return p.expr0 - p.expr1
        elif p[1] == '*': return p.expr0 * p.expr1
        elif p[1] == '/': return p.expr0 / p.expr1
        elif p[1] == '^': return p.expr0 ** p.expr1

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('NAME')
    def expr(self, p):
        return self.variables.get(p.NAME, 0)
    

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    version = "v"+"0.2.1"
    intro = ("welcome to amcOS the system that does advance math(can even do 5^5^5),welcome to advanced-math-calculator-operating-system,"+version).split(",")
    for line in intro:
        for l in line:
            print(l,end="",flush=True)
            sleep(0.1)
        print("")
    while True:
        file = input("load:")
        while file == "":
            text = input("amcOS>")
            for l in "loading...":
                print(l,end="",flush=True)
                sleep(0.1)
            print()
            parser.parse(lexer.tokenize(text))
        with open(file,"r") as amc:
            code = amc.read().split("\n")
            for c in code:
                parser.parse(lexer.tokenize(c))