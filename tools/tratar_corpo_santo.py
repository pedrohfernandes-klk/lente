"""05/11/2026: pedido do docente (elétrico de lado e alavanca ao lado da via). Trata a fotografia do Commons
«Remodelados class tram no. 541 turning street corner in Largo do Corpo Santo in Lisbon, Portugal (55127582736).jpg»
(Philip Mallis, 29 de maio de 2025, CC BY-SA 4.0) para a colagem da Justiça (tools/gerar_carris.py).
Uso: python3 tools/tratar_corpo_santo.py <miniatura de 1920 px descarregada do Commons>
Escreve assets/justica/corpo-santo-541.webp. A fotografia tratada fica com a mesma licença (CC BY-SA 4.0)."""
import hashlib, sys
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
import numpy as np

MINIATURA_SHA256 = '1a95a1226eb539dc10faec28e36313bbe4d201a12e6e35dae77e4e628f6d5d43'
DESTINO = Path(__file__).resolve().parents[1] / 'assets/justica/corpo-santo-541.webp'

def tratar(origem):
    assert hashlib.sha256(Path(origem).read_bytes()).hexdigest() == MINIATURA_SHA256, 'miniatura diferente da registada'
    im = Image.open(origem).convert('RGB')
    assert im.size == (1920, 1446), im.size
    a = np.asarray(im).copy()
    # Publicidade apagada: o painel grande da lateral e o painel da porta passam a uma cor lisa (a mediana do vermelho de cada um).
    for x0, y0, x1, y1 in ((1094, 812, 1694, 916), (889, 792, 958, 880)):
        reg = a[y0:y1, x0:x1].reshape(-1, 3)
        verm = reg[(reg[:, 0] > 120) & (reg[:, 1] < 80) & (reg[:, 2] < 80)]
        a[y0:y1, x0:x1] = np.median(verm, axis=0).astype(np.uint8)
    # Recorte: o elétrico inteiro, as duas vias que se separam e o passeio livre à esquerda da via.
    im = Image.fromarray(a).crop((0, 580, 1920, 1440)).resize((1340, 600), Image.LANCZOS)
    g = ImageEnhance.Contrast(ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)).enhance(1.08)
    ImageOps.colorize(g, black=(34, 30, 26), white=(243, 242, 238)).save(DESTINO, 'WEBP', quality=80, method=6)
    return hashlib.sha256(DESTINO.read_bytes()).hexdigest()

if __name__ == '__main__':
    print(tratar(sys.argv[1]))
