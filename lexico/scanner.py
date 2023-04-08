import re
from linguagem import *
from token import Token

class Scanner():
    def __init__(self, path):
        self.codigo = self.__readFile(path)
        self.state = 0
        self.cadeiaToken = []
        self.isspace = lambda x: re.match(r'[ \t\n\r\f\v]', x)
        self.isoperator = lambda x: re.match(r'[=|>|<]', x)

    def __readFile(self, path):
        with open(path, 'r') as file:
            lines = file.read()
        lines_wo_comments = re.sub(r'{.*}', '', lines) # remove comentarios
        return lines_wo_comments
    
    def __token(self, word, tipo):
        token: str
        if word in LALG:
            token = LALG[word]
            return token, 200
        if word in PONTOS:
            token = PONTOS[word]
            return token, 200
        if word in OPERADORES:
            token = OPERADORES[word]
            return token, 200
        # Verifica se encaixa nas regras de identificador
        if re.fullmatch(r'[a-z+A-Z+]\w*', word):
            return 'ident', 200
        # verifica se encaixa nas regras de número inteiro
        if re.fullmatch(r'\d+', word):
            return 'num (int)', 200
        # Verifica se encaixa nas regras de número real
        if re.fullmatch(r'\d+.\d*', word):
            return 'num (real)', 200
        # Caso não se encaixe em nada, retorna erro
        return f'Erro, {tipo} não reconhecido.', 404
    
    def __defineToken(self, word, tipo):
        token, status = self.__token(word, tipo)
        self.cadeiaToken.append(Token(token, word, status))

    def getTokens(self, show = False):
        if show:
            for token in self.cadeiaToken:
                print(token.cadeia, '-', token.token, token.status)
        return self.cadeiaToken

    # Automato que ira percorrer o codigo caracter por caracter
    def readCode(self):
        word = ''
        c = 0
        while c < len(self.codigo):
            char = self.codigo[c]
            match self.state:
                case 0:
                    if char.isalpha():
                        self.state = 1
                        word += char
                    elif char.isnumeric():
                        self.state = 2
                        word += char
                    elif self.isoperator(char):
                        self.state = 4
                        word += char
                    elif self.isspace(char):
                        pass
                    elif not char.isalnum():
                        self.__defineToken(char, 'pontuação')
                case 1:
                    # caso 1: identificador
                    if re.match(r'[.|,|;|:|(|)|=|<|>|+|-|/|*]', char) or self.isspace(char):
                        self.__defineToken(word, 'identificador')
                        word = ''
                        self.state = 0
                        continue # para nao consumir o caractere
                    else:
                        word += char
                case 2:
                    # caso 2: inteiro
                    if char == '.':
                        word += char
                        self.state = 3
                    elif (not char.isalnum() and re.match(r'[.|,|;|:|(|)|=|<|>|+|-|/|*]', char)) or self.isspace(char):
                        self.__defineToken(word, 'número inteiro')
                        word = ''
                        self.state = 0
                        continue
                    else:
                        word += char
                case 3:
                    # caso 3: flutuante
                    if (not char.isalnum() and re.match(r'[.|,|;|:|(|)|=|<|>|+|-|/|*]', char)) or self.isspace(char):
                        self.__defineToken(word, 'número real')
                        word = ''
                        self.state = 0
                        continue
                    else:
                        word += char
                case 4:
                    #if (not re.match('[.|,|;|:|(|)|=|<|>]', char)) or self.isspace(char):
                    if char.isalnum() or self.isspace(char):
                        self.__defineToken(word, 'operador')
                        word = ''
                        self.state = 0
                        continue
                    else:
                        word += char
            c += 1


if __name__ == '__main__':
    scanner = Scanner('teste.lalg')
    scanner.readCode()
    tokens = scanner.getTokens(True)