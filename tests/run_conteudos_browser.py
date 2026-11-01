"""01/11/2026: corre toda a bateria de navegador existente, sem parar no primeiro erro."""
import json
import shlex
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
commands=json.loads((ROOT/'tests/conteudos_browser_commands.json').read_text('utf-8'))
results=[]
for command in commands:
    print('\nCOMANDO:',command,flush=True)
    result=subprocess.run(shlex.split(command),cwd=ROOT)
    results.append({'command':command,'exit_code':result.returncode})
(ROOT/'conteudos-browser-ci.json').write_text(json.dumps(results,indent=2)+'\n','utf-8')
raise SystemExit(any(r['exit_code'] for r in results))
