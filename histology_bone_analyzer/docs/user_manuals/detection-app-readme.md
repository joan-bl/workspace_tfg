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
- **Interfaz gráfica intuitiva** desarrollada con Tkinter

## Estructura del Código

El archivo `detection_app.py` está organizado en módulos funcionales:

```
detection_app.py
├── Configuración de variables globales y rutas
├── Funciones de interfaz gráfica
│   ├── configure_window()
│   ├── configure_button()
│   ├── select_image()
│   └── show_results_simple()
├── Funciones de procesamiento de imágenes
│   ├── divide_and_save_image()
│   └── resize_image_if_too_large()
├── Funciones de análisis
│   ├── calculate_box_centers_and_areas()
│   └── calculate_distance_matrix()
├── Funciones de visualización
│   ├── plot_centers()
│   └── plot_heatmap()
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
   - Se carga el modelo YOLO pre-entrenado desde una ubicación predefinida
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
   - **Mapa de coordenadas**: Gráfico de dispersión que muestra la ubicación de cada canal sobre la imagen original
   - **Mapa de calor**: Visualización de la densidad de canales a lo largo de la imagen

6. **Presentación de Resultados**:
   - Los datos se exportan a un archivo Excel
   - Las visualizaciones se guardan como archivos PNG
   - La interfaz muestra estadísticas clave y opciones para abrir los archivos generados

## Detalles de Implementación

### Segmentación de Imágenes

La función `divide_and_save_image()` divide la imagen en segmentos más pequeños para:
- Mejorar el rendimiento de detección
- Permitir el procesamiento de imágenes de alta resolución
- Aumentar la precisión en la identificación de estructuras pequeñas

Código clave:
```python
def divide_and_save_image(image_path, output_dir, num_segments=150):
    # Configuración de la división
    cols = 15
    rows = ceil(num_segments / cols)
    segment_height = image.shape[0] // rows
    segment_width = image.shape[1] // cols
    
    # Proceso de división y guardado
    for i in range(rows):
        for j in range(cols):
            start_y = i * segment_height
            end_y = start_y + segment_height if i < rows - 1 else image.shape[0]
            start_x = j * segment_width
            end_x = start_x + segment_width if j < cols - 1 else image.shape[1]
            segment = image[start_y:end_y, start_x:end_x]
            # Guardar segmento...
```

### Detección con YOLO

El modelo YOLO (You Only Look Once) es un sistema de detección de objetos en tiempo real. En esta aplicación:
- Se utiliza un modelo específicamente entrenado para identificar canales de Havers
- Cada segmento se procesa individualmente con el modelo
- Las detecciones se transforman a coordenadas absolutas en la imagen original

Código clave:
```python
# Cargar modelo YOLO
model = YOLO(model_path)

# Procesar cada segmento
for segment_path in segment_paths:
    results = model(segment_path, conf=confidence_threshold)
    
    for result in results:
        boxes = result.boxes
        centers = calculate_box_centers_and_areas(boxes, start_x, start_y, segment_id)
        box_centers_and_areas.extend(centers)
```

### Cálculo de Áreas y Distancias

Los canales de Havers se modelan como elipses para calcular sus áreas:

```python
def calculate_box_centers_and_areas(boxes, start_x, start_y, segment_id):
    centers = []
    for box in boxes:
        xyxy = box.xyxy.clone().detach().cpu().view(1, 4)
        width = xyxy[0, 2] - xyxy[0, 0]
        height = xyxy[0, 3] - xyxy[0, 1]
        cx = start_x + (xyxy[0, 0] + xyxy[0, 2]) / 2
        cy = start_y + (xyxy[0, 1] + xyxy[0, 3]) / 2
        semi_major_axis = width / 2
        semi_minor_axis = height / 2
        ellipse_area = pi * semi_major_axis * semi_minor_axis
        centers.append((cx, cy, segment_id, ellipse_area))
    return centers
```

La distancia media entre canales se calcula usando la fórmula euclidiana:

```python
def calculate_distance_matrix(centers_df):
    distances = []
    points = centers_df[['Center X', 'Center Y']].values
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = np.sqrt(((points[i] - points[j]) ** 2).sum())
            distances.append(dist)
    return np.mean(distances) if distances else 0
```

### Visualizaciones

La aplicación genera dos tipos principales de visualizaciones:

1. **Mapa de coordenadas** (`plot_centers()`): Muestra la ubicación exacta de cada canal como puntos sobre la imagen original, permitiendo ver la distribución espacial.

2. **Mapa de calor** (`plot_heatmap()`): Utiliza histogramas bidimensionales para visualizar áreas de mayor concentración de canales, resaltando regiones de alta densidad.

## Configuración y Personalización

La aplicación permite ajustar varios parámetros para adaptarse a diferentes necesidades:

- **Umbral de confianza** (`confidence_threshold = 0.4`): Controla la sensibilidad de la detección. Valores más bajos detectan más canales pero pueden incluir falsos positivos.

- **Número de segmentos** (`num_segments = 150`): Determina la granularidad de la segmentación. Más segmentos pueden mejorar la precisión pero aumentan el tiempo de procesamiento.

- **Tamaño máximo de imagen** (`max_pixels = 178956970`): Limita el tamaño de las imágenes para evitar problemas de memoria. Las imágenes mayores se redimensionan automáticamente.

## Integración con Otras Herramientas

Detection App genera archivos que pueden ser utilizados por otras aplicaciones del proyecto:

- **Archivo Excel**: Contiene datos detallados de cada canal detectado, compatible con la Breaking App para análisis por cuadrantes.

- **Imágenes anotadas**: Los segmentos con las detecciones marcadas pueden usarse para validación manual o entrenamiento adicional.

- **Visualizaciones**: Los mapas generados pueden incorporarse en informes o presentaciones.

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
- Interfaz mejorada con opciones de configuración accesibles al usuario

## Contribuir

Si desea contribuir al desarrollo de Detection App:

1. Bifurque el repositorio
2. Cree una rama para su característica (`git checkout -b feature/amazing-feature`)
3. Confirme sus cambios (`git commit -m 'Add some amazing feature'`)
4. Envíe a la rama (`git push origin feature/amazing-feature`)
5. Abra una Pull Request

## Autores

- Joan Blanch Jiménez - Investigador principal y desarrollador
- Equipo del proyecto Phygital Human Bone

## Licencia

Este proyecto está licenciado bajo MIT License.
