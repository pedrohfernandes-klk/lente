"""03/11/2026: Ideias como eixo real; dados apenas das sessões publicadas."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
e = html.escape

def sessoes():
    dados = [json.loads(p.read_text('utf-8')) for p in sorted((ROOT/'tools/licoes').glob('ideias-s*.json'))]
    return [d for d in dados if not d.get('piloto') and (ROOT/d['saida']).exists()]

def acao(prefixo):
    dados = sessoes()
    manifesto = [{'chave': d['chave'], 'url': prefixo+d['saida'].removesuffix('index.html')} for d in dados]
    return ('<a class="cz-button ld-open" data-ideias-acao href="'+e(manifesto[0]['url'])+'">Começar Ideias →</a>'
            '<script type="application/json" data-ideias-sessoes>'+json.dumps(manifesto, ensure_ascii=False).replace('<','\\u003c')+'</script>')

def scripts(prefixo):
    return ('<script defer src="'+prefixo+'assets/licoes/progresso-laboratorio.js?v=20261102-1"></script>'
            '<script defer src="'+prefixo+'assets/laboratorio/ideias-acao.js?v=20261103-1"></script>')

def recursos(prefixo):
    return ('<nav class="ideias-recursos" aria-label="Recursos para Ideias">'
            + ''.join('<a href="'+prefixo+'narrativas/tudo/#'+p+'">'+t+'</a>' for p,t in [('ler-como-quem-escreve','Observar'),('treinar','Treinar'),('criar','Criar')])+'</nav>')

def explorar():
    grupos = json.loads((ROOT/'assets/laboratorio/ideias-explorar.json').read_text('utf-8'))
    destaques = {'Wordle', 'Color', 'Music Lab'}
    def item(recurso):
        nome,desc,url,requisito = recurso
        return '<li><a href="'+e(url)+'" target="_blank" rel="noopener noreferrer"><b>'+e(nome)+' ↗</b><span>'+e(desc)+'</span><small>'+e(requisito)+'. Novo separador.</small></a></li>'
    return ('<section class="ideias-explorar" id="explorar"><h2>Explorar</h2><p>Palavras, imagens, sons e escolhas. As ligações abrem noutro sítio.</p>'
            + '<ul class="ideias-destaques" aria-label="Três propostas">'+''.join(item(r) for _,links in grupos for r in links if r[0] in destaques)+'</ul>'
            + ''.join('<details><summary>'+e(titulo)+'</summary><ul>'+''.join(item(r) for r in links if r[0] not in destaques)+'</ul></details>' for titulo,links in grupos)+'</section>')

def portugues():
    return ('<section class="ideias-portugues"><h2>Português</h2><p>Leva a observação para a leitura e para a escrita.</p><a class="ideias-mapa" href="https://pedrohfernandes-klk.github.io/pt/">Entrar em Português →</a>'
            '<svg viewBox="0 0 360 180" aria-hidden="true"><path d="M0 35Q90 0 180 35T360 35M0 70Q90 35 180 70T360 70M0 105Q90 70 180 105T360 105M0 140Q90 105 180 140T360 140"/><path d="M110 48q35-12 70 0q35-12 70 0v90q-35-12-70 0q-35-12-70 0zM180 48v90"/></svg>'
            '<small>Grafismo gerado com recurso a IA. Livro e linhas de calçada, EPI, 2026.</small></section>')

def instalar_raiz(texto):
    import re
    inicio = texto.index('<article class="ld mobile-dest cz-door" id="inicio-narrativas"')
    fim = texto.index('</article>', inicio)+len('</article>')
    artigo = texto[inicio:fim]
    artigo = artigo.replace('<h2 class="ld-n">Laboratório.</h2>', '<h2 class="ld-n">Ideias.</h2>')
    artigo = re.sub(r'<a class="cz-button ld-open".*?</a>', lambda _:acao(''), artigo, count=1)
    # Reexecução conserva um único manifesto.
    artigo = re.sub(r'(</script>)<script type="application/json" data-ideias-sessoes>.*?</script>', r'\1', artigo)
    artigo = re.sub(r'<p class="ld-f">.*?</p>', '<p class="ld-f">Junta material e põe uma ideia tua à prova.</p>', artigo, count=1)
    artigo = re.sub(r'<ul class="lab-sets" aria-label="Entradas do Laboratório">.*?</ul>', lambda _:recursos('')+'<a class="ideias-mapa" href="narrativas/">O Laboratório →</a>', artigo)
    artigo = re.sub(r'<nav class="ideias-recursos".*?</nav>', lambda _:recursos(''), artigo)
    if 'href="narrativas/ideias/"' not in artigo:
        artigo = artigo.replace('<nav class="ideias-recursos"','<a class="ideias-mapa" href="narrativas/ideias/">O curso e as sessões →</a><nav class="ideias-recursos"')
    texto = texto[:inicio]+artigo+texto[fim:]
    if 'assets/laboratorio/ideias-acao.js' not in texto:
        texto = texto.replace('</head>', '<link rel="stylesheet" href="assets/laboratorio/ideias-eixo.css?v=20261103-1">'+scripts('')+'</head>')
    return texto

if __name__ == '__main__':
    p = ROOT/'index.html'
    p.write_bytes(instalar_raiz(p.read_text('utf-8')).encode('utf-8'))
