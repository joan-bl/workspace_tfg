# Breaking App - Análisis por Cuadrantes de Canales de Havers

## Descripción General

Breaking App es una herramienta especializada para el análisis espacial de canales de Havers en tejido óseo, diseñada como complemento de la Detection App dentro del proyecto Phygital Human Bone. Esta aplicación divide las imágenes histológicas analizadas en treinta y seis cuadrantes (matriz 6×6) y realiza un análisis detallado de la distribución espacial de los canales, identificando zonas de mayor fragilidad y posibles caminos de propagación de fracturas.


## Características Principales

- **Análisis por cuadrantes**: División de la imagen en 36 regiones (matriz 6×6) para análisis espacial localizado
- **Identificación de zonas frágiles**: Detección automática del cuadrante más propenso a fractura basado en múltiples factores biomecánicos
- **Predicción de propagación de fractura**: Identificación del camino de menor resistencia a través de cuadrantes contiguos de baja densidad
- **Reconstrucción visual de detecciones**: Representación gráfica de los canales sobre la imagen original
- **Análisis cuantitativo por región**:
  - Cantidad de canales por cuadrante
  - Área promedio por canal
  - Tamaño del canal más grande
  - Factor de tamaño (relación entre canal más grande y promedio)
  - Densidad de canales (número/área)
  - Puntuación de fragilidad
- **Visualización avanzada**:
  - Imagen con cuadrantes delimitados y codificados por color
  - Resaltado del cuadrante más frágil (rojo) y camino de propagación (azul)
  - Superposición de métricas sobre la imagen
- **Exportación de resultados**:
  - Informes en formato Excel
  - Imágenes de análisis en formato PNG
- **Interfaz gráfica intuitiva**: Diseñada para facilitar la interpretación de resultados

## Fundamentos Biomecánicos

La aplicación implementa un modelo biomecánico fundamentado en investigaciones recientes sobre fragilidad ósea:

1. **Fragilidad ósea**: En el hueso cortical, la fragilidad está influenciada principalmente por:
   - **Menor densidad de osteonas** (y canales de Havers), que reduce la capacidad para distribuir fuerzas mecánicas
   - **Canales agrandados**, que sugieren remodelación ósea patológica o envejecimiento
   - **Mayor área relativa ocupada por canales**, que indica menor matriz mineralizada disponible

2. **Propagación de fracturas**: Las fracturas tienden a propagarse siguiendo el camino de menor resistencia, que en el tejido óseo corresponde a áreas con:
   - Menor densidad de canales
   - Canales más dispersos
   - Zonas con menor mineralización entre canales

## Estructura del Código

El archivo `breaking_app.py` está organizado en los siguientes módulos funcionales:

```
breaking_app.py
├── Funciones de configuración de interfaz
│   ├── configure_window()
│   └── configure_button()
├── Funciones de procesamiento de imágenes
│   └── reconstruir_imagen_con_detecciones()
├── Funciones de análisis
│   └── analizar_cuadrantes()
├── Funciones de visualización
│   └── visualizar_resultados_cuadrantes()
└── Función principal main()
```

## Tecnologías Utilizadas

- **Python 3.7+**: Lenguaje de programación base
- **OpenCV (cv2)**: Procesamiento y manipulación de imágenes, dibujo de cuadrantes y marcadores
- **NumPy**: Procesamiento numérico y análisis de datos
- **Pandas**: Manejo de datos estructurados y generación de informes
- **Matplotlib**: Visualización de datos (opcional para análisis adicionales)
- **Tkinter**: Creación de la interfaz gráfica de usuario
- **PIL (Python Imaging Library)**: Manipulación adicional de imágenes para la interfaz

## Algoritmo de Análisis de Fragilidad

La aplicación implementa un sofisticado algoritmo de análisis de fragilidad ósea que combina múltiples factores:

### 1. Cálculo de la Puntuación de Fragilidad

```
Dado que ya tienemos una red neuronal entrenada para detectar canales de Havers (y no para segmentar hueso del fondo), creo que podemos implementar un enfoque más práctico:
Enfoque sin segmentación de hueso:

Filtrar cuadrantes periféricos: Ignorar completamente los cuadrantes que tengan muy pocos canales (por ejemplo, menos de 3-5 canales), ya que probablemente sean áreas con poco hueso o ninguno.

Usar densidad relativa: Calcular la fragilidad como:
Fragilidad = (Área total de canales) / (Número de canales)
Esto nos da el área promedio por canal.

Normalizar por número de canales: Dar más peso a los cuadrantes con mayor número de canales, ya que es más probable que representen áreas significativas de hueso:
Fragilidad ajustada = Fragilidad × log(1 + Número de canales)
Esto aumenta la importancia de áreas con muchos canales, pero de forma logarítmica para no penalizar demasiado a áreas con menos canales.

Incluir factor de tamaño: Añadir un componente que considere si hay canales particularmente grandes:
Factor tamaño = Área del canal más grande / Área promedio

Fórmula final:
Puntuación final = Fragilidad ajustada × (1 + Factor tamaño)

Este enfoque:

No requiere segmentar el hueso
Minimiza el impacto de los bordes con pocos canales
Prioriza áreas con canales grandes
Da más peso a áreas con suficientes canales para ser relevantes
Puntuación de Fragilidad = Área promedio × log(número de canales) × (1 + Factor de tamaño)
```

