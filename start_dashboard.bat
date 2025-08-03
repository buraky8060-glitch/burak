@echo off
title RENDER Trading Dashboard
color 0A

echo.
echo ============================================
echo    RENDER TRADING DASHBOARD BASLATICI
echo ============================================
echo.

echo [1/4] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadi! Python'u yükleyin: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python bulundu!

echo.
echo [2/4] Gerekli paketler yükleniyor...
pip install flask flask-socketio requests numpy --quiet
if errorlevel 1 (
    echo ❌ Paket yükleme hatasi!
    pause
    exit /b 1
)
echo ✅ Paketler yüklendi!

echo.
echo [3/4] Dosyalar kontrol ediliyor...
if not exist "dashboard_integration.py" (
    echo ❌ dashboard_integration.py bulunamadi!
    pause
    exit /b 1
)
if not exist "templates\dashboard.html" (
    echo ❌ templates\dashboard.html bulunamadi!
    pause
    exit /b 1
)
echo ✅ Dosyalar mevcut!

echo.
echo [4/4] Dashboard baslatiliyor...
echo ⏳ Lutfen bekleyin...
echo.
echo ============================================
echo    DASHBOARD HAZIR!
echo ============================================
echo 📊 Adres: http://localhost:5000
echo 🌐 Browser otomatik olarak acilacak
echo 🛑 Durdurmak icin: CTRL+C
echo ============================================
echo.

start http://localhost:5000
python dashboard_integration.py

pause