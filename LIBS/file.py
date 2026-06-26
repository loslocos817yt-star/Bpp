# file.py - Librería FILE para B++
# Compatible con sistema GH de B++

import os

def leer_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERROR leyendo archivo: {e}"

def borrar_archivo(ruta):
    try:
        if os.path.exists(ruta):
            os.remove(ruta)
            return "Archivo borrado correctamente"
        return "El archivo no existe"
    except Exception as e:
        return f"ERROR borrando archivo: {e}"

def escribir_archivo(ruta, contenido):
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        return "Archivo escrito correctamente"
    except Exception as e:
        return f"ERROR escribiendo archivo: {e}"

def existe_archivo(ruta):
    return os.path.exists(ruta)


# 🔥 puente para B++
class file:
    @staticmethod
    def Leer_archivo(ruta):
        return leer_archivo(ruta)

    @staticmethod
    def Borrar_archivo(ruta):
        return borrar_archivo(ruta)

    @staticmethod
    def Escribir_archivo(ruta, contenido):
        return escribir_archivo(ruta, contenido)

    @staticmethod
    def Existe_archivo(ruta):
        return existe_archivo(ruta)
