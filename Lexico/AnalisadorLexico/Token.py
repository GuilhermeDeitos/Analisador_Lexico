class Token:
    def __init__(self, nome, valor, linha, coluna):
        self.nome = nome
        self.valor = valor
        self.linha = linha
        self.coluna = coluna
    
    def __repr__(self):
        return f"<Token {self.nome}, '{self.valor}'> (Linha: {self.linha}, Coluna: {self.coluna})"
      