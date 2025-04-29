# Código de prueba para ver si podemos mostrar una imagen simple
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import os

# Crear una imagen de prueba con matplotlib
plt.figure(figsize=(8, 6))
plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro-')
plt.title('Prueba de Visualización')
plt.grid(True)

# Guardar en archivo
test_img_path = "test_img.png"
plt.savefig(test_img_path)
plt.close()

# Función para mostrar la imagen
def show_test_image():
    # Crear una nueva ventana
    window = tk.Toplevel()
    window.title("Prueba de Imagen")
    window.geometry("800x600")
    
    try:
        # Cargar la imagen
        img = Image.open(test_img_path)
        img = img.resize((700, 500))
        photo = ImageTk.PhotoImage(img)
        
        # Crear label para mostrarla
        label = tk.Label(window, image=photo)
        label.image = photo  # Mantener referencia
        label.pack(padx=20, pady=20)
        
        print("Imagen cargada correctamente")
    except Exception as e:
        print(f"Error al cargar imagen: {e}")
        tk.Label(window, text=f"Error: {e}").pack()

# Crear ventana principal
root = tk.Tk()
root.title("Test")
root.geometry("300x200")

# Crear botón para mostrar la imagen
btn = tk.Button(root, text="Mostrar Imagen", command=show_test_image)
btn.pack(pady=50)

root.mainloop()

# Limpiar al finalizar
if os.path.exists(test_img_path):
    os.remove(test_img_path)