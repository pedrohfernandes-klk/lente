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
        link='<li><a class="cz-row" href="narrativas/ideias/"><span class="lab-set-number" aria-hidden="true">↗</span><span class="lab-set-copy"><strong>Ideias</strong><small>O método em cinco passos</small></span><span class="lab-set-arrow" aria-hidden="true">→</span></a></li>'
        if link not in s:
            assert s.count(marker)==1
            s=s.replace(marker,marker+link)
    else:
        link='<p class="ideias-publico-link"><a href="../../narrativas/ideias/">Ideias: o método em cinco passos →</a></p>'
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
