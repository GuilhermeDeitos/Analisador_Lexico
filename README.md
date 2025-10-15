# Analisador Léxico - Compilador Calabreso Script

Este é um **analisador léxico** implementado em **Python** destinado ao desenvolvimento de um **compilador** para a **linguagem Calabreso Script**. Ele faz a **leitura de um arquivo `.cal`**, verifica e classifica cada sequência de caractere como um **token**, removendo comentários, espaçamentos e outras construções que não serão utilizadas nas próximas fases da compilação.

---

## ⚙ Funcionalidades

✅ **Identifica diferentes tipos de tokens:**  
- **Palavras reservadas:** `digue`, `integro`, `stringo`, `realo`, `incremente`, `decremente`, `receba`, etc.  
- **Identificadores:** nomes de variáveis e funções.  
- **Números:** inteiros e reais.  
- **Operadores:** lógicos, relacionais e aritméticos.  
- **Delimitadores:** `;`, `,`, `()` e `{}`.  
- **Comentários:** comentários de linha `//` e de bloco `/* */`.  
- **Cadeias de texto:** tudo que estiver entre `"`.

---

## Como funciona?

1️⃣ **Leitura:** o `AnalisadorLexico` faz a **leitura do `.cal`**, removendo comentários e espaçamentos desnecessários.

2️⃣ **Captura de tokens:** ele verifica o **padrão de cada sequência de caractere**, tentando categorizá-la como um token válido.  
Se encontrar um **padrão desconhecido**, ele emite um **erro léxico**.

3️⃣ **Saída:** grava todos os tokens reconhecidos em um **único arquivo de saída**, um **`.txt`**, mostrando o nome do token, o valor, a linha e a posição.

---

## 🔨 Estrutura de diretório
```
├── main.py
├── AnalisadorLexico/
│ ├─ AnalisadorLexico.py
│ ├─ Token.py
│ ├─ especificacao_tokens.py
├── exemplos/
│ ├─ exemplo.cal
├── tokens/
│ ├─ tokens.txt
├── README.md
```

---

## Uso

```bash
python3 main.py <nome do arquivo .cal> <nome do arquivo de saída>
```

## Exemplo
```bash
python3 main.py exemplos/exemplo1.cal tokens.txt
```

### Exemplo1.cal
```cal
ifo (num menor_que 10) {
  calma("menor que 10");
} elso ifo (num maior_que 10) {
  calma("maior que 10");
} elso {
  calma("igual a 10");
}
```

### Saída tokens.txt
```
<Token id, 'ifo'> (Linha: 1, Coluna: 1)
<Token op_logicos, '(num'> (Linha: 1, Coluna: 5)
<Token menor_que, 'menor_que'> (Linha: 1, Coluna: 10)
<Token integro, '10'> (Linha: 1, Coluna: 20)
<Token op_logicos, ')'> (Linha: 1, Coluna: 22)
<Token \{, '{'> (Linha: 1, Coluna: 24)
<Token calma, 'calma'> (Linha: 2, Coluna: 1)
<Token op_logicos, '('> (Linha: 2, Coluna: 6)
<Token stringo, 'menor que 10'> (Linha: 2, Coluna: 7)
<Token op_logicos, ')'> (Linha: 2, Coluna: 21)
<Token ;, ';'> (Linha: 2, Coluna: 22)
<Token \}, '}'> (Linha: 3, Coluna: 1)
<Token id, 'elso'> (Linha: 3, Coluna: 3)
<Token id, 'ifo'> (Linha: 3, Coluna: 8)
<Token op_logicos, '(num'> (Linha: 3, Coluna: 12)
<Token maior_que, 'maior_que'> (Linha: 3, Coluna: 17)
<Token integro, '10'> (Linha: 3, Coluna: 27)
<Token op_logicos, ')'> (Linha: 3, Coluna: 29)
<Token \{, '{'> (Linha: 3, Coluna: 31)
<Token calma, 'calma'> (Linha: 4, Coluna: 1)
<Token op_logicos, '('> (Linha: 4, Coluna: 6)
<Token stringo, 'maior que 10'> (Linha: 4, Coluna: 7)
<Token op_logicos, ')'> (Linha: 4, Coluna: 21)
<Token ;, ';'> (Linha: 4, Coluna: 22)
<Token \}, '}'> (Linha: 5, Coluna: 1)
<Token id, 'elso'> (Linha: 5, Coluna: 3)
<Token \{, '{'> (Linha: 5, Coluna: 8)
<Token calma, 'calma'> (Linha: 6, Coluna: 1)
<Token op_logicos, '('> (Linha: 6, Coluna: 6)
<Token stringo, 'igual a 10'> (Linha: 6, Coluna: 7)
<Token op_logicos, ')'> (Linha: 6, Coluna: 19)
<Token ;, ';'> (Linha: 6, Coluna: 20)
<Token \}, '}'> (Linha: 7, Coluna: 1)
```

## Melhorias Futuras
- Implementar **tratamento de erros léxicos** mais robusto.

