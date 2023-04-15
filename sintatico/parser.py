from lexico.linguagem import *

RED = "\033[1;31m"
RESET = "\033[0;0m"

class Parser:
    def __init__(self, tokens):
        self.estado = 0
        self.tokens = tokens
        lalg = list(LALG.values())
        pontos = list(PONTOS.values())
        op = list(OPERADORES.values())
        self.palavras_reservadas = lalg + pontos + op
        self.program()

    def program(self):
        # Verificacao palavra reservada program
        if self.tokens[self.estado].token != 'program':
            self.error()
        self.consume()
        if not self.isident():
            self.error()
        self.consume()
        if self.tokens[self.estado].token != ';':
            self.error()
        self.consume()
        self.corpo()
        if self.tokens[self.estado].token != '.':
            self.error()
        # Aqui nao muda estado pois o programa acaba
        
    def corpo(self):
        self.dc()
        if self.tokens[self.estado].token != 'begin':
            self.error()
        self.consume()
        self.comandos()
        if self.tokens[self.estado].token != 'end':
            self.error()
        self.consume()

    def dc(self):
        self.dc_v()
        self.dc_p()

    def dc_v(self):
        if self.tokens[self.estado].token == 'var':
            self.consume()
            self.variaveis()
            if self.tokens[self.estado].token != ':':
                self.error()
            self.consume()
            self.tipo_var()
            if self.tokens[self.estado].token != ';':
                self.error()
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
            self.error()
            self.consume()

    def variaveis(self):
        if not self.isident():
            self.error()
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
            if not self.isident():
                self.error()
            self.consume()
            self.parametros()
            if self.tokens[self.estado].token != ';':
                self.error()
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
            if self.tokens[self.estado].token == ')':
                self.consume()
            else:
                self.error()
                self.consume()
        # Vazio
        else:
            pass

    def lista_par(self):
        self.variaveis()
        if self.tokens[self.estado].token == ':':
            self.consume()
            self.tipo_var()
            self.mais_var()
        else:
            self.error()
            self.consume()

    def mais_par(self):
        if self.tokens[self.estado].token == ';':
            self.consume()
            self.lista_par()
        # Vazio
        else:
            pass

    def corpo_p(self):
        self.dc_loc()
        if self.tokens[self.estado].token != 'begin':
            self.error()
        self.consume()
        self.comandos()
        if self.tokens[self.estado].token != 'end':
            self.error()
        self.consume()
        if self.tokens[self.estado].token != ';':
            self.error()
        self.consume()

    def dc_loc(self):
        self.dc_v()

    def lista_arg(self):
        if self.tokens[self.estado].token == '(':
            self.consume()
            self.argumentos()
            if self.tokens[self.estado].token != ')':
                self.error()
            self.consume()
        # Vazio
        else:
            pass

    def argumentos(self):
        if not self.isident():
            self.error()
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
        self.cmd()
        if self.tokens[self.estado].token != ';':
            self.error()
        self.consume()
        self.comandos()

    def cmd(self):
        if self.tokens[self.estado].token == 'read':
            self.consume()
            if self.tokens[self.estado].token != '(':
                self.error()
            self.consume()
            self.variaveis()
            if self.tokens[self.estado].token != ')':
                self.error()
            self.consume()
        elif self.tokens[self.estado].token == 'write':
            self.consume()
            if self.tokens[self.estado].token != '(':
                self.error()
            self.consume()
            self.variaveis()
            if self.tokens[self.estado].token != ')':
                self.error()
            self.consume()
        elif self.tokens[self.estado].token == 'while':
            self.consume()
            self.condicao()
            if self.tokens[self.estado].token != 'do':
                self.error()
            self.consume()
            self.cmd()
        elif self.tokens[self.estado].token == 'if':
            self.consume()
            self.condicao()
            if self.tokens[self.estado].token != 'then':
                self.error()
            self.consume()
            self.cmd()
            self.pfalsa()
        elif self.tokens[self.estado].token == 'begin':
            self.consume()
            self.comandos()
            if self.tokens[self.estado].token != 'end':
                self.error()
            self.consume()
        elif self.isident():
            self.consume()
            if self.tokens[self.estado].token == ':':
                self.consume()
                if self.tokens[self.estado].token != '=':
                    self.error()
                self.consume()
                self.expressao()
            else:
                self.lista_arg()
        else:
            self.error()
            self.consume()

    def condicao(self):
        self.expressao()
        self.relacao()
        self.expressao()

    def relacao(self):
        if self.tokens[self.estado].token not in ('=', '<>', '>=', '<=', '>', '<'):
            self.error()
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
            self.error()
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
            self.error()
        self.consume()

    def fator(self):
        if self.isident():
            self.consume()
        elif self.numero_int():
            self.consume()
        elif self.numero_real:
            self.consume()
        else:
            self.error()
            self.consume()

    def numero_int(self):
        return True

    def numero_real(self):
        return True

    def isident(self):
        if self.tokens[self.estado].cadeia not in self.palavras_reservadas:
            return True
        return False

    def error(self, msg = 'Erro'):
        if msg == 'Erro':
            msg = msg + ': ' + self.tokens[self.estado].token
        print(RED + msg + RESET)
    
    def consume(self):
        print(self.tokens[self.estado].token)
        self.estado += 1

