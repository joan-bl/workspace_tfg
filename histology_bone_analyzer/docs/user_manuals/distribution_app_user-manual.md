# Manual de Usuario: Femur Osteona Distributor

## Introducción

El Femur Osteona Distributor es una herramienta diseñada para generar distribuciones realistas de osteonas en diferentes secciones del fémur humano. Esta aplicación sirve como complemento perfecto para proyectos de modelado en Grasshopper, permitiendo la generación de modelos óseos biomiméticos más precisos.

Este manual explica paso a paso cómo utilizar la aplicación, desde la configuración inicial hasta la exportación de datos para su uso en Grasshopper.

## Instalación y Ejecución

### Requisitos Previos
- Python 3.7 o superior
- Las siguientes bibliotecas de Python:
  - tkinter (generalmente incluida con Python)
  - numpy
  - matplotlib
  - pandas
  - Pillow (PIL)

### Pasos de Instalación

1. Instale las bibliotecas necesarias usando pip:
```
pip install numpy matplotlib pandas pillow
```

2. Descargue el archivo `femur_osteona_distributor.py`

3. Ejecute la aplicación:
```
python femur_osteona_distributor.py
```

## Interfaz de Usuario

La aplicación está organizada en tres pestañas principales:

1. **Parámetros**: Configuración de las características del fémur
2. **Visualización**: Representación gráfica de los resultados
3. **Exportación**: Opciones para exportar los datos

## Guía de Uso Paso a Paso

### 1. Configuración de Parámetros

#### 1.1 Parámetros Generales

En la sección superior, configure:
- **Longitud del Fémur (cm)**: Ingrese la longitud total del fémur que desea modelar (valor predeterminado: 45 cm)

#### 1.2 Parámetros por Sección

Para cada sección del fémur (Epífisis Proximal, Metáfisis Proximal, Diáfisis, Metáfisis Distal, Epífisis Distal), configure:

| Parámetro | Descripción | Valores Recomendados |
|-----------|-------------|----------------------|
| % Longitud | Porcentaje de la longitud total | Los cinco valores deben sumar 100% |
| Densidad | Cantidad de osteonas por cm² | 20-60 osteonas/cm² |
| Tamaño | Diámetro medio en micrómetros | 150-250 μm |
| Variabilidad | Irregularidad en la distribución | 0.1-0.9 (0=regular, 1=muy irregular) |

**Importante**: Asegúrese de que los porcentajes de longitud de todas las secciones sumen exactamente 100%.

#### 1.3 Generación de Resultados

Después de configurar todos los parámetros, haga clic en el botón **"Calcular Distribución"**. La aplicación procesará los datos y mostrará:

- Un resumen de los parámetros configurados
- Información sobre la longitud absoluta de cada sección
- Número total de osteonas generadas
- Distribución de osteonas por sección

### 2. Visualización de Resultados

La pestaña de visualización muestra dos gráficos:

- **Gráfico Izquierdo**: Perfil del fémur con códigos de colores para cada sección
- **Gráfico Derecho**: Distribución de osteonas a lo largo del hueso, donde:
  - La posición horizontal representa la ubicación a lo largo del fémur
  - El color indica la sección a la que pertenece la osteona
  - El tamaño del punto representa el tamaño relativo de la osteona

#### 2.1 Opciones de Visualización

- **Actualizar Visualización**: Regenera los gráficos con los datos actuales
- **Guardar Imagen**: Guarda los gráficos como archivo PNG, JPEG o PDF

### 3. Exportación de Datos

La pestaña de exportación ofrece varias opciones para guardar los resultados:

#### 3.1 Opciones de Exportación

- **Exportar a CSV**: Genera un archivo CSV ideal para importar en Grasshopper
- **Exportar a JSON**: Crea un archivo JSON con toda la información del modelo
- **Exportar Informe Completo**: Genera un conjunto de archivos incluyendo:
  - Archivo CSV con datos de osteonas
  - Archivo JSON con configuración completa
  - Imágenes de visualización
  - Informe HTML con resumen e instrucciones

