import cv2
import os
import pandas as pd
import numpy as np
from tkinter import Tk, Button, Text, Frame, Label, ttk, filedialog, Toplevel, messagebox, Scrollbar
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import math

def configure_window(window, title):
    """Configura el aspecto visual de la ventana principal"""
    window.title(title)
    window.geometry("1000x1000")
    window.configure(bg='#000000')  # Color de fondo cambiado a negro

def configure_button(button):
    """Configura el aspecto visual de los botones"""
    button.configure(
        bg="#BD0000",  # Color de botón cambiado a rojo
        fg="white",    # Color de texto a blanco
        font=("Helvetica", 12),
        padx=10,
        pady=5,
        relief="raised",
        borderwidth=2
    )
    # Añadir efectos hover
    button.bind("<Enter>", lambda e: button.configure(bg="#333333"))  # Cambia a gris al pasar el mouse
    button.bind("<Leave>", lambda e: button.configure(bg="#BD0000"))  # Vuelve a rojo al salir el mouse

def reconstruir_imagen_con_detecciones(imagen_original, excel_path, output_path):
    """
    Reconstruye la imagen original con las detecciones de canales marcadas.
    
    Args:
        imagen_original: Ruta a la imagen original
        excel_path: Ruta al archivo Excel con las coordenadas de detecciones
        output_path: Ruta donde guardar la imagen reconstruida
    
    Returns:
        imagen_reconstruida: Imagen con las detecciones marcadas
    """
    # Cargar la imagen original
    imagen = cv2.imread(imagen_original)
    
    # Si la imagen es muy grande, mostrar una advertencia pero continuar
    height, width = imagen.shape[:2]
    pixels = height * width
    if pixels > 89478485:  # Límite de PIL por defecto
        print(f"Advertencia: Imagen grande ({pixels} píxeles), el procesamiento puede ser lento")
    
    # Cargar datos de detecciones
    df = pd.read_excel(excel_path)
    
    # Dibujar cada canal detectado como un círculo en la imagen
    for i, row in df.iterrows():
        # Procesar valores de centro que podrían ser tensores o strings
        try:
            # Si es string que contiene tensor, extraer el número
            if isinstance(row['Center X'], str) and 'tensor' in row['Center X']:
                # Extraer el número entre paréntesis
                valor = row['Center X'].split('(')[1].split(')')[0]
                centro_x = float(valor)
            else:
                centro_x = float(row['Center X'])
            
            if isinstance(row['Center Y'], str) and 'tensor' in row['Center Y']:
                # Extraer el número entre paréntesis
                valor = row['Center Y'].split('(')[1].split(')')[0]
                centro_y = float(valor)
            else:
                centro_y = float(row['Center Y'])
                
            # Convertir a enteros para coordenadas de píxeles
            centro_x = int(centro_x)
            centro_y = int(centro_y)
            
            # Procesar el área de manera similar
            if isinstance(row['Ellipse Area (pixels^2)'], str) and 'tensor' in row['Ellipse Area (pixels^2)']:
                # Extraer el número entre paréntesis
                valor = row['Ellipse Area (pixels^2)'].split('(')[1].split(')')[0]
                area = float(valor)
            else:
                area = float(row['Ellipse Area (pixels^2)'])
                
            # Calcular radio aproximado del canal basado en el área (A = πr²)
            radio = int(np.sqrt(area / np.pi))
            
            # Dibujar círculo en la posición del canal
            cv2.circle(imagen, (centro_x, centro_y), radio, (0, 255, 0), 2)
        except Exception as e:
            print(f"Error procesando fila {i}: {e}")
            continue  # Saltar esta detección si hay error
    
    # Guardar imagen reconstruida
    cv2.imwrite(output_path, imagen)
    
    return imagen

