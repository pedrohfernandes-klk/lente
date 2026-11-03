"""03/11/2026: aplicação idempotente do piloto visual apenas à entrada de Algoritmos."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'cidadania/m2/index.html'
s=p.read_text('utf-8')
if 'data-fundo="ca"' not in s:
 s=s.replace('<header class="p-cab">','<header class="p-cab" data-fundo="ca" data-fundo-ciclo="36">',1)
 grafismo='''<div class="ca-grafismo" aria-hidden="true"><svg viewBox="0 0 720 300" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.4"><path class="ca-linhas" d="M35 65H180L270 115H340M35 150H340M35 235H180L270 185H340M380 115H470L560 65H685M380 150H685M380 185H470L560 235H685"/><g class="ca-entradas"><circle cx="35" cy="65" r="10"/><circle cx="35" cy="150" r="10"/><circle cx="35" cy="235" r="10"/></g><rect x="320" y="90" width="80" height="120" rx="2"/><path d="M340 115H380M340 150H380M340 185H380"/><g class="ca-saidas"><rect x="648" y="40" width="60" height="50"/><rect x="648" y="125" width="60" height="50"/><rect x="648" y="210" width="60" height="50"/></g><path class="ca-rota" d="M35 150H340L380 115H470L560 65H685" pathLength="100"/></g><rect class="ca-acento" x="352" y="142" width="16" height="16"/></svg></div>'''
 credito='''<p class="ca-credito">Grafismo gerado com recurso a IA, EPI, 2026. Esquema ilustrativo: uma regra encaminha um sinal entre vários percursos. <button type="button" class="fundo-botao" data-fundo-botao="ca" hidden>Parar o desenho</button></p>'''
 i=s.index('</header>',s.index('data-fundo="ca"'));s=s[:i]+grafismo+s[i:];s=s.replace('</header>','</header>'+credito,1)
 s=s.replace('</head>','<link rel="stylesheet" href="../../assets/fundo-algoritmos.css?v=20261103-1"><link rel="stylesheet" href="../../assets/fundos.css?v=20261102-1"><script defer src="../../assets/fundos.js?v=20261102-1"></script></head>',1)
p.write_text(s,'utf-8')
