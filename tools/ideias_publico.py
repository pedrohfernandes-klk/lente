"""02/11/2026: decisão 141; ligações nas duas páginas de HTML mantido.
As páginas de lições, Biblioteca e Laboratório continuam nos seus geradores.
"""
from pathlib import Path
import json,re,sys
R=Path(__file__).resolve().parents[1]
ROOT_URL='https://pedrohfernandes-klk.github.io/lente/'

def atualizar(rel,s):
    if rel=='index.html':
        marker='<ul class="lab-sets" aria-label="Entradas do Laboratório">'
        # 05/11/2026: revisão de 5/11 (lente-ideias-7): sem «↗», que no mesmo cartão marca as ligações externas, e com a descrição
        # em minúscula, como as três de cima. A versão anterior sai antes de se pôr a nova.
        antiga='<li><a class="cz-row" href="narrativas/ideias/"><span class="lab-set-number" aria-hidden="true">↗</span><span class="lab-set-copy"><strong>Ideias</strong><small>O método em cinco passos</small></span><span class="lab-set-arrow" aria-hidden="true">→</span></a></li>'
        link='<li><a class="cz-row" href="narrativas/ideias/"><span class="lab-set-number" aria-hidden="true"></span><span class="lab-set-copy"><strong>Ideias</strong><small>o método em cinco passos</small></span><span class="lab-set-arrow" aria-hidden="true">→</span></a></li>'
        # 05/11/2026: decisão 163 (e decisão 97). A ordem passa a Ideias, Observar, Treinar e Criar, e cada porta diz o seu
        # passo (passoTexto de percursos.json, em minúscula e sem ponto, como as outras descrições). A retoma
        # (assets/cartaz-entrada.js) passa a associar cada porta pela âncora do seu href, e não pela posição.
        s=s.replace(antiga,'').replace(link,'')
        assert s.count(marker)==1
        pos=s.index(marker)+len(marker)
        fim=s.index('</ul>',pos)
        lista=link+s[pos:fim]
        for b in json.loads((R/'assets/laboratorio/percursos.json').read_text('utf-8'))['blocks']:
            # 07/11/2026: decisão 180 (docente). Cada porta diz o seu subtítulo, e não um «passo» do método.
            t=b['subtitle']
            lista,n=re.subn(r'(<a class="cz-row" href="narrativas/tudo/#'+re.escape(b['anchor'])+r'">(?:(?!</li>).)*?<small>)[^<]*(</small>)',lambda m:m.group(1)+t+m.group(2),lista,count=1)
            assert n==1,b['id']
            # 07/11/2026: decisão 180 (docente). As portas também deixam de ter número (antes 01, 02 e 03), como a linha do Ideias.
            lista,n=re.subn(r'(<a class="cz-row" href="narrativas/tudo/#'+re.escape(b['anchor'])+r'"><span class="lab-set-number" aria-hidden="true">)\d*(</span>)',r'\1\2',lista,count=1)
            assert n==1,b['id']
        s=s[:pos]+lista+s[fim:]
    else:
        # 05/11/2026: revisão de 5/11 (lente-ideias-8): a ligação usa o estilo das outras ligações da oficina (.vpf-liga, a negrito),
        # em vez de uma classe sem CSS.
        s=s.replace('<p class="ideias-publico-link"><a href="../../narrativas/ideias/">Ideias: o método em cinco passos →</a></p>','')
        link='<p class="vpf-liga ideias-publico-link"><a href="../../narrativas/ideias/">Ideias: o método em cinco passos →</a></p>'
        if link not in s:
            assert s.count('</main>')==1
            s=s.replace('</main>',link+'</main>')
    return s

def main():
    failed=False
    for rel in ['index.html','ver-para-fazer/oficina-ideias/index.html']:
        p=R/rel;old=p.read_text('utf-8');new=atualizar(rel,old)
        if '--verificar' in sys.argv:
            if old!=new:print(rel+': falta ligação');failed=True
        elif old!=new:p.write_bytes(new.encode('utf-8'))
    return int(failed)
if __name__=='__main__':raise SystemExit(main())
