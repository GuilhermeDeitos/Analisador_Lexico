especificacao_tokens = [
    # Tokens a serem ignorados (comentários e espaços em branco)
    ('COMENTARIO', r'//[^\n]*|/\*.*?\*/'),
    ('IGNORE', r'[ \t\n]+'),

    # Palavras-chave e Símbolos (do mais específico para o mais geral)
    ('INTEGRO_TIPO', r'\bintegro\b'),
    ('STRINGO_TIPO', r'\bstringo\b'),
    ('REALO_TIPO', r'\brealo\b'),
    ('DIGUE', r'\bdigue\b'),
    ('IFO', r'\bifo\b'),
    ('ELSO_IFO', r'\belso_ifo\b'),
    ('ELSO', r'\belso\b'),
    ('DURANTO', r'\bduranto\b'),
    ('PARO', r'\bparo\b'),
    ('CALMA', r'\bcalma\b'),
    ('CALABRESO', r'\bcalabreso\b'),
    ('RECEBA', r'\breceba\b'),
    ('INCREMENTE', r'\bincremente\b'),
    ('DECREMENTE', r'\bdecremente\b'),
    
    # Operadores Lógicos (SEPARADOS para evitar conflitos LL(1))
    ('OP_E', r'\be\b'),
    ('OP_OU', r'\bou\b'),
    ('OP_NEM', r'\bnem\b'),

    # Operadores Aritméticos e Relacionais
    ('OP_MAIS', r'\bmais\b'),
    ('OP_MENOS', r'\bmenos\b'),
    ('OP_MULTIPLIQUE', r'\bmultiplique\b'),
    ('OP_DIVIDA', r'\bdivida\b'),
    ('OP_MAIOR_QUE', r'\bmaior_que\b'),
    ('OP_MENOR_QUE', r'\bmenor_que\b'),
    ('OP_MAIOR_INGUAL', r'\bmaior_ingual\b'),
    ('OP_MENOR_INGUAL', r'\bmenor_ingual\b'),
    ('OP_INGUAL', r'\b(igual|ingual)\b'),
    ('OP_VARIEGADO', r'\bvariegado\b'),

    # Literais e Identificadores
    ('REALO', r'\d+\.\d+'),
    ('INTEGRO', r'\d+'),
    ('STRINGO', r'"([^"\\]*(\\.[^"\\]*)*)"'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),

    # Símbolos e Delimitadores
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('SEMICOLON', r';'),
    ('COMMA', r','),

    # Token para qualquer outro caractere (geralmente um erro)
    ('ERRO', r'.'),
]