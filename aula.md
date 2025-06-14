# Análise léxica

## Léxico
* Conjunto de palavras que formam uma linguagem.
* Dicionário

## Papel do analisador léxico
* Em termos de LP, palavras são objetos como nomes de variáveis, operadores, palavras-chave, etc.
* O analisador léxico é responsável por identificar esses objetos e classificá-los.
* O analisador léxico transforma uma sequência de caracteres em uma sequência de tokens.
* Essa sequência de tokens é passada para o analisador sintático.
* O analisador léxico ignora espaços em branco, comentários e outros caracteres irrelevantes.
* Exemplo:
```c
int main() {
    int a = 10;
    int b = a + 20;
    return 0;
}
```
* Sequência de caracteres: `int main() { int a = 10; int b = 20; int c = a + b; return 0; }`
* Sequencia de tokens:
```	
[void,]
[id, main]
[(,]
[),]
[{,]
[tipo, int]
[id, a]
...
```
* Ele não se preocupa com a estrutura da linguagem, apenas com os tokens.
* Tarefas secundárias
  * Remover espaços em branco
  * Remover comentários
  * Exibir mensagens de erro
  * Processamento de macros
## Tokens, padrões e lexemas
* Token: unidade básica de informação que o analisador léxico identifica, `unidade léxica`.
  * Palavras-chave
  * Identificadores
  * Operadores
    * Pode ser interessante dividir os operadores em subcategorias
    * Exemplo: `+` pode ser um operador aditivo ou um operador de concatenação
  * Delimitadores geralmente são considerados tokens
    * Exemplo: `;`, `,`, `(`, `)`
  * Constantes
  * Literais
  * Números
  
* Padrão: Regra para reconhecer o token.
* Lexema: Conjunto de caracteres no programa-fonte que é reonhecido pelo padrão de um token
* Exemplo: `printf("Total: %d",score);`
  | Token | Lexema | Padrão |
  |-------|--------|--------|
  | `id`  | `printf`| `[a-zA-Z_][a-zA-Z0-9_]* (String iniciadas com letra ou _)` |
  | `(`   | `(`    | `"("` |
  | `string`   | `"Total: %d"`    | `"Sequencia de caracteres entre aspas duplas ("")"` |
  | `,`   | `,`    | `","` |
  | `id`  | `score`| `[a-zA-Z_][a-zA-Z0-9_]* (String iniciadas com letra ou _)` |
  | `)`   | `)`    | `")"` |
  | `;`   | `;`    | `";"` |

### Atributos de tokens
* Cada token é representado por 3 informações
  * Classe
    * Identificador
    * Cadeia
  * Lexema (valor): Depende da classe do token, pode ser o numero, uma sequencia de caracteres
    * Token simples: Não tem valor associado, uma vez que a classe o descreve
    * Token com argumento: Tem valor associado
  * Posição do token: Local do texto (linha, coluna) onde o token foi encontrado
    * Usado para mensagens de erro
* Exemplo:
```c
42 + (675 * 31) - 20
```
| Lexema | Tipo | Valor |
|--------|------|-------|
| `42`   | `NUM`| `42`  |
| `+`    | `OP` | `+`   |
| `(`    | `(`  | `(`   |
| `675`  | `NUM`| `675` |
| `*`    | `OP` | `*`   |
| `31`   | `NUM`| `31`  |
| `)`    | `)`  | `)`   |
| `-`    | `OP` | `-`   |
| `20`   | `NUM`| `20`  |

### Tabela de símbolos
* Estrutura de dados que armazena informações sobre os identificadores sobre os tokens
* Implementação:
  * Listas
  * Árvores
  * Tabelas hash
* Informações armazenadas:
  * Nome do identificador
  * Tipo do identificador
  * Escopo do identificador
  * Endereço do identificador
  * Valor do identificador
* Operações:
  * Inserir
  * Buscar
  * Acessar informações associadas a um nome  

