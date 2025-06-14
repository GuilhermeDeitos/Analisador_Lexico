from analisadorLexico import AnalisadorLexico
import sys


if __name__ == "__main__":
  # Ler o arquivo de entrada passado como argumento 
  if len(sys.argv) < 3:
        print("Uso: python3 main.py <nome do arquivo.cal> <nome do arquivo de saída>")
        print("Exemplo: python3 main.py teste.cal tokens.txt")
        sys.exit(1)
  arquivo_entrada = sys.argv[1]
  arquivo_saida = sys.argv[2]
  lexico = AnalisadorLexico(arquivo_entrada)
  lexico.write_tokens(arquivo_saida)
  print(f"Tokens escritos em {arquivo_saida} com sucesso!")
  
  
  