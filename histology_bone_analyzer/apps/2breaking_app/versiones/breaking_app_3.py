import cv2
import os
import pandas as pd
import numpy as np
from tkinter import Tk, Button, Text, Frame, Label, ttk, filedialog, Toplevel, messagebox, Scrollbar
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

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

def analizar_cuadrantes(imagen, df, output_path):
    """
    Divide la imagen en 36 cuadrantes (matriz 6x6) y analiza la distribución de canales.
    
    Args:
        imagen: Imagen reconstruida con detecciones
        df: DataFrame con coordenadas y áreas de canales
        output_path: Ruta donde guardar la imagen final
    
    Returns:
        imagen_con_cuadrantes: Imagen con cuadrantes y marcado el de mayor densidad
        areas_por_cuadrante: Array con áreas por cuadrante
        canales_por_cuadrante: Lista de canales agrupados por cuadrante
        cuad_min_contiguo_idx: Índice del cuadrante contiguo con menor densidad
    """
    # Obtener dimensiones originales de la imagen
    height, width = imagen.shape[:2]
    
    # Calcular dimensiones de cuadrantes manteniendo las proporciones originales
    # Ahora 6x6 en lugar de 3x3
    cuad_height = height // 6
    cuad_width = width // 6
    
    # Crear estructura para almacenar áreas por cuadrante (36 cuadrantes)
    areas_por_cuadrante = np.zeros(36)
    canales_por_cuadrante = [[] for _ in range(36)]
    
    # Clasificar cada canal en su cuadrante correspondiente
    for i, row in df.iterrows():
        try:
            # Procesar coordenadas X e Y que podrían ser tensores o strings
            if isinstance(row['Center X'], str) and 'tensor' in row['Center X']:
                # Extraer el número entre paréntesis
                valor = row['Center X'].split('(')[1].split(')')[0]
                x = float(valor)
            else:
                x = float(row['Center X'])
                
            if isinstance(row['Center Y'], str) and 'tensor' in row['Center Y']:
                # Extraer el número entre paréntesis
                valor = row['Center Y'].split('(')[1].split(')')[0]
                y = float(valor)
            else:
                y = float(row['Center Y'])
                
            # Convertir a enteros para coordenadas de píxeles
            x = int(x)
            y = int(y)
            
            # Procesar el área de manera similar
            if isinstance(row['Ellipse Area (pixels^2)'], str) and 'tensor' in row['Ellipse Area (pixels^2)']:
                # Extraer el número entre paréntesis
                valor = row['Ellipse Area (pixels^2)'].split('(')[1].split(')')[0]
                area = float(valor)
            else:
                area = float(row['Ellipse Area (pixels^2)'])
                
            # Determinar a qué cuadrante pertenece (ahora en matriz 6x6)
            cuad_col = x // cuad_width
            cuad_row = y // cuad_height
            
            # Ajustar para asegurar que está dentro de los límites
            cuad_col = min(5, max(0, cuad_col))
            cuad_row = min(5, max(0, cuad_row))
            
            # Índice del cuadrante (0-35)
            cuad_idx = cuad_row * 6 + cuad_col
            
            # Acumular área en este cuadrante
            areas_por_cuadrante[cuad_idx] += area
            
            # Guardar referencia al canal
            canales_por_cuadrante[cuad_idx].append((x, y, area))
        except Exception as e:
            print(f"Error procesando canal {i}: {e}")
            continue
    
    # Encontrar cuadrante con mayor área
    cuad_max_area_idx = np.argmax(areas_por_cuadrante)
    max_row = cuad_max_area_idx // 6
    max_col = cuad_max_area_idx % 6
    
    # Encontrar cuadrantes contiguos al de mayor área
    cuadrantes_contiguos = []
    
    # Comprobar los 8 cuadrantes adyacentes (arriba, abajo, izquierda, derecha y diagonales)
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
                
                # Calcular densidad (área total / número de canales o 1 para evitar división por cero)
                num_canales = max(1, len(canales_por_cuadrante[contiguo_idx]))
                densidad = areas_por_cuadrante[contiguo_idx] / num_canales
                
                cuadrantes_contiguos.append((contiguo_idx, densidad))
    
    # Encontrar el cuadrante contiguo con menor densidad
    if cuadrantes_contiguos:
        # Ordenar por densidad (de menor a mayor)
        cuadrantes_contiguos.sort(key=lambda x: x[1])
        cuad_min_contiguo_idx = cuadrantes_contiguos[0][0]
    else:
        # En caso de que no haya cuadrantes contiguos (poco probable)
        cuad_min_contiguo_idx = None
    
    # Imagen para visualización (mantener la imagen original sin deformación)
    imagen_con_cuadrantes = imagen.copy()
    
    # Dibujar líneas de cuadrantes (ahora 5 líneas horizontales y 5 verticales para crear 6x6 cuadrantes)
    for i in range(1, 6):
        # Líneas horizontales
        cv2.line(imagen_con_cuadrantes, (0, i*cuad_height), 
                 (width, i*cuad_height), (255, 255, 255), 1)  # Grosor reducido
        # Líneas verticales
        cv2.line(imagen_con_cuadrantes, (i*cuad_width, 0), 
                 (i*cuad_width, height), (255, 255, 255), 1)  # Grosor reducido
    
    # Marcar cuadrante con mayor área
    x1_max = max_col * cuad_width
    y1_max = max_row * cuad_height
    x2_max = (max_col + 1) * cuad_width
    y2_max = (max_row + 1) * cuad_height
    
    # Dibujar rectángulo semitransparente en el cuadrante con mayor área (ROJO)
    overlay = imagen_con_cuadrantes.copy()
    cv2.rectangle(overlay, (x1_max, y1_max), (x2_max, y2_max), (0, 0, 255), -1)
    cv2.addWeighted(overlay, 0.3, imagen_con_cuadrantes, 0.7, 0, imagen_con_cuadrantes)
    
    # Marcar el cuadrante contiguo con menor densidad
    if cuad_min_contiguo_idx is not None:
        min_row = cuad_min_contiguo_idx // 6
        min_col = cuad_min_contiguo_idx % 6
        x1_min = min_col * cuad_width
        y1_min = min_row * cuad_height
        x2_min = (min_col + 1) * cuad_width
        y2_min = (min_row + 1) * cuad_height
        
        # Dibujar rectángulo semitransparente en el cuadrante contiguo de menor densidad (AZUL)
        overlay = imagen_con_cuadrantes.copy()
        cv2.rectangle(overlay, (x1_min, y1_min), (x2_min, y2_min), (255, 0, 0), -1)
        cv2.addWeighted(overlay, 0.3, imagen_con_cuadrantes, 0.7, 0, imagen_con_cuadrantes)
    
    # Añadir texto con información por cuadrante (texto reducido por espacio limitado)
    font_scale = 0.4  # Tamaño de fuente más pequeño
    for i in range(36):
        row = i // 6
        col = i % 6
        text_x = col * cuad_width + 5  # Posición X ajustada
        text_y = row * cuad_height + 15  # Posición Y ajustada
        
        # Texto con área total y número de canales (formato condensado)
        text = f"A:{areas_por_cuadrante[i]:.0f}"  # Área redondeada
        cv2.putText(imagen_con_cuadrantes, text, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 1)  # Grosor reducido
        
        text = f"C:{len(canales_por_cuadrante[i])}"  # Número de canales
        cv2.putText(imagen_con_cuadrantes, text, (text_x, text_y + 15),  # Menos espacio vertical
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 1)  # Grosor reducido
    
    # Guardar imagen final
    cv2.imwrite(output_path, imagen_con_cuadrantes)
    
    # Añadir información del cuadrante contiguo con menor densidad al retorno
    return imagen_con_cuadrantes, areas_por_cuadrante, canales_por_cuadrante, cuad_min_contiguo_idx