Donde:
- **Área promedio**: El área promedio por canal en el cuadrante
- **log(número de canales)**: Logaritmo del número de canales (normaliza el impacto del número de canales)
- **Factor de tamaño**: Relación entre el canal más grande y el promedio `(tamaño_máximo / promedio)`

Esta fórmula prioriza cuadrantes que tienen:
- Canales de mayor tamaño promedio
- Una cantidad significativa de canales (ponderada logarítmicamente)
- Presencia de canales anormalmente grandes respecto al promedio

### 2. Detección de Caminos de Propagación

Para identificar el posible camino de propagación, el algoritmo:
1. Identifica todos los cuadrantes contiguos al más frágil
2. Calcula la densidad (canales por área) de cada cuadrante contiguo
3. Selecciona el cuadrante contiguo con la menor densidad de canales

### 3. Filtrado de Cuadrantes

Para asegurar resultados estadísticamente significativos:
- Se excluyen del análisis cuadrantes con menos de 6 canales
- Se excluyen los cuadrantes centrales (que corresponden normalmente a la cavidad medular)
- Se aplican marcas visuales claras para distinguir cuadrantes válidos e inválidos

## Flujo de Trabajo Detallado

1. **Carga de archivos de entrada**:
   - Imagen original analizada previamente
   - Archivo Excel generado por Detection App con las coordenadas y áreas de los canales

2. **Reconstrucción de la imagen con detecciones**:
   - Representación visual de cada canal como un círculo

3. **Análisis por cuadrantes**:
   - División de la imagen en 36 cuadrantes (matriz 6×6)
   - Clasificación de cada canal en su cuadrante correspondiente
   - Cálculo de métricas por cuadrante:
     - Número de canales
     - Área total ocupada
     - Área promedio por canal
     - Tamaño del canal más grande
     - Factor de tamaño
     - Densidad de canales
     - Puntuación de fragilidad

4. **Visualización de resultados**:
   - Generación de imagen con cuadrantes delimitados
   - Marcado en rojo del cuadrante más frágil
   - Marcado en azul del cuadrante contiguo de menor densidad
   - Superposición de métricas clave sobre cada cuadrante

5. **Presentación interactiva**:
   - Visualización a través de una interfaz gráfica con pestañas
   - Datos detallados por cuadrante
   - Explicación de los criterios de selección
   - Opción para exportar datos a Excel
   - Posibilidad de guardar las imágenes de análisis

## Importancia Biomecánica del Análisis por Cuadrantes

El análisis por cuadrantes proporciona información crítica para diversas aplicaciones biomédicas:

1. **Investigación de Fractura Ósea**: Permite identificar regiones con mayor susceptibilidad a fractura y predecir posibles patrones de propagación.

2. **Caracterización de Patologías Óseas**: Ayuda a identificar patrones anormales en la distribución de canales que podrían indicar condiciones como osteoporosis u osteopenia.

3. **Evaluación de Tratamientos**: Posibilita el seguimiento de cambios en la microestructura ósea en respuesta a tratamientos o intervenciones.

4. **Biomimética Avanzada**: Proporciona datos para crear modelos sintéticos con distribuciones realistas de canales que reflejan la heterogeneidad natural del hueso.

## Integración con el Flujo de Trabajo

Breaking App está diseñada para integrarse perfectamente con otras herramientas del proyecto:

1. **Entrada**: Utiliza los resultados de Detection App como datos de entrada
2. **Proceso**: Realiza un análisis espacial especializado
3. **Salida**: Genera datos que pueden alimentar modelos paramétricos en Grasshopper

Este enfoque modular permite un flujo de trabajo fluido desde la imagen histológica original hasta la generación de modelos biomiméticos.

## Requisitos

- Python 3.7 o superior
- Mínimo 8GB de RAM
- Dependencias específicas:
  ```
  opencv-python
  pandas
  numpy
  matplotlib
  pillow
  ```

## Instalación

1. Configurar entorno con Anaconda (recomendado):
   ```
   conda create -n osteona python=3.9
   conda activate osteona
   pip install opencv-python pandas numpy matplotlib pillow
   ```

2. Ejecutar la aplicación:
   ```
   python breaking_app.py
   ```

## Personalización y Opciones Avanzadas

La aplicación permite diversas personalizaciones a través de modificaciones en el código:

- **Umbral mínimo de canales**: Por defecto se ignoran cuadrantes con menos de 6 canales, pero este valor puede ajustarse
- **Fórmula de fragilidad**: Los componentes y pesos de la fórmula pueden modificarse según necesidades específicas
- **Criterio de propagación**: Por defecto se usa la densidad mínima, pero podrían implementarse otros criterios
- **Esquema de colores**: Los colores utilizados para marcar los cuadrantes pueden personalizarse

## Limitaciones Actuales y Desarrollo Futuro

### Limitaciones
- División en cuadrantes regulares, sin adaptación a la forma anatómica del hueso
- Análisis en 2D, sin considerar la estructura tridimensional completa
- Dependencia de la precisión de las detecciones realizadas por Detection App

### Desarrollos Futuros
- Implementación de divisiones adaptativas basadas en la anatomía del hueso
- Análisis de patrones de distribución utilizando algoritmos de clustering
- Integración de modelos predictivos para estimar resistencia a fractura
- Exportación directa a formatos compatibles con software de modelado 3D

## Autores

- Joan Blanch Jiménez - Desarrollador principal
- Equipo del proyecto Phygital Human Bone

## Licencia

Este proyecto está licenciado bajo MIT License.