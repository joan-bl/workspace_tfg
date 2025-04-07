@echo off
call C:\Users\joanb\anaconda3\Scripts\activate.bat
call conda activate TFG
cd C:\Users\joanb\OneDrive\Escritorio\TFG\Workspace_tfg
start cmd /k "conda activate TFG && title TFG Project"
code . "breaking_app\cuadrantes-analyzer.py"