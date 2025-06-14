from especificacao_tokens import especificacao_tokens

class Lexico:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.linhas = []
        self.caracteres = []
        self.linha_atual = 0
        self.caractere_atual = 0
        self.caracteres_por_linha = []
        self.reservadas = [
          'digue','integro','stringo','realo','incremente','decremente','receba','mais',
          'menos','multiplique','divida','maior_que',
          'menor_que','ingual','variegado','maior_ingual','menor_ingual',
          'e','ou','nem','ifo''elso','elso ifo','paro','duranto','calma','calabreso'
        ]
        self.carregar_arquivo()

    def carregar_arquivo(self):
        if not self.arquivo.endswith('.cal'):
            raise ValueError("O arquivo deve ter a extensão .cal")
        with open(self.arquivo, 'r') as file:
            self.linhas = file.readlines()
        self.caracteres = [list(linha.strip()) for linha in self.linhas]
        self.caracteres_por_linha = [len(linha) for linha in self.caracteres]
        self.linha_atual = 0
        self.caractere_atual = 0
    
    def __verifica_linha(self):
        if self.linha_atual >= len(self.linhas):
            return False
        if self.caractere_atual >= self.caracteres_por_linha[self.linha_atual]:
            return False
        return True
      
    # Capturar tokens de vários caracteres
    def __capturar_token(self,tipo, condicao, validacao=None):
        inicio = self.caractere_atual
        while self.__verifica_linha() and condicao(self.caracteres[self.linha_atual][self.caractere_atual]):
          if validacao and not validacao(self.caracteres[self.linha_atual][self.caractere_atual]):
            break
          self.caractere_atual += 1
        valor = ''.join(self.caracteres[self.linha_atual][inicio:self.caractere_atual])
        return Token(tipo, valor, self.linha_atual + 1, inicio + 1)
      
    # Retorna os tokens para um arquivo txt
    def write_tokens(self, arquivo_saida):
        with open(arquivo_saida, 'w') as file:
            token_count = 0
            while True:
                token = self.get_token()
                print(f"Token obtido: {token}")
                print(f"Posição atual: Linha {self.linha_atual}, Caractere {self.caractere_atual}")
                if token is None:
                    print("Token None encontrado - encerrando processamento")
                    break
                file.write(f"{token}\n")
                token_count += 1
            print(f"Total de tokens processados: {token_count}")
            
    def get_token(self):
      if self.linha_atual >= len(self.linhas):
        return None
        
      # Verifica se o caractere atual passa do limite da linha, se sim, avança para a próxima linha
      if self.caractere_atual >= self.caracteres_por_linha[self.linha_atual]:
        self.linha_atual += 1
        self.caractere_atual = 0
        if not self.__verifica_linha():
          return None
          
      # Obtém o caractere atual
      caractere_atual = self.caracteres[self.linha_atual][self.caractere_atual]
      
      # Verificar se é espaço ou tabulação
      if caractere_atual.isspace():
        self.caractere_atual += 1
        return self.get_token()
      
      # Processar comentários
      if caractere_atual == '/':
        # Comentário de linha
        if self.caractere_atual + 1 < self.caracteres_por_linha[self.linha_atual] and self.caracteres[self.linha_atual][self.caractere_atual+1] == '/':
          self.caractere_atual = self.caracteres_por_linha[self.linha_atual]
          return self.get_token()
        
        # Comentário de bloco
        if (self.caractere_atual + 1 < self.caracteres_por_linha[self.linha_atual] and 
          self.caracteres[self.linha_atual][self.caractere_atual+1] == '*'):
          self.caractere_atual += 2
          while self.__verifica_linha():
            if (self.caracteres[self.linha_atual][self.caractere_atual] == '*' and 
              self.caractere_atual + 1 < self.caracteres_por_linha[self.linha_atual] and 
              self.caracteres[self.linha_atual][self.caractere_atual+1] == '/'):
              self.caractere_atual += 2
              break
            self.caractere_atual += 1
            if self.caractere_atual >= self.caracteres_por_linha[self.linha_atual]:
              self.linha_atual += 1
              self.caractere_atual = 0
              if not self.__verifica_linha():
                break
          return self.get_token()
      
      # Identificador ou palavra reservada
      if caractere_atual.isalpha() or caractere_atual == '_':
        token = self.__capturar_token('id', lambda c: c.isalnum() or c == '_')
        if token.valor in self.reservadas:
          token.nome = token.valor
        return token
      
      # Número inteiro
      if caractere_atual.isdigit():
        return self.__capturar_token('integro', lambda c: c.isdigit())
      
      # String
      if caractere_atual == '"':
        inicio = self.caractere_atual
        self.caractere_atual += 1
        while self.__verifica_linha() and self.caracteres[self.linha_atual][self.caractere_atual] != '"':
          self.caractere_atual += 1
        valor = ''.join(self.caracteres[self.linha_atual][inicio+1:self.caractere_atual])
        if self.__verifica_linha():
          self.caractere_atual += 1
        return Token('stringo', valor, self.linha_atual + 1, inicio + 1)
      
      # Número real
      if caractere_atual.isdigit() or (caractere_atual == '.' and 
                      self.caractere_atual + 1 < self.caracteres_por_linha[self.linha_atual] and 
                      self.caracteres[self.linha_atual][self.caractere_atual + 1].isdigit()):
        inicio = self.caractere_atual
        while self.__verifica_linha() and self.caracteres[self.linha_atual][self.caractere_atual].isdigit():
          self.caractere_atual += 1
          if self.caractere_atual < self.caracteres_por_linha[self.linha_atual] and self.caracteres[self.linha_atual][self.caractere_atual] == '.':
            raise ValueError("Número real não pode possuir mais de um ponto.")
        valor = ''.join(self.caracteres[self.linha_atual][inicio:self.caractere_atual])
        return Token('realo', valor, self.linha_atual + 1, inicio + 1)
      
      # Operadores
      tipos_operadores = [
        ('op_logicos', especificacao_tokens['op_logicos']),
        ('op_aritmeticos_soma', especificacao_tokens['op_aritmeticos_soma']),
        ('op_aritmeticos_multiplicacao', especificacao_tokens['op_aritmeticos_multiplicacao']),
        ('op_relacionais', especificacao_tokens['op_relacionais'])
      ]
      
      for tipo, operadores in tipos_operadores:
        if caractere_atual in operadores:
          return self.__capturar_token(tipo, lambda c: c in operadores)
      
      # Delimitador
      if caractere_atual in especificacao_tokens:
        inicio = self.caractere_atual
        self.caractere_atual += 1
        return Token(especificacao_tokens[caractere_atual], caractere_atual, self.linha_atual + 1, inicio + 1)
      
      # Caractere não reconhecido
      self.caractere_atual += 1
      return Token('ERRO', caractere_atual, self.linha_atual + 1, self.caractere_atual)
     
class Token:
    def __init__(self, nome, valor, linha, coluna):
        self.nome = nome
        self.valor = valor
        self.linha = linha
        self.coluna = coluna
    
    def __repr__(self):
        return f"<Token {self.nome}, '{self.valor}'> (Linha: {self.linha}, Coluna: {self.coluna})"
      
# Exemplo de uso
if __name__ == "__main__":
    lexico = Lexico("teste.cal")
    lexico.write_tokens("tokens.txt")