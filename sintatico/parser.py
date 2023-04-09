
class Parser:
    def __init__(self, tokens):
        self.estado = 0
        self.tokens = tokens
        self.program()

    def program(self):
        # Verificacao palavra reservada program
        if self.tokens[self.estado].token != 'program':
            self.erro('Program esperado')
        self.changeState()
        # Verificacao identificador
        self.isident()
        if self.tokens[self.estado].token != ';':
            self.erro('ponto e virgula')
        self.changeState()
        self.corpo()
        if self.tokens[self.estado].token != '.':
            self.erro('Cade o ponto')
        # Aqui nao muda estado pois o programa acaba
        

    def corpo(self):
        self.dc()
        if self.tokens[self.estado].token != 'begin':
            self.erro('Begin esperado')
        self.changeState()
        self.comandos()
        if self.tokens[self.estado].token != 'end':
            self.erro('End esperado')
        self.changeState()

    def dc(self):
        self.dc_v()
        self.dc_p()

    def dc_v(self):
        if self.tokens[self.estado] == 'var':
            self.changeState()
            self.variaveis()
            if self.tokens[self.estado] != ':':
                self.erro()
            self.changeState()
            self.tipo_var()
            if self.tokens[self.estado] != ';':
                self.erro()
            self.changeState()
            self.dc_v()
        else:
            pass

    def tipo_var(self):
        pass

    def variaveis(self):
        pass

    def mais_var(self):
        pass

    def dc_p(self):
        pass

    def parametros(self):
        pass

    def lista_par(self):
        pass

    def mais_par(self):
        pass

    def corpo_p(self):
        pass

    def dc_loc(self):
        pass

    def lista_arg(self):
        pass

    def argumentos(self):
        pass

    def mais_ident(self):
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
        self.changeState()

    def erro(self, msg = 'Erro'):
        print(msg)
    
    def changeState(self):
        print(self.tokens[self.estado].token)
        self.estado += 1

