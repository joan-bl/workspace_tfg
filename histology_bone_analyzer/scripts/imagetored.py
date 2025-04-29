import cv2
import numpy as np

# Cargar la imagen
image_path = r'C:\Users\joanb\OneDrive\Escritorio\TFG\workspace\runs\detect\train\confusion_matrix_normalized.png'
imagen = cv2.imread(image_path)

# Verificar que la imagen se cargó correctamente
if imagen is None:
    print("Error: No se pudo cargar la imagen")
    exit()

# Convertir a espacio de color HSV
hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Crear una máscara para los tonos azules
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([140, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Clonar la imagen original
imagen_roja = imagen.copy()

# Donde la máscara es verdadera (azules), cambiar a rojo
imagen_roja[mask > 0] = [0, 0, 255]  # Rojo en BGR

# Guardar la imagen
cv2.imwrite('imagen_roja.png', imagen_roja)

print("Imagen convertida y guardada como imagen_roja.png")