RED = "\033[1;31m"
RESET = "\033[0;0m"

class Parser:
    def __init__(self, tokens):
        self.estado = 0
        self.tokens = tokens
        self.program()

    def program(self):
        # Verificacao palavra reservada program
        if self.tokens[self.estado].token != 'program':
            self.error()
        self.consume()
        # Verificacao identificador
        self.isident()
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
        if self.tokens[self.estado].token == 'ident':
            self.consume()
            self.mais_var()
        else:
            self.error()
            self.consume()

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
            if self.tokens[self.estado] == 'ident':
                self.consume()
                self.parametros()
                if self.tokens[self.estado] == ';':
                    self.consume()
                    self.corpo_p()
                    self.dc_p()
                else:
                    self.error()
                    self.consume()
            else:
                self.error()
                self.consume()
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
        if self.tokens[self.estado].token != 'ident':
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
        pass

    def comandos(self):
        pass

    def cmd(self):
        pass

    def condicao(self):
        pass

    def relacao(self):
        pass

    def expressao(self):
        pass

    def op_un(self):
        pass

    def outros_termos(self):
        pass

    def op_ad(self):
        pass

    def termo(self):
        pass

    def mais_fatores(self):
        pass

    def op_mul(self):
        pass

    def fator(self):
        pass

    def isident(self):
        self.consume()

    def error(self, msg = 'Erro'):
        if msg == 'Erro':
            msg = msg + self.tokens[self.estado].token
        print(RED + msg + RESET)
    
    def consume(self):
        print(self.tokens[self.estado].token)
        self.estado += 1