### Especificação de tokens
* Expressões regulares
* A especificação de tokens é feita através de expressões regulares
* Expressões regulares são uma forma de descrever padrões em cadeias de caracteres
* Uma expressão regular r é completamente definida pelo conjunto de cadeias de caracteres que ela reconhece
* Esse conjunto é denominado linguagem gerada pela expressão regular e é denotada por L(r)
* As expressões regulares descrevem todas as linguagens que podem ser formadas a partir de operadores sobre linguagem aplicados aos simbolos de algum alfabeto
* Conceitos básicos
  * Simbolo: Conjunto de caracteres
  * Cadeia vazia: A cadeia vazia é representada por `ε` e é uma cadeia que não contém nenhum símbolo
  * Alternativas: `|` é o operador de alternância, que indica que uma das alternativas deve ser escolhida
  * Concatenação: A concatenação é representada pela simples junção de dois símbolos ou expressões regulares
  * Repetição: `*` é o operador de repetição, que indica que o símbolo ou expressão regular pode aparecer zero ou mais vezes
  * [abcd]: Representa `a | b | c | d`
  * [a-z]: Representa `a | b | c | ... | z`
  * [b-gM-Q]: Representa `b | c | d | e | f | g | M | N | O | P | Q`
  * r?: Representa `r | ε`
  * r+: Representa `r | rr*`
  * ~r: Representa o complemento de r
* Exemplo:
  - Expressão regular para uma sequencia de 1 ou mais digitos
  - digito digito*`
  - digito = [0-9]

## Expressões regulares	para LP
* Numeros: Sequencia de digitos (numeros naturais), numeros decimais ou numeros com expoente
* Exemplos
  * nat = [0-9]+ -> 999
  * nat_sinal = (+|-)? [0-9]+ -> +999 ou -999
  * dec = nat_sinal ("." nat)? ("E" nat_sinal)? -> 999.99 ou 999.99E-10
* Identificadores: Sequencia de letras, digitos e sublinhados, deve começar com letra ou sublinhado
* Isso pode ser expressado como:
  * letra = [a-Z]
  * digito = [0-9]
  * id = letra (letra | digito)*
* Palavras reservadas: São mais simples
  * Exemplo: `if`, `else`, `while`, `for`, `return`
  * Exemplo: reservadas =`if` | `else` | `while` | `for` | `return`
* Comentários: Sequencia de caracteres que não são relevantes para a execução do programa
  * Exemplo: `//` ou `/* ... */`
  * Exemplo: comentario = `// (~\n)*` | `/* (~*/)* */`
## Reconhecedores de tokens - AFDs
* Uma tecnica são os autômatos finitos
* Os AFDs podem ser usados para reconhecer expressões regulares
* Transformação de ER's para AFD's 
### Erro léxico
* Ocorre quando o analisador léxico não consegue reconhecer um token
* Exemplo: `int 123abc;`
* O analisador léxico não consegue reconhecer `123abc` como um identificador
* O analisador léxico deve exibir uma mensagem de erro
* Embora incomuns, devem ser tratados pelo analisador léxico
* Não é razoavel interromper a compilação por causa do que geralmente é um pequeno erro, geralmente tentamos recuperar o erro e continuar a análise
* A forma de recuperação mais simples é a modalidade de panico
  * Recomevos caracter a partir do próximo delimitador
  * Exemplo: `for$aux`
      * o simbolo `$` terminaria a varredura do token for
      * Como não é um token valido, ele será excluido
      * O analisador léxico continua a varredura a partir do próximo delimitador
* Outras formas
  1. Remover um caractere estranho
  2. inserir um caractere ausente
  3. substituir um caractere incorreto por um correto
  4. trocar dois caracteres adjacentes
## Implementando um diagrama de transições
* Cada estado recebe um segmento de código
* Se existirem lados deixando um estado, então seu código lê caractere e seleciona um lado para seguir
* Proximo caractere ( ) -> Próximo simbolo no buffer
* Se existir um lado rotulado pelo caracter lido, o controle é transferido para o código apontado a esse lado
* Se existir, chama próximo diagrama de transição
* Se não existir, o controle é transferido para o código do estado de erro