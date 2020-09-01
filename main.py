from lexer import LCarnitineLexer
from parser import LCarnitineParser
from interpreter import LCarnitineInterpreter
import sys
import os.path

#Class LCarnitine:

def main():

    lexer = LCarnitineLexer()
    parser = LCarnitineParser()
    interpreter = LCarnitineInterpreter()

    # check input
    if len(sys.argv) < 2:
        print('usage: python main.py yourfile.lcarn')
        return

    source = sys.argv[1]
    extension = os.path.splitext(source)[1]
    if not extension == '.lcarn':
        print('Please enter a file with .lcarn extension')
        return

    if len(sys.argv) == 3:
        flag = sys.argv[2]
    # read all at once
    if source:
        with open(source, 'r') as s:
            source_file = s.read() # reads whole file into string
            source_file_ast = parser.parse(lexer.tokenize(source_file))
            interpreter.interpret(source_file_ast)
    return # for now  

    # add option to read line by line in interactive interpreter
    if source:
        with open(source, 'r') as s:
            line = s.readline()
            line_ast = parser.parse(lexer.tokenize(line))
            interpreter.interpret(line_ast)
            
            while line:
                line = s.readline()
                line_ast = parser.parse(lexer.tokenize(line))
                interpreter.interpret(line_ast)
                
if __name__ == '__main__':
    main()