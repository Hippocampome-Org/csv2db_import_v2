#!/usr/bin/env python3
"""Prepare an isolated source release. Does not activate Django or access databases."""
import argparse,io,json,subprocess,tarfile
from pathlib import Path,PurePosixPath
REPO=Path(__file__).resolve().parents[1]
ROOT=Path.home()/'hippocampome-prepared-releases'
EXCLUDED=('vendor/','__pycache__/','mysqldump/','mysqldump_Feb11_2025/','iconv/','static/csv2db/dat/')
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--ref',default='HEAD');args=ap.parse_args()
commit=subprocess.check_output(['git','-C',str(REPO),'rev-parse',args.ref+'^{commit}'],text=True).strip()
name=REPO.name+'-'+commit[:12]
if ROOT.resolve()!=ROOT:raise SystemExit('Refusing symlinked release storage')
ROOT.mkdir(mode=0o700,exist_ok=True);out=ROOT/name
if out.exists():raise SystemExit('Release already exists; inspect it instead of overwriting: '+str(out))
archive=subprocess.check_output(['git','-C',str(REPO),'archive',commit]);files=[]
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
 for m in tf:
  p=PurePosixPath(m.name)
  if not m.isfile() or p.is_absolute() or '..' in p.parts or m.name.startswith(EXCLUDED):continue
  if m.name.endswith(('.sql','.sql.gz','.tar.gz','.tgz','.pyc')) or p.name in ['settings.py','settings_staging.py','client_secrets.json'] or p.name.startswith('.env'):continue
  files.append((m.name,tf.extractfile(m).read(),m.mode&0o777))
out.mkdir(mode=0o700)
for rel,data,mode in files:
 p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(mode)
print(json.dumps({'commit':commit,'prepared_release':str(out),'files':len(files),'activated':False,'database_operations':False,'datasets_and_settings':'external; must be reviewed and provided separately'},indent=2))