def visualizar_resultados_cuadrantes(root, imagen_path, areas_por_cuadrante, canales_por_cuadrante, cuad_min_contiguo_idx=None):
    """
    Muestra los resultados del análisis por cuadrantes en una interfaz gráfica.
    
    Args:
        root: Ventana raíz de Tkinter
        imagen_path: Ruta a la imagen con cuadrantes analizados
        areas_por_cuadrante: Array con áreas por cuadrante
        canales_por_cuadrante: Lista de canales agrupados por cuadrante
        cuad_min_contiguo_idx: Índice del cuadrante contiguo con menor densidad
    """
    for widget in root.winfo_children():
        widget.destroy()
    
    configure_window(root, "Análisis por Cuadrantes")
    
    # Crear pestañas
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    
    # Pestaña de visualización
    frame1 = Frame(notebook, bg='#000000')  # Fondo negro
    frame2 = Frame(notebook, bg='#000000')  # Fondo negro
    notebook.add(frame1, text="Visualización")
    notebook.add(frame2, text="Datos por Cuadrante")
    
    # Mostrar imagen (manteniendo proporciones originales)
    try:
        img = Image.open(imagen_path)
        
        # Calcular dimensiones para mantener relación de aspecto
        display_width = 800
        display_height = int(display_width * img.height / img.width)
        
        # Redimensionar usando LANCZOS para mejor calidad
        img = img.resize((display_width, display_height), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        
        img_label = Label(frame1, image=img_tk, bg='#000000')  # Fondo negro
        img_label.image = img_tk  # Mantener referencia
        img_label.pack(pady=20)
        
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
        
        # Leyenda para el cuadrante de mayor densidad
        mayor_frame = Frame(leyenda_frame, bg='#000000')
        mayor_frame.pack(side='left', padx=20)
        
        mayor_color = Frame(mayor_frame, bg='#FF0000', width=20, height=20)
        mayor_color.pack(side='left', padx=5)
        
        mayor_label = Label(mayor_frame, text="Mayor densidad", fg="white", bg='#000000')
        mayor_label.pack(side='left')
        
        # Leyenda para el cuadrante contiguo de menor densidad
        menor_frame = Frame(leyenda_frame, bg='#000000')
        menor_frame.pack(side='left', padx=20)
        
        menor_color = Frame(menor_frame, bg='#0000FF', width=20, height=20)
        menor_color.pack(side='left', padx=5)
        
        menor_label = Label(menor_frame, text="Menor densidad contiguo", fg="white", bg='#000000')
        menor_label.pack(side='left')
        
    except Exception as e:
        error_label = Label(frame1, text=f"Error al cargar la imagen: {e}", 
                           fg="white", bg='#000000')  # Texto blanco, fondo negro
        error_label.pack(pady=20)
    
    # Crear un contenedor para el texto y la scrollbar
    text_container = Frame(frame2, bg='#000000')
    text_container.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Mostrar datos por cuadrante
    text_area = Text(text_container, bg='#000000', fg="white", font=("Helvetica", 12))  # Texto blanco, fondo negro
    
    # Crear scrollbar para el área de texto
    scrollbar = Scrollbar(text_container, command=text_area.yview)
    scrollbar.pack(side='right', fill='y')
    
    text_area.pack(side='left', fill='both', expand=True)
    text_area.config(yscrollcommand=scrollbar.set)
    
    text_area.insert('1.0', "ANÁLISIS POR CUADRANTES (MATRIZ 6×6)\n\n")
    
    # Encontrar cuadrante con mayor área
    cuad_max_area_idx = np.argmax(areas_por_cuadrante)
    
    # Mostrar información por cuadrante (ahora 36 cuadrantes)
    for i in range(36):
        row = i // 6  # 6 columnas ahora
        col = i % 6
        
        # Determinar si es el cuadrante con mayor densidad o el contiguo con menor densidad
        if i == cuad_max_area_idx:
            text_area.insert('end', f"CUADRANTE {i+1} (MAYOR DENSIDAD) - Fila {row+1}, Columna {col+1}\n")
        elif i == cuad_min_contiguo_idx:
            text_area.insert('end', f"CUADRANTE {i+1} (MENOR DENSIDAD CONTIGUO) - Fila {row+1}, Columna {col+1}\n")
        else:
            text_area.insert('end', f"CUADRANTE {i+1} - Fila {row+1}, Columna {col+1}\n")
            
        text_area.insert('end', f"  Área total: {areas_por_cuadrante[i]:.2f} pixels²\n")
        text_area.insert('end', f"  Número de canales: {len(canales_por_cuadrante[i])}\n")
        
        if len(canales_por_cuadrante[i]) > 0:
            area_promedio = sum(canal[2] for canal in canales_por_cuadrante[i]) / len(canales_por_cuadrante[i])
            text_area.insert('end', f"  Área promedio por canal: {area_promedio:.2f} pixels²\n")
            text_area.insert('end', f"  Densidad: {areas_por_cuadrante[i] / len(canales_por_cuadrante[i]):.2f} pixels²/canal\n")
        
        text_area.insert('end', "\n")
    
    # Botón para exportar resultados a Excel
    def exportar_excel():
        destino = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="resultados_cuadrantes.xlsx")
        
        if destino:
            # Crear DataFrame con resultados
            data = []
            for i in range(36):  # Ahora 36 cuadrantes
                row = i // 6  # 6 columnas
                col = i % 6
                
                # Calcular área promedio (evitando división por cero)
                num_canales = len(canales_por_cuadrante[i])
                if num_canales > 0:
                    area_promedio = sum(canal[2] for canal in canales_por_cuadrante[i]) / num_canales
                    densidad = areas_por_cuadrante[i] / num_canales
                else:
                    area_promedio = 0
                    densidad = 0
                
                # Determinar tipo de cuadrante
                if i == cuad_max_area_idx:
                    tipo = "Mayor densidad"
                elif i == cuad_min_contiguo_idx:
                    tipo = "Menor densidad contiguo"
                else:
                    tipo = "Normal"
                
                data.append({
                    'Cuadrante': i+1,
                    'Fila': row+1,
                    'Columna': col+1,
                    'Area Total': areas_por_cuadrante[i],
                    'Num Canales': num_canales,
                    'Area Promedio': area_promedio,
                    'Densidad': densidad,
                    'Tipo': tipo
                })
                
            df = pd.DataFrame(data)
            df.to_excel(destino, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados a {destino}")
    
    # Botón de exportación en un frame separado para que siempre sea visible
    export_frame = Frame(frame2, bg='#000000')
    export_frame.pack(side='bottom', fill='x', pady=10)
    
    export_button = Button(export_frame, text="Exportar a Excel", command=exportar_excel)
    configure_button(export_button)
    export_button.pack(pady=10)

def main():
    """Función principal del programa"""
    # Crear ventana principal
    root = Tk()
    
    # Definir rutas base para almacenar resultados
    results_dir = r"C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\histology_bone_analyzer\data\sample_results\breaking_app"
    
    # Crear la carpeta si no existe
    os.makedirs(results_dir, exist_ok=True)
    
    # Ignorar advertencias de PIL sobre imágenes grandes
    # Esto evita el error por DecompressionBombWarning
    Image.MAX_IMAGE_PIXELS = None  # Deshabilitar el límite de tamaño de imagen
    
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
              fg="white", bg='#000000').pack(expand=True)  # Texto blanco, fondo negro
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
            imagen_final, areas, canales, cuad_min_contiguo_idx = analizar_cuadrantes(
                imagen, df, imagen_cuadrantes_path
            )
            
            # Cerrar ventana de progreso
            progreso.destroy()
            
            # Mostrar resultados
            visualizar_resultados_cuadrantes(root, imagen_cuadrantes_path, areas, canales, cuad_min_contiguo_idx)
            
        except Exception as e:
            progreso.destroy()
            messagebox.showerror("Error", f"Error durante el análisis: {e}")
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Crear botones en la ventana principal
    titulo = Label(root, text="Análisis de Canales de Havers por Cuadrantes", 
                  font=("Helvetica", 24), fg="white", bg='#000000')  # Texto blanco, fondo negro
    titulo.pack(pady=30)
    
    descripcion = Label(root, text="Esta aplicación analiza la distribución de canales de Havers en una matriz 6×6 (36 cuadrantes)\n"
                       "y destaca el cuadrante con mayor densidad de canales.",
                       font=("Helvetica", 14), fg="white", bg='#000000')  # Texto blanco, fondo negro
    descripcion.pack(pady=20)
    
    iniciar_button = Button(root, text="Iniciar Análisis", command=iniciar_analisis)
    configure_button(iniciar_button)
    iniciar_button.pack(pady=30)
    
    # Iniciar la aplicación
    root.mainloop()

if __name__ == '__main__':
    main()