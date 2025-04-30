# Manual de Usuario: Detection App 3.0

## Descripción General

Detection App es una aplicación para la detección y análisis automatizado de canales de Havers en imágenes histológicas de tejido óseo. Utilizando un modelo YOLO (You Only Look Once) entrenado específicamente para esta tarea, la aplicación procesa imágenes de microtomografía, identifica canales de Havers, calcula sus coordenadas y áreas, y genera visualizaciones para facilitar el análisis.


## Características Principales

- **Detección automatizada**: Identificación de canales de Havers mediante inteligencia artificial
- **Procesamiento de imágenes grandes**: División en segmentos para un análisis optimizado
- **Análisis cuantitativo**: Cálculo de posiciones, áreas y distancias entre canales
- **Visualizaciones**: Generación de mapas de coordenadas y mapas de calor
- **Exportación de datos**: Guardado de resultados en formato Excel
- **Interfaz gráfica moderna**: Diseño en colores negro y rojo con controles intuitivos

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

3. **Descargar modelo entrenado**:
   - Asegúrese de tener el archivo del modelo (`best.pt`) en la carpeta:
     `C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\histology_bone_analyzer\models\`
   - La aplicación buscará el modelo automáticamente

## Guía de Uso Paso a Paso

### 1. Inicio de la Aplicación

1. Abra Anaconda Prompt
2. Active el entorno: `conda activate osteona`
3. Navegue hasta la carpeta de la aplicación: `cd ruta/histology_bone_analyzer/apps/1detection_app`
4. Ejecute la aplicación: `python detection_app.py`

### 2. Pantalla Inicial

![Pantalla de inicio](../images/start_screen.png)

Al iniciar la aplicación, verá:
- Título "Phygital Bone 3.0" en la parte superior
- Un botón rojo "Load Image" en el centro
- Fondo negro con elementos de texto en blanco

### 3. Carga de Imágenes

1. Haga clic en el botón rojo "Load Image"
2. Se abrirá un selector de archivos estándar
3. Seleccione una imagen histológica en formato JPG, JPEG o PNG
4. Para resultados óptimos, use imágenes de buena calidad y alta resolución
5. Las imágenes muy grandes se redimensionarán automáticamente

### 4. Procesamiento

Una vez seleccionada la imagen, aparecerá una pantalla de procesamiento:

![Pantalla de procesamiento](../images/processing_screen.png)

El procesamiento sigue estos pasos automáticamente:

1. La aplicación divide la imagen en 150 segmentos pequeños (15×10)
2. Cada segmento es analizado con el modelo YOLO
3. Los canales de Havers detectados son identificados y marcados
4. Se calculan la posición, área y otras métricas para cada canal
5. Se generan visualizaciones y estadísticas

Este proceso puede tomar desde segundos hasta varios minutos dependiendo del tamaño de la imagen y las capacidades de su sistema.

### 5. Pantalla de Resultados

![Pantalla de resultados](../images/results_screen.png)

Después del procesamiento, se mostrará la pantalla de resultados con:

#### Estadísticas
- **Número total de canales detectados**
- **Área promedio de los canales** (en píxeles cuadrados)
- **Distancia media entre canales** (en píxeles)

#### Archivos Generados
Lista de archivos creados durante el análisis:
- Archivo Excel con coordenadas
- Mapa de coordenadas (imagen PNG)
- Mapa de calor (imagen PNG)

#### Botones de Acceso Rápido
- **Ver datos en Excel**: Abre el archivo de Excel con los datos detallados
- **Ver mapa de coordenadas**: Abre la visualización de posiciones de canales
- **Ver mapa de calor**: Muestra la visualización de densidad
- **Abrir carpeta de resultados**: Accede directamente a la carpeta con todos los archivos generados

### 6. Visualizaciones

La aplicación genera dos tipos principales de visualizaciones:

#### Mapa de Coordenadas
![Mapa de coordenadas](../images/coordinates_map.png)

- Muestra la imagen original con puntos rojos que marcan cada canal detectado
- Permite ver la distribución espacial de los canales en el tejido
- Los puntos son proporcionales al tamaño de los canales

#### Mapa de Calor
![Mapa de calor](../images/heatmap.png)

- Muestra las zonas de mayor concentración de canales con tonalidades más intensas
- Proporciona una vista intuitiva de la densidad de canales en diferentes áreas
- Útil para identificar patrones de distribución

### 7. Archivos Generados

La aplicación crea la siguiente estructura de archivos:

```
histology_bone_analyzer\
├── data\
│   ├── sample_results\
│   │   └── detection_app\
│   │       ├── images_segmented\        # 150 segmentos de la imagen
│   │       ├── segmented_results\       # Segmentos con detecciones
│   │       ├── results\                 # Mapas de coordenadas y calor
│   │       └── excel\                   # Datos Excel
│   └── sample_images\                   # Imágenes reconstruidas
└── docs\
    └── technical\                       # Copia de seguridad del Excel
