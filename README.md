# Phygital Human Bone - Análisis de Canales de Havers

## Resumen General del Proyecto

Este proyecto se centra en el desarrollo de una aplicación para analizar imágenes histológicas de secciones óseas, específicamente para detectar canales de Havers y osteonas en tejido óseo cortical. Esta herramienta forma parte del proyecto "Phygital Human Bone", que busca crear modelos biomiméticos de hueso humano mediante algoritmos paramétricos, machine learning y fabricación aditiva.

## Estructura del Repositorio

El repositorio contiene varios componentes principales:

### Directorios Principales:
1. `detection_app`: Contiene el código principal para la detección de canales de Havers
2. `breaking_app`: Incluye código para analizar las imágenes por cuadrantes
3. `utility codes`: Scripts de utilidad para entrenamiento, comprobación de GPU y conversión de imágenes

### Códigos Principales:
1. **fixed-phygital-code.py**: Versión mejorada del código para detección de canales de Havers
2. **cuadrantes-analyzer.py**: Herramienta para analizar la distribución espacial dividiendo la imagen en 9 cuadrantes
3. **train_model.py**: Script para entrenar el modelo YOLO con los datos de canales de Havers
4. **topng5mb.py**: Utilidad para convertir imágenes TIF a PNG reduciendo su tamaño

## Análisis Técnico

### Enfoque de Machine Learning
- Utiliza el modelo YOLO (You Only Look Once) para la detección de osteonas
- El entrenamiento del modelo se realizó durante 100 epochs con un batch size de 16
- El código divide las imágenes grandes en 150 segmentos (15×10) para mejorar la precisión de detección

### Flujo del Programa Principal
1. Selección de una imagen histológica por parte del usuario
2. División de la imagen en segmentos más pequeños
3. Aplicación de un modelo YOLO previamente entrenado para detectar canales de Havers
4. Cálculo de coordenadas, áreas y distribución de los canales
5. Generación de visualizaciones (mapa de coordenadas, mapa de calor)
6. Presentación de resultados en una interfaz gráfica

### Análisis por Cuadrantes
Herramienta complementaria que:
1. Divide la imagen en 9 cuadrantes (matriz 3×3)
2. Analiza la distribución de canales por cuadrante
3. Identifica el cuadrante con mayor densidad de canales
4. Permite exportar los resultados a Excel

## Contexto del Proyecto

Este trabajo se enmarca en un esfuerzo más amplio para desarrollar modelos biomiméticos de hueso humano. La parte específica del proyecto está enfocada en la sección de Inteligencia Artificial, desarrollando herramientas para analizar histologías de secciones óseas.

El objetivo de toda esta investigación es crear modelos sintéticos de hueso que repliquen fielmente las propiedades biomecánicas del hueso real, con aplicaciones potenciales en prótesis, investigación biomecánica y medicina regenerativa.

## Tecnologías Utilizadas

- **Lenguaje**: Python
- **Librerías principales**: OpenCV, PyTorch, Ultralytics (YOLO), Pandas, NumPy, Matplotlib, Tkinter
- **Interfaz gráfica**: Tkinter para crear una GUI amigable
- **Visualización de datos**: Matplotlib para generar gráficos y mapas de calor
