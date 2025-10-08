@echo off
echo Starting NewsHub Application...
echo.

echo [1/2] Starting Flask Backend...
start "Flask Backend" cmd /k "python app.py"

timeout /t 3 /nobreak >nul

echo [2/2] Starting React Frontend...
start "React Frontend" cmd /k "npm start"

echo.
echo ✅ NewsHub is starting up!
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:5000
echo.
echo Press any key to exit...
pause >nul
