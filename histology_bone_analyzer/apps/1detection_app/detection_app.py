import cv2
import os
import shutil
import pandas as pd
from math import ceil, pi
from ultralytics import YOLO
import torch
from tkinter import Tk, Button, Text, Scrollbar, Frame, Label, filedialog, StringVar
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import numpy as np

# Rutas de directorios
BASE_DIR = r"C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\histology_bone_analyzer\data\sample_results\detection_app"
IMAGES_SEGMENTED_DIR = os.path.join(BASE_DIR, "images_segmented")
OUTPUT_DIR = os.path.join(BASE_DIR, "segmented_results")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
EXCEL_DIR = os.path.join(BASE_DIR, "excel")
TECHNICAL_DIR = r"C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\histology_bone_analyzer\docs\technical"
RECONSTRUCTED_IMAGES_DIR = r"C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\histology_bone_analyzer\data\sample_images"

# Color corporativo
BACKGROUND_COLOR = '#000000'  # Negro para el fondo
BUTTON_COLOR = '#BD0000'      # Rojo para los botones
BUTTON_HOVER_COLOR = '#333333'  # Gris para el hover de botones
TEXT_COLOR = 'white'          # Blanco para todo el texto

def initialize_directories():
    """Crea todas las carpetas necesarias si no existen."""
    for directory in [BASE_DIR, IMAGES_SEGMENTED_DIR, OUTPUT_DIR, RESULTS_DIR, EXCEL_DIR, TECHNICAL_DIR, RECONSTRUCTED_IMAGES_DIR]:
        os.makedirs(directory, exist_ok=True)

