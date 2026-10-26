"""Instala/atualiza o carregamento comum, sem reescrever conteúdos ou motores.
Executar depois de gerar HTML. --check falha se houver páginas por integrar.
"""
from pathlib import Path
import re,sys,json

ROOT=Path(__file__).resolve().parents[1]
SITE='pt' if (ROOT/'m9').exists() else 'lente'
VERSION='20261025-universal-1'
READING_GRID=re.compile(r'class\s*=\s*\\?["\'][^"\'<>]*\b(?:ess-mini|paralelo)\b')
SCRIPT_GRIDS={}
def has_reading_grid(text,path):
    if READING_GRID.search(text):return True
    for src in re.findall(r'<script\b[^>]*src=["\']([^"\']+)["\']',text,re.I):
        src=src.split('?')[0]
        if '://' in src:
            prefix=f'https://pedrohfernandes-klk.github.io/{SITE}/'
            if not src.startswith(prefix):continue
            target=ROOT/src[len(prefix):]
        else:target=path.parent/src
        target=target.resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():continue
        if target not in SCRIPT_GRIDS:SCRIPT_GRIDS[target]=bool(READING_GRID.search(target.read_text('utf-8')))
        if SCRIPT_GRIDS[target]:return True
    return False
def integrated(path):
    raw=path.read_bytes(); text=raw.decode('utf-8')
    if not re.search(r'</head\s*>',text,re.I): return raw
    text=re.sub(r'<link\b[^>]*href=["\'][^"\']*/?assets/appearance\.css[^"\']*["\'][^>]*>','',text,flags=re.I)
    text=re.sub(r'<script\b[^>]*src=["\'][^"\']*/?assets/appearance\.js[^"\']*["\'][^>]*>\s*</script>','',text,flags=re.I)
    def html_tag(m):
        tag=re.sub(r'\sdata-appearance-(?:family|site)=["\'][^"\']*["\']','',m[0])
        kind='cards' if 'casca-topo' in text else 'paper' if 'button.p{' in text else None
        family=f' data-appearance-family="{kind}"' if kind else ''
        return tag[:-1]+f' data-appearance-site="{SITE}"'+family+'>'
    text=re.sub(r'<html\b[^>]*>',html_tag,text,count=1,flags=re.I)
    depth=len(path.relative_to(ROOT).parts)-1
    prefix='../'*depth
    # Invalidar a cache só nas páginas que usam estes blocos de leitura.
    reading_grid=has_reading_grid(text,path)
    css_version='20261025-reading1' if reading_grid else VERSION+'-slides1' if 'class="deck"' in text else VERSION
    tags=f'<link rel="stylesheet" href="{prefix}assets/appearance.css?v={css_version}"><script src="{prefix}assets/appearance.js?v={VERSION}"></script>'
    text=re.sub(r'</head\s*>',lambda m:tags+m[0],text,count=1,flags=re.I)
    return text.encode('utf-8')

def pages():
    return [p for p in ROOT.rglob('*.html') if not any(part in ('.git','tests','_qa') for part in p.relative_to(ROOT).parts)]
if __name__=='__main__':
    changed=[]; scanned=pages()
    for p in scanned:
        updated=integrated(p)
        if updated!=p.read_bytes():
            changed.append(p.relative_to(ROOT).as_posix())
            if '--check' not in sys.argv:p.write_bytes(updated)
    print(json.dumps({'site':SITE,'pages':len(scanned),'pending' if '--check' in sys.argv else 'updated':len(changed),'paths':changed if '--check' in sys.argv else []}))
    if '--check' in sys.argv and changed:sys.exit(1)
