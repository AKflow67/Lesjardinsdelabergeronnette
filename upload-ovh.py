"""
Upload du site Les Jardins de la Bergeronnette vers OVH via SFTP
"""
import subprocess
import sys
import os

# Installer paramiko si absent
try:
    import paramiko
except ImportError:
    print("Installation de paramiko (SFTP)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
    import paramiko

SFTP_HOST = "ftp.cluster121.hosting.ovh.net"
SFTP_USER = "jardiib"
SFTP_PASS = "Berger2026ftp"
SFTP_PORT = 22

site_dir = os.path.dirname(os.path.abspath(__file__)) or "."
os.chdir(site_dir)

exclude = {"upload-ovh.py", "UPLOAD-OVH.bat"}
files = [f for f in os.listdir(".") if os.path.isfile(f) and not f.startswith('.') and f not in exclude]

print(f"\n{'='*50}")
print(f"  Upload SFTP vers OVH")
print(f"  jardins-bergeronnette.fr")
print(f"{'='*50}")
print(f"\n{len(files)} fichiers a uploader:")
total_size = 0
for f in sorted(files):
    size_kb = os.path.getsize(f) / 1024
    total_size += size_kb
    print(f"  {f:40s} {size_kb:>8.0f} Ko")
print(f"  {'':40s} {'─'*8}")
print(f"  {'Total':40s} {total_size:>8.0f} Ko")

print(f"\nConnexion SFTP a {SFTP_HOST}:{SFTP_PORT}...")
try:
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)
    print("Connecte !")
except Exception as e:
    print(f"ERREUR connexion SFTP : {e}")
    input("\nAppuie sur Entree pour fermer...")
    sys.exit(1)

# Aller dans www/
remote_dir = "/home/jardiib/www"
try:
    sftp.chdir(remote_dir)
    print(f"Dossier cible : {remote_dir}")
except:
    print(f"Dossier {remote_dir} introuvable, on reste a la racine")
    remote_dir = "."

print(f"\n--- Upload en cours ---\n")
uploaded = 0
errors = []

for i, f in enumerate(sorted(files)):
    size_kb = os.path.getsize(f) / 1024
    print(f"  [{i+1}/{len(files)}] {f} ({size_kb:.0f} Ko)...", end=" ", flush=True)
    try:
        remote_path = f"{remote_dir}/{f}" if remote_dir != "." else f
        sftp.put(f, remote_path)
        print("OK")
        uploaded += 1
    except Exception as e:
        print(f"ERREUR: {e}")
        errors.append(f)

print(f"\n{'='*50}")
print(f"  {uploaded}/{len(files)} fichiers uploades")
if errors:
    print(f"  Erreurs: {', '.join(errors)}")
else:
    print(f"  Tout est passe !")
print(f"{'='*50}")

# Liste finale
try:
    print(f"\nContenu du serveur ({remote_dir}) :")
    for entry in sorted(sftp.listdir(remote_dir)):
        try:
            stat = sftp.stat(f"{remote_dir}/{entry}")
            print(f"  {entry:40s} {stat.st_size/1024:>8.0f} Ko")
        except:
            print(f"  {entry}")
except:
    pass

sftp.close()
transport.close()

print(f"\nTermine ! Verifie : https://jardins-bergeronnette.fr")
print("(Le SSL peut prendre quelques minutes a s'activer)")
input("\nAppuie sur Entree pour fermer...")
