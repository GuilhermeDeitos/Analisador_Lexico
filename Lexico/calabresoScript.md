# Gramática

P = {
  ( -> '(',
  ) -> ')',
  , -> ',',
  palavra_reservada -> [a-zA-Z_][a-zA-Z0-9_]*,
  ; -> ';',
  { -> '{',
  } -> '}',
  constante -> 'digue'
  integro -> [0-9]+,
  stringo -> ["] [^"\n] ["] ,
  realo -> [0-9]+.[0-9]+,
  id -> [a-zA-Z_][a-zA-Z0-9_]*,
  op_incremento -> 'incremente',
  op_decremento -> 'decremente',
  op_atribuicao -> 'receba',
  op_aritmetico_soma -> 'mais' | 'menos',
  op_aritmetico_mult -> 'multiplique' | 'divida',
  op_relacional -> 'maior_que' | 'menor_que' | 'ingual' | 'variegado' | 'maior_ingual' | 'menor_ingual',
  op_logico -> 'e' | 'ou' | 'nem',
  if -> 'ifo',
  else -> 'elso',
  else_if -> 'elso ifo',
  for -> 'paro',
  while -> 'duranto',
  print -> 'calma',
  input -> 'calabreso',
  comentario -> '//' [^"\n]* | '/*' [^"*/]* '*/',
  espaco -> [\s]+
  tabulacao -> [\t]+
  quebra_linha -> [\n]+
}