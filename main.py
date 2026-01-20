from AnalisadorLL1 import AnalisadorLL1
from criar_gramatica_calabreso import criar_gramatica_calabreso
from TokenReader import TokenReader
from ConversorGramatica import ConversorGramatica
import sys
import os
import json


def exibir_tabela_analise(analisador, gramatica):
    nao_terminais = sorted(gramatica.nao_terminais)
    terminais = sorted(gramatica.terminais.union({'$'}))
    # Cabeçalho
    header = ["NT"] + terminais
    col_widths = [max(2, max(len(nt) for nt in nao_terminais))]
    for t in terminais:
        col_widths.append(max(8, len(t)))
    # Montar linhas
    linhas = []
    linhas.append(" | ".join(h.ljust(w) for h, w in zip(header, col_widths)))
    linhas.append("-+-".join('-'*w for w in col_widths))
    for nt in nao_terminais:
        row = [nt.ljust(col_widths[0])]
        for idx, t in enumerate(terminais):
            cell = ""
            entry = analisador.tabela[nt][t]
            if entry is not None:
                if entry[0] == 'sinc':
                    cell = "sinc"
                else:
                    nt_prod, idx_prod = entry
                    prod = gramatica.producoes[nt_prod][idx_prod]
                    cell = f"{nt_prod}→{' '.join(prod) if prod != [gramatica.epsilon] else 'ε'}"
            row.append(cell.ljust(col_widths[idx+1]))
        linhas.append(" | ".join(row))
    print("\nTabela de Análise LL(1):")
    print("\n".join(linhas))  

def salvar_resultado_json(resultado, arquivo_saida):
    """Salva os resultados da análise em formato JSON."""
    for item in resultado['log']:
        item['pilha'] = str(item['pilha'])
    
    with open(arquivo_saida, 'w', encoding='utf-8') as file:
        json.dump(resultado, file, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo_tokens> [arquivo_saida.json]")
        return
    
    arquivo_tokens = sys.argv[1]
    
    if len(sys.argv) >= 3:
        arquivo_saida = sys.argv[2]
    else:
        nome_base = os.path.splitext(os.path.basename(arquivo_tokens))[0]
        arquivo_saida = f"resultado_{nome_base}.json"
    
    print(f"Analisando tokens de {arquivo_tokens}...")
    
    token_reader = TokenReader(arquivo_tokens, arquivo_saida)
    
    if token_reader.tem_erro_lexico():
        print("Análise sintática interrompida devido a erro léxico.")
        return  
    
    gramatica_original = criar_gramatica_calabreso()
    
    print("Verificando se a gramática é LL(1)...")
    try:
        analisador_teste = AnalisadorLL1(gramatica_original)
        analisador_teste.calcular_first()
        analisador_teste.calcular_follow()
        analisador_teste.construir_tabela_analise()
        print("A gramática já é LL(1).")
        gramatica = gramatica_original
    except Exception as e:
        print(f"A gramática não é LL(1): {e}")
        print("Transformando a gramática em LL(1)...")
        
        transformador = ConversorGramatica(gramatica_original)
        gramatica = transformador.transformar_em_ll1()
        print("Gramática transformada com sucesso.")
    
    gramatica.atualizar_terminais()
    analisador = AnalisadorLL1(gramatica)
    
    print("Calculando conjuntos FIRST...")
    analisador.calcular_first()
    
    print("Calculando conjuntos FOLLOW...")
    analisador.calcular_follow()
    
    print("Construindo tabela de análise...")
    analisador.construir_tabela_analise()
    
    # print("\nConjuntos FIRST:")
    # for simbolo in sorted(analisador.first.keys()):
    #     print(f"FIRST({simbolo}) = {analisador.first[simbolo]}")
    # 
    # print("\nConjuntos FOLLOW:")
    # for nt in sorted(analisador.follow.keys()):
    #     print(f"FOLLOW({nt}) = {analisador.follow[nt]}")
    # 
    # print("\nTabela de análise:")
    # exibir_tabela_analise(analisador, gramatica)
    
    print("\nIniciando análise sintática...")
    token_reader = TokenReader(arquivo_tokens, arquivo_saida)
    
    resultado = analisador.analisar_tokens(token_reader)
    
    if resultado['sucesso']:
        print("\nAnálise sintática concluída com sucesso!")
    else:
        print("\nAnálise sintática falhou.")
        print("\nErros encontrados:")
        for erro in resultado['erros']:
            print(f"- {erro}")
    
    salvar_resultado_json(resultado, arquivo_saida)
    print(f"\nResultado detalhado salvo em {arquivo_saida}")
    
    return resultado

if __name__ == "__main__":
    main()