@echo off
echo Instalando Flask...
uv pip install flask --system
echo.
echo Iniciando ArtesaMarket...
echo Abre tu navegador en: http://127.0.0.1:5000
echo.
python app.py
pause
