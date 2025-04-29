# Manual de Usuario: Breaking App

## Introducción

Breaking App es una herramienta especializada para el análisis espacial de canales de Havers en imágenes histológicas de tejido óseo. Esta aplicación complementa a Detection App dividiendo la imagen en nueve cuadrantes para analizar la distribución de canales, identificar zonas de mayor densidad y proporcionar estadísticas específicas para cada región del tejido.

![Ejemplo de Análisis por Cuadrantes](../images/breaking_app_example.png)

Esta herramienta forma parte del proyecto "Phygital Human Bone", que busca crear modelos biomiméticos de hueso humano mediante algoritmos paramétricos, machine learning y fabricación aditiva.

## Propósito y Contexto

El análisis por cuadrantes es esencial para comprender la heterogeneidad espacial en la distribución de canales de Havers, lo que tiene importantes implicaciones para:

- Determinar patrones estructurales del tejido óseo
- Identificar zonas potencialmente más susceptibles a fracturas
- Comprender procesos de remodelación ósea
- Generar modelos biomiméticos más precisos

Breaking App automatiza este análisis, proporcionando visualizaciones claras y métricas cuantitativas para cada región del tejido.

## Características Principales

- **Análisis por cuadrantes**: División de la imagen en 9 regiones (matriz 3×3)
- **Identificación de zonas críticas**: Detección automática del cuadrante con mayor densidad
- **Análisis cuantitativo por región**: Número de canales, área total y promedio por región
- **Visualizaciones interactivas**: Imagen segmentada por cuadrantes con código de colores
- **Exportación de resultados**: Guardado de imágenes e informes en Excel

## Requisitos del Sistema

- **Sistema operativo**: Windows 10/11, macOS, o Linux
- **Python**: Versión 3.7 o superior
- **Memoria RAM**: 4GB mínimo (8GB recomendado)
- **Espacio en disco**: 1GB mínimo
- **Pantalla**: Resolución mínima 1280x720

## Instalación

1. **Configurar entorno Anaconda** (recomendado):
   ```
   conda create -n osteona python=3.9
   conda activate osteona
   ```

2. **Instalar dependencias**:
   ```
   pip install opencv-python numpy pandas matplotlib pillow
   ```

3. **Descargar la aplicación**:
   - Asegúrese de tener todos los archivos del repositorio descargados
   - La aplicación se encuentra en la carpeta `apps/2breaking_app/`

## Guía de Uso Paso a Paso

### 1. Inicio de la Aplicación

1. Abra Anaconda Prompt
2. Active el entorno: `conda activate osteona`
3. Navegue hasta la carpeta de la aplicación: `cd ruta/histology_bone_analyzer/apps/2breaking_app`
4. Ejecute la aplicación: `python breaking_app.py`

### 2. Análisis de una Imagen

1. Al iniciar la aplicación, verá la pantalla principal con el título "Análisis de Canales por Cuadrantes"
2. Haga clic en el botón "Iniciar Análisis"
3. Se abrirá un cuadro de diálogo para seleccionar la imagen original
   - Seleccione la imagen histológica que desea analizar (JPG, JPEG o PNG)
4. A continuación, se abrirá otro cuadro de diálogo para seleccionar el archivo Excel
   - Seleccione el archivo Excel generado previamente por Detection App
   - Este archivo debe contener las coordenadas y áreas de los canales detectados

### 3. Procesamiento de la Imagen

Una vez seleccionados los archivos, la aplicación procesará automáticamente:

1. Reconstruirá la imagen con las detecciones de canales basándose en los datos del Excel
2. Dividirá la imagen en 9 cuadrantes de igual tamaño
3. Clasificará cada canal detectado en su cuadrante correspondiente
4. Calculará estadísticas para cada cuadrante
5. Identificará el cuadrante con mayor densidad de canales
6. Generará una visualización con los cuadrantes marcados y el cuadrante de mayor densidad resaltado

Este proceso puede tardar desde unos segundos hasta un minuto, dependiendo del tamaño de la imagen y el número de canales detectados.

### 4. Visualización de Resultados

Después del procesamiento, la aplicación mostrará una nueva ventana con dos pestañas:

#### Pestaña "Visualización"

Muestra la imagen dividida en 9 cuadrantes con:
- Líneas blancas que delimitan cada cuadrante
- Un rectángulo semitransparente rojo que marca el cuadrante con mayor densidad
- Texto en cada cuadrante mostrando:
  - Área total de canales
  - Número de canales detectados

En esta pestaña encontrará un botón "Guardar Imagen" que le permitirá guardar esta visualización en formato PNG.

#### Pestaña "Datos por Cuadrante"

Presenta un informe textual detallado con:
- Información de cada cuadrante (numerados del 1 al 9)
- Ubicación (fila y columna) de cada cuadrante
- Área total de canales por cuadrante
- Número de canales por cuadrante
- Área promedio por canal
- Indicación del cuadrante con mayor densidad

En esta pestaña encontrará un botón "Exportar a Excel" que le permitirá guardar todos estos datos en un archivo Excel para análisis adicionales.

### 5. Interpretación de los Resultados

