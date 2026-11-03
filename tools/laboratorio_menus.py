"""02/11/2026: piloto das quatro entradas, sem alterar peças ou progresso."""
import re

def apresentar(base, body):
    # Sem JavaScript, conservar o conteúdo aberto; menus.js aplica a abertura progressiva.
    if base=='narrativas':
        # Uma ação principal; as sessões diretas continuam disponíveis por abertura.
        body=re.sub(r'(<nav aria-label="Ideias">)(<a .*?</a>)(.*?)(</nav>)',
                    lambda m:m[1]+m[2]+'<details class="menu-sessoes"><summary>As sessões publicadas</summary><div>'+m[3]+'</div></details>'+m[4],body,flags=re.S)
        body=re.sub(r'(<section class="bloco"[^>]*>)(<header>.*?</header>)(<figure.*?</figure>)(<details[^>]*>)(<summary>.*?</summary>)(.*?</details>)',
                    lambda m:m[1]+m[2]+m[4]+m[5]+m[3]+m[6],body,flags=re.S)
        body=re.sub(r'(<section class="bloco"[^>]*>)<header><h2>(.*?)</h2>(.*?)</header>(<details[^>]*>)<summary>.*?</summary>',
                    lambda m:m[1]+m[4]+'<summary><h2>'+m[2]+'</h2><span>Ver percursos</span></summary><header>'+m[3]+'</header>',body,flags=re.S)
        body=body.replace('<section class="progresso"><h2>O teu progresso</h2>', '<details class="progresso menu-registos"><summary>O teu progresso e os teus registos</summary><div>')
        body=body.replace('<p data-registos-aviso role="status">O ficheiro guarda só os estados, sem respostas nem textos.</p></section>', '<p data-registos-aviso role="status">O ficheiro guarda só os estados, sem respostas nem textos.</p></div></details>')
    else:
        body=re.sub(r'(<a class="continuar[^"]*") hidden',r'\1',body,count=1)
        body=re.sub(r'(<figure.*?</figure>)',r'<details class="menu-imagem"><summary>A imagem de partida</summary>\1</details>',body,count=1,flags=re.S)
    return body
