@echo off
echo.
echo ============================================
echo   Upload jardins-bergeronnette.fr vers OVH
echo ============================================
echo.
cd /d "%~dp0"
python upload-ovh.py
echo.
pause
