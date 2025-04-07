import cv2
import os
import shutil
import pandas as pd
from math import ceil, pi
from ultralytics import YOLO
import torch
from tkinter import Tk, Button, Text, Scrollbar, Frame, Label, filedialog
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import numpy as np

# Define base directory for all image-related files
BASE_DIR = r"C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\All_img_related\detection_app"
# Define paths for segmented images and results
IMAGES_SEGMENTED_DIR = os.path.join(BASE_DIR, "images_segmented")
OUTPUT_DIR = os.path.join(BASE_DIR, "resultado_img")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

def configure_window(window, title):
    window.title(title)
    window.geometry("800x600")
    window.configure(bg='#001f3f')

def configure_button(button):
    # Define el aspecto visual del botón
    button.configure(
        bg="#4CAF50",
        fg="white",
        font=("Helvetica", 12),
        padx=10,
        pady=5,
        relief="raised",
        borderwidth=2
    )
    # Añadir efectos hover si se desea
    button.bind("<Enter>", lambda e: button.configure(bg="#45a049"))
    button.bind("<Leave>", lambda e: button.configure(bg="#4CAF50"))

def select_image(root):
    image_path = None
    
    def on_button_click():
        nonlocal image_path
        file_path = askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            image_path = file_path
            root.quit()
            for widget in root.winfo_children():
                widget.destroy()

    configure_window(root, "Select Image")
    title = Label(root, text="PhygitalBone 2.0", font=("Helvetica", 24), fg="white", bg="#001f3f")
    title.pack(pady=20)

    button = Button(root, text="Load Image", command=on_button_click)
    configure_button(button)
    button.pack(expand=True)

    root.mainloop()
    return image_path

def divide_and_save_image(image_path, output_dir, num_segments=150):
    """
    Divide una imagen en segmentos más pequeños y los guarda en el directorio especificado.
    """
    # Verificar si el directorio existe y limpiarlo (sin eliminarlo)
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            if file.startswith("segment_") and file.endswith(".png"):
                os.remove(os.path.join(output_dir, file))
    else:
        os.makedirs(output_dir, exist_ok=True)

    # Leer la imagen
    print(f"Leyendo imagen desde: {image_path}")
    try:
        # Usar cv2.imread directamente para leer la imagen
        image = cv2.imread(image_path)
        
        # Si falla, intentar con otro método
        if image is None:
            print("cv2.imread falló, intentando otro método...")
            # Leer como bytes y decodificar
            with open(image_path, 'rb') as f:
                img_bytes = f.read()
            image = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
            
        if image is None:
            print(f"Error: No se pudo cargar la imagen {image_path}")
            return None, None, None
    except Exception as e:
        print(f"Error al leer la imagen: {e}")
        return None, None, None

    # Obtener dimensiones de la imagen
    print(f"Dimensiones de la imagen: {image.shape}")
    
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
            print(f"Guardado segmento {i * cols + j + 1} en {segment_path}")
            
            segment_positions.append((start_x, start_y, i * cols + j + 1))

    print(f"Se guardaron {len(segment_positions)} segmentos en {output_dir}")
    return segment_positions, segment_width, segment_height

def calculate_box_centers_and_areas(boxes, start_x, start_y, segment_id):
    """
    Calcula los centros y áreas de las cajas de detección.
    """
    centers = []
    for box in boxes:
        xyxy = box.xyxy.clone().detach().cpu().view(1, 4)
        width = xyxy[0, 2] - xyxy[0, 0]
        height = xyxy[0, 3] - xyxy[0, 1]
        cx = start_x + (xyxy[0, 0] + xyxy[0, 2]) / 2
        cy = start_y + (xyxy[0, 1] + xyxy[0, 3]) / 2
        semi_major_axis = width / 2
        semi_minor_axis = height / 2
        ellipse_area = pi * semi_major_axis * semi_minor_axis  # Calcula el área de la elipse
        centers.append((cx, cy, segment_id, ellipse_area))
    return centers

def plot_centers(df, image_path):
    """
    Genera un gráfico de dispersión con los centros de los canales de Havers.
    """
    plt.figure(figsize=(10, 10))
    # Cargar la imagen inicial
    image = plt.imread(image_path)
    plt.imshow(image, extent=[0, image.shape[1], image.shape[0], 0], alpha=0.6)
    plt.scatter(df['Center X'], df['Center Y'], c='blue', marker='o', s=10)  # Puntos más pequeños
    plt.title('Mapa de coordenadas de canales de Havers')
    plt.xlabel('Center X')
    plt.ylabel('Center Y')
    plt.grid(True)
    plt.gca().invert_yaxis()  # Invertir el eje Y para que coincida con la representación de la imagen
    
    # Guardar en archivo físico
    plot_filename = os.path.join(RESULTS_DIR, "mapa_coordenadas.png")
    plt.savefig(plot_filename, format='png', dpi=100)
    plt.close()
    return plot_filename