```

El archivo Excel (`bounding_box_centers.xlsx`) contiene:
- Coordenadas X, Y de cada canal
- ID del segmento donde se detectó
- Área en píxeles cuadrados

## Solución de Problemas

### Problemas Comunes y Soluciones

| Problema | Causa Posible | Solución |
|----------|---------------|----------|
| La aplicación no inicia | Entorno Python incorrecto | Verifique que está usando el entorno correcto con todas las dependencias instaladas |
| Error al cargar la imagen | Formato no soportado o imagen corrupta | Convierta la imagen a formato PNG o JPG usando un editor de imágenes |
| No se detectan canales | Calidad de imagen baja o modelo no apropiado | Intente con una imagen de mejor calidad o ajuste el umbral de confianza |
| Detecciones incorrectas | Artefactos en la imagen o similitud con otras estructuras | Limpie la imagen de entrada o use imágenes con mejor contraste |
| Error "Modelo no encontrado" | Ruta del modelo incorrecta | Asegúrese de tener el archivo `best.pt` en la carpeta `models` |

### Mensajes de Error Comunes

- **"No se seleccionó ninguna imagen"**: Debe seleccionar un archivo de imagen válido.
- **"ERROR: El archivo X no existe"**: Verifique la ruta y el nombre del archivo.
- **"Error al dividir la imagen"**: Pruebe con una imagen en otro formato o de menor tamaño.
- **"No se detectaron canales de Havers"**: La imagen no contiene canales detectables o el umbral de confianza es demasiado alto.

## Integración con Breaking App

Para un análisis más detallado de la distribución espacial:

1. Ejecute primero Detection App y complete el análisis
2. Use el archivo Excel generado como entrada para Breaking App
3. Siga las instrucciones del manual de Breaking App para el análisis por cuadrantes

## Recomendaciones para Mejores Resultados

- **Imágenes de alta calidad**: Use imágenes con buen contraste y resolución
- **Iluminación adecuada**: Las imágenes con iluminación uniforme dan mejores resultados
- **Preparación correcta**: Muestras bien preparadas y teñidas mejoran la detección
- **Procesamiento previo**: En imágenes con ruido, considere un preprocesamiento con software de edición
- **Múltiples análisis**: Compare resultados de diferentes muestras para conclusiones más robustas

## Novedades de la Versión 3.0

- **Nueva interfaz gráfica**: Diseño moderno con fondo negro y botones rojos
- **Ventana centrada**: Posicionamiento automático en el centro de la pantalla
- **Ventanas redimensionables**: Permite ajustar el tamaño de la ventana
- **Gestión mejorada de carpetas**: Organización más clara de archivos de salida
- **Copia de seguridad de datos**: Crea automáticamente copias de los resultados
- **Rendimiento optimizado**: Mejor gestión de memoria y procesamiento
- **Guardado de imágenes reconstruidas**: Almacenamiento de resultados en ubicación dedicada

## Soporte y Contacto

Para soporte técnico o consultas, contacte al equipo de desarrollo del proyecto Phygital Human Bone a través del repositorio GitHub:

[https://github.com/joan-bl/workspace_tfg](https://github.com/joan-bl/workspace_tfg)

---

Este manual fue creado para la versión 3.0 de Detection App, parte del proyecto Phygital Human Bone.