from ultralytics import YOLO
import os

# Configura la ruta al archivo data.yaml
DATA_YAML_PATH = r'C:\Users\joanb\OneDrive\Escritorio\TFG\workspace\osteona\Roboflow\OsteonasDetector.v1i.yolov8\data.yaml'

def train_yolo_model():
    # Crea un nuevo modelo YOLOv8-nano
    model = YOLO('yolov8n.pt')
    
    # Configura y entrena el modelo
    results = model.train(
        data=DATA_YAML_PATH,
        epochs=100,
        imgsz=640,
        batch=16,
        patience=50,
        verbose=True,
        device=0       # Cambiado de 'device='0'' a 'device=0'
    )
    
    print("Entrenamiento completado!")
    print(f"El modelo entrenado se ha guardado en: {model.export()}")

if __name__ == "__main__":
    train_yolo_model()