# Phygital Human Bone - Análisis de Canales de Havers

## Resumen General del Proyecto

Este proyecto se centra en el desarrollo de herramientas de software para analizar imágenes histológicas de secciones óseas, específicamente para detectar canales de Havers y osteonas en tejido óseo cortical. Utilizando técnicas de visión por computadora y aprendizaje automático, el software permite identificar estructuras microanatómicas del hueso y analizar su distribución espacial. Esta herramienta forma parte del proyecto "Phygital Human Bone", que busca crear modelos biomiméticos de hueso humano mediante algoritmos paramétricos, machine learning y fabricación aditiva.

## Estructura del Repositorio

El repositorio contiene varios componentes principales:

### Directorios Principales:

```
histology_bone_analyzer/
├── apps/                      # Aplicaciones principales
│   ├── 1detection_app/        # Detección de canales de Havers
│   │   ├── detection_app.py   # Versión actual
│   │   └── old_versions/      # Versiones anteriores
│   ├── 2breaking_app/         # Análisis por cuadrantes
│   │   └── breaking_app.py
│   └── 3ditribution_app/      # Generación de distribuciones
│       └── distribution_app.py
├── docs/                      # Documentación del proyecto
│   └── user_manuals/          # Manuales de usuario
├── scripts/                   # Scripts de utilidad
│   ├── check_gpu.py           # Verificación de disponibilidad de GPU
│   ├── topng5mb.py            # Conversión de imágenes TIF a PNG
│   └── other_scripts/         # Scripts adicionales
└── README.md                  # Este archivo
```

## Componentes Principales

El proyecto consta de tres aplicaciones principales:

### 1. Detection App (fixed-phygital-code.py)

Aplicación para la detección automática de canales de Havers utilizando un modelo YOLO entrenado:

- **Funcionalidades**:
  - Carga y procesamiento de imágenes de microtomografía CT
  - División de imágenes en segmentos más pequeños para análisis detallado
  - Detección automática de canales de Havers mediante modelo YOLO
  - Cálculo de parámetros relevantes: posición, área y distribución de canales
  - Generación de visualizaciones: mapa de coordenadas y mapa de calor
  - Interfaz gráfica para interacción con el usuario
  
- **Principales funciones**:
  - `divide_and_save_image`: Divide la imagen en 150 segmentos (15×10)
  - `calculate_box_centers_and_areas`: Calcula coordenadas y áreas de canales
  - `plot_centers` y `plot_heatmap`: Generan visualizaciones de resultados
  - `calculate_distance_matrix`: Calcula la distancia media entre canales

### 2. Breaking App (cuadrantes-analyzer.py)

Herramienta complementaria que analiza la distribución espacial de los canales dividiendo la imagen en nueve cuadrantes:

- **Funcionalidades**:
  - División de la imagen analizada en nueve cuadrantes (matriz 3×3)
  - Análisis de la distribución de canales por cuadrante
  - Identificación del cuadrante con mayor densidad de canales
  - Visualización de resultados con marcado de cuadrantes
  - Exportación de datos a formato Excel
  
- **Principales funciones**:
  - `reconstruir_imagen_con_detecciones`: Visualiza canales en la imagen original
  - `analizar_cuadrantes`: Divide en 9 cuadrantes e identifica el de mayor densidad
  - `visualizar_resultados_cuadrantes`: Presenta resultados en una interfaz gráfica

### 3. Distribution App

Aplicación para generar distribuciones parametrizadas de osteonas para diferentes secciones del fémur:

- **Funcionalidades**:
  - Definición de la longitud total del fémur
  - Configuración de parámetros específicos por sección (epífisis, metáfisis, diáfisis)
  - Generación procedural de distribuciones de osteonas con propiedades biomecánicamente realistas
  - Exportación de datos para integración con Grasshopper
  - Visualización de la distribución generada

## Tecnologías Utilizadas

- **Lenguaje**: Python como lenguaje de programación principal
- **Procesamiento de imágenes**: OpenCV
- **Machine Learning**: YOLO (You Only Look Once), PyTorch, Ultralytics
- **Análisis de datos**: Pandas y NumPy
- **Visualización**: Matplotlib para generación de gráficos y mapas de calor
- **Interfaz gráfica**: Tkinter para crear una GUI amigable

## Enfoque de Machine Learning

