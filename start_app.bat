@echo off
echo Starting News App - Full Stack
echo.
echo This will start both the backend (Flask) and frontend (React) servers
echo.
echo Backend will run on: http://localhost:5000
echo Frontend will run on: http://localhost:3000
echo.
echo Press Ctrl+C to stop both servers
echo.

echo Starting Flask backend...
start "Flask Backend" cmd /k "python app.py"

echo Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak > nul

echo Starting React frontend...
start "React Frontend" cmd /k "npm start"

echo.
echo Both servers are starting...
echo Open your browser and go to: http://localhost:3000
echo.
pause