def plot_heatmap(df, image_path):
    """
    Genera un mapa de calor para visualizar la densidad de canales de Havers.
    """
    plt.figure(figsize=(10, 10))
    # Generar el mapa de calor
    heatmap, xedges, yedges = np.histogram2d(df['Center X'], df['Center Y'], bins=(100, 100))
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    plt.imshow(heatmap.T, extent=extent, origin='lower', cmap='hot', alpha=0.6)
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
    plt.savefig(heatmap_filename, format='png', dpi=100)
    plt.close()
    return heatmap_filename

def calculate_distance_matrix(centers_df):
    """
    Calcula la distancia media entre los centros de los canales de Havers.
    """
    distances = []
    points = centers_df[['Center X', 'Center Y']].values
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = np.sqrt(((points[i] - points[j]) ** 2).sum())
            distances.append(dist)
    return np.mean(distances) if distances else 0

def show_results_simple(root, results):
    """
    Muestra los resultados en una interfaz simple.
    """
    for widget in root.winfo_children():
        widget.destroy()
    
    configure_window(root, "PhygitalBone 2.0 - Results")
    
    # Título
    title = Label(root, text="Resultados del análisis", font=("Helvetica", 20), fg="white", bg="#001f3f")
    title.pack(pady=20)
    
    # Mostrar estadísticas
    stats_frame = Frame(root, bg="#001f3f", padx=20, pady=20)
    stats_frame.pack(fill="both", expand=True)
    
    stats_text = f"""
    Número de canales de Havers detectados: {results['count']}
    
    Área promedio de los canales: {results['avg_area']:.2f} pixels²
    
    Distancia media entre canales: {results['avg_distance']:.2f} pixels
    """
    
    stats_label = Label(stats_frame, text=stats_text, font=("Helvetica", 14), 
                       fg="white", bg="#001f3f", justify="left")
    stats_label.pack(anchor="w", pady=10)
    
    # Información de archivos
    files_text = f"""
    Archivos generados:
    
    Excel con coordenadas: {results['excel_path']}
    Mapa de coordenadas: {results['plot_path']}
    Mapa de calor: {results['heatmap_path']}
    """
    
    files_label = Label(stats_frame, text=files_text, font=("Helvetica", 12), 
                       fg="white", bg="#001f3f", justify="left")
    files_label.pack(anchor="w", pady=10)
    
    # Botones para abrir resultados
    buttons_frame = Frame(root, bg="#001f3f", padx=20, pady=20)
    buttons_frame.pack(fill="x")
    
    # Función para abrir archivos
    def open_file(file_path):
        import os
        import subprocess
        
        if os.path.exists(file_path):
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # Linux, macOS
                subprocess.call(('xdg-open', file_path))
    
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
    
    # Mantener la ventana abierta
    root.mainloop()

