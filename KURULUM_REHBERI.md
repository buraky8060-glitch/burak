# 🚀 RENDER Trading Dashboard - Kurulum Rehberi

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- İnternet bağlantısı (API veriler için)
- Web tarayıcı (Chrome, Firefox, Safari, Edge)

## 🔧 Kurulum Adımları

### 1. Gerekli Paketleri Yükleyin

```bash
# Terminal/Command Prompt'ta şu komutu çalıştırın:
pip install -r requirements.txt
```

### 2. Dosya Yapısını Kontrol Edin

Klasör yapınız şöyle olmalı:
```
📁 proje_klasoru/
├── 📄 app.py                    # Basit dashboard
├── 📄 dashboard_integration.py  # Gelişmiş entegre dashboard
├── 📄 requirements.txt          # Gerekli paketler
├── 📁 templates/
│   └── 📄 dashboard.html        # Web arayüzü
└── 📁 static/
    ├── 📁 css/
    └── 📁 js/
```

## 🚀 Çalıştırma Seçenekleri

### Seçenek 1: Basit Dashboard (app.py)

```bash
python app.py
```

### Seçenek 2: Gelişmiş Dashboard (Önerilen)

```bash
python dashboard_integration.py
```

## 🌐 Erişim

Dashboard çalıştıktan sonra:

1. Web tarayıcınızı açın
2. Bu adrese gidin: **http://localhost:5000**
3. Dashboard otomatik olarak yüklenecek!

## 📊 Özellikler

✅ **Real-time Fiyat Takibi**
- Güncel RENDER/USDT fiyatı
- 24 saat değişim yüzdesi
- Yüksek/düşük değerler
- Hacim bilgileri

✅ **Teknik İndikatörler**
- RSI (14)
- MACD
- Stochastic
- Volume analizi
- Hareketli ortalamalar

✅ **İnteraktif Grafik**
- Real-time fiyat grafiği
- 50 periyot mum çubuğu
- Zoom/pan özelliği

✅ **AI Analiz Sistemi**
- Otomatik sinyal üretimi
- Güven yüzdesi
- AL/SAT/BEKLE önerileri

✅ **Real-time Güncellemeler**
- WebSocket bağlantısı
- 30 saniyede bir otomatik güncelleme
- Bağlantı durumu göstergesi

## 🔧 Sorun Giderme

### Hata: "ModuleNotFoundError"
```bash
# Eksik paketleri yükleyin:
pip install flask flask-socketio requests numpy
```

### Hata: "Port already in use"
```bash
# Farklı port kullanın (app.py son satırını değiştirin):
socketio.run(app, debug=True, host='0.0.0.0', port=5001)
# Sonra http://localhost:5001 adresine gidin
```

### Hata: "API connection failed"
- İnternet bağlantınızı kontrol edin
- Firewall ayarlarını kontrol edin
- VPN kullanıyorsanız kapatmayı deneyin

## 📱 Mobil Uyumluluk

Dashboard mobil cihazlarda da mükemmel çalışır:
- Responsive tasarım
- Touch-friendly butonlar
- Mobil optimizasyonu

## 🔄 Güncelleme

Dashboard otomatik olarak güncellenecek, ancak manuel yenilemek için:
- "Verileri Yenile" butonuna tıklayın
- Veya F5 tuşuna basın

## 📊 Veri Kaydetme

"Verileri İndir" butonu ile:
- JSON formatında veri indirme
- Analiz sonuçlarını kaydetme
- Backtest verileri

## ⚙️ Gelişmiş Ayarlar

### Güncelleme Sıklığını Değiştirmek

`dashboard_integration.py` dosyasında:
```python
time.sleep(30)  # 30 saniye -> istediğiniz süre
```

### Farklı Coin Analizi

API endpoint'lerini değiştirerek başka coinleri de analiz edebilirsiniz:
```python
params = {'fsym': 'BTC', 'tsyms': 'USDT,USD'}  # RENDER yerine BTC
```

## 🎯 Performans İpuçları

1. **Hızlı Yükleme**: Gereksiz sekmeler kapatın
2. **Smooth Grafik**: Hardware acceleration aktif olsun
3. **Stabil Bağlantı**: WiFi yerine kablo bağlantı kullanın

## 🔐 Güvenlik

- Dashboard sadece localhost'ta çalışır (güvenli)
- API anahtarı gerektirmez
- Kişisel veri saklanmaz

## 📞 Destek

Sorun yaşarsanız:
1. Terminal'deki hata mesajlarını kontrol edin
2. Browser console'unu açın (F12)
3. İnternet bağlantınızı test edin

## 🎉 Başarılı Kurulum Göstergeleri

✅ Terminal'de "Dashboard başlatılıyor..." mesajı
✅ Browser'da dashboard yüklendi
✅ Yeşil "Bağlı - Real-time" göstergesi
✅ Fiyat verileri görünüyor
✅ Grafik çiziyor

---

## 🚀 Hızlı Başlangıç (1 Dakika)

```bash
# 1. Paketleri yükle
pip install flask flask-socketio requests numpy

# 2. Dashboard'u başlat
python dashboard_integration.py

# 3. Browser'da aç
# http://localhost:5000
```

**Hazır! 🎉 Dashboard çalışıyor!**