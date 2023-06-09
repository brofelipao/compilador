from lexico.linguagem import *
import re

RED = "\033[1;31m"
RESET = "\033[0;0m"
REDN = '\033[31m'
GREEN = "\033[1;32m"

lalg = list(LALG.values())
pontos = list(PONTOS.values())
op = list(OPERADORES.values())

class Parser:
    def __init__(self, tokens):
        self.estado = 0
        self.tokens = tokens
        self.linhas = ['' for i in range(len(tokens))]
        self.erros = []
        self.variaveislist = []
        self.palavras_reservadas = lalg + pontos + op
        self.program()
    
    def match(self, word):
        if self.tokens[self.estado].token != word:
            self.error(word)

    def program(self):
        # Verificacao palavra reservada program
        self.match('program')
        self.consume()
        if not self.isident(nova_variavel=True):
            self.error('var')
        self.consume()
        self.match(';')
        self.consume()
        self.corpo()
        if self.tokens[self.estado].token != '.':
            self.error('.')
        else:
            self.consume()
        if self.estado < len(self.tokens):
            print(RED + 'Processo finalizado pois as regras não foram capazes de reconhecer a cadeia.' + RESET)
            while self.estado < len(self.tokens):
                self.tokens[self.estado].erro = True
                self.consume()
        # Aqui nao muda estado pois o programa acaba
        self.resultado()
 
    def corpo(self):
        self.dc()
        self.match('begin')
        self.consume()
        self.comandos()
        self.match('end')
        self.consume()

    def dc(self):
        self.dc_v()
        self.dc_p()

    def dc_v(self):
        if self.tokens[self.estado].token == 'var':
            self.consume()
            self.variaveis()
            self.match(':')
            self.consume()
            self.tipo_var()
            self.match(';')
            self.consume()
            self.dc_v()
        # Vazio
        else:
            pass

    def tipo_var(self):
        if self.tokens[self.estado].token == 'real':
            self.consume()
        elif self.tokens[self.estado].token == 'integer':
            self.consume()
        else:
            self.error('real ou integer')
            self.consume()

    def variaveis(self):
        if not self.isident(nova_variavel=True):
            self.error('var')
        self.consume()
        self.mais_var()

    def mais_var(self):
        if self.tokens[self.estado].token == ',':
            self.consume()
            self.variaveis()
        # Vazio    
        else:
            pass

    def dc_p(self):
        if self.tokens[self.estado].token == 'procedure':
            self.consume()
            if not self.isident(nova_variavel=True):
                self.error('var')
            self.consume()
            self.parametros()
            self.match(';')
            self.consume()
            self.corpo_p()
            self.dc_p()
        # Vazio
        else:
            pass

    def parametros(self):
        if self.tokens[self.estado].token == '(':
            self.consume()
            self.lista_par()
            self.match(')')
            self.consume()
        # Vazio
        else:
            pass

    def lista_par(self):
        if self.tokens[self.estado].token == 'ident':
            self.variaveis()
            self.match(':')
            self.consume()
            self.tipo_var()
            self.mais_var()
        else:
            pass

    def mais_par(self):
        if self.tokens[self.estado].token == ';':
            self.consume()
            self.lista_par()
        # Vazio
        else:
            pass

    def corpo_p(self):
        self.dc_loc()
        self.match('begin')
        self.consume()
        self.comandos()
        self.match('end')
        self.consume()
        self.match(';')
        self.consume()

    def dc_loc(self):
        self.dc_v()

    def lista_arg(self):
        if self.tokens[self.estado].token == '(':
            self.consume()
            self.argumentos()
            self.match(')')
            self.consume()
        # Vazio
        else:
            pass

    def argumentos(self):
        if not self.isident():
            self.error('var')
        self.consume()
        self.mais_ident()

    def mais_ident(self):
        if self.tokens[self.estado].token == ';':
            self.consume()
            self.argumentos()
        # Vazio
        else:
            pass

    def pfalsa(self):
        if self.tokens[self.estado].token == 'else':
            self.consume()
            self.cmd()
        else:
            pass

    def comandos(self):
        if self.tokens[self.estado].token in ('read', 'write', 'while', 'if', 'ident', 'begin'):
            self.cmd()
            self.match(';')
            self.consume()
            self.comandos()
        else:
            pass

    def cmd(self):
        if self.tokens[self.estado].token == 'read':
            self.consume()
            self.match('(')
            self.consume()
            self.variaveis()
            self.match(')')
            self.consume()
        elif self.tokens[self.estado].token == 'write':
            self.consume()
            self.match('(')
            self.consume()
            self.variaveis()
            self.match(')')
            self.consume()
        elif self.tokens[self.estado].token == 'while':
            self.consume()
            self.condicao()
            self.match('do')
            self.consume()
            self.cmd()
        elif self.tokens[self.estado].token == 'if':
            self.consume()
            self.condicao()
            self.match('then')
            self.consume()
            self.cmd()
            self.pfalsa()
        elif self.isident():
            self.consume()
            if self.tokens[self.estado].token == ':':
                self.consume()
                self.match('=')
                self.consume()
                self.expressao()
            else:
                self.lista_arg()
        elif self.tokens[self.estado].token == 'begin':
            self.consume()
            self.comandos()
            self.match('end')
            self.consume()
        else:
            self.error('read, write, while, if, ident ou begin')
            self.consume()

    def condicao(self):
        self.expressao()
        self.relacao()
        self.expressao()

    def relacao(self):
        if self.tokens[self.estado].token not in ('=', '<>', '>=', '<=', '>', '<'):
            self.error('operador de comparação')
        self.consume()

    def expressao(self):
        self.termo()
        self.outros_termos()

    def op_un(self):
        if self.tokens[self.estado].token in ('+', '-'):
            self.consume()
        else:
            pass

    def outros_termos(self):
        if self.tokens[self.estado].token in ('+', '-'):
            self.op_ad()
            self.termo()
            self.outros_termos()
        else:
            pass

    def op_ad(self):
        if self.tokens[self.estado].token not in ('+', '-'):
            self.error('operador matemático')
        self.consume()

    def termo(self):
        self.op_un()
        self.fator()
        self.mais_fatores()

    def mais_fatores(self):
        if self.tokens[self.estado].token in ('*', '/'):
            self.op_mul()
            self.fator()
            self.mais_fatores()
        else:
            pass

    def op_mul(self):
        if self.tokens[self.estado].token not in ('*', '/'):
            self.error('operador matemático')
        self.consume()

    def fator(self):
        if self.isident():
            self.consume()
        elif self.numero_int():
            self.consume()
        elif self.numero_real():
            self.consume()
        elif self.tokens[self.estado].token == '(':
            self.consume()
            self.expressao()
            self.match(')')
            self.consume()
        else:
            self.error('var')
            self.consume()

    def numero_int(self):
        if re.fullmatch(r'\d+', self.tokens[self.estado].cadeia):
            return True
        return False

    def numero_real(self):
        if re.fullmatch(r'\d+.\d*', self.tokens[self.estado].cadeia):
            return True
        return False

    def isident(self, nova_variavel = False):
        #print(self.tokens[self.estado].cadeia, self.tokens[self.estado].erro, self.tokens[self.estado].token)
        token = self.tokens[self.estado]
        r = False
        if token.erro:
            return r
        if token.cadeia not in self.palavras_reservadas and token.token == 'ident':
            r = True
        if nova_variavel:
            self.variaveislist.append(token.cadeia)
        elif token.cadeia not in self.variaveislist:
            r = False
        return r

    def error(self, msg = None):
        if msg == None:
            msg = f'Erro: {self.tokens[self.estado].cadeia} na linha {self.tokens[self.estado].linha}'
        elif msg == 'out':
            msg = f'Erro: o {self.tokens[self.estado].cadeia} está fora do escopo da função main.'
        elif msg == 'var':
            msg = f'Identificador {self.tokens[self.estado].cadeia} inválido ou inexistente.'
        else:
            msg = f'Erro: Esperava {msg} recebeu {self.tokens[self.estado].cadeia} na linha {self.tokens[self.estado].linha}'
        
        self.erros.append(RED + msg + RESET)
        self.tokens[self.estado].erro = True
    
    def consume(self):
        token = self.tokens[self.estado]
        msg = token.cadeia
        if token.erro:
            msg = REDN + msg + RESET
        if len(self.linhas[token.linha]) > 0:
            msg = ' ' + msg
        self.linhas[token.linha] += msg
        #print(msg)
        self.estado += 1

    def resultado(self):
        cod = '\n'.join(list(filter(len, self.linhas))).strip()
        print(cod)
        if len(self.erros) == 0:
            print(GREEN + 'Não foram encontrados erros.' + RESET)    
        erros = '\n'.join(self.erros).strip()
        print(erros)

