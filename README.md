
# 🚀 B++ Language (B Plus Plus)

**B++** es un lenguaje de programación y transpilador minimalista diseñado específicamente para entornos móviles como **Termux** y **Pydroid 3**.

### 🛠️ Creado por:
* **Developer:** insano de cartón_MC
* **Empresa:** PattitexTEC

---

## ⚡ Características
* **Auto-sangría:** Editor integrado que maneja bloques `{ }` automáticamente.
* **Sistema de Colores:** Soporte para textos en ROJO, VERDE, AZUL, y más.
* **Transpilador:** Exporta tus proyectos `.bpp` a código real en `.py` (Python) o `.cpp` (C++).
* **Gestor de Proyectos:** Crea, edita y borra proyectos fácilmente.

## 📝 Ejemplo de código
```text
{
  text ("Iniciando B++...") -> VERDE
  val nombre = "Insano"
  preguntar ("¿Como te llamas?") -> user
  text ("Bienvenido al sistema") -> CYAN
  text (user) -> AMARILLO
}
