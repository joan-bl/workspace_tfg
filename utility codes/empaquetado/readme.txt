# Phygital Bone Analyzer - Empaquetado

## Requisitos Previos
- Anaconda con entorno virtual TFG
- Python 3.13
- Modelo YOLO entrenado

## Pasos de Empaquetado

### 1. Preparar Entorno
```bash
conda activate TFG
```

### 2. Instalar PyInstaller
```bash
pip install pyinstaller
```

### 3. Verificar Rutas
- Actualizar `YOLO_MODEL_PATH` en `havers_bone_analyzer.spec`
- Asegurar ruta correcta del script principal

### 4. Generar Ejecutable
```bash
pyinstaller havers_bone_analyzer.spec
```

### 5. Ubicación del Ejecutable
- Se generará en la carpeta `dist/PhygitalBoneAnalyzer`
- Contendrá ejecutable independiente

## Solución de Problemas
- Verificar todas las dependencias
- Comprobar compatibilidad de bibliotecas
- Revisar rutas de archivos

## Notas Adicionales
- El empaquetado puede tardar varios minutos
- Tamaño del ejecutable: ~500MB-1GB
- Requiere Windows 10/11 de 64 bits
```