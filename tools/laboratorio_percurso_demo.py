"""03/11/2026: demonstração isolada do percurso, sem escrever progresso."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'demonstracoes/laboratorio-percurso'


def gerar():
    dados = json.loads((ROOT / 'tools/licoes/ideias-s01.json').read_text(encoding='utf-8'))
    leitura = next(c for c in dados['cartoes'] if c.get('titulo') == 'Vê, mas não observa')
    pergunta = next(c for c in dados['cartoes'] if c.get('g') == 'watson')
    metodo = next(c for c in dados['cartoes'] if c.get('rot') == 'O método')
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'conteudo.js').write_text('window.PERCURSO=' + json.dumps(
        {'leitura': leitura, 'pergunta': pergunta, 'metodo': metodo}, ensure_ascii=False
    ).replace('</', '<\\/') + ';\n', encoding='utf-8')


if __name__ == '__main__':
    gerar()