def analizar_cuadrantes(imagen, df, output_path, min_canales=5):
    """
    Divide la imagen en 36 cuadrantes (matriz 6x6) y analiza la distribución de canales.
    Implementa el nuevo enfoque de fragilidad que considera áreas con canales grandes
    como más propensas a fractura.
    
    Args:
        imagen: Imagen reconstruida con detecciones
        df: DataFrame con coordenadas y áreas de canales
        output_path: Ruta donde guardar la imagen final
        min_canales: Número mínimo de canales para considerar un cuadrante válido
    
    Returns:
        imagen_con_cuadrantes: Imagen con cuadrantes y marcado el más frágil
        areas_por_cuadrante: Array con áreas por cuadrante
        canales_por_cuadrante: Lista de canales agrupados por cuadrante
        cuad_contiguo_fragil_idx: Índice del cuadrante contiguo más frágil
        puntuacion_fragilidad: Puntuaciones calculadas para cada cuadrante
    """
    # Obtener dimensiones originales de la imagen
    height, width = imagen.shape[:2]
    
    # Calcular dimensiones de cuadrantes
    cuad_height = height // 6
    cuad_width = width // 6
    
    # Crear estructuras para almacenar datos por cuadrante
    areas_por_cuadrante = np.zeros(36)
    canales_por_cuadrante = [[] for _ in range(36)]
    canales_maximos = np.zeros(36)  # Para almacenar el área del canal más grande por cuadrante
    puntuacion_fragilidad = np.zeros(36)  # Nueva métrica
    
    # Clasificar cada canal en su cuadrante correspondiente
    for i, row in df.iterrows():
        try:
            # Procesar coordenadas X e Y
            if isinstance(row['Center X'], str) and 'tensor' in row['Center X']:
                valor = row['Center X'].split('(')[1].split(')')[0]
                x = float(valor)
            else:
                x = float(row['Center X'])
                
            if isinstance(row['Center Y'], str) and 'tensor' in row['Center Y']:
                valor = row['Center Y'].split('(')[1].split(')')[0]
                y = float(valor)
            else:
                y = float(row['Center Y'])
                
            x = int(x)
            y = int(y)
            
            # Procesar el área
            if isinstance(row['Ellipse Area (pixels^2)'], str) and 'tensor' in row['Ellipse Area (pixels^2)']:
                valor = row['Ellipse Area (pixels^2)'].split('(')[1].split(')')[0]
                area = float(valor)
            else:
                area = float(row['Ellipse Area (pixels^2)'])
                
            # Determinar a qué cuadrante pertenece
            cuad_col = x // cuad_width
            cuad_row = y // cuad_height
            
            cuad_col = min(5, max(0, cuad_col))
            cuad_row = min(5, max(0, cuad_row))
            
            cuad_idx = cuad_row * 6 + cuad_col
            
            # Acumular área en este cuadrante
            areas_por_cuadrante[cuad_idx] += area
            
            # Guardar referencia al canal
            canales_por_cuadrante[cuad_idx].append((x, y, area))
            
            # Actualizar el área del canal más grande si corresponde
            if area > canales_maximos[cuad_idx]:
                canales_maximos[cuad_idx] = area
                
        except Exception as e:
            print(f"Error procesando canal {i}: {e}")
            continue
    
    # Calcular puntuación de fragilidad para cada cuadrante
    for i in range(36):
        num_canales = len(canales_por_cuadrante[i])
        
        # Solo considerar cuadrantes con suficientes canales
        if num_canales >= min_canales:
            # Área promedio por canal
            area_promedio = areas_por_cuadrante[i] / num_canales
            
            # Normalizar por número de canales (uso de logaritmo para suavizar el efecto)
            factor_num_canales = np.log10(1 + num_canales)
            
            # Factor de tamaño (relación entre el canal más grande y el promedio)
            # Si todos los canales son de tamaño similar, será cercano a 1
            # Si hay canales anormalmente grandes, será mayor que 1
            factor_tamaño = canales_maximos[i] / area_promedio if area_promedio > 0 else 1
            
            # Puntuación final de fragilidad: área promedio × factor de canales × factor de tamaño
            puntuacion_fragilidad[i] = area_promedio * factor_num_canales * (1 + 0.5*(factor_tamaño - 1))
        else:
            # Si hay muy pocos canales, asignar puntuación cero
            puntuacion_fragilidad[i] = 0
    
    # Definir los índices de los 4 cuadrantes centrales (en una matriz 6x6)
    cuadrantes_centrales = [
        2*6 + 2,  # (2,2)
        2*6 + 3,  # (2,3)
        3*6 + 2,  # (3,2)
        3*6 + 3   # (3,3)
    ]
    
    # Encontrar cuadrante con mayor fragilidad (excluyendo centrales)
    puntuacion_mascara = puntuacion_fragilidad.copy()
    for idx in cuadrantes_centrales:
        puntuacion_mascara[idx] = -1  # Excluir cuadrantes centrales
        
    # También excluir cuadrantes con menos del mínimo de canales
    for i in range(36):
        if len(canales_por_cuadrante[i]) < min_canales:
            puntuacion_mascara[i] = -1
            
    cuad_max_fragil_idx = np.argmax(puntuacion_mascara)
    max_row = cuad_max_fragil_idx // 6
    max_col = cuad_max_fragil_idx % 6
    
    # Encontrar cuadrantes contiguos al más frágil
    cuadrantes_contiguos = []
    
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Saltar el propio cuadrante
            if dr == 0 and dc == 0:
                continue
                
            # Calcular fila y columna del cuadrante contiguo
            contiguo_row = max_row + dr
            contiguo_col = max_col + dc
            
            # Comprobar que está dentro de los límites
            if 0 <= contiguo_row < 6 and 0 <= contiguo_col < 6:
                # Calcular índice del cuadrante contiguo
                contiguo_idx = contiguo_row * 6 + contiguo_col
                
                # Verificar que no es uno de los 4 cuadrantes centrales
                # y que tiene suficientes canales
                if (contiguo_idx not in cuadrantes_centrales and 
                    len(canales_por_cuadrante[contiguo_idx]) >= min_canales):
                    # Usamos la misma métrica de fragilidad
                    cuadrantes_contiguos.append((contiguo_idx, puntuacion_fragilidad[contiguo_idx]))
    
    # Encontrar el cuadrante contiguo con MAYOR puntuación de fragilidad
    if cuadrantes_contiguos:
        # Ordenar por puntuación de fragilidad (de mayor a menor)
        cuadrantes_contiguos.sort(key=lambda x: x[1], reverse=True)
        cuad_contiguo_fragil_idx = cuadrantes_contiguos[0][0]
    else:
        # En caso de que no haya cuadrantes contiguos válidos
        cuad_contiguo_fragil_idx = None
    
    # Imagen para visualización
    imagen_con_cuadrantes = imagen.copy()
    
    # Dibujar líneas de cuadrantes
    for i in range(1, 6):
        # Líneas horizontales
        cv2.line(imagen_con_cuadrantes, (0, i*cuad_height), 
                 (width, i*cuad_height), (255, 255, 255), 1)
        # Líneas verticales
        cv2.line(imagen_con_cuadrantes, (i*cuad_width, 0), 
                 (i*cuad_width, height), (255, 255, 255), 1)
    
    # Marcar cuadrante más frágil
    x1_max = max_col * cuad_width
    y1_max = max_row * cuad_height
    x2_max = (max_col + 1) * cuad_width
    y2_max = (max_row + 1) * cuad_height
    
    # Dibujar rectángulo semitransparente en el cuadrante más frágil (ROJO)
    overlay = imagen_con_cuadrantes.copy()
    cv2.rectangle(overlay, (x1_max, y1_max), (x2_max, y2_max), (0, 0, 255), -1)
    cv2.addWeighted(overlay, 0.3, imagen_con_cuadrantes, 0.7, 0, imagen_con_cuadrantes)
    
    # Marcar el cuadrante contiguo también frágil
    if cuad_contiguo_fragil_idx is not None:
        min_row = cuad_contiguo_fragil_idx // 6
        min_col = cuad_contiguo_fragil_idx % 6
        x1_min = min_col * cuad_width
        y1_min = min_row * cuad_height
        x2_min = (min_col + 1) * cuad_width
        y2_min = (min_row + 1) * cuad_height
        
        # Dibujar rectángulo semitransparente en el cuadrante contiguo (AZUL)
        overlay = imagen_con_cuadrantes.copy()
        cv2.rectangle(overlay, (x1_min, y1_min), (x2_min, y2_min), (255, 0, 0), -1)
        cv2.addWeighted(overlay, 0.3, imagen_con_cuadrantes, 0.7, 0, imagen_con_cuadrantes)
    
    # Añadir texto con información por cuadrante
    font_scale = 0.4
    for i in range(36):
        row = i // 6
        col = i % 6
        text_x = col * cuad_width + 5
        text_y = row * cuad_height + 15
        
        # Verificar si es un cuadrante central
        is_central = i in cuadrantes_centrales
        
        # Colorear el texto para diferentes tipos de cuadrantes
        if len(canales_por_cuadrante[i]) < min_canales:
            text_color = (100, 100, 100)  # Gris oscuro para cuadrantes con pocos canales
        elif is_central:
            text_color = (128, 128, 128)  # Gris para cuadrantes centrales
        else:
            text_color = (255, 255, 255)  # Blanco para cuadrantes normales
        
        # Número de canales y área
        num_canales = len(canales_por_cuadrante[i])
        area_total = areas_por_cuadrante[i]
        
        # Mostrar información básica
        text1 = f"A:{area_total:.0f}"
        text2 = f"C:{num_canales}"
        
        cv2.putText(imagen_con_cuadrantes, text1, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, 1)
        
        cv2.putText(imagen_con_cuadrantes, text2, (text_x, text_y + 15),
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, 1)
        
        # Añadir indicador de fragilidad para cuadrantes válidos
        if num_canales >= min_canales and not is_central:
            # Normalizar la puntuación para visualización (0-100)
            max_valid_score = np.max(puntuacion_fragilidad) if np.max(puntuacion_fragilidad) > 0 else 1
            normalized_score = int((puntuacion_fragilidad[i] / max_valid_score) * 100)
            text3 = f"F:{normalized_score}"
            cv2.putText(imagen_con_cuadrantes, text3, (text_x, text_y + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, 1)
                       
        # Para cuadrantes centrales, añadir una marca especial
        if is_central:
            x1 = col * cuad_width
            y1 = row * cuad_height
            x2 = (col + 1) * cuad_width
            y2 = (row + 1) * cuad_height
            overlay = imagen_con_cuadrantes.copy()
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (128, 128, 128), -1)
            cv2.addWeighted(overlay, 0.2, imagen_con_cuadrantes, 0.8, 0, imagen_con_cuadrantes)
            
        # Para cuadrantes con pocos canales, marcarlos como no válidos
        if num_canales < min_canales:
            x1 = col * cuad_width
            y1 = row * cuad_height
            x2 = (col + 1) * cuad_width
            y2 = (row + 1) * cuad_height
            # Dibujar una X para indicar que no es válido
            cv2.line(imagen_con_cuadrantes, (x1, y1), (x2, y2), (50, 50, 50), 1)
            cv2.line(imagen_con_cuadrantes, (x1, y2), (x2, y1), (50, 50, 50), 1)
    
    # Guardar imagen final
    cv2.imwrite(output_path, imagen_con_cuadrantes)
    
    # Retornar datos
    return imagen_con_cuadrantes, areas_por_cuadrante, canales_por_cuadrante, cuad_contiguo_fragil_idx, puntuacion_fragilidad

