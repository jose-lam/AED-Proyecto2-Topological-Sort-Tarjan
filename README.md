# Topological Sort (Tarjan) — Visualización Matemática con C++ y Manim

Proyecto final del curso **CS2023 Algoritmos y Estructuras de Datos** (Universidad de Ingeniería y Tecnología — UTEC). Implementa el algoritmo de **Ordenamiento Topológico de Tarjan** basado en búsqueda en profundidad (DFS), control de tres estados y tiempos de finalización (`tout`), acoplado a un motor de animación matemática en **Manim Community**.

---

## Descripción del Algoritmo

Dado un Grafo Dirigido Acíclico (DAG) $G = (V, E)$, un **ordenamiento topológico** es una permutación lineal de sus vértices tal que, para cada arista dirigida $(u, v) \in E$, el vértice $u$ precede a $v$.

La formulación de **Tarjan** extiende el recorrido DFS clásico mediante:
1. **Control de 3 estados por vértice:**
   - `0` (*No visitado*): El vértice aún no ha sido descubierto.
   - `1` (*En proceso*): El vértice está activo en la pila de recursión actual (permite detectar ciclos dirigidos en $\mathcal{O}(1)$ si se encuentra una arista hacia un nodo en estado `1`).
   - `2` (*Terminado*): Todos los descendientes del vértice han sido explorados completamente.
2. **Tiempos de descubrimiento (`tin`) y finalización (`tout`):**
   - Cada vez que un vértice transiciona a estado `2`, recibe su marca temporal `tout` y se inserta en una pila. Al invertir dicha pila al finalizar el DFS, los vértices quedan ordenados de mayor a menor `tout`, garantizando que $tout[u] > tout[v]$ para toda arista $(u, v) \in E$.

---

## Arquitectura y Estructura del Repositorio

El flujo de trabajo sigue una arquitectura **orientada a datos (*data-driven*)**: el programa en C++ ejecuta el algoritmo real y exporta cada evento en `traza.json`, el cual es consumido directamente por Python/Manim para renderizar la animación sin simular ni recalcular el grafo.

```text
topological-sort-tarjan/
├── main.cpp        # Implementación en C++17 (DFS 3 estados, tin/tout y exportador JSON)
├── traza.json      # Traza de ejecución generada automáticamente por main.cpp
├── scene.py        # Escena de animación en Manim Community (consumidor de traza.json)
└── README.md       # Documentación y guía de reproducción
```

---

## Requisitos de Software

Para compilar el código fuente y renderizar el video en alta definición se requiere:

- **Compilador C++:** `g++` con soporte para estándar **C++17** o superior (GCC 9+ / Clang 10+).
- **Python:** Versión **3.10** o superior.
- **Manim Community Edition:** `manim` (`v0.18.0` o superior).
- **FFmpeg:** Necesario para la codificación de video `.mp4` a 60 FPS.
- **Distribución LaTeX:** TeX Live / MiKTeX (para renderizar ecuaciones `MathTex` en Manim y compilar `informe.tex`).

Instalación rápida de dependencias en Python:
```bash
pip install manim
```

---

## Instrucciones de Compilación y Reproducción Paso a Paso

### Paso 1: Compilar el código en C++
```bash
g++ -std=c++17 -O2 -Wall main.cpp -o tarjan_toposort
```

### Paso 2: Ejecutar el programa y generar `traza.json`
```bash
./tarjan_toposort
```
Este comando imprimirá en consola el orden topológico del DAG de 6 cursos, reportará la detección de ciclo en el caso borde y generará el archivo `traza.json` en el directorio raíz.

### Paso 3: Renderizar la animación en Manim (`1080p60`)
```bash
manim -qh --fps 60 scene.py TopologicalSortTarjan
```

El archivo final `.mp4` estará disponible en:
```text
media/videos/scene/1080p60/TopologicalSortTarjan.mp4
```

---

## Equipo de Desarrollo

- **José Enrique Hilario Ruiz Lam**
- **Francesco Aroldo Ferrante Quino**
- **Osmar Armengol Vilchez Aguirre**
