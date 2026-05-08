import os, subprocess

def check_deps():
    for dep in ["python", "clang", "git"]:
        if not subprocess.run(["which", dep], capture_output=True, text=True).stdout:
            print(f"Instalando {dep}...")
            subprocess.run(["pkg", "install", dep, "-y"])

try:
    import requests
except ImportError:
    check_deps()
    subprocess.run(["pip", "install", "requests"])
    import requests

def main():
    os.system('clear')
    print("--- B++ ALL-SCAN INSTALLER (PattitexTEC) ---")
    check_deps()
    url = "https://api.github.com/repos/loslocos817yt-star/B-/contents/"
    headers = {'User-Agent': 'PattitexTEC-Agent'}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            ignorar = ["README.md", ".gitignore", "BppInstaler.py", "BppInstaller.py"]
            archivos = [f['name'] for f in r.json() if f['name'] not in ignorar and not f['name'].startswith('.')]
            if not archivos:
                print("[!] No hay archivos.")
                return
            for i, name in enumerate(archivos, 1):
                print(f"[{i}] {name}")
            sel = input("\nNombre del archivo: ").strip()
            if sel in archivos:
                raw_url = f"https://raw.githubusercontent.com/loslocos817yt-star/B-/main/{sel}"
                res = requests.get(raw_url)
                with open(sel, "w", encoding="utf-8") as f:
                    f.write(res.text)
                os.system(f'chmod +x "{sel}"')
                print(f"\n[OK] '{sel}' instalado. Ejecútalo con: python \"{sel}\"")
            else:
                print("[!] No existe.")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__": main()
