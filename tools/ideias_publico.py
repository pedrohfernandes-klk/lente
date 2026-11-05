"""02/11/2026: decisão 141; ligações nas duas páginas de HTML mantido.
As páginas de lições, Biblioteca e Laboratório continuam nos seus geradores.
"""
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1]
ROOT_URL='https://pedrohfernandes-klk.github.io/lente/'

def atualizar(rel,s):
    if rel=='index.html':
        marker='<ul class="lab-sets" aria-label="Entradas do Laboratório">'
        # 05/11/2026: revisão de 5/11 (lente-ideias-7): sem «↗», que no mesmo cartão marca as ligações externas, e com a descrição
        # em minúscula, como as três de cima. A versão anterior sai antes de se pôr a nova.
        antiga='<li><a class="cz-row" href="narrativas/ideias/"><span class="lab-set-number" aria-hidden="true">↗</span><span class="lab-set-copy"><strong>Ideias</strong><small>O método em cinco passos</small></span><span class="lab-set-arrow" aria-hidden="true">→</span></a></li>'
        link='<li><a class="cz-row" href="narrativas/ideias/"><span class="lab-set-number" aria-hidden="true"></span><span class="lab-set-copy"><strong>Ideias</strong><small>o método em cinco passos</small></span><span class="lab-set-arrow" aria-hidden="true">→</span></a></li>'
        # 02/11/2026: a retoma associa os três primeiros itens às portas.
        # A ligação nova vem depois deles, preservando esse contrato sem mudar o motor.
        s=s.replace(antiga,'').replace(link,'')
        assert s.count(marker)==1
        pos=s.index('</ul>',s.index(marker))
        s=s[:pos]+link+s[pos:]
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
