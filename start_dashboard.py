#!/usr/bin/env python3
"""
🚀 RENDER Trading Dashboard - Otomatik Başlatıcı
Bu script dashboard'u otomatik olarak kurar ve başlatır
"""

import subprocess
import sys
import os
import webbrowser
import time

def check_python_version():
    """Python versiyonunu kontrol et"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 veya üzeri gerekli!")
        print(f"   Mevcut versiyon: {sys.version}")
        print("   Python'u güncelleyin: https://www.python.org/downloads/")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} - Uyumlu!")
    return True

def install_requirements():
    """Gerekli paketleri yükle"""
    print("\n📦 Gerekli paketler yükleniyor...")
    
    required_packages = [
        'flask==2.3.3',
        'flask-socketio==5.3.6', 
        'requests==2.31.0',
        'numpy==1.24.3',
        'python-socketio==5.8.0',
        'python-engineio==4.7.1',
        'eventlet==0.33.3',
        'werkzeug==2.3.7'
    ]
    
    try:
        for package in required_packages:
            print(f"   📥 {package.split('==')[0]} yükleniyor...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package, '--quiet'
            ])
        print("✅ Tüm paketler başarıyla yüklendi!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Paket yükleme hatası: {e}")
        print("   Manuel yükleme deneyin: pip install -r requirements.txt")
        return False

def check_files():
    """Gerekli dosyaları kontrol et"""
    print("\n📁 Dosyalar kontrol ediliyor...")
    
    required_files = [
        'dashboard_integration.py',
        'templates/dashboard.html'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"   ✅ {file}")
    
    if missing_files:
        print(f"❌ Eksik dosyalar: {missing_files}")
        return False
    
    print("✅ Tüm dosyalar mevcut!")
    return True

def create_directories():
    """Gerekli klasörleri oluştur"""
    print("\n📂 Klasörler oluşturuluyor...")
    
    directories = ['templates', 'static', 'static/css', 'static/js']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"   📁 {directory} oluşturuldu")
        else:
            print(f"   ✅ {directory} mevcut")

def start_dashboard():
    """Dashboard'u başlat"""
    print("\n🚀 Dashboard başlatılıyor...")
    print("   ⏳ Lütfen bekleyin...")
    
    try:
        # Dashboard'u arka planda başlat
        process = subprocess.Popen([
            sys.executable, 'dashboard_integration.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 3 saniye bekle
        time.sleep(3)
        
        # Process hala çalışıyor mu kontrol et
        if process.poll() is None:
            print("✅ Dashboard başarıyla başlatıldı!")
            print("📊 Adres: http://localhost:5000")
            
            # Browser'ı otomatik aç
            try:
                webbrowser.open('http://localhost:5000')
                print("🌐 Browser otomatik olarak açıldı!")
            except:
                print("🌐 Browser'ınızı manuel olarak açın: http://localhost:5000")
            
            print("\n" + "="*50)
            print("🎉 DASHBOARD HAZIR!")
            print("="*50)
            print("📊 Web arayüzü: http://localhost:5000")
            print("🔄 Otomatik güncelleme: Aktif")
            print("📈 Real-time veriler: Aktif")
            print("🛑 Durdurmak için: CTRL+C")
            print("="*50)
            
            # Process'i canlı tut
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Dashboard durduruluyor...")
                process.terminate()
                print("✅ Dashboard durduruldu!")
                
        else:
            # Hata mesajlarını al
            stdout, stderr = process.communicate()
            print("❌ Dashboard başlatılamadı!")
            if stderr:
                print(f"Hata: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Başlatma hatası: {e}")
        return False
    
    return True

def main():
    """Ana fonksiyon"""
    print("🚀 RENDER TRADING DASHBOARD - OTOMATIK KURULUM")
    print("="*55)
    
    # 1. Python versiyonu kontrol
    if not check_python_version():
        return
    
    # 2. Klasörleri oluştur
    create_directories()
    
    # 3. Dosyaları kontrol et
    if not check_files():
        print("\n❌ Eksik dosyalar var! Lütfen tüm dosyaları indirin.")
        return
    
    # 4. Paketleri yükle
    if not install_requirements():
        return
    
    # 5. Dashboard'u başlat
    start_dashboard()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 İşlem kullanıcı tarafından iptal edildi.")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        print("📞 Destek için hata mesajını paylaşın.")