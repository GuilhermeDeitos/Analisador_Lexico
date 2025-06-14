especificacao_tokens = {
        'id': r'[a-zA-Z_][a-zA-Z0-9_]*',
        'integro': r'[0-9]+',
        'stringo': r'"([^"\\]*(\\.[^"\\]*)*)"',
        'realo': r'[0-9]+\.[0-9]+',
        '(': r'\(',
        ')': r'\)',
        '{': r'\{',
        '}': r'\}',
        ';': r';',
        ',': r',',
        'receba': r'=',
        'op_logicos': r'\b(?:e|ou|nem)\b',
        'op_aritmeticos_soma': ['incremente', 'decremente','mais', 'menos'],
        'op_aritmeticos_multiplicacao': ['multiplique', 'divida'],
        'op_relacionais': ['maior_que', 'menor_que', 'maior_ingual',
                           'menor_ingual', 'ingual','variegado'],
        'if': 'ifo',
        'else': 'elso',
        'else_if': 'elso ifo',
        'for': 'paro',
        'while': 'duranto',
        'print': 'calma',
        
        'input': 'calabreso',
        # Comentário de linha: começa com // até o fim da linha
        'comentario_linha': r'//[^\n]*',
        # Comentário de bloco: começa com /* e termina com */
        'comentario_bloco': r'/\*.*?\*/',
        # Espaços em branco, tabulações e novas linhas
        'espaco': r'\s+',
        'tabulacao': r'\t',
        'nova_linha': r'\n'
    }

