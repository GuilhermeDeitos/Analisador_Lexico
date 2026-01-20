class ConversorGramatica:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.novas_producoes = {}
        self.contador_novos_simbolos = 0
    
    def eliminar_recursao_esquerda(self):
        """
        Elimina a recursão à esquerda direta da gramática.
        
        Transforma produções do tipo:
        A → Aα₁ | Aα₂ | ... | Aαm | β₁ | β₂ | ... | βn
        
        Em:
        A → β₁A' | β₂A' | ... | βnA'
        A' → α₁A' | α₂A' | ... | αmA' | ε
        """
        resultado = {}
        
        for nt in sorted(self.gramatica.nao_terminais):
            producoes = self.gramatica.producoes[nt]
            
            recursivas = []
            nao_recursivas = []
            
            for producao in producoes:
                if producao and producao[0] == nt:
                    recursivas.append(producao[1:]) 
                else:
                    nao_recursivas.append(producao)
            
            if not recursivas:
                resultado[nt] = producoes
                continue
            
            novo_nt = self._gerar_novo_simbolo(nt)
            
            novas_producoes_a = []
            for beta in nao_recursivas:
                if beta == [self.gramatica.epsilon]:
                    novas_producoes_a.append([novo_nt])
                else:
                    nova_prod = beta.copy()
                    nova_prod.append(novo_nt)
                    novas_producoes_a.append(nova_prod)
            
            novas_producoes_a_linha = []
            for alfa in recursivas:
                nova_prod = alfa.copy()
                nova_prod.append(novo_nt)
                novas_producoes_a_linha.append(nova_prod)
            
            novas_producoes_a_linha.append([self.gramatica.epsilon])
            
            resultado[nt] = novas_producoes_a
            resultado[novo_nt] = novas_producoes_a_linha
            
            self.gramatica.nao_terminais.add(novo_nt)
        
        self.gramatica.producoes = resultado
        return self.gramatica
    
    def fatorar_esquerda(self):
        """
        Aplica fatoração à esquerda na gramática.
        
        Transforma produções do tipo:
        A → αβ₁ | αβ₂ | ... | αβn | γ₁ | γ₂ | ... | γm
        
        Em:
        A → αA' | γ₁ | γ₂ | ... | γm
        A' → β₁ | β₂ | ... | βn
        """
        alteracoes = True
        
        while alteracoes:
            alteracoes = False
            resultado = {}
            
            for nt in self.gramatica.nao_terminais:
                producoes = self.gramatica.producoes[nt]
                
                prefixos = {}
                for producao in producoes:
                    if not producao:  
                        if self.gramatica.epsilon not in prefixos:
                            prefixos[self.gramatica.epsilon] = []
                        prefixos[self.gramatica.epsilon].append([])
                        continue
                    
                    primeiro = producao[0]
                    if primeiro not in prefixos:
                        prefixos[primeiro] = []
                    
                    prefixos[primeiro].append(producao)
                
                necessita_fatoracao = False
                for prefixo, prods in prefixos.items():
                    if len(prods) > 1:
                        prefixo_comum = self._maior_prefixo_comum(prods)
                        if len(prefixo_comum) > 0:
                            necessita_fatoracao = True
                            break
                
                if not necessita_fatoracao:
                    resultado[nt] = producoes
                    continue
                
                alteracoes = True
                
                grupos = self._agrupar_por_prefixo_comum(producoes)
                
                novas_producoes = []
                for prefixo, grupo in grupos.items():
                    if len(grupo) <= 1:
                        novas_producoes.extend(grupo)
                        continue
                    
                    novo_nt = self._gerar_novo_simbolo(nt)
                    self.gramatica.nao_terminais.add(novo_nt)
                    
                    restos = []
                    for prod in grupo:
                        if len(prod) <= len(prefixo):
                            restos.append([self.gramatica.epsilon])
                        else:
                            restos.append(prod[len(prefixo):])
                    
                    novas_producoes.append(prefixo + [novo_nt])
                    
                    if novo_nt not in resultado:
                        resultado[novo_nt] = []
                    
                    resultado[novo_nt] = restos
                
                resultado[nt] = novas_producoes
            
            self.gramatica.producoes = resultado
        
        return self.gramatica
    
    def _maior_prefixo_comum(self, producoes):
        """Encontra o maior prefixo comum entre várias produções."""
        if not producoes:
            return []
        
        prefixo = producoes[0]
        
        for prod in producoes[1:]:
            tamanho = 0
            for i in range(min(len(prefixo), len(prod))):
                if prefixo[i] == prod[i]:
                    tamanho += 1
                else:
                    break
            
            prefixo = prefixo[:tamanho]
            
            if not prefixo:
                break
        
        return prefixo
    
    def _agrupar_por_prefixo_comum(self, producoes):
        """Agrupa produções por seus prefixos comuns mais longos."""
        grupos = {}
        processadas = set()
        
        for i, prod1 in enumerate(producoes):
            if i in processadas:
                continue
            
            grupo = [prod1]
            processadas.add(i)
            
            prefixo_atual = prod1

            for j, prod2 in enumerate(producoes):
                if j in processadas or i == j:
                    continue
                
                prefixo = self._maior_prefixo_comum([prod1, prod2])
                
                if prefixo:  
                    grupo.append(prod2)
                    processadas.add(j)
                    prefixo_atual = prefixo
            
            prefixo_str = "".join(prefixo_atual)
            if prefixo_atual:
                if prefixo_str not in grupos:
                    grupos[prefixo_str] = []
                grupos[prefixo_str].append(grupo)
        
        resultado = {}
        for prefixo_str, lista_grupos in grupos.items():
            for grupo in lista_grupos:
                if prefixo_atual := self._maior_prefixo_comum(grupo):
                    prefixo_str = "".join(prefixo_atual)
                    resultado[prefixo_str] = grupo
        
        for i, prod in enumerate(producoes):
            if i not in processadas:
                prod_str = "".join(prod)
                resultado[prod_str] = [prod]
        
        return resultado
    
    def _gerar_novo_simbolo(self, base):
        """Gera um novo símbolo não-terminal único."""
        self.contador_novos_simbolos += 1
        return f"{base}_{self.contador_novos_simbolos}"
    
    def transformar_em_ll1(self):
        """Aplica todas as transformações necessárias para obter uma gramática LL(1)."""
        self.eliminar_recursao_esquerda()
        
        self.fatorar_esquerda()
        
        return self.gramatica