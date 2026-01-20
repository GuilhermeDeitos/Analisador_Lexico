class AnalisadorLL1:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.first = {}   
        self.follow = {}  
        self.tabela = {}  
    
    def calcular_first(self):
        """Calcula o conjunto FIRST para todos os símbolos da gramática."""
        
        self.first[self.gramatica.epsilon] = {self.gramatica.epsilon}      
        for nt in self.gramatica.nao_terminais:
            self.first[nt] = set()
        
        alterou = True
        while alterou:
            alterou = False
            
            for nt in self.gramatica.nao_terminais:
                tamanho_antes = len(self.first[nt])
                
                for producao in self.gramatica.producoes[nt]:
                    self._calcular_first_sequencia(nt, producao)
                
                if len(self.first[nt]) > tamanho_antes:
                    alterou = True
    
    def _calcular_first_sequencia(self, nt, sequencia):
        """
        Calcula o FIRST de uma sequência e adiciona ao FIRST do não-terminal.
        """
        if not sequencia: 
            self.first[nt].add(self.gramatica.epsilon)
            return
        
        primeiro_simbolo = sequencia[0]
        
        if primeiro_simbolo in self.gramatica.terminais or primeiro_simbolo == self.gramatica.epsilon:
            self.first[nt].add(primeiro_simbolo)
            return
        
        for simbolo in self.first[primeiro_simbolo]:
            if simbolo != self.gramatica.epsilon:
                self.first[nt].add(simbolo)
        
        i = 0
        while i < len(sequencia) and self.gramatica.epsilon in self.first[sequencia[i]]:
            i += 1
            if i < len(sequencia):
                for simbolo in self.first[sequencia[i]]:
                    if simbolo != self.gramatica.epsilon:
                        self.first[nt].add(simbolo)
            else:
                self.first[nt].add(self.gramatica.epsilon)
    
    def calcular_follow(self):
      """Calcula o conjunto FOLLOW para todos os não-terminais."""
      for nt in self.gramatica.nao_terminais:
          self.follow[nt] = set()
      self.follow[self.gramatica.simbolo_inicial].add('$')
      alterou = True
      while alterou:
          alterou = False
          for A in self.gramatica.nao_terminais:
              for producao in self.gramatica.producoes[A]:
                  for i, X in enumerate(producao):
                      if X not in self.gramatica.nao_terminais:
                          continue
                      beta = producao[i+1:]
                      tamanho_antes = len(self.follow[X])
                      first_beta = self._calcular_first_lista(beta,'follow')
                      for s in first_beta:
                          if s != self.gramatica.epsilon:
                              self.follow[X].add(s)
                      if not beta or self._pode_derivar_epsilon(beta):
                          for s in self.follow[A]:
                              self.follow[X].add(s)
                      if len(self.follow[X]) > tamanho_antes:
                          alterou = True
    
    def _calcular_first_lista(self, simbolos, local=None):
      """Calcula o FIRST de uma lista de símbolos."""
      if not simbolos:
          return {self.gramatica.epsilon}
      
      resultado = set()
      for simbolo in simbolos:
          if simbolo in self.gramatica.terminais or simbolo == '$':
              resultado.add(simbolo)
              break
          elif simbolo in self.gramatica.nao_terminais:
              for primeiro in self.first[simbolo]:
                  if primeiro != self.gramatica.epsilon:
                      resultado.add(primeiro)
              if self.gramatica.epsilon not in self.first[simbolo]:
                  break
          elif simbolo == self.gramatica.epsilon:
              resultado.add(self.gramatica.epsilon)
              break
      else:
          resultado.add(self.gramatica.epsilon)

      return resultado
            
    def _pode_derivar_epsilon(self, simbolos):
        """Verifica se uma sequência de símbolos pode derivar epsilon."""
        for simbolo in simbolos:
            if simbolo in self.gramatica.terminais or simbolo == '$':
                return False
            if self.gramatica.epsilon not in self.first[simbolo]:
                return False
        return True
    
    def construir_tabela_analise(self):
        """Constrói a tabela de análise sintática LL(1)."""
        for nt in self.gramatica.nao_terminais:
            self.tabela[nt] = {}
            for terminal in self.gramatica.terminais.union({'$'}):
                self.tabela[nt][terminal] = None
        
        for nt in self.gramatica.nao_terminais:
            for i, producao in enumerate(self.gramatica.producoes[nt]):
                first_producao = self._calcular_first_lista(producao,'tabela')
                
                for terminal in first_producao:
                    if terminal != self.gramatica.epsilon:
                        if self.tabela[nt][terminal] is not None:
                            raise Exception(f"Conflito na tabela: [{nt},{terminal}] já possui produção {self.tabela[nt][terminal]}")
                        self.tabela[nt][terminal] = (nt, i)  
                
                if self.gramatica.epsilon in first_producao:
                    for terminal in self.follow[nt]:
                        if self.tabela[nt][terminal] is not None:
                            raise Exception(f"Conflito na tabela: [{nt},{terminal}] já possui produção {self.tabela[nt][terminal]}")
                        self.tabela[nt][terminal] = (nt, i) 
        
        self._adicionar_acoes_sincronizacao()
    
    def _adicionar_acoes_sincronizacao(self):
        """Adiciona ações de sincronização para recuperação de erros."""
        for nt in self.gramatica.nao_terminais:
            for terminal in self.follow[nt]:
                if self.tabela[nt][terminal] is None:
                    self.tabela[nt][terminal] = ('sinc', None)
    
    def analisar_tokens(self, token_reader):
        """
        Analisa uma sequência de tokens usando o leitor de tokens.
        token_reader: instância de TokenReader
        Retorna: dicionário com resultados da análise
        """
        pilha = ['$', self.gramatica.simbolo_inicial]
        
        log = []
        erros = []
        
        while pilha[-1] != '$':
            X = pilha[-1]  
            token = token_reader.proximo_token()
            
            if token is None:
                a = '$' 
            else:
                a = token.nome  
            
            log.append({
                'pilha': pilha.copy(),
                'token_atual': f"{a} ('{token.valor}')" if token else "$",
                'linha': token.linha if token else "EOF",
                'coluna': token.coluna if token else "EOF",
                'acao': ''
            })
            
            if X in self.gramatica.terminais:
                if X == a:
                    pilha.pop()
                    token_reader.consumir()
                    log[-1]['acao'] = f"Match: {X}"
                else:
                    if token is not None:
                        erro_msg = f"Erro na linha {token.linha}, coluna {token.coluna}: esperado '{X}', encontrado '{a}'"
                    else:
                        erro_msg = f"Erro no fim da entrada: esperado '{X}', encontrado fim de arquivo"
                    erros.append(erro_msg)
                    log[-1]['acao'] = erro_msg
                    pilha.pop()
            else: 
                if a in self.tabela.get(X, {}) and self.tabela[X][a] is not None:
                    producao = self.tabela[X][a]
                    if producao[0] == 'sinc':
                        if token is not None:
                            erro_msg = f"Erro de sintaxe na linha {token.linha}, coluna {token.coluna}: token inesperado '{a}', sincronizando"
                        else:
                            erro_msg = f"Erro de sintaxe no fim da entrada: token inesperado '{a}', sincronizando"
                        erros.append(erro_msg)
                        log[-1]['acao'] = erro_msg
                        pilha.pop() 
                    else:
                        nt, prod_idx = producao
                        producao_corpo = self.gramatica.producoes[nt][prod_idx] 
                        pilha.pop()
                        
                        if producao_corpo != [self.gramatica.epsilon]:
                            for simbolo in reversed(producao_corpo):
                                pilha.append(simbolo)
                        
                        log[-1]['acao'] = f"Aplica {nt} -> {' '.join(producao_corpo) if producao_corpo else 'ε'}"
                else:  
                    erro_msg = f"Erro de sintaxe na linha {token.linha if token else 'EOF'}, coluna {token.coluna if token else 'EOF'}: não há produção para [{X}, {a}]"
                    erros.append(erro_msg)
                    log[-1]['acao'] = erro_msg
                    
                    
                    token_reader.consumir()
        
        if not token_reader.fim():
            while not token_reader.fim():
                token_extra = token_reader.proximo_token()
                erros.append(f"Erro: token adicional '{token_extra.nome}' após o fim da análise.")
                token_reader.consumir()

        sucesso_final = (len(erros) == 0 and pilha[-1] == '$')
        
        return {
            'sucesso': sucesso_final,
            'log': log,
            'erros': erros
        }