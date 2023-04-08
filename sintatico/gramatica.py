class Gramatica():
    def __init__(self):
        self.gramatica = {
            'programa': ['program', 'ident', ';', 'corpo', '.'],
            'corpo': ['dc', 'begin', 'comandos', 'end'] 
        }