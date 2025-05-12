from roboflow import Roboflow

# Tu API Key de Roboflow
rf = Roboflow(api_key="Z2MuryeZnIvUISHKvSHV")
workspace = rf.workspace("phycharm30")  # Cambia por tu nombre de workspace

# Despliegue del modelo
workspace.deploy_model(
    model_type="yolov8",  # Tipo de modelo
    model_path="C:/Users/joanb/OneDrive/Escritorio/TFG/Workspace_tfg/Models/runs/detect/train/weights",  # Ruta a los pesos
    project_ids=["canales-de-havers"],  # ID de tu proyecto
    model_name="Detect_c_dehavers",  # Nombre para el modelo
    filename="best.pt"  # Nombre del archivo de pesos
)