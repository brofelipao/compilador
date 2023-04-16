from lexico.scanner import Scanner
from sintatico.parser import Parser
from lexico.linguagem import *
import os

if __name__ == '__main__':
    os.system('cls')
    scanner = Scanner('testes/teste1.lalg')
    scanner.readCode()
    tokens = scanner.getTokens(show=0)

    parser = Parser(tokens)