def visualizar_resultados_cuadrantes(root, imagen_path, areas_por_cuadrante, canales_por_cuadrante, cuad_contiguo_fragil_idx=None, puntuacion_fragilidad=None, min_canales=5):
    """
    Muestra los resultados del análisis por cuadrantes en una interfaz gráfica.
    
    Args:
        root: Ventana raíz de Tkinter
        imagen_path: Ruta a la imagen con cuadrantes analizados
        areas_por_cuadrante: Array con áreas por cuadrante
        canales_por_cuadrante: Lista de canales agrupados por cuadrante
        cuad_contiguo_fragil_idx: Índice del cuadrante contiguo más frágil
        puntuacion_fragilidad: Array con puntuaciones de fragilidad por cuadrante
        min_canales: Número mínimo de canales para considerar un cuadrante válido
    """
    for widget in root.winfo_children():
        widget.destroy()
    
    configure_window(root, "Análisis por Cuadrantes")
    
    # Crear pestañas
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    
    # Pestaña de visualización
    frame1 = Frame(notebook, bg='#000000')
    frame2 = Frame(notebook, bg='#000000')
    notebook.add(frame1, text="Visualización")
    notebook.add(frame2, text="Datos por Cuadrante")
    
    # Mostrar imagen
    try:
        img = Image.open(imagen_path)
        
        # Calcular dimensiones para mantener relación de aspecto
        display_width = 800
        display_height = int(display_width * img.height / img.width)
        
        img = img.resize((display_width, display_height), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        
        img_label = Label(frame1, image=img_tk, bg='#000000')
        img_label.image = img_tk
        img_label.pack(pady=20)
        
        # Guardar referencias a nivel global para el cálculo de área
        global img_width, img_height
        img_width, img_height = img.size
        
        # Botón para guardar imagen
        def guardar_imagen():
            destino = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialfile="analisis_cuadrantes.png")
            if destino:
                import shutil
                shutil.copy(imagen_path, destino)
                messagebox.showinfo("Éxito", f"Imagen guardada en {destino}")
                
        save_button = Button(frame1, text="Guardar Imagen", command=guardar_imagen)
        configure_button(save_button)
        save_button.pack(pady=10)
        
        # Añadir leyenda
        leyenda_frame = Frame(frame1, bg='#000000')
        leyenda_frame.pack(pady=10)
        
        # Leyenda para el cuadrante más frágil
        mayor_frame = Frame(leyenda_frame, bg='#000000')
        mayor_frame.pack(side='left', padx=20)
        
        mayor_color = Frame(mayor_frame, bg='#FF0000', width=20, height=20)
        mayor_color.pack(side='left', padx=5)
        
        mayor_label = Label(mayor_frame, text="Cuadrante más frágil", fg="white", bg='#000000')
        mayor_label.pack(side='left')
        
        # Leyenda para el cuadrante contiguo más frágil
        menor_frame = Frame(leyenda_frame, bg='#000000')
        menor_frame.pack(side='left', padx=20)
        
        menor_color = Frame(menor_frame, bg='#0000FF', width=20, height=20)
        menor_color.pack(side='left', padx=5)
        
        menor_label = Label(menor_frame, text="Contiguo frágil", fg="white", bg='#000000')
        menor_label.pack(side='left')
        
        # Leyenda para los cuadrantes centrales
        central_frame = Frame(leyenda_frame, bg='#000000')
        central_frame.pack(side='left', padx=20)
        
        central_color = Frame(central_frame, bg='#808080', width=20, height=20)
        central_color.pack(side='left', padx=5)
        
        central_label = Label(central_frame, text="Centrales", fg="white", bg='#000000')
        central_label.pack(side='left')
        
        # Leyenda para cuadrantes no válidos (menos de min_canales)
        invalid_frame = Frame(leyenda_frame, bg='#000000')
        invalid_frame.pack(side='left', padx=20)
        
        invalid_label = Label(invalid_frame, text="X = < 5 canales", fg="#666666", bg='#000000')
        invalid_label.pack(side='left')
        
    except Exception as e:
        error_label = Label(frame1, text=f"Error al cargar la imagen: {e}", 
                           fg="white", bg='#000000')
        error_label.pack(pady=20)
    
    # Crear un contenedor para el texto y la scrollbar
    text_container = Frame(frame2, bg='#000000')
    text_container.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Mostrar datos por cuadrante
    text_area = Text(text_container, bg='#000000', fg="white", font=("Helvetica", 12))
    
    # Crear scrollbar para el área de texto
    scrollbar = Scrollbar(text_container, command=text_area.yview)
    scrollbar.pack(side='right', fill='y')
    
    text_area.pack(side='left', fill='both', expand=True)
    text_area.config(yscrollcommand=scrollbar.set)
    
    text_area.insert('1.0', "ANÁLISIS POR CUADRANTES (MATRIZ 6×6)\n\n")
    text_area.insert('end', "NUEVA MÉTRICA: Puntuación de fragilidad = Área promedio × log(N° canales) × (1 + Factor tamaño)\n")
    text_area.insert('end', f"Se ignoran cuadrantes con menos de {min_canales} canales\n\n")
    
    # Encontrar cuadrante con mayor puntuación de fragilidad
    cuadrantes_centrales = [2*6 + 2, 2*6 + 3, 3*6 + 2, 3*6 + 3]
    
    # Crear copia de la puntuación excluyendo centrales y cuadrantes con pocos canales
    if puntuacion_fragilidad is not None:
        puntuacion_mascara = puntuacion_fragilidad.copy()
        for i in range(36):
            if i in cuadrantes_centrales or len(canales_por_cuadrante[i]) < min_canales:
                puntuacion_mascara[i] = -1
        cuad_max_fragil_idx = np.argmax(puntuacion_mascara)
    else:
        # Fallback por si no tenemos puntuación de fragilidad
        cuad_max_fragil_idx = np.argmax(areas_por_cuadrante)
    
    # Mostrar información por cuadrante
    for i in range(36):
        row = i // 6
        col = i % 6
        
        # Verificar si es un cuadrante central
        is_central = i in cuadrantes_centrales
        
        # Verificar si tiene suficientes canales
        has_min_canales = len(canales_por_cuadrante[i]) >= min_canales
        
        # Determinar tipo de cuadrante
        if not has_min_canales:
            text_area.insert('end', f"CUADRANTE {i+1} (IGNORADO - POCOS CANALES) - Fila {row+1}, Columna {col+1}\n")
            text_area.insert('end', f"  Número de canales: {len(canales_por_cuadrante[i])} (mínimo requerido: {min_canales})\n\n")
            continue
        
        if i == cuad_max_fragil_idx:
            text_area.insert('end', f"CUADRANTE {i+1} (MÁS FRÁGIL) - Fila {row+1}, Columna {col+1}\n")
        elif i == cuad_contiguo_fragil_idx:
            text_area.insert('end', f"CUADRANTE {i+1} (CONTIGUO FRÁGIL) - Fila {row+1}, Columna {col+1}\n")
        elif is_central:
            text_area.insert('end', f"CUADRANTE {i+1} (CENTRAL) - Fila {row+1}, Columna {col+1}\n")
        else:
            text_area.insert('end', f"CUADRANTE {i+1} - Fila {row+1}, Columna {col+1}\n")
            
        text_area.insert('end', f"  Área total: {areas_por_cuadrante[i]:.2f} pixels²\n")
        text_area.insert('end', f"  Número de canales: {len(canales_por_cuadrante[i])}\n")
        
        # Mostrar métricas adicionales
        num_canales = len(canales_por_cuadrante[i])
        if num_canales > 0:
            area_promedio = areas_por_cuadrante[i] / num_canales
            text_area.insert('end', f"  Área promedio por canal: {area_promedio:.2f} pixels²\n")
            
            # Calcular el canal más grande
            areas_canales = [canal[2] for canal in canales_por_cuadrante[i]]
            canal_max = max(areas_canales) if areas_canales else 0
            text_area.insert('end', f"  Área del canal más grande: {canal_max:.2f} pixels²\n")
            
            # Factor de tamaño
            factor_tamaño = canal_max / area_promedio if area_promedio > 0 else 1
            text_area.insert('end', f"  Factor de tamaño: {factor_tamaño:.2f}\n")
            
            # Mostrar la puntuación de fragilidad si está disponible
            if puntuacion_fragilidad is not None:
                text_area.insert('end', f"  Puntuación de fragilidad: {puntuacion_fragilidad[i]:.2f}\n")
                
                # Si es el cuadrante más frágil, mostrar por qué fue seleccionado
                if i == cuad_max_fragil_idx:
                    text_area.insert('end', f"  MOTIVO DE SELECCIÓN: Este cuadrante tiene la mayor puntuación de fragilidad\n")
                    text_area.insert('end', f"  combinando el tamaño de los canales y su distribución.\n")
        
        text_area.insert('end', "\n")
    
    # Botón para exportar resultados a Excel
    def exportar_excel():
        destino = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="resultados_fragilidad_cuadrantes.xlsx")
        
        if destino:
            # Crear DataFrame con resultados
            data = []
            
            # Usar las dimensiones de la imagen que tenemos en la UI
            area_cuadrante = (img_height // 6) * (img_width // 6)
            
            for i in range(36):
                row = i // 6
                col = i % 6
                
                # Calcular métricas
                num_canales = len(canales_por_cuadrante[i])
                area_total = areas_por_cuadrante[i]
                
                # Determinar tipo de cuadrante
                is_central = i in [2*6 + 2, 2*6 + 3, 3*6 + 2, 3*6 + 3]
                has_min_canales = num_canales >= min_canales
                
                if num_canales > 0:
                    area_promedio = area_total / num_canales
                    
                    # Calcular área del canal más grande
                    areas_canales = [canal[2] for canal in canales_por_cuadrante[i]]
                    canal_max = max(areas_canales) if areas_canales else 0
                    
                    # Factor de tamaño
                    factor_tamaño = canal_max / area_promedio if area_promedio > 0 else 1
                    
                    # Usar la puntuación calculada o recalcularla
                    if puntuacion_fragilidad is not None and i < len(puntuacion_fragilidad):
                        fragilidad = puntuacion_fragilidad[i]
                    else:
                        # Solo calcular si tiene suficientes canales
                        if has_min_canales:
                            factor_num_canales = np.log10(1 + num_canales)
                            fragilidad = area_promedio * factor_num_canales * (1 + 0.5 * (factor_tamaño - 1))
                        else:
                            fragilidad = 0
                else:
                    area_promedio = 0
                    canal_max = 0
                    factor_tamaño = 0
                    fragilidad = 0
                
                # Determinar estado del cuadrante
                if not has_min_canales:
                    tipo = "Ignorado (pocos canales)"
                elif i == cuad_max_fragil_idx:
                    tipo = "Más frágil"
                elif i == cuad_contiguo_fragil_idx:
                    tipo = "Contiguo frágil"
                elif is_central:
                    tipo = "Central"
                else:
                    tipo = "Normal"
                
                data.append({
                    'Cuadrante': i+1,
                    'Fila': row+1,
                    'Columna': col+1,
                    'Area Total': area_total,
                    'Num Canales': num_canales,
                    'Area Promedio': area_promedio,
                    'Canal Más Grande': canal_max,
                    'Factor Tamaño': factor_tamaño,
                    'Puntuacion Fragilidad': fragilidad,
                    'Tipo': tipo,
                    'Válido': "Sí" if has_min_canales else "No"
                })
                
            df = pd.DataFrame(data)
            df.to_excel(destino, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados a {destino}")
    
    # Botón de exportación
    export_frame = Frame(frame2, bg='#000000')
    export_frame.pack(side='bottom', fill='x', pady=10)
    
    export_button = Button(export_frame, text="Exportar a Excel", command=exportar_excel)
    configure_button(export_button)
    export_button.pack(pady=10)

def main():
    """Función principal del programa"""
    # Crear ventana principal
    root = Tk()
    
    # Variables globales para dimensiones de imagen
    global img_width, img_height
    img_width, img_height = 800, 800  # Valores predeterminados iniciales
    
    # Definir rutas base para almacenar resultados
    results_dir = r"C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\histology_bone_analyzer\data\sample_results\breaking_app"
    
    # Crear la carpeta si no existe
    os.makedirs(results_dir, exist_ok=True)
    
    # Ignorar advertencias de PIL sobre imágenes grandes
    Image.MAX_IMAGE_PIXELS = None
    
    # Mínimo de canales para considerar un cuadrante válido
    min_canales = 5
    
    # Título de la ventana
    configure_window(root, "Análisis de Canales por Cuadrantes")
    
    # Función para iniciar el análisis
    def iniciar_analisis():
        # Seleccionar imagen original
        imagen_original = filedialog.askopenfilename(
            title="Seleccione la imagen original",
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
        )
        
        if not imagen_original:
            return
            
        # Seleccionar archivo Excel con detecciones
        excel_path = filedialog.askopenfilename(
            title="Seleccione el archivo Excel con las detecciones",
            filetypes=[("Excel files", "*.xlsx")]
        )
        
        if not excel_path:
            return
            
        # Mostrar ventana de progreso
        progreso = Toplevel(root)
        configure_window(progreso, "Procesando")
        Label(progreso, text="Procesando imagen...", font=("Helvetica", 16),
              fg="white", bg='#000000').pack(expand=True)
        progreso.update()
        
        try:
            # Definir rutas para los archivos de resultados
            imagen_reconstruida_path = os.path.join(results_dir, "imagen_reconstruida.png")
            imagen_cuadrantes_path = os.path.join(results_dir, "imagen_cuadrantes.png")
            
            # Reconstruir imagen con detecciones
            imagen = reconstruir_imagen_con_detecciones(
                imagen_original, excel_path, imagen_reconstruida_path
            )
            
            # Cargar datos de detecciones
            df = pd.read_excel(excel_path)
            
            # Analizar por cuadrantes
            imagen_final, areas, canales, cuad_contiguo_fragil_idx, puntuacion_fragilidad = analizar_cuadrantes(
                imagen, df, imagen_cuadrantes_path, min_canales
            )
            
            # Cerrar ventana de progreso
            progreso.destroy()
            
            # Mostrar resultados
            visualizar_resultados_cuadrantes(root, imagen_cuadrantes_path, areas, canales, 
                                           cuad_contiguo_fragil_idx, puntuacion_fragilidad, min_canales)
            
        except Exception as e:
            progreso.destroy()
            messagebox.showerror("Error", f"Error durante el análisis: {e}")
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Crear botones en la ventana principal
    titulo = Label(root, text="Análisis de Fragilidad Ósea por Cuadrantes", 
                  font=("Helvetica", 24), fg="white", bg='#000000')
    titulo.pack(pady=30)
    
    descripcion = Label(root, text=f"Esta aplicación analiza la distribución de canales de Havers y evalúa la fragilidad ósea.\n"
                       f"Se ignoran cuadrantes con menos de {min_canales} canales y se identifican las zonas más frágiles.",
                       font=("Helvetica", 14), fg="white", bg='#000000')
    descripcion.pack(pady=20)
    
    iniciar_button = Button(root, text="Iniciar Análisis", command=iniciar_analisis)
    configure_button(iniciar_button)
    iniciar_button.pack(pady=30)
    
    # Iniciar la aplicación
    root.mainloop()

if __name__ == '__main__':
    main()