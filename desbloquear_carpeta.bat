@echo off
echo ============================================
echo   DESBLOQUEADOR DE CARPETAS (Windows)
echo ============================================

REM --- PIDE LA RUTA DE LA CARPETA ---
set /p target="Introduce la ruta completa de la carpeta a desbloquear: "

echo.
echo Cerrando procesos que pueden bloquear Node...
taskkill /F /IM node.exe  >nul 2>&1
taskkill /F /IM code.exe  >nul 2>&1
taskkill /F /IM cmd.exe   >nul 2>&1

echo.
echo Otorgando permisos completos a la carpeta...
icacls "%target%" /grant *S-1-1-0:(OI)(CI)F /T >nul 2>&1

echo.
echo Quitando permisos de solo lectura...
attrib -r -s -h "%target%" /S /D

echo.
echo Intentando eliminar la carpeta node_modules...
rmdir /s /q "%target%\node_modules" >nul 2>&1

echo.
echo Intentando eliminar .staging bloqueado...
rmdir /s /q "%target%\node_modules\.staging" >nul 2>&1

echo.
echo Carpeta desbloqueada correctamente.
echo Ahora puedes ejecutar: npm install
echo ============================================
pause
