# Manual de Usuario para el Repositorio Phygital Human Bone - Histology Bone Analyzer

## Guía Completa de Instalación y Uso

Este manual te guiará paso a paso para configurar y ejecutar todas las aplicaciones del proyecto Histology Bone Analyzer. El proyecto incluye tres aplicaciones principales que forman un flujo de trabajo completo para el análisis de imágenes histológicas de tejido óseo.

## Índice

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación del Entorno](#instalación-del-entorno)
3. [Estructura del Repositorio](#estructura-del-repositorio)
4. [Configuración Inicial](#configuración-inicial)
5. [Detection App: Detección de Canales de Havers](#detection-app-detección-de-canales-de-havers)
6. [Breaking App: Análisis por Cuadrantes](#breaking-app-análisis-por-cuadrantes)
7. [Distribution App: Generación Paramétrica para Grasshopper](#distribution-app-generación-paramétrica-para-grasshopper)
8. [Solución de Problemas Comunes](#solución-de-problemas-comunes)

## Requisitos del Sistema

### Hardware Recomendado
- Procesador: Intel Core i5 o superior (multihilo)
- Memoria RAM: 8GB mínimo, 16GB recomendado
- Espacio en disco: 5GB disponibles
- GPU: Compatible con CUDA (recomendado para mejor rendimiento)

### Software Necesario
- Windows 10/11, macOS o Linux
- Python 3.7 o superior
- Git
- Anaconda o Miniconda (recomendado para gestión de entornos)

## Instalación del Entorno

### 1. Instalar Git
Descarga e instala Git desde [git-scm.com](https://git-scm.com/downloads)

### 2. Instalar Anaconda
Descarga e instala Anaconda desde [anaconda.com/download](https://www.anaconda.com/download/)

### 3. Clonar el Repositorio
Abre una terminal (Símbolo del sistema, PowerShell o Terminal) y ejecuta:

```bash
git clone https://github.com/joan-bl/workspace_tfg.git
cd workspace_tfg
```

### 4. Crear y Activar el Entorno Conda
```bash
# Crear entorno con Python 3.9
conda create -n osteona python=3.9

# Activar el entorno
conda activate osteona

# Instalar dependencias
pip install opencv-python numpy pandas matplotlib pillow torch ultralytics tkinter
```

## Estructura del Repositorio

El repositorio está organizado de la siguiente manera:

```
phygital-bone-analyzer/
├── histology_bone_analyzer/         # Proyecto principal
│   ├── apps/                        # Aplicaciones principales
│   │   ├── 1detection_app/          # Detección de canales de Havers
│   │   ├── 2breaking_app/           # Análisis por cuadrantes
│   │   └── 3distribution_app/       # Generación para Grasshopper
│   ├── scripts/                     # Scripts de utilidad
│   ├── docs/                        # Documentación
│   │   └── user_manuals/            # Manuales de usuario
│   └── data/                        # Imágenes y resultados
├── models/                          # Modelos pre-entrenados
├── osteona/                         # Materiales relacionados al modelo
└── start_project.bat                # Script de inicio rápido (Windows)
```

## Configuración Inicial

### 1. Verificar Disponibilidad de GPU (Opcional)
Para comprobar si CUDA está disponible en tu sistema:

```bash
# Desde la carpeta raíz del repositorio
python histology_bone_analyzer/scripts/check_gpu.py
```

Si tienes GPU compatible con CUDA, verás un mensaje confirmando la disponibilidad.

### 2. Script de Inicio Rápido (Solo Windows)
Si estás en Windows, puedes usar el script de inicio rápido:

1. Haz doble clic en `start_project.bat` en la carpeta raíz
2. Esto activará automáticamente el entorno de Anaconda y abrirá VS Code (si está instalado)

## Detection App: Detección de Canales de Havers

Esta aplicación analiza imágenes histológicas e identifica canales de Havers utilizando un modelo YOLO.

### Ejecutar la Aplicación

1. Asegúrate de tener el entorno activado:
   ```bash
   conda activate osteona
   ```

2. Navega hasta la carpeta de la aplicación:
   ```bash
   cd histology_bone_analyzer/apps/1detection_app
   ```

3. Ejecuta la aplicación:
   ```bash
   python detection_app.py
   ```

### Uso de Detection App

1. Se abrirá una ventana con el título "Phygital Bone 3.0" y un botón "Load Image"
2. Haz clic en "Load Image" y selecciona una imagen histológica (formatos: JPG, JPEG o PNG)
3. Espera mientras la aplicación procesa la imagen (puede tardar de segundos a varios minutos según el tamaño)
4. Una vez completado el análisis, verás una pantalla de resultados con:
   - Número de canales detectados
   - Área promedio de los canales
   - Distancia media entre canales
   - Botones para ver los resultados (Excel, mapa de coordenadas, mapa de calor)

### Outputs Generados

La aplicación genera varios archivos en la carpeta `histology_bone_analyzer/data/sample_results/detection_app`:

- **Excel con coordenadas**: Archivo con las posiciones y áreas de los canales
- **Mapa de coordenadas**: Visualización de la posición de los canales
- **Mapa de calor**: Visualización de la densidad de canales

Estos archivos son necesarios para las siguientes aplicaciones del flujo.

## Breaking App: Análisis por Cuadrantes

Esta aplicación divide la imagen analizada en cuadrantes para identificar zonas frágiles y posibles caminos de propagación de fracturas.

### Ejecutar la Aplicación

1. Asegúrate de tener el entorno activado:
   ```bash
   conda activate osteona
   ```

2. Navega hasta la carpeta de la aplicación:
   ```bash
   cd histology_bone_analyzer/apps/2breaking_app
   ```

3. Ejecuta la aplicación:
   ```bash
   python breaking_app.py
   ```

### Uso de Breaking App

1. En la ventana principal, haz clic en "Iniciar Análisis"
2. Selecciona la imagen original que analizaste con Detection App
3. Selecciona el archivo Excel generado por Detection App (normalmente en `data/sample_results/detection_app/excel/bounding_box_centers.xlsx`)
4. Espera mientras la aplicación procesa los datos
5. Los resultados se mostrarán en dos pestañas:
   - **Visualización**: Imagen dividida en cuadrantes con el más frágil marcado en rojo y el camino de propagación en azul
   - **Datos por Cuadrante**: Estadísticas detalladas para cada cuadrante

### Interpretación de Resultados

- **Cuadrante Rojo**: Zona con mayor probabilidad de iniciar una fractura
- **Cuadrante Azul**: Dirección más probable de propagación de una fractura
- **Cuadrantes con X**: Áreas con menos de 6 canales (ignoradas en el análisis)
- **Cuadrantes Centrales (Gris)**: Áreas centrales del hueso

## Distribution App: Generación Paramétrica para Grasshopper

Esta aplicación permite generar distribuciones paramétricas de osteonas para diferentes secciones del fémur, útil para la creación de modelos biomiméticos en Grasshopper.

### Ejecutar la Aplicación

1. Asegúrate de tener el entorno activado:
   ```bash
   conda activate osteona
   ```

2. Navega hasta la carpeta de la aplicación:
   ```bash
   cd histology_bone_analyzer/apps/3distribution_app
   ```

3. Ejecuta la aplicación:
   ```bash
   python distribution_app.py
   ```

### Uso de Distribution App

1. En la pestaña "Parámetros", configura:
   - Longitud del fémur (cm)
   - Porcentajes de longitud para cada sección
   - Densidad de osteonas por sección
   - Tamaño de las osteonas
   - Variabilidad de la distribución

2. Haz clic en "Calcular Distribución"

3. Revisa los resultados en las pestañas:
   - **Visualización**: Perfil del fémur y distribución de osteonas
   - **Exportación**: Previsualización de datos y opciones para exportar

4. Exporta los resultados:
   - CSV para Grasshopper
   - JSON para almacenar configuración
   - Informe completo con todos los datos

### Integración con Grasshopper

Para usar los datos en Grasshopper:

1. Exporta a CSV desde la aplicación
2. En Grasshopper:
   - Usa el componente "Read File" para importar el CSV
   - Divide los datos en filas y columnas
   - Usa `position_z_cm` como coordenada Z
   - Convierte `angle_degrees` en coordenadas X e Y usando funciones trigonométricas
   - Usa `size_um` para escalar las osteonas

Para más detalles sobre la configuración en Grasshopper, consulta el archivo `histology_bone_analyzer/docs/user_manuals/Distribution application on grashopper.ini`.

## Solución de Problemas Comunes

### 1. Error "Modelo no encontrado"

**Problema**: La aplicación Detection App no encuentra el modelo YOLO.

**Solución**: 
- Verifica que el archivo `best.pt` existe en alguna de estas rutas:
  - `histology_bone_analyzer/models/best.pt`
  - `workspace/runs/detect/train/weights/best.pt`
  - `Workspace_tfg/runs/detect/train13/weights/best.pt`
  - `Workspace_tfg/osteona/best.pt`
- Si no existe, contacta al autor para obtener el modelo entrenado

### 2. Error al cargar imágenes grandes

**Problema**: La aplicación falla al intentar procesar imágenes muy grandes.

**Solución**:
- Usa el script de conversión para reducir el tamaño:
  ```bash
  python histology_bone_analyzer/scripts/topng5mb.py
  ```
- Modifica las variables `input_folder` y `output_folder` en el script para apuntar a tus carpetas

### 3. Problemas con CUDA/GPU

**Problema**: Error relacionado con CUDA al ejecutar Detection App.

**Solución**:
- Verifica que tienes los drivers de NVIDIA actualizados
- Si no tienes GPU compatible, la aplicación funcionará con CPU, pero será más lenta
- Asegúrate de tener instalado torch con soporte CUDA:
  ```bash
  pip uninstall torch
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```

### 4. Problemas con Tkinter

**Problema**: Error "No module named 'tkinter'" al ejecutar las aplicaciones.

**Solución**:
- En Windows: Reinstala Python asegurándote de marcar la opción "tcl/tk and IDLE"
- En Linux: Instala el paquete tkinter:
  ```bash
  sudo apt-get install python3-tk
  ```
- En macOS usando Homebrew:
  ```bash
  brew install python-tk
  ```

## Recomendaciones para un Uso Óptimo

1. **Imágenes de buena calidad**: Use imágenes con buen contraste y resolución
2. **Flujo de trabajo secuencial**: Siga el orden Detection App → Breaking App → Distribution App
3. **Conservar archivos intermedios**: No elimine los archivos generados entre aplicaciones
4. **Verificar resultados**: Inspeccione visualmente las detecciones para asegurar precisión
5. **Recursos de sistema**: Cierre otras aplicaciones exigentes al ejecutar Detection App

---

## Información adicional: Organización del Repositorio GitHub

Para mantener tu repositorio bien organizado, sigue esta estructura recomendada:

```
phygital-bone-analyzer/
│
├── README.md                   # Descripción del proyecto y guía de inicio
├── LICENSE                     # Licencia del proyecto
├── requirements.txt            # Dependencias necesarias
├── setup.py                    # Script de instalación (opcional)
│
├── data/                       # Datos de ejemplo
│   ├── sample_images/          # Imágenes de muestra
│   └── sample_results/         # Resultados de ejemplo
│
├── src/                        # Código fuente principal
│   ├── detection/              # Código para detección
│   ├── analysis/               # Código para análisis
│   ├── visualization/          # Código para visualización
│   └── utils/                  # Utilidades generales
│
├── apps/                       # Aplicaciones con interfaces
│   ├── detection_app/          # App principal de detección
│   ├── distributor_app/        # App de distribución
│   └── cuadrantes_app/         # App de análisis por cuadrantes
│
├── models/                     # Modelos pre-entrenados
│
├── docs/                       # Documentación
│   ├── user_manuals/           # Manuales de usuario
│   └── technical/              # Documentación técnica
│
├── notebooks/                  # Jupyter notebooks
│
├── scripts/                    # Scripts de utilidad
│
└── tests/                      # Pruebas automatizadas
```

### Consejos para el workflow con GitHub:

1. **Uso del archivo .gitignore**: Excluye:
   - Archivos grandes (modelos, datasets)
   - Archivos temporales (\_\_pycache\_\_, .ipynb_checkpoints)
   - Información sensible
   - Archivos de entorno virtual

2. **Branches**: 
   - `main`: Versión estable
   - `development`: Desarrollo continuo
   - Branches separados para nuevas características

3. **Commits descriptivos**: Usa mensajes claros que expliquen el propósito del cambio

4. **README detallado**: Incluye:
   - Descripción del proyecto
   - Instrucciones de instalación
   - Guía de uso básica
   - Enlaces a documentación
   - Información de contacto

5. **Versionado semántico**: Usa tags para marcar versiones importantes (v1.0.0, v1.1.0, etc.)