def configure_window(window, title):
    """Configura el aspecto visual y posición de la ventana."""
    window.title(title)
    
    # Configurar tamaños y posición
    ancho_ventana = 800
    alto_ventana = 600
    x = (window.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y = (window.winfo_screenheight() // 2) - (alto_ventana // 2)
    window.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
    
    # Permitir redimensión
    window.resizable(True, True)
    
    # Establecer tamaño mínimo
    window.minsize(600, 400)
    
    # Color de fondo negro
    window.configure(bg=BACKGROUND_COLOR)

def configure_button(button):
    """Aplica estilo visual a los botones."""
    button.configure(
        bg=BUTTON_COLOR,  # Rojo para los botones
        fg=TEXT_COLOR,    # Texto blanco
        font=("Helvetica", 12),
        padx=10,
        pady=5,
        relief="raised",
        borderwidth=2
    )
    # Añadir efectos hover
    button.bind("<Enter>", lambda e: button.configure(bg=BUTTON_HOVER_COLOR))
    button.bind("<Leave>", lambda e: button.configure(bg=BUTTON_COLOR))

def clear_window(window):
    """Elimina todos los widgets de una ventana."""
    for widget in window.winfo_children():
        widget.destroy()

def select_image_in_window(window):
    """Interfaz para seleccionar una imagen, reutilizando la ventana existente."""
    clear_window(window)
    configure_window(window, "Select Image")
    
    image_path_var = StringVar()
    
    def on_button_click():
        file_path = askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            image_path_var.set(file_path)
            window.quit()  # Solo detiene el mainloop, no destruye la ventana
    
    title = Label(window, text="Phygital Bone 3.0", font=("Helvetica", 24), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
    title.pack(pady=20)
    
    button = Button(window, text="Load Image", command=on_button_click)
    configure_button(button)
    button.pack(expand=True)
    
    window.mainloop()  # Espera hasta que se seleccione una imagen
    
    return image_path_var.get()

def show_processing_screen(window):
    """Muestra pantalla de procesamiento reutilizando la ventana existente."""
    clear_window(window)
    configure_window(window, "Processing")
    Label(window, text="Processing, please wait...", font=("Helvetica", 16), 
          fg="white", bg=BACKGROUND_COLOR).pack(expand=True)
    window.update()

def resize_image_if_too_large(image_path, max_pixels=178956970):
    """Redimensiona una imagen si es demasiado grande."""
    print(f"Verificando tamaño de imagen: {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    height, width = img.shape[:2]
    pixels = height * width
    print(f"Tamaño original: {width}x{height} = {pixels} píxeles")
    
    if pixels > max_pixels:
        # Calcular factor de escala para reducir
        scale = (max_pixels / pixels) ** 0.5
        new_width = int(width * scale)
        new_height = int(height * scale)
        print(f"Redimensionando a: {new_width}x{new_height}")
        
        # Redimensionar
        resized = cv2.resize(img, (new_width, new_height))
        
        # Guardar versión redimensionada
        resized_path = image_path.rsplit('.', 1)[0] + '_resized.' + image_path.rsplit('.', 1)[1]
        cv2.imwrite(resized_path, resized)
        print(f"Imagen redimensionada guardada en: {resized_path}")
        
        return resized_path
    
    return image_path

def divide_and_save_image(image_path, output_dir, num_segments=150):
    """Divide una imagen en segmentos más pequeños y los guarda."""
    # Limpiar carpeta de segmentos
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            if file.startswith("segment_") and file.endswith(".png"):
                os.remove(os.path.join(output_dir, file))
    else:
        os.makedirs(output_dir, exist_ok=True)

    # Leer la imagen
    print(f"Leyendo imagen desde: {image_path}")
    try:
        image = cv2.imread(image_path)
        
        # Si falla, intentar método alternativo
        if image is None:
            print("cv2.imread falló, intentando otro método...")
            with open(image_path, 'rb') as f:
                img_bytes = f.read()
            image = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
            
        if image is None:
            print(f"Error: No se pudo cargar la imagen {image_path}")
            return None, None, None
    except Exception as e:
        print(f"Error al leer la imagen: {e}")
        return None, None, None

    # Configurar la división
    cols = 15
    rows = ceil(num_segments / cols)
    segment_height = image.shape[0] // rows
    segment_width = image.shape[1] // cols
    
    print(f"Dividiendo en {rows}x{cols} segmentos")
    print(f"Tamaño de cada segmento: {segment_width}x{segment_height}")

    # Dividir y guardar
    segment_positions = []
    for i in range(rows):
        for j in range(cols):
            start_y = i * segment_height
            end_y = start_y + segment_height if i < rows - 1 else image.shape[0]
            start_x = j * segment_width
            end_x = start_x + segment_width if j < cols - 1 else image.shape[1]
            
            segment = image[start_y:end_y, start_x:end_x]
            segment_filename = f"segment_{i * cols + j + 1}.png"
            segment_path = os.path.join(output_dir, segment_filename)
            
            cv2.imwrite(segment_path, segment)
            
            segment_positions.append((start_x, start_y, i * cols + j + 1))

    print(f"Se guardaron {len(segment_positions)} segmentos en {output_dir}")
    return segment_positions, segment_width, segment_height

def find_model_path():
    """Busca la ruta del modelo YOLO en diferentes ubicaciones posibles."""
    # Ruta principal donde debería estar el modelo
    main_path = r"C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\histology_bone_analyzer\models\weights.pt"
    
    # Si existe, retornarlo directamente
    if os.path.exists(main_path):
        return main_path
        
    # Rutas alternativas a revisar
    alternative_paths = [
        r"C:\Users\joanb\OneDrive\Escritorio\TFG\workspace\runs\detect\train\weights\weights.pt",
        r"C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\runs\detect\train13\weights\weights.pt",
        r"C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\osteona\weights.pt"
    ]
    
    # Revisar cada ruta alternativa
    for path in alternative_paths:
        if os.path.exists(path):
            return path
    
    # Si no se encuentra, retornar None
    return None

def calculate_box_centers_and_areas(boxes, start_x, start_y, segment_id):
    """Calcula los centros y áreas de las cajas de detección."""
    centers = []
    for box in boxes:
        xyxy = box.xyxy.clone().detach().cpu().view(1, 4)
        width = xyxy[0, 2] - xyxy[0, 0]
        height = xyxy[0, 3] - xyxy[0, 1]
        cx = start_x + (xyxy[0, 0] + xyxy[0, 2]) / 2
        cy = start_y + (xyxy[0, 1] + xyxy[0, 3]) / 2
        semi_major_axis = width / 2
        semi_minor_axis = height / 2
        ellipse_area = pi * semi_major_axis * semi_minor_axis
        centers.append((cx, cy, segment_id, ellipse_area))
    return centers

def process_image_segments(segment_positions, model, confidence_threshold=0.4):
    """Procesa cada segmento con el modelo YOLO."""
    box_centers_and_areas = []
    
    for start_x, start_y, segment_id in segment_positions:
        segment_filename = f"segment_{segment_id}.png"
        segment_path = os.path.join(IMAGES_SEGMENTED_DIR, segment_filename)
        
        if not os.path.exists(segment_path):
            print(f"Advertencia: Archivo de segmento no encontrado: {segment_path}")
            continue
            
        # Detectar con YOLO
        results = model(segment_path, conf=confidence_threshold)
        
        for result in results:
            boxes = result.boxes
            print(f"Segmento {segment_id}: Se detectaron {len(boxes)} canales de Havers")
            centers = calculate_box_centers_and_areas(boxes, start_x, start_y, segment_id)
            box_centers_and_areas.extend(centers)

            # Guardar imagen con anotaciones
            annotated_img = result.plot()
            output_path = os.path.join(OUTPUT_DIR, f"result_{segment_id}.png")
            cv2.imwrite(output_path, annotated_img)

            # También guardar una copia en la nueva ubicación para imágenes reconstruidas
            reconstructed_path = os.path.join(RECONSTRUCTED_IMAGES_DIR, f"reconstructed_{segment_id}.png")
            cv2.imwrite(reconstructed_path, annotated_img)
    
    return box_centers_and_areas

def calculate_distance_matrix(centers_df):
    """Calcula la distancia media entre los centros de los canales de Havers."""
    distances = []
    points = centers_df[['Center X', 'Center Y']].values
    
    # Si hay menos de 2 puntos, no se puede calcular distancias
    if len(points) < 2:
        return 0
        
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = np.sqrt(((points[i] - points[j]) ** 2).sum())
            distances.append(dist)
    
    return np.mean(distances) if distances else 0

def plot_centers(df, image_path):
    """Genera un gráfico de dispersión con los centros de los canales de Havers."""
    plt.figure(figsize=(16, 16))
    # Cargar la imagen inicial
    image = plt.imread(image_path)
    plt.imshow(image, extent=[0, image.shape[1], image.shape[0], 0], alpha=0.6)
    plt.scatter(df['Center X'], df['Center Y'], c=BUTTON_COLOR, marker='o', s=10)  # Puntos rojos (color de botones)
    plt.title('Mapa de coordenadas de canales de Havers')
    plt.xlabel('Center X')
    plt.ylabel('Center Y')
    plt.grid(True)
    plt.gca().invert_yaxis()
    
    # Guardar en archivo físico
    plot_filename = os.path.join(RESULTS_DIR, "mapa_coordenadas.png")
    plt.savefig(plot_filename, format='png', dpi=600, bbox_inches='tight')
    plt.close()
    return plot_filename

def plot_heatmap(df, image_path):
    """Genera un mapa de calor para visualizar la densidad de canales de Havers."""
    plt.figure(figsize=(16, 16))
    # Generar el mapa de calor
    heatmap, xedges, yedges = np.histogram2d(df['Center X'], df['Center Y'], bins=(100, 100))
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    plt.imshow(heatmap.T, extent=extent, origin='lower', cmap='Reds', alpha=0.6)
    plt.colorbar()
    # Cargar la imagen inicial con transparencia
    image = plt.imread(image_path)
    plt.imshow(image, extent=[0, image.shape[1], image.shape[0], 0], alpha=0.4)
    plt.title('Mapa de densidad de canales de Havers')
    plt.xlabel('Center X')
    plt.ylabel('Center Y')
    plt.grid(True)
    plt.gca().invert_yaxis()
    
    # Guardar en archivo físico
    heatmap_filename = os.path.join(RESULTS_DIR, "mapa_calor.png")
    plt.savefig(heatmap_filename, format='png', dpi=600, bbox_inches='tight')
    plt.close()
    return heatmap_filename

def generate_visualizations(df, image_path):
    """Genera todas las visualizaciones y estadísticas."""
    plot_filename = plot_centers(df, image_path)
    heatmap_filename = plot_heatmap(df, image_path)
    avg_area = df['Ellipse Area (pixels^2)'].mean()
    count_havers = df.shape[0]
    avg_distance = calculate_distance_matrix(df)
    
    return {
        'plot_path': plot_filename,
        'heatmap_path': heatmap_filename,
        'avg_area': avg_area,
        'count': count_havers,
        'avg_distance': avg_distance
    }

def save_results_to_excel(box_centers_and_areas):
    """Guarda los resultados en Excel y crea una copia de seguridad."""
    # Crear DataFrame
    df = pd.DataFrame(box_centers_and_areas, columns=['Center X', 'Center Y', 'Segment ID', 'Ellipse Area (pixels^2)'])
    
    # Guardar en la ubicación principal
    excel_path = os.path.join(EXCEL_DIR, 'bounding_box_centers.xlsx')
    df.to_excel(excel_path, index=False)
    print(f"Centros y áreas de las cajas delimitadoras guardados en {excel_path}")
    
    # Crear copia en directorio técnico
    excel_copy_path = os.path.join(TECHNICAL_DIR, 'bounding_box_centers_copy.xlsx')
    shutil.copy2(excel_path, excel_copy_path)
    print(f"Copia del archivo Excel guardada en {excel_copy_path}")
    
    return excel_path, df

def open_file(file_path):
    """Abre un archivo con la aplicación predeterminada del sistema."""
    import os
    import subprocess
    
    if os.path.exists(file_path):
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # Linux, macOS
            subprocess.call(('xdg-open', file_path))

def show_results(window, results):
    """Muestra los resultados en la interfaz gráfica."""
    clear_window(window)
    configure_window(window, "PhygitalBone 2.0 - Results")
    
    # Título
    title = Label(window, text="Resultados del análisis", font=("Helvetica", 20), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
    title.pack(pady=20)
    
    # Mostrar estadísticas
    stats_frame = Frame(window, bg=BACKGROUND_COLOR, padx=20, pady=20)
    stats_frame.pack(fill="both", expand=True)
    
    stats_text = f"""
    Número de canales de Havers detectados: {results['count']}
    
    Área promedio de los canales: {results['avg_area']:.2f} pixels²
    
    Distancia media entre canales: {results['avg_distance']:.2f} pixels
    """
    
    stats_label = Label(stats_frame, text=stats_text, font=("Helvetica", 14), 
                       fg=TEXT_COLOR, bg=BACKGROUND_COLOR, justify="left")
    stats_label.pack(anchor="w", pady=10)
    
    # Información de archivos
    files_text = f"""
    Archivos generados:
    
    Excel con coordenadas: {results['excel_path']}
    Mapa de coordenadas: {results['plot_path']}
    Mapa de calor: {results['heatmap_path']}
    """
    
    files_label = Label(stats_frame, text=files_text, font=("Helvetica", 12), 
                       fg=TEXT_COLOR, bg=BACKGROUND_COLOR, justify="left")
    files_label.pack(anchor="w", pady=10)
    
    # Botones para abrir resultados
    buttons_frame = Frame(window, bg=BACKGROUND_COLOR, padx=20, pady=20)
    buttons_frame.pack(fill="x")
    
    # Botón para abrir Excel
    excel_button = Button(buttons_frame, text="Ver datos en Excel", 
                         command=lambda: open_file(results['excel_path']))
    configure_button(excel_button)
    excel_button.pack(side="left", padx=10)
    
    # Botón para abrir mapa de coordenadas
    plot_button = Button(buttons_frame, text="Ver mapa de coordenadas", 
                        command=lambda: open_file(results['plot_path']))
    configure_button(plot_button)
    plot_button.pack(side="left", padx=10)
    
    # Botón para abrir mapa de calor
    heatmap_button = Button(buttons_frame, text="Ver mapa de calor", 
                           command=lambda: open_file(results['heatmap_path']))
    configure_button(heatmap_button)
    heatmap_button.pack(side="left", padx=10)
    
    # Botón para abrir carpeta de resultados
    folder_button = Button(buttons_frame, text="Abrir carpeta de resultados", 
                          command=lambda: open_file(RESULTS_DIR))
    configure_button(folder_button)
    folder_button.pack(side="left", padx=10)
    
    window.mainloop()

def handle_error(error, window=None):
    """Maneja errores de forma centralizada."""
    print(f"Error durante la ejecución: {error}")
    import traceback
    traceback.print_exc()
    
    if window:
        window.destroy()

def process_image(image_path, window):
    """Procesa una imagen completa desde la división hasta el análisis."""
    try:
        # Dividir la imagen en segmentos
        print(f"Dividiendo imagen {image_path} en segmentos...")
        segment_positions, segment_width, segment_height = divide_and_save_image(image_path, IMAGES_SEGMENTED_DIR)
        if segment_positions is None:
            print("Error al dividir la imagen.")
            return None
        
        # Cargar modelo YOLO
        print("Cargando modelo YOLO...")
        model_path = find_model_path()
        if not model_path:
            print("ERROR: No se encontró el modelo en ninguna de las rutas verificadas.")
            return None
            
        model = YOLO(model_path)
        print(f"Modelo cargado desde: {model_path}")
        
        # Procesar segmentos con el modelo
        print("Analizando segmentos con el modelo YOLO...")
        box_centers_and_areas = process_image_segments(segment_positions, model)
        
        # Verificar si se detectaron canales
        if not box_centers_and_areas:
            print("No se detectaron canales de Havers.")
            return None
        
        print(f"Se detectaron un total de {len(box_centers_and_areas)} canales de Havers")
        
        # Guardar resultados en Excel
        excel_path, df = save_results_to_excel(box_centers_and_areas)
        
        # Generar visualizaciones
        print("Generando visualizaciones...")
        visualization_results = generate_visualizations(df, image_path)
        
        # Combinar todos los resultados
        results = {
            'excel_path': excel_path,
            **visualization_results
        }
        
        return results
        
    except Exception as e:
        handle_error(e, window)
        return None

def main():
    """Función principal del programa."""
    # Crear directorios necesarios
    initialize_directories()
    
    # Crear ventana principal
    root = Tk()
    
    try:
        # Selección de imagen
        image_path = select_image_in_window(root)
        if not image_path:
            print("No se seleccionó ninguna imagen.")
            root.destroy()
            return
        
        # Verificar que el archivo existe
        if not os.path.exists(image_path):
            print(f"ERROR: El archivo {image_path} no existe.")
            root.destroy()
            return
        
        # Verificar y ajustar tamaño de imagen si es necesario
        image_path = resize_image_if_too_large(image_path)
        if not image_path:
            print("Error al procesar la imagen.")
            root.destroy()
            return
        
        # Mostrar pantalla de procesamiento
        show_processing_screen(root)
        
        # Procesar la imagen
        results = process_image(image_path, root)
        
        # Mostrar resultados
        if results:
            print("Mostrando resultados...")
            show_results(root, results)
        else:
            print("Error en el procesamiento de la imagen.")
            root.destroy()
            
    except Exception as e:
        handle_error(e, root)

if __name__ == '__main__':
    main()