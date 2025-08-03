from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import threading
import time
from datetime import datetime, timedelta
import requests
import numpy as np
from collections import deque

# Mevcut analiz sınıfınızı import edin
# from your_existing_file import RenderUltimatePrediction, VolumeIndicators, BacktestResults

app = Flask(__name__)
app.config['SECRET_KEY'] = 'render_trading_dashboard_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

class WebDashboardAPI:
    def __init__(self):
        self.base_url = "https://min-api.cryptocompare.com/data"
        self.current_data = {}
        self.is_running = False
        
    def get_current_price(self):
        """Güncel fiyat al"""
        try:
            url = f"{self.base_url}/price"
            params = {'fsym': 'RENDER', 'tsyms': 'USDT,USD'}
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('USDT', data.get('USD'))
        except Exception as e:
            print(f"Hata (get_current_price): {e}")
        return None
    
    def get_detailed_stats(self):
        """Detaylı istatistikler"""
        try:
            url = f"{self.base_url}/pricemultifull"
            params = {'fsyms': 'RENDER', 'tsyms': 'USDT'}
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'RAW' in data and 'RENDER' in data['RAW']:
                    return data['RAW']['RENDER']['USDT']
        except Exception as e:
            print(f"Hata (get_detailed_stats): {e}")
        return None
    
    def get_historical_data(self, interval='minute', limit=100):
        """Geçmiş veriler"""
        try:
            endpoint = f"v2/histo{interval}"
            url = f"{self.base_url}/{endpoint}"
            params = {
                'fsym': 'RENDER',
                'tsym': 'USDT',
                'limit': limit
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['Response'] == 'Success':
                    return data['Data']['Data']
        except Exception as e:
            print(f"Hata (get_historical_data): {e}")
        return None
    
    def calculate_rsi(self, prices, period=14):
        """RSI hesaplama"""
        if len(prices) < period + 1:
            return 50
        
        changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [change if change > 0 else 0 for change in changes]
        losses = [-change if change < 0 else 0 for change in changes]
        
        if len(gains) >= period:
            avg_gain = sum(gains[:period]) / period
            avg_loss = sum(losses[:period]) / period
            
            for i in range(period, len(gains)):
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            
            if avg_loss == 0:
                return 100
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        return 50
    
    def get_dashboard_data(self):
        """Dashboard için tüm verileri topla"""
        current_price = self.get_current_price()
        stats = self.get_detailed_stats()
        minute_data = self.get_historical_data('minute', 100)
        
        if not current_price or not stats or not minute_data:
            return None
        
        # Fiyat verileri
        closes = [d['close'] for d in minute_data]
        highs = [d['high'] for d in minute_data]
        lows = [d['low'] for d in minute_data]
        volumes = [d['volumeto'] for d in minute_data]
        timestamps = [d['time'] * 1000 for d in minute_data]  # JavaScript için milisaniye
        
        # Teknik indikatörler
        rsi = self.calculate_rsi(closes)
        
        # Chart verileri
        chart_data = []
        for i, data in enumerate(minute_data):
            chart_data.append({
                'time': data['time'] * 1000,
                'open': data['open'],
                'high': data['high'],
                'low': data['low'],
                'close': data['close'],
                'volume': data['volumeto']
            })
        
        dashboard_data = {
            'current_price': current_price,
            'price_change_24h': stats.get('CHANGEPCT24HOUR', 0),
            'volume_24h': stats.get('VOLUME24HOURTO', 0),
            'high_24h': stats.get('HIGH24HOUR', 0),
            'low_24h': stats.get('LOW24HOUR', 0),
            'market_cap': stats.get('MKTCAP', 0),
            'rsi': rsi,
            'chart_data': chart_data[-50:],  # Son 50 mum
            'last_update': datetime.now().isoformat()
        }
        
        return dashboard_data

# Global API instance
dashboard_api = WebDashboardAPI()

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    """API endpoint - dashboard verileri"""
    data = dashboard_api.get_dashboard_data()
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Veri alınamadı'}), 500

@app.route('/api/analysis')
def get_analysis():
    """Detaylı analiz endpoint"""
    # Burada mevcut RenderUltimatePrediction sınıfınızı kullanabilirsiniz
    return jsonify({
        'status': 'analysis_ready',
        'message': 'Detaylı analiz hazır',
        'recommendation': 'AL',
        'confidence': 75.5,
        'indicators': {
            'rsi': 45.2,
            'macd': 'BUY',
            'stochastic': 'NEUTRAL'
        }
    })

@socketio.on('connect')
def handle_connect():
    """WebSocket bağlantısı"""
    print('Client connected')
    emit('status', {'msg': 'WebSocket bağlantısı kuruldu'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('request_data')
def handle_data_request():
    """Real-time veri isteği"""
    data = dashboard_api.get_dashboard_data()
    if data:
        emit('data_update', data)

def background_thread():
    """Arka plan thread - real-time veri güncelleme"""
    while True:
        time.sleep(10)  # 10 saniyede bir güncelle
        data = dashboard_api.get_dashboard_data()
        if data:
            socketio.emit('data_update', data)

if __name__ == '__main__':
    # Arka plan thread'i başlat
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()
    
    print("🚀 RENDER Trading Dashboard başlatılıyor...")
    print("📊 http://localhost:5000 adresinde erişilebilir")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)