@echo off
chcp 65001 >nul
echo 🚀 Starting Khel Bhoomi Development Server
echo ======================================
echo.

REM Check if MongoDB is running (Windows)
echo Checking MongoDB status...
tasklist /FI "IMAGENAME eq mongod.exe" 2>NUL | find /I /N "mongod.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ MongoDB is already running
) else (
    echo Starting MongoDB service...
    net start MongoDB 2>NUL || echo Please start MongoDB manually: net start MongoDB
)

REM Start backend
echo.
echo Starting backend server...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating backend .env file...
    copy .env.example .env
)

REM Create dummy users
echo Setting up dummy users...
python create_dummy_users.py 2>NUL || echo Dummy users already exist or MongoDB not ready

REM Start backend server in new window
start "Khel Bhoomi Backend" cmd /k "venv\Scripts\activate && uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
cd ..

REM Wait for backend
echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

REM Start frontend
echo.
echo Starting frontend server...
cd frontend

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating frontend .env file...
    copy .env.example .env
)

REM Install dependencies if needed
if not exist "node_modules" (
    echo Installing frontend dependencies...
    where yarn >nul 2>nul
    if %errorlevel% equ 0 (
        yarn install
    ) else (
        npm install
    )
)

REM Start frontend server in new window
where yarn >nul 2>nul
if %errorlevel% equ 0 (
    start "Khel Bhoomi Frontend" cmd /k "yarn start"
) else (
    start "Khel Bhoomi Frontend" cmd /k "npm start"
)
cd ..

echo.
echo ✅ Khel Bhoomi is starting up!
echo 📍 Frontend: http://localhost:3000
echo 📍 Backend: http://localhost:8001
echo 📍 API Docs: http://localhost:8001/docs
echo.
echo 🔒 Demo Credentials:
echo    - Athlete: demo_athlete / demo123
echo    - Scout: demo_scout / demo123
echo    - Fan: demo_fan / demo123
echo.
echo Close the terminal windows to stop the servers
echo.
pause