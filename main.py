from lexico.scanner import Scanner
from sintatico.parser import Parser
from lexico.linguagem import *


if __name__ == '__main__':
    scanner = Scanner('testes/teste1.lalg')
    scanner.readCode()
    tokens = scanner.getTokens(show=0)

    parser = Parser(tokens)