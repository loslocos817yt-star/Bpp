import sys, re, os, time, subprocess

def ejecutar_comando(linea, memoria, num_linea=0):
    l_clean = linea.strip()
    if l_clean.startswith('//') or not l_clean or l_clean in ["{", "}"]: return True
    
    COLORES = {
        "ROJO": "\033[91m", "VERDE": "\033[92m", "AZUL": "\033[94m", 
        "AMARILLO": "\033[93m", "CYAN": "\033[96m", "MAGENTA": "\033[95m", 
        "GRIS": "\033[90m", "RESET": "\033[0m"
    }
    
    def error_sintaxis(detalle):
        print(f"\n{COLORES['ROJO']}[ERROR DE SINTAXIS] Línea {num_linea}: {detalle}{COLORES['RESET']}")
        print(f"{COLORES['GRIS']} > {linea.strip()}{COLORES['RESET']}\n")
        return False

    def resolver_mates(expresion):
        expresion = expresion.replace(" ", "")
        try: return str(eval(expresion, {"__builtins__": None}, {}))
        except: return expresion

    try:
        if l_clean == "limpiar": 
            os.system('clear')
        elif l_clean.startswith('esperar'):
            match = re.search(r'\(([\d.]+)\)', l_clean)
            if match: time.sleep(float(match.group(1)))
            else: return error_sintaxis("Falta el tiempo en esperar(). Ej: esperar(1.5)")
        
        elif l_clean.startswith('val '):
            match = re.match(r'val\s+(\w+)\s*=\s*(.*)', l_clean)
            if match:
                var_nombre, valor_raw = match.groups()
                memoria[var_nombre] = valor_raw.replace('"', '') if '"' in valor_raw else resolver_mates(valor_raw)
            else: return error_sintaxis("Uso incorrecto de 'val'. Ej: val x = 10")
        
        elif 'preguntar' in l_clean and '->' in l_clean:
            match = re.search(r'preguntar\s*\(\"(.*)\"\)\s*->\s*(\w+)', l_clean)
            if match:
                texto_p, var_d = match.groups()
                memoria[var_d] = input(f"{texto_p} ")
            else: return error_sintaxis("Uso incorrecto de 'preguntar'.")
        
        elif l_clean.startswith('si '):
            match = re.search(r'si\s+(\w+)\s*==\s*\"(.*)\"\s*->\s*(.*)', l_clean)
            if match:
                var_n, val_c, accion = match.groups()
                if var_n not in memoria: return error_sintaxis(f"Variable '{var_n}' no definida.")
                if memoria.get(var_n) == val_c: return ejecutar_comando(accion, memoria, num_linea)
            else: return error_sintaxis("Uso incorrecto de 'si'.")
        
        elif l_clean.startswith('text'):
            color_inicio = ""
            linea_final = l_clean
            if "->" in l_clean:
                partes = l_clean.split("->")
                linea_final = partes[0].strip()
                color_nombre = partes[1].strip().upper()
                color_inicio = COLORES.get(color_nombre, "")
            
            match = re.search(r'\((.*)\)', linea_final)
            if match:
                cont = match.group(1).strip()
                msg = cont[1:-1] if cont.startswith('"') and cont.endswith('"') else (str(memoria[cont]) if cont in memoria else resolver_mates(cont))
                print(f"{color_inicio}{msg}\033[0m")
            else: return error_sintaxis("Faltan paréntesis en text().")
        else:
            return error_sintaxis("Comando no reconocido.")
    except Exception as e:
        return error_sintaxis(f"Error interno: {str(e)}")
    return True

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

