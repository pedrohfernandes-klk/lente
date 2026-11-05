"""05/11/2026: pedido do docente (elétrico de lado, alavanca ao lado da via, e as duas vias possíveis para o elétrico).
Recorta o elétrico 541 da fotografia do Commons «Remodelados class tram no. 541 turning street corner in Largo do Corpo
Santo in Lisbon, Portugal (55127582736).jpg» (Philip Mallis, 29 de maio de 2025, CC BY-SA 4.0) para a colagem da Justiça
(tools/gerar_carris.py): publicidade apagada, só o elétrico e a vara do troleio, a preto e branco, com fundo transparente.
Uso: python3 tools/tratar_corpo_santo.py <miniatura de 1920 px descarregada do Commons>
Escreve assets/justica/eletrico-541-recorte.webp. O recorte fica com a mesma licença (CC BY-SA 4.0)."""
import hashlib, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
import numpy as np

MINIATURA_SHA256 = '1a95a1226eb539dc10faec28e36313bbe4d201a12e6e35dae77e4e628f6d5d43'
DESTINO = Path(__file__).resolve().parents[1] / 'assets/justica/eletrico-541-recorte.webp'
# Contorno do elétrico e a vara do troleio, em píxeis da miniatura (origem 840, 300).
OX, OY = 840, 300
CORPO = [(24,628),(24,592),(44,586),(44,340),(50,330),(64,321),(250,303),(252,262),(350,262),(352,290),(382,280),(432,282),
         (440,294),(690,291),(694,288),(790,288),(796,300),(912,316),(934,338),(938,596),(958,604),(958,626),(930,636),
         (905,652),(70,652),(46,640)]
VARA = (((505,270),(322,158),15),((322,158),(552,48),11))
CAIXA = (OX+10, OY+38, OX+972, OY+672)

def tratar(origem):
    assert hashlib.sha256(Path(origem).read_bytes()).hexdigest() == MINIATURA_SHA256, 'miniatura diferente da registada'
    im = Image.open(origem).convert('RGB')
    assert im.size == (1920, 1446), im.size
    a = np.asarray(im).copy()
    # Publicidade apagada: o painel grande da lateral e o painel da porta passam a uma cor lisa (a mediana do vermelho).
    for x0, y0, x1, y1 in ((1094, 812, 1694, 916), (889, 792, 958, 880)):
        reg = a[y0:y1, x0:x1].reshape(-1, 3)
        verm = reg[(reg[:, 0] > 120) & (reg[:, 1] < 80) & (reg[:, 2] < 80)]
        a[y0:y1, x0:x1] = np.median(verm, axis=0).astype(np.uint8)
    im = Image.fromarray(a)
    mascara = Image.new('L', im.size, 0)
    d = ImageDraw.Draw(mascara)
    d.polygon([(x + OX, y + OY) for x, y in CORPO], fill=255)
    for (x0, y0), (x1, y1), w in VARA:
        d.line([(x0 + OX, y0 + OY), (x1 + OX, y1 + OY)], fill=255, width=w)
    mascara = mascara.filter(ImageFilter.GaussianBlur(1.2))
    g = ImageEnhance.Contrast(ImageOps.autocontrast(ImageOps.grayscale(im.crop(CAIXA)), cutoff=1)).enhance(1.08)
    t = ImageOps.colorize(g, black=(34, 30, 26), white=(243, 242, 238)).convert('RGBA')
    t.putalpha(mascara.crop(CAIXA))
    t.save(DESTINO, 'WEBP', quality=82, method=6)
    return hashlib.sha256(DESTINO.read_bytes()).hexdigest()

if __name__ == '__main__':
    print(tratar(sys.argv[1]))
