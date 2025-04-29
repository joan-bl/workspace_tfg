# Breaking App - Análisis por Cuadrantes de Canales de Havers

## Descripción General

Breaking App es una herramienta especializada para el análisis espacial de canales de Havers en tejido óseo, diseñada como complemento de la Detection App dentro del proyecto Phygital Human Bone. Esta aplicación divide las imágenes histológicas analizadas en nueve cuadrantes (matriz 3×3) y realiza un análisis detallado de la distribución espacial de los canales, identificando zonas de mayor densidad y calculando estadísticas específicas por región.

![Ejemplo de Análisis por Cuadrantes](../images/breaking_app_example.png)

## Características Principales

- **Análisis por cuadrantes**: División de la imagen en 9 regiones (matriz 3×3) para análisis espacial localizado
- **Identificación de zonas críticas**: Detección automática del cuadrante con mayor densidad de canales de Havers
- **Reconstrucción visual de detecciones**: Representación gráfica de los canales sobre la imagen original
- **Análisis cuantitativo por región**:
  - Cantidad de canales por cuadrante
  - Área total y promedio por cuadrante
  - Densidad de canales (número/área)
- **Visualización avanzada**:
  - Imagen con cuadrantes delimitados y codificados por color
  - Resaltado del cuadrante con mayor densidad
  - Superposición de métricas sobre la imagen
- **Exportación de resultados**:
  - Informes en formato Excel
  - Imágenes de análisis en formato PNG
- **Interfaz gráfica intuitiva**: Diseñada para facilitar la interpretación de resultados

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

## Flujo de Trabajo Detallado

1. **Selección de archivos de entrada**:
   - Imagen original analizada previamente
   - Archivo Excel generado por Detection App con las coordenadas y áreas de los canales

2. **Reconstrucción de la imagen con detecciones**:
   - Lectura de la imagen original
   - Procesamiento del archivo Excel para obtener coordenadas
   - Representación de cada canal como un círculo en la imagen

3. **Análisis por cuadrantes**:
   - División de la imagen en 9 cuadrantes iguales (matriz 3×3)
   - Clasificación de cada canal en su cuadrante correspondiente
   - Cálculo de métricas por cuadrante:
     - Número de canales
     - Área total ocupada
     - Área promedio por canal
   - Identificación del cuadrante con mayor área total o densidad

4. **Visualización de resultados**:
   - Generación de imagen con cuadrantes delimitados
   - Marcado del cuadrante con mayor densidad o área
   - Superposición de métricas clave sobre cada cuadrante

5. **Presentación de resultados**:
   - Visualización a través de una interfaz gráfica con pestañas
   - Opción para exportar datos detallados a Excel
   - Posibilidad de guardar las imágenes de análisis

## Detalles de Implementación

### Reconstrucción de Imagen con Detecciones

La función `reconstruir_imagen_con_detecciones()` toma la imagen original y los datos del archivo Excel para reconstruir una representación visual de los canales detectados:

```python
def reconstruir_imagen_con_detecciones(imagen_original, excel_path, output_path):
    # Cargar imagen original
    imagen = cv2.imread(imagen_original)
    
    # Cargar datos de detecciones desde Excel
    df = pd.read_excel(excel_path)
    
    # Dibujar cada canal detectado
    for i, row in df.iterrows():
        # Procesar valores (manejar posibles tensores o strings)
        centro_x = int(float(procesar_valor(row['Center X'])))
        centro_y = int(float(procesar_valor(row['Center Y'])))
        area = float(procesar_valor(row['Ellipse Area (pixels^2)']))
        
        # Calcular radio aproximado basado en el área
        radio = int(np.sqrt(area / np.pi))
        
        # Dibujar círculo en la posición del canal
        cv2.circle(imagen, (centro_x, centro_y), radio, (0, 255, 0), 2)
    
    # Guardar imagen reconstruida
    cv2.imwrite(output_path, imagen)
    
    return imagen
```

Esta función maneja robustamente diferentes formatos de datos, ya que las coordenadas pueden estar almacenadas como cadenas de texto o valores numéricos, e incluso como representaciones de tensores de PyTorch.

### Análisis por Cuadrantes

La función `analizar_cuadrantes()` implementa la división en cuadrantes y el análisis espacial:

```python
def analizar_cuadrantes(imagen, df, output_path):
    height, width = imagen.shape[:2]
    
    # Calcular dimensiones de cuadrantes
    cuad_height = height // 3
    cuad_width = width // 3
    
    # Estructuras para almacenar resultados
    areas_por_cuadrante = np.zeros(9)
    canales_por_cuadrante = [[] for _ in range(9)]
    
    # Clasificar cada canal en su cuadrante
    for i, row in df.iterrows():
        x = int(float(procesar_valor(row['Center X'])))
        y = int(float(procesar_valor(row['Center Y'])))
        area = float(procesar_valor(row['Ellipse Area (pixels^2)']))
        
        # Determinar cuadrante
        cuad_col = min(2, max(0, x // cuad_width))
        cuad_row = min(2, max(0, y // cuad_height))
        cuad_idx = cuad_row * 3 + cuad_col
        
        # Acumular área y guardar referencia
        areas_por_cuadrante[cuad_idx] += area
        canales_por_cuadrante[cuad_idx].append((x, y, area))
    
    # Encontrar cuadrante con mayor área
    cuad_max_area_idx = np.argmax(areas_por_cuadrante)
    
    # Crear visualización
    imagen_con_cuadrantes = imagen.copy()
    
    # Dibujar líneas de cuadrantes
    for i in range(1, 3):
        cv2.line(imagen_con_cuadrantes, (0, i*cuad_height), 
                 (width, i*cuad_height), (255, 255, 255), 2)
        cv2.line(imagen_con_cuadrantes, (i*cuad_width, 0), 
                 (i*cuad_width, height), (255, 255, 255), 2)
    
    # Marcar cuadrante con mayor área
    max_row = cuad_max_area_idx // 3
    max_col = cuad_max_area_idx % 3
    x1 = max_col * cuad_width
    y1 = max_row * cuad_height
    x2 = (max_col + 1) * cuad_width
    y2 = (max_row + 1) * cuad_height
    
    # Dibujar rectángulo semitransparente
    overlay = imagen_con_cuadrantes.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 255), -1)
    cv2.addWeighted(overlay, 0.3, imagen_con_cuadrantes, 0.7, 0, imagen_con_cuadrantes)
    
    # Añadir texto con información por cuadrante
    for i in range(9):
        row = i // 3
        col = i % 3
        text_x = col * cuad_width + 10
        text_y = row * cuad_height + 30
        
        # Texto con información
        cv2.putText(imagen_con_cuadrantes, 
                   f"Area: {areas_por_cuadrante[i]:.1f}", 
                   (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.putText(imagen_con_cuadrantes, 
                   f"Canales: {len(canales_por_cuadrante[i])}", 
                   (text_x, text_y + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Guardar imagen final
    cv2.imwrite(output_path, imagen_con_cuadrantes)
    
    return imagen_con_cuadrantes, areas_por_cuadrante, canales_por_cuadrante
```

### Visualización de Resultados

La función `visualizar_resultados_cuadrantes()` muestra los resultados en una interfaz gráfica con pestañas:

- **Pestaña de visualización**: Muestra la imagen con los cuadrantes analizados
- **Pestaña de datos**: Presenta información detallada por cuadrante

También proporciona opciones para:
- Guardar la imagen del análisis
- Exportar los datos a Excel para análisis adicionales

## Importancia Biomecánica del Análisis por Cuadrantes

El análisis por cuadrantes no es solo una conveniencia visual, sino que tiene importantes implicaciones biomecánicas:

1. **Heterogeneidad estructural**: El tejido óseo no es homogéneo; las diferentes regiones pueden tener densidades variables de canales de Havers según las cargas mecánicas que soportan.

2. **Predicción de zonas de fractura**: Las regiones con distribuciones anómalas de canales pueden ser más propensas a fracturas.

3. **Evaluación de remodelación ósea**: Los patrones de distribución por cuadrantes pueden indicar procesos de remodelación en curso.

4. **Aplicación en biomimética**: Permite replicar patrones naturales de distribución en modelos sintéticos, mejorando su fidelidad estructural.

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

## Instrucciones de Ejecución

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

3. En la interfaz:
   - Seleccionar la imagen original
   - Seleccionar el archivo Excel con los datos de los canales
   - Seguir las instrucciones en pantalla para visualizar y analizar los resultados

## Personalización y Opciones Avanzadas

La aplicación permite diversas personalizaciones a través de modificaciones en el código:

- **Número de cuadrantes**: Aunque la configuración predeterminada es 3×3, puede modificarse para usar una división diferente (por ejemplo, 2×2 o 4×4)
- **Criterio de importancia**: Por defecto se usa el área total, pero puede cambiarse a densidad de canales u otras métricas
- **Esquema de colores**: Los colores utilizados para marcar los cuadrantes pueden personalizarse

## Limitaciones Actuales y Desarrollo Futuro

### Limitaciones
- Actualmente solo trabaja con divisiones regulares (cuadrantes del mismo tamaño)
- El análisis se realiza en 2D, sin considerar la profundidad de las estructuras
- Depende de la precisión de las detecciones realizadas por Detection App

### Desarrollos Futuros
- Implementación de divisiones adaptativas basadas en la anatomía del hueso
- Análisis de patrones de distribución utilizando algoritmos de clustering
- Integración de modelos estadísticos para detectar anomalías en la distribución
- Exportación directa a formatos compatibles con software de modelado 3D

## Contribuir

Si desea contribuir al desarrollo de Breaking App:

1. Bifurque el repositorio
2. Cree una rama para su característica (`git checkout -b feature/nueva-funcionalidad`)
3. Confirme sus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Envíe a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abra una Pull Request

## Autores

- Joan Blanch Jiménez - Desarrollador principal
- Equipo del proyecto Phygital Human Bone

## Licencia

Este proyecto está licenciado bajo MIT License.
