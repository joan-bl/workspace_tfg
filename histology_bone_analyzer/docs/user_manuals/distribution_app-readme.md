# Femur Osteona Distributor

## Descripción General

El Femur Osteona Distributor es una aplicación diseñada para generar y parametrizar la distribución de osteonas en un modelo de fémur humano. Esta herramienta permite crear distribuciones realistas y personalizables de osteonas a lo largo de las diferentes secciones del fémur (epífisis proximal, metáfisis proximal, diáfisis, metáfisis distal y epífisis distal), generando datos que pueden ser utilizados directamente en Grasshopper para la creación de modelos biomiméticos tridimensionales.

## Propósito y Contexto

Esta aplicación fue desarrollada como parte del proyecto "Phygital Human Bone", que busca crear modelos sintéticos de hueso humano mediante algoritmos paramétricos y técnicas de fabricación aditiva. La distribución realista de osteonas es crucial para el desarrollo de modelos de hueso que imiten con precisión las propiedades biomecánicas y estructurales del hueso natural.

El principal problema que resuelve esta herramienta es evitar la generación de patrones homogéneos de osteonas, permitiendo:

1. Crear distribuciones variables según la sección anatómica del hueso
2. Ajustar parámetros de densidad, tamaño y variabilidad en cada zona
3. Exportar datos procesables para Grasshopper

## Características Principales

- **Parametrización basada en longitud**: Toda la distribución se calcula a partir de la longitud total del fémur
- **Personalización por secciones**: Ajustes específicos para cada región del hueso
- **Visualización en tiempo real**: Representación gráfica del fémur y la distribución de osteonas
- **Múltiples opciones de exportación**: CSV (compatible con Grasshopper), JSON e informes HTML
- **Interfaz gráfica intuitiva**: Fácil de usar incluso para usuarios sin experiencia técnica

## Requisitos

- Python 3.7 o superior
- Bibliotecas:
  - tkinter
  - numpy
  - matplotlib
  - pandas
  - Pillow (PIL)

## Instalación

1. Clone o descargue el repositorio:
```
git clone https://github.com/username/femur-osteona-distributor.git
```

2. Instale las dependencias necesarias:
```
pip install numpy matplotlib pandas pillow
```

3. Ejecute la aplicación:
```
python femur_osteona_distributor.py
```

## Guía de Uso

### Pantalla Principal

La aplicación consta de tres pestañas principales:

1. **Parámetros**: Para configurar los valores del fémur y las características de las osteonas
2. **Visualización**: Para ver representaciones gráficas del fémur y la distribución de osteonas
3. **Exportación**: Para exportar los datos en diferentes formatos

### Configuración de Parámetros

#### Parámetros Básicos:
- **Longitud del Fémur (cm)**: Define la longitud total del hueso

#### Parámetros por Sección:
Para cada sección (Epífisis Proximal, Metáfisis Proximal, Diáfisis, Metáfisis Distal, Epífisis Distal):

- **% Longitud**: Porcentaje de la longitud total que ocupa esta sección (los cinco valores deben sumar 100%)
- **Densidad (osteonas/cm²)**: Cantidad aproximada de osteonas por centímetro cuadrado
- **Tamaño (μm)**: Diámetro medio de las osteonas en micrómetros
- **Variabilidad (0-1)**: Grado de variación en la distribución (0 = regular, 1 = muy irregular)

Una vez configurados los parámetros, haga clic en "Calcular Distribución" para generar los resultados.

### Visualización

La pestaña de visualización muestra dos gráficos:

1. **Perfil del Fémur**: Muestra la forma aproximada del hueso con sus diferentes secciones coloreadas
2. **Distribución de Osteonas**: Representa la ubicación y tamaño relativo de las osteonas a lo largo del hueso

Puede actualizar la visualización y guardar las imágenes utilizando los botones disponibles.

### Exportación de Datos

Desde la pestaña de exportación puede:

- **Exportar a CSV**: Genera un archivo CSV con los datos de las osteonas, ideal para importar a Grasshopper
- **Exportar a JSON**: Crea un archivo JSON con datos completos del fémur y las osteonas
- **Exportar Informe Completo**: Genera un conjunto de archivos incluyendo CSV, JSON, visualizaciones y un informe HTML

## Uso con Grasshopper

Para utilizar los datos exportados en Grasshopper:

1. Exporte los datos en formato CSV
2. En Grasshopper, utilice el componente "Read File" para importar el archivo CSV
3. Utilice los siguientes campos:
   - `section_name`: Nombre de la sección (útil para aplicar diferentes propiedades)
   - `position_z_cm`: Posición longitudinal desde el inicio del fémur (en cm)
   - `angle_degrees`: Ángulo en grados (0-360) alrededor del eje del hueso
   - `size_um`: Tamaño de la osteona (en micrómetros)

4. Transforme estos datos en geometría 3D:
   - Use `position_z_cm` como coordenada Z
   - Convierta `angle_degrees` y un radio apropiado para generar coordenadas X e Y
   - Utilice `size_um` para determinar el tamaño de cada osteona

## Modelo Matemático

La aplicación utiliza diferentes modelos matemáticos para generar las distribuciones:

- **Distribución uniforme**: Para variabilidad baja (valores cercanos a 0)
- **Distribución normal**: Para variabilidad media (valores entre 0.3 y 0.7)
- **Distribución bimodal**: Para variabilidad alta (valores superiores a 0.7)

Estos algoritmos aseguran que el patrón de osteonas refleje las características naturales de cada sección del hueso.

## Personalización Avanzada

El código está estructurado de manera modular, lo que permite:

- Modificar la forma del perfil del fémur ajustando la función de generación
- Cambiar los algoritmos de distribución para reflejar patrones específicos
- Añadir nuevas secciones o características del hueso

## Limitaciones Actuales

- Los valores predeterminados son aproximados y deben ajustarse con datos reales
- La visualización 2D simplifica la distribución real 3D de las osteonas
- El perfil del fémur es una aproximación simplificada

## Próximas Mejoras

- Importación de datos reales de microtomografías
- Integración directa con Grasshopper mediante API
- Soporte para otros tipos de huesos
- Análisis estadístico avanzado de las distribuciones

## Licencia

MIT License

## Contacto

Para preguntas, sugerencias o reportes de errores, contacte a través del repositorio de GitHub.

---

*Este proyecto forma parte del trabajo de investigación "Phygital Human Bone" para el desarrollo de modelos biomiméticos de hueso humano mediante algoritmos paramétricos, machine learning y fabricación aditiva.*