#### 3.2 Previsualización de Datos

El área de texto muestra una vista previa de los primeros 20 registros de datos, con el formato:
```
section_name, position_z_cm, angle_degrees, size_um
```

## Integración con Grasshopper

### Proceso de Importación

1. Genere y exporte los datos en formato CSV
2. En Grasshopper, use el componente "Read File" para importar el archivo CSV
3. Separe las columnas de datos usando el componente "Split Text"
4. Convierta los valores de texto a números usando "Text to Number"

### Transformación a Coordenadas 3D

Para cada osteona, utilice:
- `position_z_cm` directamente como coordenada Z
- `angle_degrees` para calcular las coordenadas X e Y:
  ```
  X = radio_del_hueso * cos(angle_degrees * π/180)
  Y = radio_del_hueso * sin(angle_degrees * π/180)
  ```
- `size_um` para determinar el diámetro de la osteona

### Ejemplo de Definición en Grasshopper

1. Importe el CSV con el componente "Read File"
2. Divida las líneas con el componente "Split Text" (separador: nueva línea)
3. Descarte la primera línea (encabezados)
4. Para cada línea restante:
   - Divida por comas para obtener los valores individuales
   - Convierta los valores numéricos con "Text to Number"
   - Utilice "Construct Point" para crear puntos 3D
   - Genere círculos o esferas basados en el tamaño de la osteona

## Consejos y Solución de Problemas

### Consejos Útiles

- Comience con los valores predeterminados y realice ajustes graduales
- Para resultados más realistas, utilice variabilidad alta en las epífisis y baja en la diáfisis
- Las metáfisis suelen tener valores intermedios entre la diáfisis y las epífisis

### Solución de Problemas Comunes

| Problema | Causa Posible | Solución |
|----------|--------------|----------|
| Los porcentajes no suman 100% | Error en los valores ingresados | Ajuste los porcentajes para que sumen exactamente 100% |
| No se genera ninguna osteona | Valores de densidad demasiado bajos | Aumente los valores de densidad en las secciones |
| Error al exportar | Permisos de escritura insuficientes | Elija una ubicación diferente para guardar los archivos |
| Visualización incorrecta | Valores extremos en los parámetros | Utilice valores dentro de los rangos recomendados |

## Personalización Avanzada

Para usuarios con conocimientos de Python, el código puede modificarse para:

- Cambiar la forma del perfil del fémur
- Ajustar los algoritmos de distribución
- Añadir nuevos parámetros o características
- Integrar con otras herramientas de modelado

---

## Ejemplo Completo: De la Aplicación a Grasshopper

### Escenario: Modelado de Fémur de 40 cm

1. **Configuración de Parámetros**:
   - Longitud del Fémur: 40 cm
   - Epífisis Proximal: 15%, densidad 25 ost/cm², tamaño 220 μm, variabilidad 0.8
   - Metáfisis Proximal: 10%, densidad 40 ost/cm², tamaño 190 μm, variabilidad 0.5
   - Diáfisis: 50%, densidad 60 ost/cm², tamaño 150 μm, variabilidad 0.2
   - Metáfisis Distal: 10%, densidad 40 ost/cm², tamaño 190 μm, variabilidad 0.5
   - Epífisis Distal: 15%, densidad 25 ost/cm², tamaño 220 μm, variabilidad 0.8

2. **Cálculo y Exportación**:
   - Haga clic en "Calcular Distribución"
   - Revise la visualización para verificar el resultado
   - Exporte a CSV para Grasshopper

3. **En Grasshopper**:
   - Importe el CSV
   - Cree la geometría del fémur (un cilindro modificado con la forma apropiada)
   - Coloque las osteonas según las coordenadas calculadas
   - Genere geometría 3D para cada osteona

4. **Resultado Final**:
   - Un modelo 3D del fémur con distribución realista de osteonas en cada sección
   - Listo para análisis biomecánico o fabricación mediante impresión 3D

---

*Para asistencia técnica adicional o para reportar errores, por favor contacte al equipo de desarrollo del proyecto Phygital Human Bone.*