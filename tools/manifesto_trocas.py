"""05/11/2026: decisão 147. Gera trocas literais [antigo, novo, 1] que levam a versão de BASE de cada ficheiro à versão
do disco, para os testes que comparam com bases antigas aceitarem só estas mudanças, com contagem exata.
Uso: python3 tools/manifesto_trocas.py BASE ficheiro... > tests/fixtures/<manifesto>.json (na raiz do repositório)."""
import difflib,json,re,subprocess,sys
base=sys.argv[1];out={}
TOK=re.compile(r'<[^>]*>|[^<\s]+|\s+')
def trocas(A,B):
    a=TOK.findall(A);b=TOK.findall(B);assert ''.join(a)==A and ''.join(b)==B
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    ops=[o for o in sm.get_opcodes() if o[0]!='equal']
    grupos=[]
    for o in ops:
        if grupos and o[1]-grupos[-1][2]<=12:grupos[-1]=[grupos[-1][0],grupos[-1][1],o[2],grupos[-1][3],o[4]]
        else:grupos.append(['x',o[1],o[2],o[3],o[4]])
    res=[]
    for _,i1,i2,j1,j2 in grupos:
        k=0
        while True:
            lo,hi=max(0,i1-k),min(len(a),i2+k);ant=''.join(a[lo:hi])
            if ant and A.count(ant)==1:break
            k+=1
        res.append([ant,''.join(a[lo:i1])+''.join(b[j1:j2])+''.join(a[i2:hi]),1])
    t=A
    for x,y,n in res:
        assert t.count(x)==1,(x[:80]);t=t.replace(x,y)
    assert t==B
    return res
for f in sys.argv[2:]:
    A=subprocess.check_output(['git','show',base+':'+f]).decode('utf-8');B=open(f,encoding='utf-8').read()
    if A!=B:out[f]=trocas(A,B)
json.dump(out,sys.stdout,ensure_ascii=False,indent=1);print()
