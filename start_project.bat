@echo off
call C:\Users\joanb\anaconda3\Scripts\activate.bat
call conda activate TFG
cd C:\Users\joanb\OneDrive\Escritorio\TFG\workspace
start cmd /k "conda activate TFG && title TFG Project"
code .