# Titkosított munkacsomag: python3 vault.py pack|unpack <könyvtár> <fájl>   (kulcs: VAULT_KEY környezeti változó, base64)
import sys, os, io, tarfile, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
mode, d, f = sys.argv[1:4]; key = base64.b64decode(os.environ['VAULT_KEY'])
if mode == 'pack':
    bio = io.BytesIO()
    with tarfile.open(fileobj=bio, mode='w:gz') as t:
        for n in sorted(os.listdir(d)):
            if n in ('lines.txt','load.py','ingest.py','check.py','agg2.py','render2.js','extra2.css','build2.py','build_art2.py','plan.py','monthsum.py','run.sh','NOTES.md'):
                t.add(os.path.join(d, n), arcname=n)
    iv = os.urandom(12); open(f, 'wb').write(iv + AESGCM(key).encrypt(iv, bio.getvalue(), None)); print('packed', f)
else:
    b = open(f, 'rb').read(); data = AESGCM(key).decrypt(b[:12], b[12:], None)
    os.makedirs(d, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as t: t.extractall(d, filter='data')
    print('unpacked to', d)
