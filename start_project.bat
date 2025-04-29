@echo off
call C:\Users\joanb\anaconda3\Scripts\activate.bat
call conda activate TFG
cd C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg\histology_bone_analyzer
start cmd /k "conda activate TFG && title TFG Project"
code . "apps\1detection_app\detection_app.py"