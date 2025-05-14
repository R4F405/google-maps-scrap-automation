# Google Maps Scraper

Scripts para automatizar la recolección de datos de Google Maps mediante una API de scraping.

## Guía rápida (para empezar rápidamente)

Estos scripts te permiten extraer datos de Google Maps de forma automática. Para utilizarlos, necesitas:

1. Tener Python instalado (versión 3.6 o superior)
2. Instalar las dependencias con: `pip install requests tkinter`
3. Tener la API de scraping funcionando en tu equipo local u otro servidor

### Modo más fácil (Launcher Gráfico):

```bash
python scraper_launcher.py
```

**Este launcher te permite elegir entre las diferentes opciones disponibles:**
- Scraper Simple
- Batch Scraper
- Interfaz Gráfica (GUI)

### Uso rápido del script básico:

```bash
python scraper.py
```

**Este script te guiará paso a paso:**
1. Te pedirá un nombre para el trabajo
2. Elegirás una categoría de las disponibles (ejemplo: "abogado", "dentista", etc.)
3. Seleccionarás una palabra clave específica (ejemplo: "Abogado especializado en familia")
4. Elegirás una localidad (Gandia, Oliva, etc.)
5. Confirmarás el envío con "s"

### Uso rápido del script avanzado:

```bash
python scraper_advanced.py
```

**Ejemplo de uso:**
1. Introduce la dirección del servidor (por defecto http://localhost:8000)
2. Ingresa un nombre como "Busqueda-Abogados-Gandia"
3. Selecciona una categoría (por ejemplo: 1 para abogados)
4. Para seleccionar varios keywords, escribe "1,3,5" o "all" para todos
5. Selecciona una localidad (por ejemplo: 1 para Gandia)
6. Personaliza radio (10000), profundidad (10) y tiempo máximo (15) o deja valores por defecto
7. Confirma con "s" y luego selecciona "s" para monitorizar el estado

### Uso rápido del script por lotes:

```bash
# Para ejecutar un trabajo en todas las categorías y localizaciones:
python batch_scraper.py

# Para ejecutar solo en categorías específicas (por ejemplo, abogados y dentistas) en una localización específica:
python batch_scraper.py --categories "1,5" --locations "1"

# Para probar sin enviar solicitudes reales:
python batch_scraper.py --dry-run
```

### Uso de la Interfaz Gráfica (GUI):

```bash
python scraper_gui.py
```

**Características de la interfaz gráfica:**
1. Interfaz con pestañas para configurar todos los parámetros
2. Selección visual de categorías y localizaciones mediante checkboxes
3. Vista previa de palabras clave disponibles
4. Información detallada de las localizaciones seleccionadas
5. Resumen del trabajo antes de ejecutarlo
6. Panel de logs para seguir el progreso
7. Posibilidad de cancelar trabajos en ejecución

**Los resultados** se guardarán automáticamente en la carpeta "results".

---

## Estructura del proyecto

- `keywords/`: Directorio con archivos de palabras clave organizados por categoría.
- `location/`: Directorio con archivos de coordenadas para diferentes localidades.
- `results/`: Directorio donde se guardarán los resultados de los trabajos.
- `scraper_launcher.py`: Launcher gráfico para seleccionar el modo de scraping.
- `scraper_gui.py`: Interfaz gráfica completa para configurar y ejecutar trabajos.

## Scripts disponibles

### 1. scraper_launcher.py

Launcher gráfico que permite seleccionar entre los diferentes modos de scraping disponibles.

#### Uso:

```bash
python scraper_launcher.py
```

El launcher te permite elegir entre:
- Scraper Simple: Ejecuta el script básico interactivo
- Batch Scraper: Ejecuta el script para procesamiento por lotes
- Interfaz Gráfica (GUI): Abre la interfaz gráfica completa

### 2. scraper_gui.py

Interfaz gráfica completa para configurar y ejecutar trabajos de scraping con todas las opciones.

#### Uso:

```bash
python scraper_gui.py
```

Características:
- Interfaz de pestañas para una organización clara
- Pestaña de Configuración: Host API, nombre del trabajo, radio, profundidad, tiempos
- Pestaña de Categorías: Selección múltiple de categorías con vista previa de keywords
- Pestaña de Localizaciones: Selección múltiple de localizaciones con información detallada
- Pestaña de Ejecución: Resumen del trabajo, panel de logs, controles de ejecución
- Gestión automatizada de resultados

### 3. scraper.py

Script básico para realizar un solo trabajo de scraping.

#### Uso:

```bash
python scraper.py
```

El script te guiará interactivamente para:
- Introducir un nombre para el trabajo
- Seleccionar una categoría de palabras clave
- Seleccionar una palabra clave específica
- Seleccionar una localidad
- Enviar la solicitud a la API

### 4. scraper_advanced.py

Versión avanzada que permite seleccionar múltiples palabras clave y monitorea el estado del trabajo hasta que se complete.

#### Uso:

```bash
python scraper_advanced.py
```

Características adicionales:
- Posibilidad de seleccionar múltiples palabras clave o todas dentro de una categoría
- Configuración personalizada de radio, profundidad y tiempo máximo
- Monitoreo del estado del trabajo en tiempo real
- Guardado automático de los resultados

### 5. batch_scraper.py

Script para procesamiento por lotes que permite ejecutar varios trabajos secuencialmente.

#### Uso:

```bash
python batch_scraper.py [opciones]
```

#### Opciones:

```
--host TEXT               API host URL (por defecto: http://localhost:8000)
--categories TEXT         Índices de categorías a procesar separados por comas (ej: "1,2,3")
--locations TEXT          Índices de localidades a procesar separados por comas (ej: "1,2")
--keywords TEXT           Palabras clave específicas o "all" para todas (por defecto: all)
--radius INTEGER          Radio de búsqueda en metros (por defecto: 10000)
--depth INTEGER           Profundidad de búsqueda (por defecto: 10)
--max-time INTEGER        Tiempo máximo para cada trabajo en minutos (por defecto: 15)
--wait-time INTEGER       Tiempo máximo de espera para la finalización del trabajo en minutos (por defecto: 30)
--job-prefix TEXT         Prefijo para los nombres de los trabajos
--dry-run                 Simular ejecución sin enviar trabajos reales
```

#### Ejemplos:

Ejecutar para todas las categorías y localidades:
```bash
python batch_scraper.py
```

Ejecutar solo para las categorías 1 y 3 en la localidad 2:
```bash
python batch_scraper.py --categories "1,3" --locations "2"
```

Simular ejecución sin enviar trabajos:
```bash
python batch_scraper.py --dry-run
```

## Formato de archivos

### Archivos de keywords (keywords/*.txt)

Cada línea contiene una palabra clave distinta.

### Archivos de localidades (location/*.txt)

Cada archivo contiene tres líneas:
1. Nivel de zoom
2. Latitud
3. Longitud

## Requisitos

- Python 3.6 o superior
- Módulos: requests, tkinter (incluido en la mayoría de instalaciones de Python)

Instalar dependencias:
```bash
pip install requests
```

## Formato de la solicitud API

```json
{
  "name": "string",
  "keywords": [
    "string"
  ],
  "lang": "es",
  "zoom": 0,
  "lat": "string",
  "lon": "string",
  "fast_mode": true,
  "radius": 10000,
  "depth": 10,
  "email": true,
  "max_time": 15,
  "proxies": []
}
```

## Resultados

Los resultados se guardan en el directorio `results/` en formato JSON. 