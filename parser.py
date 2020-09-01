from sly import Lexer, Parser
from lexer import LCarnitineLexer

class LCarnitineParser(Parser):
    tokens = LCarnitineLexer.tokens

    def __init__(self):
        self.names = { }

    precedence = (
        ('left','OROR'),
        ('left', 'ANDAND'),
        ('left','EQUALEQUAL'),
        ('left', 'LT', 'GT', 'LE', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'NOT')
    ) 

    @_('element lcarnitine') # parse tree root? p[0] indices may need to be reduced by 1, so [p[0]] + p[1]?
    def lcarnitine(self, p):
        return [p[0]] + p[1]

    @_('empty') # can go to empty rule
    def lcarnitine(self, p):
        return []
        
    @_('') # use for optional empty 
    def empty(self, p):
        pass

     # function names define the grammar rule name, and the params to decorator define where they go
    @_('FUNCTION IDENTIFIER LPAREN optparams RPAREN compoundstmt')
    def element(self, p):
        return ("function", p[1], p[3], p[5]) # this is building up AST

    @_('stmt SEMICOLON') # removed semi-colon, maybe remove this if you don't want to end stmt with ; (SEMICOLON)
    def element(self, p):
        return ("stmt", p[0])

    @_('params')
    def optparams(self, p):
        return p[0]

    @_('empty')
    def optparams(self, p):
        return []

    @_('IDENTIFIER COMMA params')
    def params(self, p):
        return [p[0]] + p[2]

    @_('IDENTIFIER') # last parameter
    def params(self, p):
        return [p[0]]

    @_('LBRACE statements RBRACE')
    def compoundstmt(self, p):
        return p[1]

    @_('stmt SEMICOLON statements')
    def statements(self, p):
        return [p[0]] + p[2]

    @_('empty') # empty statements
    def statements(self, p):
        return []

    @_('IF exp compoundstmt') # if-then stmt
    def stmt(self, p):
        return ("if-then", p[1], p[2])
    
    @_('IF exp compoundstmt ELSE compoundstmt') # if-then-else stmt
    def stmt(self, p):
        return ("if-then-else", p[1], p[2], p[4])
    

    @_('IDENTIFIER EQUAL exp') # assignment stmt
    def stmt(self, p):
        return ("assign", p[0], p[2])

    @_('RETURN exp') # return stmt
    def stmt(self, p):
        return ("return", p[1])

    @_('VAR IDENTIFIER EQUAL exp') # var stmt
    def stmt(self, p):
        return ("var", p[1], p[3])

    @_('exp') # exp stmt
    def stmt(self, p):
        return ("exp", p[0])

    @_('IDENTIFIER') # one expression for now
    def exp(self, p): 
        return ("identifier", p[0]) 
    
    @_('NUMBER') # exp number
    def exp(self, p):
        return ("number", p[0])

    @_('STRING') # exp string
    def exp(self, p):
        return ("string", p[0])

    @_('TRUE') # exp true? why return 'true'?
    def exp(self, p):
        return ("true", "true")

    @_('FALSE') # exp false?
    def exp(self, p):
        return ("false", "false")

    @_('NOT exp') # exp not
    def exp(self, p):
        return ("not", p[1])
    
    @_('LPAREN exp RPAREN') # exp parens
    def exp(self, p):
        return p[1]

    # combining grammar rules
    @_('exp NOT exp',
        'exp DIVIDE exp',
        'exp TIMES exp',
        'exp MINUS exp',
        'exp PLUS exp',
        'exp GE exp',
        'exp LE exp',
        'exp GT exp',
        'exp LT exp',
        'exp EQUALEQUAL exp',
        'exp ANDAND exp',
        'exp OROR exp',
        )
    def exp(self, p):
        return ("binop", p[0], p[1], p[2])
    
    @_('IDENTIFIER LPAREN optargs RPAREN')
    def exp(self, p): # function expression call
        return ("call", p[0], p[2])

    @_('args')
    def optargs(self, p):
        return p[0]

    @_('empty')
    def optargs(self, p):
        return []

    @_('exp COMMA args')
    def args(self, p):
        return [p[0]] + p[2]

    @_('exp')
    def args(self, p):
        return [p[0]] # because params are always a list
        
    # @_('NAME')
    # def expr(self, p):
    #     try:
    #         return self.names[p.NAME]
    #     except LookupError:
    #         print(f'Undefined name {p.NAME!r}')
    #         return 0