from AnalisadorLexico.Token import Token

class AnalisadorLexico:
    def __init__(self, arquivo):
        self.arquivo = arquivo  
        self.linhas = []
        self.caracteres = []
        self.linha_atual = 0
        self.caractere_atual = 0
        self.caracteres_por_linha = []
        self.reservadas = {
            'digue': 'DIGUE',
            'integro': 'INTEGRO_TIPO',
            'stringo': 'STRINGO_TIPO',
            'realo': 'REALO_TIPO',
            'incremente': 'INCREMENTE',
            'decremente': 'DECREMENTE',
            'receba': 'RECEBA',
            'mais': 'OP_MAIS',
            'menos': 'OP_MENOS',
            'multiplique': 'OP_MULTIPLIQUE',
            'divida': 'OP_DIVIDA',
            'maior_que': 'OP_MAIOR_QUE',
            'menor_que': 'OP_MENOR_QUE',
            'maior_ingual': 'OP_MAIOR_INGUAL',
            'menor_ingual': 'OP_MENOR_INGUAL',
            'ingual': 'OP_INGUAL',
            'variegado': 'OP_VARIEGADO',
            'e': 'OP_E',
            'ou': 'OP_OU',
            'nem': 'OP_NEM',
            'ifo': 'IFO',
            'elso_ifo': 'ELSO_IFO',
            'elso': 'ELSO',
            'paro': 'PARO',
            'duranto': 'DURANTO',
            'calma': 'CALMA',
            'calabreso': 'CALABRESO'
        }
        self.delimitadores = {
            '(': 'LPAREN',
            ')': 'RPAREN',
            '{': 'LBRACE',
            '}': 'RBRACE',
            ';': 'SEMICOLON',
            ',': 'COMMA'
        }
        if not self.arquivo.endswith('.cal'):
            raise ValueError("O arquivo deve ter a extensão .cal")
        with open(self.arquivo, 'r', encoding='utf-8') as file:
            self.linhas = file.readlines()
        self.caracteres = [list(linha.rstrip('\n')) for linha in self.linhas]
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
    def __capturar_token(self, tipo, condicao, validacao=None):
        inicio = self.caractere_atual
        while self.__verifica_linha() and condicao(self.caracteres[self.linha_atual][self.caractere_atual]):
            if validacao and not validacao(self.caracteres[self.linha_atual][self.caractere_atual]):
                break
            self.caractere_atual += 1
        valor = ''.join(self.caracteres[self.linha_atual][inicio:self.caractere_atual])
        return Token(tipo, valor, self.linha_atual + 1, inicio + 1)
      
    # Retorna os tokens para um arquivo txt
    def write_tokens(self, arquivo_saida):
        arquivo_saida = arquivo_saida if arquivo_saida.endswith('.txt') else arquivo_saida + '.txt'
        # O arquivo de saida deve ficar no diretorio tokens
        if not arquivo_saida.startswith('tokens/'):
            arquivo_saida = 'tokens/' + arquivo_saida
        with open(arquivo_saida, 'w', encoding='utf-8') as file:
            token_count = 0
            while True:
                token = self.get_token()
                if token is None:
                    break
                file.write(f"{token}\n")
                token_count += 1
            print(f"Total de tokens processados: {token_count}")
            
    def get_token(self):
        if self.linha_atual >= len(self.linhas):
            return None
        
        # Verifica se o caractere atual passa do limite da linha, se sim, avança para a próxima linha
        while self.caractere_atual >= self.caracteres_por_linha[self.linha_atual]:
            self.linha_atual += 1
            self.caractere_atual = 0
            # Se chegamos ao fim do arquivo após avançar linha, retorna None
            if self.linha_atual >= len(self.linhas):
                return None
          
        # Obtém o caractere atual
        caractere_atual = self.caracteres[self.linha_atual][self.caractere_atual]
        
        # Verificar se é espaço ou tabulação
        if caractere_atual in [' ', '\t']:
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
                # Avança para depois do "/*"
                self.caractere_atual += 2
                
                # Flag para indicar se encontrou o fim do comentário
                comentario_finalizado = False
                
                # Loop até encontrar "*/" ou atingir o fim do arquivo
                while not comentario_finalizado and self.linha_atual < len(self.linhas):
                    # Se chegou ao fim da linha atual
                    if self.caractere_atual >= self.caracteres_por_linha[self.linha_atual]:
                        self.linha_atual += 1
                        self.caractere_atual = 0
                        # Se chegou ao fim do arquivo
                        if self.linha_atual >= len(self.linhas):
                            break
                        continue
                    
                    # Verifica se encontrou o fim do comentário "*/"
                    if (self.caractere_atual + 1 < self.caracteres_por_linha[self.linha_atual] and
                        self.caracteres[self.linha_atual][self.caractere_atual] == '*' and
                        self.caracteres[self.linha_atual][self.caractere_atual + 1] == '/'):
                        self.caractere_atual += 2  # Pula o "*/"
                        comentario_finalizado = True
                        break
                        
                    # Avança para o próximo caractere
                    self.caractere_atual += 1
                
                # Depois de processar o comentário, continua a análise
                return self.get_token()
        
        # Identificador ou palavra reservada
        if caractere_atual.isalpha() or caractere_atual == '_':
            token = self.__capturar_token('ID', lambda c: c.isalnum() or c == '_')
            # Verifica se é palavra reservada
            if token.valor in self.reservadas:
                token.nome = self.reservadas[token.valor]
            return token
        
        # Número (inteiro ou real)
        if caractere_atual.isdigit():
            inicio = self.caractere_atual
            tem_ponto = False
            
            # Captura dígitos
            while self.__verifica_linha() and self.caracteres[self.linha_atual][self.caractere_atual].isdigit():
                self.caractere_atual += 1
            
            # Verifica se tem ponto decimal
            if (self.__verifica_linha() and 
                self.caractere_atual < self.caracteres_por_linha[self.linha_atual] and 
                self.caracteres[self.linha_atual][self.caractere_atual] == '.'):
                
                # Verifica se há dígito após o ponto
                if (self.caractere_atual + 1 < self.caracteres_por_linha[self.linha_atual] and 
                    self.caracteres[self.linha_atual][self.caractere_atual + 1].isdigit()):
                    tem_ponto = True
                    self.caractere_atual += 1  # Pula o ponto
                    
                    # Captura dígitos após o ponto
                    while self.__verifica_linha() and self.caracteres[self.linha_atual][self.caractere_atual].isdigit():
                        self.caractere_atual += 1
            
            valor = ''.join(self.caracteres[self.linha_atual][inicio:self.caractere_atual])
            tipo = 'REALO' if tem_ponto else 'INTEGRO'
            return Token(tipo, valor, self.linha_atual + 1, inicio + 1)
        
        # String
        if caractere_atual == '"':
            inicio = self.caractere_atual
            self.caractere_atual += 1
            while self.__verifica_linha() and self.caracteres[self.linha_atual][self.caractere_atual] != '"':
                self.caractere_atual += 1
            valor = ''.join(self.caracteres[self.linha_atual][inicio+1:self.caractere_atual])
            if self.__verifica_linha():
                self.caractere_atual += 1
            return Token('STRINGO', valor, self.linha_atual + 1, inicio + 1)
        
        # Delimitadores
        if caractere_atual in self.delimitadores:
            inicio = self.caractere_atual
            self.caractere_atual += 1
            return Token(self.delimitadores[caractere_atual], caractere_atual, self.linha_atual + 1, inicio + 1)

        # Caractere não reconhecido
        inicio = self.caractere_atual
        self.caractere_atual += 1
        return Token('ERRO', caractere_atual, self.linha_atual + 1, inicio + 1)