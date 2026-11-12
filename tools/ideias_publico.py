"""02/11/2026: decisão 141; ligações nas duas páginas de HTML mantido.
As páginas de lições, Biblioteca e Laboratório continuam nos seus geradores.
"""
from pathlib import Path
import json,re,sys
R=Path(__file__).resolve().parents[1]
ROOT_URL='https://pedrohfernandes-klk.github.io/lente/'

def atualizar(rel,s):
    if rel=='index.html':
        # 05/11/2026: revisão de 5/11 (lente-ideias-7): sem «↗», que no mesmo cartão marca as ligações externas, e com a descrição
        # em minúscula, como as três de cima. A versão anterior sai antes de se pôr a nova.
        # 05/11/2026: decisão 163 (e decisão 97). A ordem passa a Ideias, Observar, Treinar e Criar.
        # 07/11/2026: decisão 180 (docente). Cada porta diz o seu subtítulo e deixa de ter número.
        # 12/11/2026: pedido entrada-temas. A entrada abre por quatro temas e a lista «Entradas do Laboratório» saiu: o cartão do
        # Laboratório é agora o do tema 03 («Histórias e criação», com o mesmo id, inicio-narrativas) e as três portas do catálogo
        # passaram para o mapa. A exigência da decisão 141 fica igual: a entrada tem de ter, dentro desse cartão, exatamente uma
        # ligação ao Ideias, com o mesmo texto das outras páginas públicas; se faltar, repõe-se antes da seta do cartão.
        marker='id="inicio-narrativas"'
        assert s.count(marker)==1
        pos=s.index(marker);fim=s.index('</article>',pos)
        link='<p class="tm-extra"><a href="narrativas/ideias/">Ideias: o método em cinco passos</a></p>'
        cartao=s[pos:fim].replace(link,'')
        assert 'narrativas/ideias/' not in cartao
        seta='<span class="tm-seta" aria-hidden="true">→</span></div>'
        assert cartao.count(seta)==1
        s=s[:pos]+cartao.replace(seta,link+seta)+s[fim:]
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
