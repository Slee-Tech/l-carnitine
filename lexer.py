from sly import Lexer, Parser

class LCarnitineLexer(Lexer):
    tokens = { ANDAND, COMMA, DIVIDE, ELSE, EQUAL, EQUALEQUAL, FALSE, FUNCTION, GE, GT, IDENTIFIER, IF, LBRACE, LE, LPAREN, LT, MINUS, NOT, NUMBER, OROR, PLUS, RBRACE, RETURN, RPAREN, SEMICOLON, STRING, TIMES, TRUE, VAR }

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    EQUAL = r'Is assigned the following value of:'
    EQUALEQUAL = r'Is equal to the value of:'
    FALSE = r'False, untrue, or incorrect'
    FUNCTION = r'Perform the procedure:'
    GE = r'Is greater than or equal to:'
    GT = r'Is greater than:'
    IF = r'If is is the case that:'
    LPAREN = r'<\(' # <(
    RPAREN = r'>\)' # >)
    ELSE = r'If the preceeding statement was not true, then perhaps:'
    LBRACE = r'<@' # <^^ braces have 2 pipes
    LE = r'Is less than or equal to:'
    RBRACE = r'>@' # >^^
    LT = r'Is less than:'
    NOT = r'The negation of:'
    ANDAND = r'And it is also the case that:'
    OROR = r'Or it is the case that:'
    RETURN = r'Return the value of:'
    TRUE = r'True, accurate, or correct:'
    VAR = r'The following variable:'
    IDENTIFIER = r'[a-zA-Z][a-zA-Z_]*'
    SEMICOLON = r'%%' # -|
    COMMA = r'::'
   
    # Ignored pattern
    ignore_newline = r'\n+'

    ignore_whitespace = ' \t\r' # whitespace, removed space character 

    @_(r'-?[0-9]+\.?[0-9]*')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    @_(r'```(?:[^`\\]|(\\.))*```') # can use any char except backtick `
    def STRING(self, t):
        t.value = t.value[3:-3]
        return t
    
    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        #print("Illegal character '%s'" % t.value[0])
        self.index += 1