import re
import json
import sys
from Token import Token

class TokenReader:
    def __init__(self, arquivo_tokens, arquivo_saida):
        self.tokens = []
        self.posicao = 0
        self.erro_lexico = None
        self.arquivo_saida = arquivo_saida
        self._carregar_tokens(arquivo_tokens)
    
    def _carregar_tokens(self, arquivo_tokens):
        """Carrega tokens de um arquivo gerado pelo analisador léxico."""
        with open(arquivo_tokens, 'r') as file:
            linhas = file.readlines()
        
        padrao = r"<Token ([^,]+), '([^']*)'> \(Linha: (\d+), Coluna: (\d+)\)"
        
        for linha in linhas:
            match = re.match(padrao, linha.strip())
            if match:
                nome_token, valor, linha_num, coluna = match.groups()
                token = Token(nome_token, valor, int(linha_num), int(coluna))
                
                if nome_token == 'ERRO':
                    mensagem = f"Erro lexico: Simbolo invalido '{valor}' na linha {linha_num}, coluna {coluna}"
                    print(mensagem)
                    
                    self.erro_lexico = {
                        "tipo": "erro_lexico",
                        "mensagem": mensagem,
                        "linha": int(linha_num),
                        "coluna": int(coluna),
                        "simbolo": valor
                    }
                    
                    self._salvar_resultado_erro()
                    
                    return
                
                self.tokens.append(token)
    
    def _salvar_resultado_erro(self):
        """Salva informações do erro no arquivo resultado.json."""
        resultado = {
            "sucesso": False,
            "erro": self.erro_lexico
        }

        with open(self.arquivo_saida, "w") as file:
            json.dump(resultado, file, indent=4)
    
    def tem_erro_lexico(self):
        """Verifica se foi encontrado algum erro léxico."""
        return self.erro_lexico is not None
    
    def proximo_token(self):
        """Retorna o próximo token sem avançar a posição."""
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return None
    
    def consumir(self):
        """Consome o token atual e avança para o próximo."""
        if self.posicao < len(self.tokens):
            token = self.tokens[self.posicao]
            self.posicao += 1
            return token
        return None
    
    def reset(self):
        """Reinicia a leitura dos tokens."""
        self.posicao = 0
    
    def fim(self):
        """Verifica se chegou ao fim dos tokens."""
        return self.posicao >= len(self.tokens)