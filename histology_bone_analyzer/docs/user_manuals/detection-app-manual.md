# Manual de Usuario: Detection App

## Descripción General

Detection App es una aplicación para la detección y análisis automatizado de canales de Havers en imágenes histológicas de tejido óseo. Utilizando un modelo YOLO (You Only Look Once) entrenado específicamente para esta tarea, la aplicación procesa imágenes de microtomografía, identifica canales de Havers, calcula sus coordenadas y áreas, y genera visualizaciones para facilitar el análisis.

![Ejemplo de interfaz](../images/detection_app_ui.png)

## Características Principales

- **Detección automatizada**: Identificación de canales de Havers mediante inteligencia artificial
- **Procesamiento de imágenes grandes**: División en segmentos para un análisis optimizado
- **Análisis cuantitativo**: Cálculo de posiciones, áreas y distancias entre canales
- **Visualizaciones**: Generación de mapas de coordenadas y mapas de calor
- **Exportación de datos**: Guardado de resultados en formato Excel
- **Interfaz gráfica intuitiva**: Fácil de usar sin conocimientos técnicos avanzados

## Requisitos del Sistema

- **Sistema operativo**: Windows 10/11, macOS, o Linux
- **Python**: Versión 3.7 o superior
- **Memoria RAM**: 8GB mínimo (16GB recomendado)
- **Espacio en disco**: 2GB mínimo para la aplicación y sus dependencias
- **GPU**: Recomendada para mejor rendimiento (compatible con CUDA)

## Instalación

1. **Configurar entorno Anaconda** (recomendado):
   ```
   conda create -n osteona python=3.9
   conda activate osteona
   ```

2. **Instalar dependencias**:
   ```
   pip install opencv-python numpy pandas matplotlib torch ultralytics
   ```

3. **Descargar el modelo entrenado**:
   - Asegúrese de tener el archivo del modelo (`best.pt`) en una ubicación conocida
   - La aplicación buscará el modelo en varias rutas predefinidas

## Guía de Uso Paso a Paso

### 1. Inicio de la Aplicación

1. Abra Anaconda Prompt
2. Active el entorno: `conda activate osteona`
3. Navegue hasta la carpeta de la aplicación: `cd ruta/histology_bone_analyzer/apps/1detection_app`
4. Ejecute la aplicación: `python detection_app.py`

### 2. Carga de Imágenes

1. En la ventana inicial, haga clic en el botón "Load Image"
2. Seleccione una imagen histológica en formato JPG, JPEG o PNG
3. Para resultados óptimos, use imágenes de buena calidad y alta resolución
4. Las imágenes muy grandes se redimensionarán automáticamente

### 3. Procesamiento

Una vez seleccionada la imagen, el procesamiento comenzará automáticamente:

1. La aplicación dividirá la imagen en segmentos más pequeños (15×10)
2. Cada segmento será analizado con el modelo YOLO
3. Los canales de Havers detectados serán identificados y marcados
4. Se calculará la posición, área y otras métricas para cada canal
5. Se generarán visualizaciones y estadísticas

Este proceso puede tomar desde segundos hasta varios minutos dependiendo del tamaño de la imagen y las capacidades de su sistema.

### 4. Análisis de Resultados

Después del procesamiento, se mostrará una ventana con los resultados:

#### Visualización
- **Mapa de coordenadas**: Muestra la posición de cada canal sobre la imagen original
- **Mapa de calor**: Visualiza áreas de mayor concentración de canales

#### Datos
- **Número total de canales detectados**
- **Área promedio de los canales**: En píxeles cuadrados
- **Distancia media entre canales**: En píxeles

#### Archivos Generados
- **Archivo Excel**: Contiene coordenadas y áreas de todos los canales detectados
- **Imágenes de segmentos con anotaciones**: Muestran las detecciones individuales

### 5. Guardado de Resultados

Después de revisar los resultados, puede:

1. Guardar el mapa de coordenadas como imagen PNG
2. Guardar el mapa de calor como imagen PNG
3. Abrir y revisar el archivo Excel con los datos detallados
4. Acceder a la carpeta de resultados para ver todos los archivos generados

## Solución de Problemas

### Problemas Comunes y Soluciones

| Problema | Causa Posible | Solución |
|----------|---------------|----------|
| La aplicación no inicia | Entorno Python incorrecto | Verifique que está usando el entorno correcto con todas las dependencias instaladas |
| Error al cargar la imagen | Formato no soportado o imagen corrupta | Convierta la imagen a formato PNG o JPG usando un editor de imágenes |
| No se detectan canales | Calidad de imagen baja o modelo no apropiado | Intente con una imagen de mejor calidad o ajuste el umbral de confianza |
| Detecciones incorrectas | Artefactos en la imagen o similitud con otras estructuras | Limpie la imagen de entrada o ajuste el umbral de confianza |
| Error "Modelo no encontrado" | Ruta del modelo incorrecta | Coloque el archivo `best.pt` en una de las rutas predefinidas o modifique la variable `model_path` |

## Información Técnica

### Flujo de Procesamiento

1. **Segmentación de imagen**: División en segmentos de tamaño manejable
2. **Detección mediante YOLO**: Aplicación del modelo a cada segmento
3. **Post-procesamiento**: Cálculo de métricas, consolidación de resultados
4. **Visualización**: Generación de gráficos y mapas
5. **Exportación**: Almacenamiento de resultados en diversos formatos

### Limitaciones Actuales

- La precisión depende de la calidad de la imagen de entrada
- Imágenes con tinciones no estándar pueden afectar la detección
- La aplicación está optimizada para secciones transversales de hueso cortical
- Imágenes con dimensiones extremadamente grandes pueden necesitar redimensionamiento

## Uso Avanzado

### Ajuste de Parámetros

Si necesita modificar parámetros avanzados, puede editar el archivo `detection_app.py`:

- **Umbral de confianza**: Modificar la variable `confidence_threshold` (valor predeterminado: 0.4)
- **Número de segmentos**: Cambiar el valor en `divide_and_save_image` (valor predeterminado: 150)
- **Tamaño máximo de imagen**: Ajustar el valor en `resize_image_if_too_large`

### Integración con Breaking App

Para un análisis más detallado de la distribución espacial:

1. Ejecute primero Detection App y complete el análisis
2. Use el archivo Excel generado como entrada para Breaking App
3. Siga las instrucciones del manual de Breaking App para el análisis por cuadrantes

## Soporte y Contacto

Para soporte técnico o consultas, contacte al equipo de desarrollo del proyecto Phygital Human Bone.

---

Este manual fue creado para la versión 2.0 de Detection App, parte del proyecto Phygital Human Bone.
