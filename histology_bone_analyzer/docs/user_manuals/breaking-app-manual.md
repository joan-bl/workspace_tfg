# Manual de Usuario: Breaking App

## Introducción

Breaking App es una herramienta especializada para el análisis espacial de canales de Havers en imágenes histológicas de tejido óseo. Esta aplicación complementa a Detection App dividiendo la imagen en treinta y seis cuadrantes para analizar la distribución de canales, identificar zonas de mayor fragilidad y predecir posibles caminos de propagación de fracturas.

Esta herramienta forma parte del proyecto "Phygital Human Bone", que busca crear modelos biomiméticos de hueso humano mediante algoritmos paramétricos, machine learning y fabricación aditiva.

## Propósito y Contexto

El análisis por cuadrantes es esencial para comprender la heterogeneidad espacial en la distribución de canales de Havers, lo que tiene importantes implicaciones para:

- Determinar zonas de mayor fragilidad ósea
- Predecir posibles caminos de propagación de fracturas
- Comprender procesos de remodelación ósea
- Generar modelos biomiméticos más precisos

Breaking App automatiza este análisis, proporcionando visualizaciones claras y métricas cuantitativas para cada región del tejido.

## Características Principales

- **Análisis por cuadrantes**: División de la imagen en 36 regiones (matriz 6×6)
- **Identificación de zonas frágiles**: Detección automática del cuadrante más propenso a fracturarse
- **Predicción de propagación**: Identificación del camino de menor resistencia
- **Análisis cuantitativo por región**: Métricas detalladas para cada cuadrante
- **Visualizaciones interactivas**: Imagen con cuadrantes codificados por color
- **Exportación de resultados**: Guardado de imágenes e informes en Excel

## Fundamentos Teóricos

La aplicación implementa un modelo de análisis basado en investigaciones recientes sobre fragilidad ósea:

1. **Determinación de zonas frágiles**:
   - Áreas con pocos canales pero de gran tamaño son más propensas a fractura
   - La puntuación de fragilidad se calcula como:
     ```
     Fragilidad = Área promedio × log(número de canales) × (1 + Factor de tamaño)
     ```
   - El factor de tamaño (`tamaño_máximo / promedio`) identifica cuadrantes con canales anormalmente grandes

2. **Predicción de propagación de fractura**:
   - Las fracturas se propagan por el camino de menor resistencia
   - Se identifica el cuadrante contiguo con la menor densidad de canales
   - La baja densidad indica zonas con menos obstáculos para la propagación de la fractura

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

1. Al iniciar la aplicación, verá la pantalla principal con el título "Análisis de Fragilidad Ósea por Cuadrantes"
2. Haga clic en el botón "Iniciar Análisis"
3. Se abrirá un cuadro de diálogo para seleccionar la imagen original
   - Seleccione la imagen histológica que desea analizar (JPG, JPEG o PNG)
4. A continuación, se abrirá otro cuadro de diálogo para seleccionar el archivo Excel
   - Seleccione el archivo Excel generado previamente por Detection App
   - Este archivo debe contener las coordenadas y áreas de los canales detectados

### 3. Procesamiento de la Imagen

Una vez seleccionados los archivos, la aplicación procesará automáticamente:

1. Reconstruirá la imagen con las detecciones de canales basándose en los datos del Excel
2. Dividirá la imagen en 36 cuadrantes (matriz 6×6)
3. Clasificará cada canal detectado en su cuadrante correspondiente
4. Calculará métricas detalladas para cada cuadrante:
   - Área total y promedio
   - Factor de tamaño
   - Densidad de canales
   - Puntuación de fragilidad
5. Identificará el cuadrante más frágil (mayor puntuación de fragilidad)
6. Identificará el cuadrante contiguo con menor densidad (camino de propagación)
7. Generará una visualización con los cuadrantes marcados:
   - Rojo para el cuadrante más frágil
   - Azul para el cuadrante de menor densidad contiguo
   - Gris para los cuadrantes centrales
   - X para cuadrantes con menos de 6 canales (ignorados)

Este proceso puede tardar desde unos segundos hasta un minuto, dependiendo del tamaño de la imagen y el número de canales detectados.

### 4. Visualización de Resultados

Después del procesamiento, la aplicación mostrará una nueva ventana con dos pestañas:

#### Pestaña "Visualización"

Muestra la imagen dividida en 36 cuadrantes con:
- Líneas blancas que delimitan cada cuadrante
- Rectángulo rojo semitransparente que marca el cuadrante más frágil
- Rectángulo azul semitransparente que marca el cuadrante de propagación
- Rectángulos grises para los cuadrantes centrales
- Una "X" en cuadrantes con menos de 6 canales (ignorados)
- Texto en cada cuadrante mostrando:
  - A: Área total de canales
  - C: Número de canales
  - F: Puntuación de fragilidad normalizada (0-100)
  - D: Densidad de canales

En esta pestaña encontrará un botón "Guardar Imagen" que le permitirá guardar esta visualización en formato PNG.

#### Pestaña "Datos por Cuadrante"

Presenta un informe textual detallado con:
- Información de cada cuadrante (numerados del 1 al 36)
- Ubicación (fila y columna) de cada cuadrante
- Estadísticas completas:
  - Área total de canales
  - Número de canales
  - Área promedio por canal
  - Área del canal más grande
  - Factor de tamaño
  - Densidad de canales
  - Puntuación de fragilidad