def compilar_proyecto(nombre_archivo):
    lineas = abrir_proyecto(nombre_archivo)
    if not lineas: return
    os.system('clear')
    print(f"--- COMPILAR: {nombre_archivo} ---")
    print("[1] Python (.py) | [2] C++ (.cpp) | [3] BINARIO")
    opc = input("\nSelección: ").strip()
    if opc not in ["1", "2", "3"]: return
    
    ext = ".py" if opc == "1" else ".cpp" if opc == "2" else ".bin"
    ruta_base = os.path.join(CARPETA_PROYECTOS, nombre_archivo.replace(".bpp", ""))
    ruta_final = ruta_base + ext

    try:
        if opc in ["2", "3"]:
            temp_cpp = ruta_base + "_temp.cpp"
            with open(temp_cpp if opc == "3" else ruta_final, "w") as f:
                f.write("#include <iostream>\n#include <string>\n#include <thread>\n#include <chrono>\nusing namespace std;\nint main() {\n")
                for l in lineas:
                    l = l.strip()
                    if l.startswith("val "):
                        m = re.match(r'val\s+(\w+)\s*=\s*(.*)', l)
                        if m: f.write(f'    string {m.group(1)} = {m.group(2)};\n')
                    elif l.startswith("text"):
                        res = re.search(r'\((.*)\)', l.split("->")[0])
                        if res: f.write(f'    cout << {res.group(1)} << endl;\n')
                f.write("    return 0;\n}")
            if opc == "3":
                subprocess.run(["g++", temp_cpp, "-o", ruta_final])
                if os.path.exists(temp_cpp): os.remove(temp_cpp)
        elif opc == "1":
            with open(ruta_final, "w") as f:
                f.write("import time, os\nmemoria = {}\n\n")
                for l in lineas:
                    l = l.strip()
                    if "text" in l:
                        res = re.search(r'\((.*)\)', l.split("->")[0])
                        if res: f.write(f"print({res.group(1)})\n")
        print(f"\n[OK]: Archivo generado en {ruta_final}")
    except Exception as e: print(f"Error: {e}")
    time.sleep(2)

def menu_proyectos():
    while True:
        os.system('clear')
        print("--- B++ PROJECT MANAGER v0.3 ---")
        proyectos = listar_proyectos()
        for i, p in enumerate(proyectos, 1): print(f"[{i}] {p}")
        opcion = input("\n[N] Nuevo | [B] Borrar | [W] Compilar | [X] Salir\n> ").strip().upper()
        if opcion == "N":
            n = input("Nombre: ").strip()
            if n: guardar_proyecto(n if n.endswith(".bpp") else n + ".bpp", [])
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
        print("RUN | SAVE | DEL | EDIT [num] | EXIT")
        print("-" * 35)
        for i, l in enumerate(lineas): print(f"{i+1}: {l}")
        print("-" * 35)
        
        abiertas = sum(1 for l in lineas if "{" in l)
        cerradas = sum(1 for l in lineas if "}" in l)
        sangria = "  " * (abiertas - cerradas)
        
        entrada = input(f"{sangria}> ")
        cmd = entrada.strip().upper()
        
        if cmd == "RUN":
            print("\n--- EJECUTANDO ---")
            mem = {}
            for i, l in enumerate(lineas):
                if not ejecutar_comando(l, mem, i+1): break
            input("\nENTER para volver..."); continue
        elif cmd == "SAVE":
            guardar_proyecto(nombre_proyecto, lineas); continue
        elif cmd == "DEL":
            if lineas: lineas.pop()
        elif cmd.startswith("EDIT "):
            try:
                num = int(cmd.split()[1]) - 1
                if 0 <= num < len(lineas):
                    lineas_previas = lineas[:num]
                    nivel = sum(1 for l in lineas_previas if "{" in l) - sum(1 for l in lineas_previas if "}" in l)
                    nueva_version = input(f"Nuevo texto (L{num+1}): ")
                    lineas[num] = ("  " * nivel) + nueva_version.strip()
            except: pass
        elif cmd == "EXIT":
            guardar_proyecto(nombre_proyecto, lineas); break
        else:
            lineas.append(sangria + entrada.strip())

if __name__ == "__main__": menu_proyectos()
                                 
