"""Apply the LR4 UI kit after committing LR1–3. Keeps a full source backup."""
from pathlib import Path
import argparse, shutil, datetime
p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parents[1]
source=root/'materials/lr4/frontend';target=root/'frontend'
if not a.apply:raise SystemExit('Save a Git commit, then run: python tools/prepare_lr4.py --apply')
backup=root/'.course-backups'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
backup.mkdir(parents=True)
for name in ['src','angular.json','package.json','proxy.conf.json']:
    dest=target/name
    if dest.exists():shutil.move(str(dest),str(backup/name))
    src=source/name
    if src.is_dir():shutil.copytree(src,dest)
    else:shutil.copy2(src,dest)
print('UI kit applied. Backup:',backup)
print('Implement TODO(LR4) and run npm test in frontend. package-lock.json is preserved.')