- **Cuadrante con mayor densidad**: Destacado en rojo, representa la región con mayor concentración de canales. Esta zona puede tener implicaciones biomecánicas importantes.
- **Distribución por cuadrantes**: La variación en el número de canales y áreas entre cuadrantes refleja la heterogeneidad del tejido óseo.
- **Área vs. número de canales**: Un cuadrante puede tener pocos canales pero de gran tamaño, o muchos canales pequeños. Ambos factores son relevantes para el análisis biomecánico.

### 6. Exportación de Datos

Para un análisis más detallado o para incluir los resultados en informes:

1. Use el botón "Guardar Imagen" en la pestaña de visualización para guardar la representación visual
2. Use el botón "Exportar a Excel" en la pestaña de datos para guardar todas las estadísticas
   - El archivo Excel incluirá datos detallados de cada cuadrante
   - Esta información puede utilizarse en análisis estadísticos posteriores o para alimentar modelos paramétricos

## Ejemplos de Uso

### Ejemplo 1: Análisis Básico de Distribución

1. Ejecute la aplicación y cargue una imagen histológica junto con su archivo Excel de detecciones
2. Observe el cuadrante resaltado en rojo (mayor densidad)
3. Compare las estadísticas entre diferentes cuadrantes
4. Exporte los resultados para documentación

### Ejemplo 2: Comparación de Muestras

1. Analice múltiples muestras del mismo tipo de hueso
2. Guarde las imágenes y datos de cada análisis
3. Compare las distribuciones entre diferentes muestras
4. Identifique patrones consistentes o anomalías en la distribución espacial

### Ejemplo 3: Integración con Investigación Biomecánica

1. Analice una muestra específica y exporte los datos a Excel
2. Utilice estos datos para alimentar modelos biomecánicos
3. Correlacione la distribución de canales con propiedades mecánicas del hueso
4. Integre los resultados en el diseño de estructuras biomiméticas

## Solución de Problemas

### Problemas Comunes y Soluciones

| Problema | Causa Posible | Solución |
|----------|---------------|----------|
| La aplicación no inicia | Entorno Python incorrecto | Verifique que está usando el entorno correcto con todas las dependencias instaladas |
| Error al cargar la imagen | Formato no soportado | Convierta la imagen a formato PNG o JPG usando un editor de imágenes |
| Error al cargar Excel | Formato de Excel incompatible | Asegúrese de usar un archivo Excel generado por Detection App sin modificaciones |
| Visualización incorrecta | Resolución de pantalla baja | Usar una pantalla con mayor resolución o redimensionar la ventana |
| Error "tensor" en consola | Formato de datos inesperado | La aplicación maneja este error automáticamente; puede ignorar los mensajes en consola |

### Mensajes de Error Específicos

- **"Error durante el análisis"**: Revise la consola para detalles. Generalmente ocurre por incompatibilidad entre la imagen y el archivo Excel.
- **"Error al cargar el archivo Excel"**: Asegúrese de que el archivo existe y tiene el formato correcto con columnas "Center X", "Center Y" y "Ellipse Area (pixels^2)".
- **"Error al guardar"**: Verifique que tiene permisos de escritura en la ubicación seleccionada.

## Funcionalidades Avanzadas

### Personalización del Análisis

Aunque la interfaz no expone estas opciones, usuarios avanzados pueden modificar el código para:

1. **Cambiar el número de cuadrantes**: Modificar la matriz de división (por ejemplo, 4×4 en lugar de 3×3)
2. **Ajustar criterios de importancia**: Usar densidad en lugar de área total para destacar cuadrantes
3. **Personalizar la visualización**: Cambiar colores, grosores de línea o formato de texto

### Integración con Workflows Científicos

Breaking App está diseñada para integrarse en flujos de trabajo científicos más amplios:

1. **Investigación histológica**:
   - Análisis cuantitativo de heterogeneidad tisular
   - Comparación de patrones entre muestras sanas y patológicas

2. **Modelado biomecánico**:
   - Datos para simulaciones de elementos finitos
   - Validación de modelos de comportamiento óseo

3. **Bioingeniería y diseño paramétrico**:
   - Generación de distribuciones para modelos en Grasshopper
   - Diseño de estructuras sintéticas con patrones biológicamente inspirados

## Limitaciones Actuales

- La aplicación asume una división uniforme en 9 cuadrantes, que puede no reflejar la anatomía real del hueso
- El análisis es puramente 2D, sin considerar la estructura tridimensional
- Los resultados dependen de la precisión de las detecciones previas realizadas por Detection App

## Desarrollo Futuro

Las próximas versiones de Breaking App podrían incluir:

- División adaptativa basada en características anatómicas
- Análisis de clusters para identificar patrones de distribución
- Integración de estadísticas más avanzadas
- Exportación directa a formatos para modelado 3D

## Soporte y Contacto

Para soporte técnico o consultas sobre esta aplicación, contacte al equipo de desarrollo del proyecto Phygital Human Bone.

---

Este manual fue creado para la versión 1.0 de Breaking App, parte del proyecto Phygital Human Bone.