- Explicación del motivo de selección para cuadrantes destacados

En esta pestaña encontrará un botón "Exportar a Excel" que le permitirá guardar todos estos datos en un archivo Excel para análisis adicionales.

### 5. Interpretación de los Resultados

#### Cuadrante Rojo (Más Frágil)
- Representa la zona con mayor probabilidad de iniciar una fractura
- Su selección se basa en la fórmula de fragilidad que considera:
  - El tamaño promedio de los canales
  - La presencia de canales anormalmente grandes
  - Un número significativo de canales (ponderado logarítmicamente)
- Valores altos de fragilidad indican zonas donde la estructura ósea está más comprometida

#### Cuadrante Azul (Camino de Propagación)
- Representa la dirección más probable de propagación de una fractura
- Es el cuadrante contiguo al más frágil con la menor densidad de canales
- La baja densidad indica menos obstáculos para la propagación de la fractura
- Sirve como predictor del camino que seguiría una fractura iniciada en el cuadrante rojo

#### Cuadrantes Ignorados (con X)
- Cuadrantes con menos de 6 canales
- Se excluyen por no tener suficiente información estadística
- Normalmente corresponden a bordes de la imagen o áreas con poco tejido óseo

#### Cuadrantes Centrales (Gris)
- Representan las cuatro regiones centrales de la imagen
- Típicamente corresponden a la cavidad medular o áreas no relevantes para el análisis
- Se excluyen automáticamente del análisis de fragilidad

### 6. Exportación de Datos

Para un análisis más detallado o para incluir los resultados en informes:

1. Use el botón "Guardar Imagen" en la pestaña de visualización para guardar la representación visual
2. Use el botón "Exportar a Excel" en la pestaña de datos para guardar todas las estadísticas
   - El archivo Excel incluirá datos detallados de cada cuadrante
   - Esta información puede utilizarse en análisis estadísticos posteriores o para alimentar modelos paramétricos

## Ejemplos de Uso

### Ejemplo 1: Análisis de Fragilidad Ósea

1. Ejecute la aplicación y cargue una imagen histológica junto con su archivo Excel de detecciones
2. Observe el cuadrante resaltado en rojo (mayor fragilidad)
3. Note el cuadrante azul (posible dirección de propagación)
4. Compare las puntuaciones de fragilidad entre diferentes cuadrantes
5. Exporte los resultados para documentación

### Ejemplo 2: Comparación de Muestras

1. Analice múltiples muestras del mismo tipo de hueso
2. Guarde las imágenes y datos de cada análisis
3. Compare las distribuciones entre diferentes muestras
4. Identifique patrones consistentes o anomalías en las zonas de fragilidad
5. Determine si las direcciones de propagación son similares entre muestras

### Ejemplo 3: Integración con Investigación Biomecánica

1. Analice una muestra específica y exporte los datos a Excel
2. Utilice estos datos para alimentar modelos biomecánicos
3. Correlacione las puntuaciones de fragilidad con propiedades mecánicas del hueso
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
| No se detectan cuadrantes de interés | Pocos canales por cuadrante | Asegúrese de que su imagen contenga suficientes canales por cuadrante (mínimo 6) |

### Mensajes de Error Específicos

- **"Error durante el análisis"**: Revise la consola para detalles. Generalmente ocurre por incompatibilidad entre la imagen y el archivo Excel.
- **"Error al cargar el archivo Excel"**: Asegúrese de que el archivo existe y tiene el formato correcto con columnas "Center X", "Center Y" y "Ellipse Area (pixels^2)".
- **"Error al guardar"**: Verifique que tiene permisos de escritura en la ubicación seleccionada.

## Aspectos Técnicos

### Cálculos Realizados

Para cada cuadrante, la aplicación calcula:

1. **Área total de canales**:
   ```
   Área total = Suma de áreas de todos los canales en el cuadrante
   ```

2. **Área promedio por canal**:
   ```
   Área promedio = Área total / Número de canales
   ```

3. **Factor de tamaño**:
   ```
   Factor de tamaño = Área del canal más grande / Área promedio
   ```
   
4. **Densidad de canales**:
   ```
   Densidad = Número de canales / Área del cuadrante
   ```

5. **Puntuación de fragilidad**:
   ```
   Fragilidad = Área promedio × log(número de canales) × (1 + 0.5*(Factor de tamaño - 1))
   ```

### Criterios de Selección

1. **Cuadrante más frágil (rojo)**:
   - Se selecciona el cuadrante con la mayor puntuación de fragilidad
   - Solo se consideran cuadrantes con al menos 6 canales
   - Se excluyen los cuadrantes centrales

2. **Cuadrante de propagación (azul)**:
   - Se identifican todos los cuadrantes contiguos al más frágil
   - Se selecciona el cuadrante contiguo con la menor densidad de canales
   - Solo se consideran cuadrantes con al menos 6 canales
   - Se excluyen los cuadrantes centrales

## Conclusión

Breaking App proporciona una herramienta poderosa para el análisis espacial de microestructuras óseas, identificando zonas de mayor fragilidad y prediciendo posibles caminos de propagación de fracturas. Esta información es invaluable para la investigación biomecánica, el desarrollo de modelos biomiméticos y la comprensión de patologías óseas.

---

Este manual fue creado para la versión 2.0 de Breaking App, parte del proyecto Phygital Human Bone.