import urllib.request
import sys, re, os, time, subprocess

CARPETA_PROYECTOS = "BppProjects"
CARPETA_LIBS = os.path.join(CARPETA_PROYECTOS, "LIBS")
if not os.path.exists(CARPETA_LIBS): os.makedirs(CARPETA_LIBS)

def gestor_librerias():
    os.system("clear" if sys.platform != "win32" else "cls")
    print("\033[95m--- B++ LIBRARY INSTALLER ---\033[0m")
    url = "https://raw.githubusercontent.com/loslocos817yt-star/Bpp/main/LIBS/mate.py"
    print("Descargando mate.py...")
    try:
        with urllib.request.urlopen(url) as response, open(os.path.join(CARPETA_LIBS, "mate.py"), "wb") as out_file:
            out_file.write(response.read())
        print("\033[92m¡mate.py instalado con éxito!\033[0m")
    except Exception as e: print(f"Error: {e}")
    time.sleep(2)

def sonar_nativo(frecuencia, duracion):
    try:
        if sys.platform == "win32":
            import winsound
            winsound.Beep(int(frecuencia), int(duracion * 1000))
        else:
            # Método PattitexTEC para sistemas basados en Unix/Android
            for _ in range(int(duracion * 5)):
                sys.stdout.write('\a')
                sys.stdout.flush()
                time.sleep(0.1)
    except Exception:
        pass

def ejecutar_comando(linea, memoria, num_linea=0):
    l_clean = linea.strip()
    if l_clean.startswith('//') or not l_clean or l_clean in ["{", "}"] or l_clean.startswith("$Name$"): return True
    
    COLORES = {
        "ROJO": "\033[91m", "VERDE": "\033[92m", "AZUL": "\033[94m", 
        "AMARILLO": "\033[93m", "CYAN": "\033[96m", "MAGENTA": "\033[95m", 
        "GRIS": "\033[90m", "RESET": "\033[0m", "FONDO_R": "\033[41m"
    }
    
    def error_fatal(tipo, detalle):
        print(f"\n{COLORES['FONDO_R']}{COLORES['RESET']} {COLORES['ROJO']}B++ SYSTEM ERROR{COLORES['RESET']}")
        print(f"{COLORES['MAGENTA']}TIPO: {tipo}{COLORES['RESET']}")
        print(f"{COLORES['AMARILLO']}LÍNEA: {num_linea}{COLORES['RESET']}")
        print(f"{COLORES['GRIS']}DETALLE: {detalle}{COLORES['RESET']}")
        print(f"{COLORES['GRIS']}ENTRADA > {linea.strip()}{COLORES['RESET']}")
        # Puntero de error dinámico
        espacios = linea.find(detalle.split()[0]) if detalle.split() else 0
        print(f"{COLORES['ROJO']}{' ' * (espacios + 10)}^--- ERROR AQUÍ{COLORES['RESET']}\n")
        return False

    def resolver_mates_pro(expresion):
        # Limpieza profunda de expresiones para el motor B++
        expresion = expresion.replace(" ", "")
        try:
            # Solo permitimos matemáticas básicas por seguridad
            if any(c in expresion for c in "abcdefghijklmnopqrstuvwxyz"):
                for var in memoria:
                    if var in expresion:
                        expresion = expresion.replace(var, str(memoria[var]))
            return str(eval(expresion, {"__builtins__": None}, {}))
        except Exception:
            return expresion

    try:
        if l_clean == "limpiar": 
            os.system('clear' if sys.platform != 'win32' else 'cls')
            
        elif l_clean.startswith('pitido'):
            match = re.search(r'pitido\(([\d.]+)\)\s*->\s*([\d.]+)', l_clean)
            if match:
                f, s = match.groups()
                if float(f) < 37 or float(f) > 32767:
                    return error_fatal("RANGO", "Frecuencia debe estar entre 37 y 32767Hz")
                sonar_nativo(float(f), float(s))
            else: return error_fatal("SINTAXIS", "Uso: pitido(frecuencia) -> segundos")

        elif l_clean.startswith('esperar'):
            match = re.search(r'\(([\d.]+)\)', l_clean)
            if match: time.sleep(float(match.group(1)))
            else: return error_fatal("SINTAXIS", "Falta el tiempo en esperar().")
        
        elif l_clean.startswith("mate("):
            match = re.search(r"mate\((.*)\)\s*->\s*(\w+)", l_clean)
            if match:
                exp, var_dest = match.groups()
                try:
                    if CARPETA_LIBS not in sys.path: sys.path.append(CARPETA_LIBS)
                    import mate
                    memoria[var_dest] = mate.procesar(exp)
                    return True
                except ImportError: return error_fatal("LIB", "Librería mate no encontrada. Usa [L]")
        elif l_clean.startswith('val '):
            match = re.match(r'val\s+(\w+)\s*=\s*(.*)', l_clean)
            if match:
                var_nombre, valor_raw = match.groups()
                if '"' in valor_raw:
                    memoria[var_nombre] = valor_raw.replace('"', '')
                else:
                    memoria[var_nombre] = resolver_mates_pro(valor_raw)
            else: return error_fatal("DECLARACIÓN", "Uso incorrecto de 'val'. Ej: val x = 10")
        
        elif 'preguntar' in l_clean and '->' in l_clean:
            match = re.search(r'preguntar\s*\(\"(.*)\"\)\s*->\s*(\w+)', l_clean)
            if match:
                texto_p, var_d = match.groups()
                memoria[var_d] = input(f"{COLORES['CYAN']}{texto_p}{COLORES['RESET']} ")
            else: return error_fatal("ENTRADA", "Falta el destino '-> variable'.")
        
        elif l_clean.startswith('si '):
            match = re.search(r'si\s+(\w+)\s*==\s*\"(.*)\"\s*->\s*(.*)', l_clean)
            if match:
                var_n, val_c, accion = match.groups()
                if var_n not in memoria: return error_fatal("VARIABLE", f"'{var_n}' no definida.")
                if str(memoria.get(var_n)) == val_c: 
                    return ejecutar_comando(accion, memoria, num_linea)
            else: return error_fatal("LÓGICA", "Error en estructura 'si'. Verifique flecha '->'")
        
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
                if cont.startswith('"') and cont.endswith('"'):
                    msg = cont[1:-1]
                elif cont in memoria:
                    msg = str(memoria[cont])
                else:
                    msg = resolver_mates_pro(cont)
                print(f"{color_inicio}{msg}{COLORES['RESET']}")
            else: return error_fatal("SINTAXIS", "Faltan paréntesis en text().")
        else:
            return error_fatal("COMANDO", f"No se reconoce '{l_clean.split()[0]}'")
    except Exception as e:
        return error_fatal("SISTEMA", str(e))
    return True

