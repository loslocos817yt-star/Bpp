import sys, re, os, time

def ejecutar_comando(linea, memoria):
    l_clean = linea.strip()
    if l_clean.startswith('//') or not l_clean or l_clean in ["{", "}"]: return
    COLORES = {"ROJO": "\033[91m", "VERDE": "\033[92m", "AZUL": "\033[94m", "AMARILLO": "\033[93m", "CYAN": "\033[96m", "MAGENTA": "\033[95m", "GRIS": "\033[90m", "RESET": "\033[0m"}
    def resolver_mates(expresion):
        expresion = expresion.replace(" ", "")
        try: return str(eval(expresion, {"__builtins__": None}, {}))
        except: return expresion
    if l_clean == "limpiar": os.system('clear')
    elif l_clean.startswith('esperar'):
        match = re.search(r'\(([\d.]+)\)', l_clean)
        if match: time.sleep(float(match.group(1)))
    elif l_clean.startswith('val '):
        match = re.match(r'val\s+(\w+)\s*=\s*(.*)', l_clean)
        if match:
            var_nombre, valor_raw = match.groups()
            memoria[var_nombre] = valor_raw.replace('"', '') if '"' in valor_raw else resolver_mates(valor_raw)
    elif 'preguntar' in l_clean and '->' in l_clean:
        match = re.search(r'preguntar\s*\(\"(.*)\"\)\s*->\s*(\w+)', l_clean)
        if match:
            texto_p, var_d = match.groups()
            memoria[var_d] = input(f"{texto_p} ")
    elif l_clean.startswith('si '):
        match = re.search(r'si\s+(\w+)\s*==\s*\"(.*)\"\s*->\s*(.*)', l_clean)
        if match:
            var_n, val_c, accion = match.groups()
            if memoria.get(var_n) == val_c: ejecutar_comando(accion, memoria)
    elif l_clean.startswith('text'):
        color_inicio = ""
        linea_final = l_clean
        if "->" in l_clean:
            partes = l_clean.split("->")
            linea_final = partes[0].strip()
            color_inicio = COLORES.get(partes[1].strip().upper(), "")
        match = re.search(r'\((.*)\)', linea_final)
        if match:
            cont = match.group(1).strip()
            msg = cont[1:-1] if cont.startswith('"') and cont.endswith('"') else (str(memoria[cont]) if cont in memoria else resolver_mates(cont))
            print(f"{color_inicio}{msg}\033[0m")

def compilar_proyecto(nombre_archivo):
    lineas = abrir_proyecto(nombre_archivo)
    if not lineas: return
    os.system('clear')
    print(f"--- EXPORTAR: {nombre_archivo} ---")
    print("[1] Python (.py) | [2] C++ (.cpp)")
    opc = input("\nFormato: ").strip()
    if opc not in ["1", "2"]: return
    ext = ".py" if opc == "1" else ".cpp"
    ruta_input = input("\nRuta (> para BppProjects/): ").strip()
    ruta_final = (ruta_input if ruta_input.endswith(ext) else ruta_input + ext) if ruta_input else os.path.join(CARPETA_PROYECTOS, nombre_archivo.replace(".bpp", ext))
    try:
        with open(ruta_final, "w", encoding="utf-8") as f:
            if opc == "1":
                f.write("import time, os\nmemoria = {}\n\n")
                for l in lineas:
                    l = l.strip()
                    if "text" in l:
                        res = re.search(r'\((.*)\)', l.split("->")[0])
                        if res: f.write(f"print({res.group(1)})\n")
                    elif "esperar" in l:
                        res = re.search(r'\((.*)\)', l)
                        if res: f.write(f"time.sleep({res.group(1)})\n")
            else:
                f.write("#include <iostream>\nusing namespace std;\nint main() { cout << \"B++ Build\" << endl; return 0; }")
        print(f"\n[OK]: {ruta_final}")
    except Exception as e: print(f"\n[!]: {e}")
    time.sleep(2)

CARPETA_PROYECTOS = "BppProjects"
if not os.path.exists(CARPETA_PROYECTOS): os.makedirs(CARPETA_PROYECTOS)

def listar_proyectos(): return [f for f in os.listdir(CARPETA_PROYECTOS) if f.endswith(".bpp")]

def abrir_proyecto(n):
    ruta = os.path.join(CARPETA_PROYECTOS, n)
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f: return [line.rstrip("\n") for line in f.readlines()]
    return []

def guardar_proyecto(n, l):
    with open(os.path.join(CARPETA_PROYECTOS, n), "w", encoding="utf-8") as f: f.write("\n".join(l))

def menu_proyectos():
    while True:
        os.system('clear')
        print("--- B++ PROJECT MANAGER ---")
        proyectos = listar_proyectos()
        for i, p in enumerate(proyectos, 1): print(f"[{i}] {p}")
        opcion = input("\n[N] Nuevo | [B] Borrar | [W] Exportar | [X] Salir\n> ").strip().upper()
        if opcion == "N":
            n = input("Nombre: ").strip()
            if n: guardar_proyecto(n + ".bpp" if not n.endswith(".bpp") else n, [])
        elif opcion == "B":
            idx = input("ID: ")
            if idx.isdigit() and 0 < int(idx) <= len(proyectos): os.remove(os.path.join(CARPETA_PROYECTOS, proyectos[int(idx)-1]))
        elif opcion == "W":
            idx = input("ID: ")
            if idx.isdigit() and 0 < int(idx) <= len(proyectos): compilar_proyecto(proyectos[int(idx)-1])
        elif opcion == "X": break
        elif opcion.isdigit():
            idx = int(opcion) - 1
            if 0 <= idx < len(proyectos): editor_bpp(proyectos[idx])

def editor_bpp(nombre_proyecto):
    lineas = abrir_proyecto(nombre_proyecto)
    while True:
        os.system('clear')
        print(f"--- EDITANDO: {nombre_proyecto} ---")
        print("RUN | SAVE | DEL | EXIT")
        print("-" * 30)
        for i, l in enumerate(lineas): print(f"{i+1}: {l}")
        print("-" * 30)
        abiertas = sum(1 for l in lineas if "{" in l)
        cerradas = sum(1 for l in lineas if "}" in l)
        sangria = "  " * (abiertas - cerradas)
        entrada = input(f"{sangria}> ")
        cmd = entrada.strip().upper()
        if cmd == "RUN":
            print("\n--- RUN ---"); mem = {}
            for l in lineas: ejecutar_comando(l, mem)
            input("\nENTER..."); continue
        elif cmd == "SAVE": guardar_proyecto(nombre_proyecto, lineas); time.sleep(0.5); continue
        elif cmd == "DEL":
            if lineas: lineas.pop()
        elif cmd == "EXIT": guardar_proyecto(nombre_proyecto, lineas); break
        else: lineas.append(sangria + entrada.strip())

if __name__ == "__main__": menu_proyectos()
