# 🚀 B++ Language (B Plus Plus)

**B++** es un lenguaje de programación y transpilador minimalista diseñado específicamente para entornos móviles como **Termux** y **Pydroid 3**. Creado para quienes no necesitan una PC para construir lógica potente.

### 🛠️ Creado por:
* **Developer:** insano de cartón_MC
* **Empresa:** PattitexTEC

---

## 💎 Características Principales
* **Transpilación Nativa:** Convierte código `.bpp` a **Python** o **C++** ejecutable.
* **Sistema de Memoria:** Gestión de variables con `val` y `preguntar`.
* **Control de Flujo:** Estructuras de bucles (`Repetir`/`FB`) y condicionales (`si`).
* **Ligero:** Arquitectura ultra compacta de 19KB en la 0.7 ¡Sin bloatware!
* **Portabilidad:** Diseñado para funcionar 100% en Android.

---

## 📝 Ejemplo de código
```text
$Name$: Lanzador_Loco
{
  text ("Iniciando B++...") -> VERDE
  Repetir 5:
    aleatoria(1, 10) -> resultado
    text ("Dato generado: ") -> AZUL
    text (resultado)
  FB
}