CARPETA_PROYECTOS = "BppProjects"
if not os.path.exists(CARPETA_PROYECTOS): os.makedirs(CARPETA_PROYECTOS)

def listar_proyectos():
    return [f for f in os.listdir(CARPETA_PROYECTOS) if f.endswith(".bpp")]

def abrir_proyecto(n):
    ruta = os.path.join(CARPETA_PROYECTOS, n)
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f.readlines()]
    return []

def guardar_proyecto(n, l):
    with open(os.path.join(CARPETA_PROYECTOS, n), "w", encoding="utf-8") as f:
        f.write("\n".join(l))

def compilar_proyecto(nombre_archivo):
    lineas = abrir_proyecto(nombre_archivo)
    if not lineas: return
    os.system('clear' if sys.platform != 'win32' else 'cls')
    print(f"\033[94m--- B++ COMPILER CORE v0.6 ---\033[0m")
    print(f"PROYECTO: {nombre_archivo}")
    print("\n[1] Python (.py)\n[2] C++ Nativo (.cpp)\n[3] Binario Ejecutable\n[X] Cancelar")
    opc = input("\nSelección: ").strip().upper()
    
    if opc == "X": return
    
    ext = ".py" if opc == "1" else ".cpp" if opc == "2" else ".bin"
    ruta_final = os.path.join(CARPETA_PROYECTOS, nombre_archivo.replace(".bpp", "")) + ext

    try:
        print(f"\033[93mCompilando...\033[0m")
        if opc in ["2", "3"]:
            temp_cpp = ruta_final.replace(".bin", ".cpp") if opc == "3" else ruta_final
            with open(temp_cpp, "w") as f:
                f.write("#include <iostream>\n#include <string>\n#include <thread>\n#include <chrono>\n")
                f.write("using namespace std;\n\nvoid sonar(int f, float d) { /* Logic */ }\n\n")
                f.write("int main() {\n    // Generado por B++ Core v0.6\n")
                for l in lineas:
                    l = l.strip()
                    if l.startswith("val "):
                        m = re.match(r'val\s+(\w+)\s*=\s*(.*)', l)
                        if m: f.write(f'    string {m.group(1)} = {m.group(2)};\n')
                    elif l.startswith("text"):
                        res = re.search(r'\((.*)\)', l.split("->")[0])
                        if res: f.write(f'    cout << {res.group(1)} << endl;\n')
                    elif l.startswith("limpiar"): f.write('    system("clear");\n')
                f.write("    return 0;\n}")
            
            if opc == "3":
                subprocess.run(["g++", temp_cpp, "-o", ruta_final])
                if os.path.exists(temp_cpp): os.remove(temp_cpp)
                
        elif opc == "1":
            with open(ruta_final, "w") as f:
                f.write("import time, os, sys\n\n# B++ SDK v0.6 Generated Code\n")
                f.write("memoria = {}\n\ndef sonar(f, d):\n    if sys.platform == 'win32':\n        import winsound\n        winsound.Beep(int(f), int(d*1000))\n\n")
                for l in lineas:
                    l = l.strip()
                    if "text" in l:
                        res = re.search(r'\((.*)\)', l.split("->")[0])
                        if res: f.write(f"print({res.group(1)})\n")
                    elif "val " in l:
                        m = re.match(r'val\s+(\w+)\s*=\s*(.*)', l)
                        if m: f.write(f"memoria['{m.group(1)}'] = {m.group(2)}\n")

        print(f"\n\033[92m[ÉXITO]:\033[0m {ruta_final}")
    except Exception as e:
        print(f"\033[91m[ERROR]:\033[0m {e}")
    time.sleep(2)

