# Detection App - Análisis Automatizado de Canales de Havers

## Descripción General

Detection App es una aplicación Python diseñada para la detección, medición y análisis de canales de Havers en imágenes histológicas de hueso mediante visión computacional e inteligencia artificial. Desarrollada como parte del proyecto Phygital Human Bone, esta herramienta automatiza el proceso de identificación de microestructuras óseas que tradicionalmente requiere análisis manual, ahorrando tiempo y proporcionando resultados consistentes.

![Ejemplo de Detección](../images/detection_example.png)

## Características Principales

- **Detección automatizada de canales de Havers** usando un modelo YOLO (You Only Look Once) entrenado específicamente para este propósito
- **Procesamiento de imágenes de alta resolución** mediante segmentación inteligente
- **Análisis cuantitativo** con cálculo de:
  - Posiciones exactas (coordenadas X, Y) de cada canal
  - Áreas de cada canal en píxeles cuadrados (modeladas como elipses)
  - Distancias medias entre canales
  - Conteo total de canales detectados
- **Visualizaciones avanzadas**:
  - Mapa de coordenadas con superposición sobre la imagen original
  - Mapa de calor de densidad de canales
- **Exportación de datos** a formato Excel para análisis posterior
- **Interfaz gráfica moderna** con tema visual corporativo (negro/rojo)

## Estructura del Código

El archivo `detection_app.py` está organizado en módulos funcionales:

```
detection_app.py
├── Definición de constantes y rutas
├── Funciones de interfaz gráfica
│   ├── configure_window() - Configura apariencia visual de ventanas
│   ├── configure_button() - Aplica estilo a botones
│   ├── select_image_in_window() - Maneja selección de imágenes
│   └── show_results() - Presenta resultados al usuario
├── Funciones de procesamiento de imágenes
│   ├── divide_and_save_image() - Divide imagen en segmentos
│   ├── resize_image_if_too_large() - Redimensiona imágenes grandes
│   └── process_image_segments() - Procesa segmentos con YOLO
├── Funciones de análisis
│   ├── calculate_box_centers_and_areas() - Calcula métricas para detecciones
│   ├── calculate_distance_matrix() - Calcula distancias entre canales
│   └── save_results_to_excel() - Exporta resultados a Excel
├── Funciones de visualización
│   ├── plot_centers() - Genera mapa de coordenadas
│   ├── plot_heatmap() - Genera mapa de calor
│   └── generate_visualizations() - Coordina visualizaciones
└── Función principal main()
```

## Tecnologías Utilizadas

- **Python 3.7+**: Lenguaje de programación base
- **OpenCV (cv2)**: Procesamiento y manipulación de imágenes
- **Ultralytics YOLO**: Framework de detección de objetos para identificar canales de Havers
- **PyTorch**: Backend para el modelo de machine learning
- **NumPy & Pandas**: Análisis y manipulación de datos numéricos
- **Matplotlib**: Generación de visualizaciones y gráficos
- **Tkinter**: Creación de la interfaz gráfica de usuario
- **PIL (Python Imaging Library)**: Manipulación adicional de imágenes

## Flujo de Trabajo Detallado

1. **Selección de imagen**: 
   - El usuario selecciona una imagen histológica a través de la interfaz gráfica
   - Se verifica el tamaño de la imagen y, si es necesario, se redimensiona

2. **Preprocesamiento**:
   - La imagen se divide en aproximadamente 150 segmentos (matriz de 15×10)
   - Cada segmento se guarda temporalmente para su procesamiento individual

3. **Detección con YOLO**:
   - Se carga el modelo YOLO pre-entrenado
   - Cada segmento se analiza con el modelo con un umbral de confianza de 0.4
   - Las detecciones se recopilan, registrando sus posiciones absolutas en la imagen original

4. **Cálculos y Análisis**:
   - Para cada detección, se calcula:
     - Coordenadas del centro (X, Y)
     - Dimensiones (ancho y alto)
     - Área de la elipse aproximada (π × semi-eje mayor × semi-eje menor)
   - Se calculan estadísticas globales como:
     - Número total de canales detectados
     - Área promedio
     - Distancia media entre canales vecinos

5. **Generación de Visualizaciones**:
   - **Mapa de coordenadas**: Gráfico de dispersión que muestra la ubicación de cada canal
   - **Mapa de calor**: Visualización de la densidad de canales a lo largo de la imagen

6. **Presentación de Resultados**:
   - Los datos se exportan a un archivo Excel (con copia de seguridad)
   - Las visualizaciones se guardan como archivos PNG
   - La interfaz muestra estadísticas clave y botones para acceder a los archivos generados

## Estructura de Carpetas

La aplicación genera y utiliza las siguientes carpetas:

```
histology_bone_analyzer\
├── data\
│   ├── sample_results\
│   │   └── detection_app\
│   │       ├── images_segmented\        # Segmentos de la imagen original
│   │       ├── segmented_results\       # Segmentos con detecciones marcadas
│   │       ├── results\                 # Visualizaciones (mapas)
│   │       └── excel\                   # Archivo Excel con datos
│   └── sample_images\                   # Imágenes reconstruidas
└── docs\
    └── technical\                       # Copia de seguridad de datos
```

## Mejoras de Interfaz

- **Tema visual moderno**: Fondo negro con botones rojos y texto blanco
- **Interfaz centrada**: La ventana se coloca automáticamente en el centro de la pantalla
- **Ventanas redimensionables**: La aplicación permite ajustar el tamaño de las ventanas
- **Diseño responsivo**: Los elementos se adaptan al tamaño de la ventana

## Requisitos

- Python 3.7 o superior
- GPU compatible con CUDA (recomendado para rendimiento óptimo)
- Mínimo 8GB de RAM (16GB recomendado para imágenes grandes)
- Dependencias específicas:
  ```
  opencv-python
  ultralytics
  torch
  pandas
  numpy
  matplotlib
  pillow
  ```

## Instrucciones de Ejecución

1. Configurar entorno con Anaconda (recomendado):
   ```
   conda create -n osteona python=3.9
   conda activate osteona
   pip install opencv-python ultralytics pandas numpy matplotlib pillow torch
   ```

2. Ejecutar la aplicación:
   ```
   python detection_app.py
   ```

## Limitaciones Actuales y Desarrollo Futuro

### Limitaciones
- El rendimiento depende de la calidad y resolución de las imágenes de entrada
- La precisión del modelo está actualmente en aproximadamente 80% bajo condiciones ideales
- El procesamiento de imágenes muy grandes puede ser lento en sistemas sin GPU

### Desarrollos Futuros
- Implementación de técnicas de data augmentation para mejorar el entrenamiento
- Optimización del modelo para alcanzar 85%+ de precisión
- Integración de análisis de laminillas y otras estructuras óseas
- Incorporación de detección de patrones de fractura

## Integración con Breaking App

Los resultados generados por Detection App pueden ser utilizados directamente por Breaking App para realizar un análisis por cuadrantes, identificando zonas de mayor densidad de canales y proporcionando estadísticas específicas por región.

## Autores

- Joan Blanch Jiménez - Desarrollador principal
- Equipo del proyecto Phygital Human Bone

## Repositorio

[https://github.com/joan-bl/workspace_tfg](https://github.com/joan-bl/workspace_tfg)

## Licencia

Este proyecto está licenciado bajo MIT License.