import cv2
import numpy as np
from matplotlib import pyplot as plt

# Cargar la imagen
image = cv2.imread('tu_imagen.png')

# Convertir la imagen a HSV para facilitar la detección de colores
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Definir el rango de colores rojos en HSV
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])

# Crear una máscara para los puntos rojos
mask = cv2.inRange(hsv_image, lower_red, upper_red)

# Aplicar la máscara a la imagen original
result = cv2.bitwise_and(image, image, mask=mask)

# Guardar la imagen resultante
cv2.imwrite('puntos_rojos.png', result)

# Mostrar la imagen resultante (opcional)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()