def menu_proyectos():
    while True:
        os.system('clear' if sys.platform != 'win32' else 'cls')
        print(f"\033[91m==============================\033[0m")
        print(f"   B++ PROJECT MANAGER v0.6")
        print(f"   Dev: Insano de Cartón_MC")
        print(f"\033[91m==============================\033[0m")
        proyectos = listar_proyectos()
        if not proyectos:
            print(f"\033[90m   (Sin proyectos guardados)\033[0m")
        else:
            for i, p in enumerate(proyectos, 1):
                print(f"  [{i}] {p}")
        
        print(f"\n[N] Nuevo | [B] Borrar | [L] Libs | [W] Compilar | [X] Salir")
        opcion = input("\nB++ > ").strip().upper()
        
        if opcion == "L": gestor_librerias()
        if opcion == "N":
            n = input("Nombre del proyecto: ").strip()
            if n:
                nombre = n if n.endswith(".bpp") else n + ".bpp"
                guardar_proyecto(nombre, ["// Nuevo Proyecto B++", "{", "", "}"])
        elif opcion == "B":
            idx = input("ID del proyecto a borrar: ")
            if idx.isdigit() and 0 < int(idx) <= len(proyectos):
                confirmar = input(f"¿Borrar {proyectos[int(idx)-1]}? (S/N): ").upper()
                if confirmar == "S":
                    os.remove(os.path.join(CARPETA_PROYECTOS, proyectos[int(idx)-1]))
        elif opcion == "W":
            idx = input("ID del proyecto a compilar: ")
            if idx.isdigit() and 0 < int(idx) <= len(proyectos):
                compilar_proyecto(proyectos[int(idx)-1])
        elif opcion == "X":
            print("Cerrando B++..."); break
        elif opcion.isdigit():
            idx = int(opcion) - 1
            if 0 <= idx < len(proyectos):
                editor_bpp(proyectos[idx])

def editor_bpp(nombre_proyecto):
    lineas = abrir_proyecto(nombre_proyecto)
    while True:
        os.system('clear' if sys.platform != 'win32' else 'cls')
        print(f"\033[96mEditor B++\033[0m | Archivo: {nombre_proyecto}")
        print(f"\033[90mRUN | SAVE | DEL | EDIT [n] | EXIT\033[0m")
        print("-" * 45)
        for i, l in enumerate(lineas):
            print(f"\033[90m{i+1:02d} |\033[0m {l}")
        print("-" * 45)
        
        abiertas = sum(1 for l in lineas if "{" in l)
        cerradas = sum(1 for l in lineas if "}" in l)
        sangria = "  " * max(0, abiertas - cerradas)
        
        entrada = input(f"\033[92m{sangria}>>\033[0m ")
        cmd = entrada.strip().upper()
        
        if cmd == "RUN":
            print(f"\n\033[93m--- EJECUTANDO B++ CORE ---\033[0m")
            
            nombre_programa = "B++"
            for linea in lineas:
                if linea.strip().startswith("$Name$"):
                    partes = linea.split(":", 1)
                    if len(partes) > 1:
                        nombre_programa = partes[1].strip()
                    else:
                        nombre_programa = linea.replace("$Name$", "").strip()
                    break

            print(f"\n=== {nombre_programa} ===\n")
            
            mem = {}
            inicio_t = time.time()
            for i, l in enumerate(lineas):
                if not ejecutar_comando(l, mem, i+1): break
            fin_t = time.time()
            print(f"\n\033[90mProceso finalizado en {fin_t - inicio_t:.4f}s\033[0m")
            input("Presione ENTER para volver..."); continue
        elif cmd == "SAVE":
            guardar_proyecto(nombre_proyecto, lineas)
            print("¡Guardado!"); time.sleep(0.5)
        elif cmd == "DEL":
            if lineas: lineas.pop()
        elif cmd.startswith("EDIT "):
            try:
                num = int(cmd.split()[1]) - 1
                if 0 <= num < len(lineas):
                    lineas_previas = lineas[:num]; nivel = sum(1 for l in lineas_previas if "{" in l) - sum(1 for l in lineas_previas if "}" in l); lineas[num] = ("  " * nivel) + input(f"Nueva línea {num+1}: ").strip()
            except: pass
        elif cmd == "EXIT":
            guardar_proyecto(nombre_proyecto, lineas); break
        else:
            lineas.append(sangria + entrada.strip())

if __name__ == "__main__":
    try:
        menu_proyectos()
    except KeyboardInterrupt:
        print("\nB++ interrumpido.")
