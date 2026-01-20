class Gramatica:
    def __init__(self):
        self.producoes = {}
        self.nao_terminais = set()
        self.terminais = set()
        self.simbolo_inicial = None
        self.epsilon = 'ε'

    def adicionar_producao(self, nao_terminal, producao):
        if nao_terminal not in self.producoes:
            self.producoes[nao_terminal] = []
        self.producoes[nao_terminal].append(producao)
        self.nao_terminais.add(nao_terminal)

    def definir_simbolo_inicial(self, simbolo):
        self.simbolo_inicial = simbolo

    def atualizar_terminais(self):
        todos_simbolos = set()
        for prods in self.producoes.values():
            for prod in prods:
                todos_simbolos.update(prod)
        self.terminais = {s for s in todos_simbolos if s not in self.nao_terminais and s != self.epsilon}