#!/usr/bin/env python3
"""
Auto-deploy vers GitHub Pages dès qu'un fichier HTML est modifié.
Lancer : python3 watch-deploy.py
"""
import os, time, subprocess

FOLDER = os.path.dirname(os.path.abspath(__file__))
FILES = [f for f in os.listdir(FOLDER) if f.endswith('.html')]

def get_mtimes():
    mtimes = {}
    for f in FILES:
        path = os.path.join(FOLDER, f)
        if os.path.exists(path):
            mtimes[f] = os.path.getmtime(path)
    return mtimes

def deploy(changed):
    print(f"\n🔄 Changement détecté : {', '.join(changed)}")
    cmds = [
        ["git", "-C", FOLDER, "add"] + [os.path.join(FOLDER, f) for f in changed],
        ["git", "-C", FOLDER, "commit", "-m", f"Update: {', '.join(changed)}"],
        ["git", "-C", FOLDER, "push"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 and "nothing to commit" not in result.stdout:
            print(f"  ⚠️  {result.stderr.strip()}")
        else:
            print(f"  ✅ {' '.join(cmd[2:4])}")
    print("  🌐 Déployé — visible dans ~1 min sur GitHub Pages\n")

print(f"👀 Surveillance de {len(FILES)} fichiers HTML dans :")
print(f"   {FOLDER}\n")
print("Ctrl+C pour arrêter.\n")

prev = get_mtimes()
while True:
    time.sleep(2)
    curr = get_mtimes()
    changed = [f for f in FILES if curr.get(f) != prev.get(f)]
    if changed:
        deploy(changed)
        prev = curr