def resize_image_if_too_large(image_path, max_pixels=178956970):
    """
    Redimensiona una imagen si es demasiado grande.
    """
    print(f"Verificando tamaño de imagen: {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        return False
    
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
        
        # Guardar versión redimensionada (con un nombre diferente)
        resized_path = image_path.rsplit('.', 1)[0] + '_resized.' + image_path.rsplit('.', 1)[1]
        cv2.imwrite(resized_path, resized)
        print(f"Imagen redimensionada guardada en: {resized_path}")
        
        return resized_path
    
    return image_path

def main():
    """
    Función principal del programa.
    """
    # Asegurar que los directorios base existan
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    # Crear ventana principal
    root = Tk()
    
    # Selección de imagen
    image_path = select_image(root)
    if not image_path:
        print("No se seleccionó ninguna imagen.")
        root.destroy()
        return
    
    # Imprimir la ruta de la imagen para depuración
    print(f"Imagen seleccionada: {image_path}")
    
    # Verificar que el archivo existe
    if not os.path.exists(image_path):
        print(f"ERROR: El archivo {image_path} no existe.")
        root.destroy()
        return
    
    # Antes de dividir la imagen, verifica su tamaño
    image_path = resize_image_if_too_large(image_path)
    if not image_path:
        print("Error al procesar la imagen.")
        root.destroy()
        return
    
    # Actualizar la ventana para mostrar el progreso
    root = Tk()  # Crear una nueva ventana ya que la anterior se cerró
    configure_window(root, "Processing")
    Label(root, text="Processing, please wait...", font=("Helvetica", 16), fg="white", bg='#001f3f').pack(expand=True)
    root.update()
    
    confidence_threshold = 0.4
    
    try:
        # Dividir la imagen en segmentos
        print(f"Dividiendo imagen {image_path} en segmentos...")
        segment_positions, segment_width, segment_height = divide_and_save_image(image_path, IMAGES_SEGMENTED_DIR)
        if segment_positions is None:
            print("Error al dividir la imagen.")
            root.destroy()
            return
        
        # Cargar modelo YOLO
        print("Cargando modelo YOLO...")
        model_path = r"C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\runs\detect\train\weights\best.pt"
        print(f"Ruta del modelo: {model_path}")
        
        # Comprobar si el modelo existe en esta ruta
        if not os.path.exists(model_path):
            print(f"Modelo no encontrado en: {model_path}")
            print("Intentando rutas alternativas...")
            
            # Intentar con rutas alternativas
            alternative_paths = [
                r"C:\Users\joanb\OneDrive\Escritorio\TFG\workspace\runs\detect\train\weights\best.pt",
                r"C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\runs\detect\train13\weights\best.pt",
                r"C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\osteona\best.pt"
            ]
            
            for alt_path in alternative_paths:
                print(f"Comprobando: {alt_path}")
                if os.path.exists(alt_path):
                    model_path = alt_path
                    print(f"Modelo encontrado en: {model_path}")
                    break
        
        if not os.path.exists(model_path):
            print(f"ERROR: No se encontró el modelo en ninguna de las rutas verificadas.")
            root.destroy()
            return
            
        model = YOLO(model_path)
        
        # Obtener lista de archivos de segmentos
        segment_files = sorted(
            [f for f in os.listdir(IMAGES_SEGMENTED_DIR) if f.startswith("segment_") and f.endswith('.png')],
            key=lambda x: int(x.split('_')[-1].split('.')[0]) if '_' in x and x.split('_')[-1].split('.')[0].isdigit() else 0
        )
        
        if not segment_files:
            print(f"No se encontraron archivos de segmentos en {IMAGES_SEGMENTED_DIR}")
            root.destroy()
            return
            
        print(f"Se encontraron {len(segment_files)} archivos de segmentos")
        
        # Lista para almacenar los centros y áreas de las cajas delimitadoras
        box_centers_and_areas = []
        
        # Analizar cada segmento
        print("Analizando segmentos con el modelo YOLO...")
        for idx, (start_x, start_y, segment_id) in enumerate(segment_positions):
            segment_filename = f"segment_{segment_id}.png"
            segment_path = os.path.join(IMAGES_SEGMENTED_DIR, segment_filename)
            
            if not os.path.exists(segment_path):
                print(f"Advertencia: Archivo de segmento no encontrado: {segment_path}")
                continue
                
            print(f"Analizando segmento {segment_id}: {segment_path}")
            
            # Realizar detección con YOLO
            results = model(segment_path, conf=confidence_threshold)
            
            for result in results:
                boxes = result.boxes
                print(f"Segmento {segment_id}: Se detectaron {len(boxes)} canales de Havers")
                centers = calculate_box_centers_and_areas(boxes, start_x, start_y, segment_id)
                box_centers_and_areas.extend(centers)

                # Guardar imagen con anotaciones
                annotated_img = result.plot()
                output_path = os.path.join(OUTPUT_DIR, f"result_{segment_id}.png")
                
                # Asegurar que el directorio de salida existe
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                
                cv2.imwrite(output_path, annotated_img)
        
        # Si no se detectaron canales
        if not box_centers_and_areas:
            print("No se detectaron canales de Havers.")
            root.destroy()
            return
        
        print(f"Se detectaron un total de {len(box_centers_and_areas)} canales de Havers")
        
        # Generar DataFrame con coordenadas y áreas
        df = pd.DataFrame(box_centers_and_areas, columns=['Center X', 'Center Y', 'Segment ID', 'Ellipse Area (pixels^2)'])
        excel_path = os.path.join(RESULTS_DIR, 'bounding_box_centers.xlsx')
        
        df.to_excel(excel_path, index=False)
        print(f"Centros y áreas de las cajas delimitadoras guardados en {excel_path}")
        
        # Generar visualizaciones
        print("Generando visualizaciones...")
        plot_filename = plot_centers(df, image_path)
        heatmap_filename = plot_heatmap(df, image_path)
        avg_area = df['Ellipse Area (pixels^2)'].mean()
        count_havers = df.shape[0]
        avg_distance = calculate_distance_matrix(df)
        
        # Preparar resultados
        results = {
            'excel_path': excel_path,
            'plot_path': plot_filename,
            'heatmap_path': heatmap_filename,
            'avg_area': avg_area,
            'count': count_havers,
            'avg_distance': avg_distance
        }
        
        # Mostrar resultados
        print("Mostrando resultados...")
        show_results_simple(root, results)
        
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
        root.destroy()

if __name__ == '__main__':
    main()