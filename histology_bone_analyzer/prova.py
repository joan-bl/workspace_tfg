import numpy as np
import matplotlib.pyplot as plt
import random

# Parámetros por sección (simplificados)
sections = {
    "Epífisis Proximal": {"density": 25, "size_mean": 200, "variability": 0.7},
    "Metáfisis Proximal": {"density": 40, "size_mean": 180, "variability": 0.5},
    "Diáfisis": {"density": 60, "size_mean": 150, "variability": 0.3},
    "Metáfisis Distal": {"density": 40, "size_mean": 180, "variability": 0.5},
    "Epífisis Distal": {"density": 25, "size_mean": 200, "variability": 0.7}
}

# Longitudes de cada sección (en cm)
lengths = {
    "Epífisis Proximal": 7.0,
    "Metáfisis Proximal": 4.5,
    "Diáfisis": 22.5,
    "Metáfisis Distal": 4.5,
    "Epífisis Distal": 7.0
}

# Generar osteonas para cada sección
osteonas = []
z_position = 0.0  # Posición longitudinal acumulada

for section, params in sections.items():
    section_length = lengths[section]
    num_osteonas = int(params["density"] * section_length)  # Aproximación
    
    for _ in range(num_osteonas):
        # Posición z con variabilidad (mayor concentración en bordes si variability > 0.5)
        if params["variability"] > 0.5:
            pos_z = z_position + random.choice([
                random.uniform(0, section_length * 0.2),
                random.uniform(section_length * 0.8, section_length)
            ])
        else:
            pos_z = z_position + random.uniform(0, section_length)
        
        # Tamaño con variación ±20%
        size = params["size_mean"] * random.uniform(0.8, 1.2)
        
        osteonas.append({
            "section": section,
            "position_z": pos_z,
            "size": size
        })
    
    z_position += section_length

# Preparar versiones abreviadas de los nombres de sección
section_names = {section: section.replace("Proximal", "Prox.").replace("Distal", "Dist.") 
                for section in sections}

# Visualización
fig, ax = plt.subplots(figsize=(12, 4))  # Ventana más ancha
colors = {"Epífisis Prox.": "red", "Metáfisis Prox.": "orange", 
          "Diáfisis": "green", "Metáfisis Dist.": "blue", "Epífisis Dist.": "purple"}

# Agrupar osteonas por sección para dibujar
for section in sections:
    section_short = section_names[section]
    section_osteonas = [o for o in osteonas if o["section"] == section]
    
    # Extraer posiciones y tamaños
    positions = [o["position_z"] for o in section_osteonas]
    sizes = [o["size"]/10 for o in section_osteonas]
    
    # Dibujar todas las osteonas de esta sección de una vez
    ax.scatter(positions, [0] * len(positions), 
               s=sizes, 
               color=colors.get(section_short, "gray"), 
               alpha=0.7, label=section_short)

# Líneas para separar secciones
z_pos = 0.0
for section, length in lengths.items():
    z_pos += length
    ax.axvline(x=z_pos, color="black", linestyle="--", alpha=0.3)

ax.set_title("Distribución Simplificada de Osteonas en Fémur")
ax.set_xlabel("Posición Longitudinal (cm)")
ax.set_yticks([])

# Configuración mejorada de la leyenda
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

# Más espacio para la leyenda
plt.tight_layout()
plt.subplots_adjust(right=0.85)  # Ajustar para dar más espacio a la leyenda

plt.show()