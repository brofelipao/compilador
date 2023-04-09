from lexico.scanner import Scanner
from sintatico.gramatica import gramatica

if __name__ == '__main__':
    scanner = Scanner('testes/teste1.lalg')
    scanner.readCode()
    tokens = scanner.getTokens()


    print(gramatica)