- Utiliza el modelo YOLO (You Only Look Once) para la detección de osteonas
- El entrenamiento del modelo se realizó con los siguientes parámetros:
  - Modelo base: YOLOv8n
  - Epochs: 100
  - Batch size: 16
  - Tamaño de imagen: 640x640
  - Threshold de confianza: 0.4
- El código divide las imágenes grandes en 150 segmentos (15×10) para mejorar la precisión de detección

## Flujo de Trabajo Completo

1. **Selección de imagen**: El usuario carga una imagen de microtomografía CT
2. **Procesamiento**: La imagen se divide en segmentos más pequeños
3. **Detección**: Se aplica el modelo YOLO para identificar canales de Havers
4. **Análisis**: Se calculan estadísticas relevantes (conteo, áreas, distancias)
5. **Visualización**: Se generan gráficos y mapas de calor para facilitar la interpretación
6. **Análisis espacial**: Se estudia la distribución por cuadrantes (opcional)
7. **Generación paramétrica**: Creación de distribuciones realistas (opcional)
8. **Integración con Grasshopper**: Uso de los datos para modelado 3D (opcional)

## Requisitos del Sistema

### Software
- Python 3.7 o superior
- Bibliotecas requeridas:
  - opencv-python (cv2)
  - numpy
  - pandas
  - matplotlib
  - pillow (PIL)
  - ultralytics (YOLO)
  - torch

### Hardware Recomendado
- Procesador multinúcleo moderno
- 8GB de RAM mínimo (16GB recomendado para imágenes grandes)
- GPU compatible con CUDA (opcional pero recomendado para mejor rendimiento)

## Instalación

1. **Clonar el repositorio**:
   ```
   git clone https://github.com/username/histology_bone_analyzer.git
   cd histology_bone_analyzer
   ```

2. **Configurar entorno Anaconda** (recomendado):
   ```
   conda create -n osteona python=3.9
   conda activate osteona
   ```

3. **Instalar dependencias**:
   ```
   pip install opencv-python numpy pandas matplotlib pillow ultralytics torch
   ```

4. **Ejecutar la aplicación deseada**:
   ```
   # Para Detection App
   python apps/1detection_app/detection_app.py
   
   # Para Breaking App
   python apps/2breaking_app/breaking_app.py
   
   # Para Distribution App
   python apps/3ditribution_app/distribution_app.py
   ```

## Datos de Entrada/Salida

### Entrada:
- Imágenes de microtomografía CT en formato JPG, JPEG o PNG

### Salida:
- Archivo Excel con coordenadas y áreas de los canales detectados
- Visualizaciones gráficas (mapa de coordenadas, mapa de calor)
- Imagen con cuadrantes analizados (opcional)
- Estadísticas por cuadrante (opcional)
- Datos paramétricos para Grasshopper (opcional)

## Limitaciones Actuales

- El rendimiento óptimo se obtiene con imágenes de microtomografía CT de alta calidad
- Imágenes muy grandes pueden requerir redimensionamiento
- La precisión de detección actual está en aproximadamente 80%

## Uso Recomendado

Este software está diseñado para:

- Investigación en biomecánica y estructura ósea
- Análisis histológico cuantitativo
- Estudios de distribución espacial de canales de Havers
- Desarrollo de modelos biomiméticos de tejido óseo
- Integración con sistemas de modelado paramétrico como Grasshopper

## Contexto del Proyecto

Este trabajo se enmarca en un esfuerzo más amplio para desarrollar modelos biomiméticos de hueso humano. La parte específica del proyecto está enfocada en la sección de Inteligencia Artificial, desarrollando herramientas para analizar histologías de secciones óseas.

El objetivo de toda esta investigación es crear modelos sintéticos de hueso que repliquen fielmente las propiedades biomecánicas del hueso real, con aplicaciones potenciales en prótesis, investigación biomecánica y medicina regenerativa.

## Desarrollo Futuro

- Mejora del modelo de IA para superar el 85% de precisión
- Implementación de métricas adicionales como densidad de laminillas
- Desarrollo de análisis de patrones de fractura
- Integración directa con software de CAD y modelado 3D
- Expansión para analizar otros tipos de huesos además del fémur

## Autores y Contribuciones

Este proyecto es parte del trabajo de investigación "Phygital Human Bone", desarrollado por Joan Blanch Jiménez y colaboradores.

## Licencia

Este proyecto está licenciado bajo MIT License.
