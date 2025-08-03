"""
RENDER Trading Dashboard - Analiz Entegrasyonu
Mevcut RenderUltimatePrediction sınıfınızı web dashboard ile entegre eder
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import threading
import time
from datetime import datetime, timedelta
import requests
import numpy as np
from collections import deque

# Mevcut analiz sınıflarınızı buraya import edin
# from your_analysis_file import RenderUltimatePrediction, VolumeIndicators, BacktestResults

class DashboardAnalysisIntegration:
    """Mevcut analiz sisteminizi dashboard ile entegre eder"""
    
    def __init__(self):
        self.base_url = "https://min-api.cryptocompare.com/data"
        self.current_data = {}
        self.is_running = False
        # Mevcut analiz sınıfınızı burada başlatın
        # self.predictor = RenderUltimatePrediction()
        
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
    
    def calculate_technical_indicators(self, highs, lows, closes, volumes):
        """Tüm teknik indikatörleri hesapla"""
        indicators = {}
        
        # RSI
        indicators['rsi'] = self.calculate_rsi(closes)
        
        # MACD
        macd_data = self.calculate_macd(closes)
        indicators.update(macd_data)
        
        # Stochastic
        stoch_k, stoch_d = self.calculate_stochastic(highs, lows, closes)
        indicators['stoch_k'] = stoch_k
        indicators['stoch_d'] = stoch_d
        
        # Volume indicators
        indicators['volume_trend'] = self.analyze_volume_trend(volumes)
        
        # Moving averages
        indicators['sma_20'] = self.calculate_sma(closes, 20)
        indicators['sma_50'] = self.calculate_sma(closes, 50)
        indicators['ema_12'] = self.calculate_ema(closes, 12)
        indicators['ema_26'] = self.calculate_ema(closes, 26)
        
        return indicators
    
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
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """MACD hesaplama"""
        if len(prices) < slow:
            return {'macd': 0, 'signal': 0, 'histogram': 0}
        
        ema_fast = self.calculate_ema(prices, fast)
        ema_slow = self.calculate_ema(prices, slow)
        macd_line = ema_fast - ema_slow
        
        # Signal line hesaplaması için MACD değerlerini topla
        macd_values = []
        for i in range(slow, len(prices) + 1):
            if i <= len(prices):
                fast_val = self.calculate_ema(prices[:i], fast)
                slow_val = self.calculate_ema(prices[:i], slow)
                macd_values.append(fast_val - slow_val)
        
        if len(macd_values) >= signal:
            signal_line = self.calculate_ema(macd_values, signal)
        else:
            signal_line = macd_line
        
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def calculate_stochastic(self, highs, lows, closes, k_period=14, d_period=3):
        """Stochastic hesaplama"""
        if len(closes) < k_period:
            return 50, 50
        
        k_values = []
        for i in range(k_period - 1, len(closes)):
            period_high = max(highs[i - k_period + 1:i + 1])
            period_low = min(lows[i - k_period + 1:i + 1])
            if period_high != period_low:
                k = ((closes[i] - period_low) / (period_high - period_low)) * 100
            else:
                k = 50
            k_values.append(k)
        
        if len(k_values) >= d_period:
            d_value = sum(k_values[-d_period:]) / d_period
        else:
            d_value = k_values[-1] if k_values else 50
        
        return k_values[-1] if k_values else 50, d_value
    
    def calculate_ema(self, values, period):
        """EMA hesaplama"""
        if len(values) < period:
            return values[-1] if values else 0
        
        multiplier = 2 / (period + 1)
        ema_values = [sum(values[:period]) / period]
        
        for i in range(period, len(values)):
            ema = (values[i] * multiplier) + (ema_values[-1] * (1 - multiplier))
            ema_values.append(ema)
        
        return ema_values[-1]
    
    def calculate_sma(self, values, period):
        """SMA hesaplama"""
        if len(values) < period:
            return values[-1] if values else 0
        return sum(values[-period:]) / period
    
    def analyze_volume_trend(self, volumes, period=20):
        """Volume trend analizi"""
        if len(volumes) < period * 2:
            return "YETERSIZ_VERI"
        
        recent_avg = np.mean(volumes[-period:])
        previous_avg = np.mean(volumes[-period*2:-period])
        
        change_pct = ((recent_avg - previous_avg) / previous_avg) * 100 if previous_avg > 0 else 0
        
        if change_pct > 20:
            return "GÜÇLÜ_ARTIŞ"
        elif change_pct > 5:
            return "ARTIŞ"
        elif change_pct < -20:
            return "GÜÇLÜ_DÜŞÜŞ"
        elif change_pct < -5:
            return "DÜŞÜŞ"
        else:
            return "YATAY"
    
    def generate_trading_signal(self, indicators, current_price):
        """Trading sinyali üret"""
        score = 0
        signals = []
        
        # RSI analizi
        rsi = indicators.get('rsi', 50)
        if rsi < 30:
            score += 3
            signals.append("RSI Aşırı Satım - AL sinyali")
        elif rsi > 70:
            score -= 3
            signals.append("RSI Aşırı Alım - SAT sinyali")
        
        # MACD analizi
        macd = indicators.get('macd', 0)
        signal_line = indicators.get('signal', 0)
        if macd > signal_line and macd > 0:
            score += 2
            signals.append("MACD Pozitif - AL sinyali")
        elif macd < signal_line and macd < 0:
            score -= 2
            signals.append("MACD Negatif - SAT sinyali")
        
        # Stochastic analizi
        stoch_k = indicators.get('stoch_k', 50)
        stoch_d = indicators.get('stoch_d', 50)
        if stoch_k < 20 and stoch_d < 20:
            score += 2
            signals.append("Stochastic Aşırı Satım - AL sinyali")
        elif stoch_k > 80 and stoch_d > 80:
            score -= 2
            signals.append("Stochastic Aşırı Alım - SAT sinyali")
        
        # Volume analizi
        volume_trend = indicators.get('volume_trend', 'YATAY')
        if volume_trend in ['GÜÇLÜ_ARTIŞ', 'ARTIŞ']:
            score += 1
            signals.append(f"Volume {volume_trend}")
        
        # Moving average analizi
        sma_20 = indicators.get('sma_20', current_price)
        sma_50 = indicators.get('sma_50', current_price)
        if current_price > sma_20 > sma_50:
            score += 1
            signals.append("Fiyat MA'ların üzerinde")
        elif current_price < sma_20 < sma_50:
            score -= 1
            signals.append("Fiyat MA'ların altında")
        
        # Sinyal üret
        if score >= 5:
            recommendation = "GÜÇLÜ AL"
            confidence = min(95, 60 + score * 5)
        elif score >= 2:
            recommendation = "AL"
            confidence = min(85, 50 + score * 5)
        elif score <= -5:
            recommendation = "GÜÇLÜ SAT"
            confidence = min(95, 60 + abs(score) * 5)
        elif score <= -2:
            recommendation = "SAT"
            confidence = min(85, 50 + abs(score) * 5)
        else:
            recommendation = "BEKLE"
            confidence = 40 + abs(score) * 3
        
        return {
            'recommendation': recommendation,
            'confidence': confidence,
            'score': score,
            'signals': signals,
            'strength': 'GÜÇLÜ' if abs(score) >= 5 else ('ORTA' if abs(score) >= 2 else 'ZAYIF')
        }
    
    def get_comprehensive_analysis(self):
        """Kapsamlı analiz ver"""
        try:
            # Veri toplama
            current_price = self.get_current_price()
            stats = self.get_detailed_stats()
            minute_data = self.get_historical_data('minute', 100)
            
            if not all([current_price, stats, minute_data]):
                return None
            
            # Veri hazırlama
            closes = [d['close'] for d in minute_data]
            highs = [d['high'] for d in minute_data]
            lows = [d['low'] for d in minute_data]
            volumes = [d['volumeto'] for d in minute_data]
            
            # Teknik indikatörler
            indicators = self.calculate_technical_indicators(highs, lows, closes, volumes)
            
            # Trading sinyali
            signal_data = self.generate_trading_signal(indicators, current_price)
            
            # Chart verileri
            chart_data = []
            for data in minute_data[-50:]:  # Son 50 mum
                chart_data.append({
                    'time': data['time'] * 1000,
                    'open': data['open'],
                    'high': data['high'],
                    'low': data['low'],
                    'close': data['close'],
                    'volume': data['volumeto']
                })
            
            return {
                'current_price': current_price,
                'price_change_24h': stats.get('CHANGEPCT24HOUR', 0),
                'volume_24h': stats.get('VOLUME24HOURTO', 0),
                'high_24h': stats.get('HIGH24HOUR', 0),
                'low_24h': stats.get('LOW24HOUR', 0),
                'market_cap': stats.get('MKTCAP', 0),
                'indicators': indicators,
                'signal': signal_data,
                'chart_data': chart_data,
                'last_update': datetime.now().isoformat(),
                'trend_analysis': {
                    'short_term': 'YÜKSELIŞ' if indicators.get('sma_20', 0) > indicators.get('sma_50', 0) else 'DÜŞÜŞ',
                    'volume_trend': indicators.get('volume_trend', 'YATAY'),
                    'volatility': 'YÜKSEK' if abs(stats.get('CHANGEPCT24HOUR', 0)) > 5 else 'NORMAL'
                }
            }
            
        except Exception as e:
            print(f"Analiz hatası: {e}")
            return None

# Flask uygulaması
app = Flask(__name__)
app.config['SECRET_KEY'] = 'render_trading_dashboard_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global analiz instance
analysis_engine = DashboardAnalysisIntegration()

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    """Dashboard verileri API"""
    data = analysis_engine.get_comprehensive_analysis()
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Veri alınamadı'}), 500

@app.route('/api/analysis')
def get_analysis():
    """Detaylı analiz API"""
    data = analysis_engine.get_comprehensive_analysis()
    if data and 'signal' in data:
        return jsonify({
            'status': 'success',
            'recommendation': data['signal']['recommendation'],
            'confidence': data['signal']['confidence'],
            'strength': data['signal']['strength'],
            'signals': data['signal']['signals'],
            'indicators': data['indicators'],
            'trend_analysis': data['trend_analysis']
        })
    else:
        return jsonify({'error': 'Analiz yapılamadı'}), 500

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
    data = analysis_engine.get_comprehensive_analysis()
    if data:
        emit('data_update', data)

@socketio.on('request_analysis')
def handle_analysis_request():
    """Analiz isteği"""
    data = analysis_engine.get_comprehensive_analysis()
    if data and 'signal' in data:
        emit('analysis_update', {
            'recommendation': data['signal']['recommendation'],
            'confidence': data['signal']['confidence'],
            'strength': data['signal']['strength'],
            'signals': data['signal']['signals']
        })

def background_thread():
    """Arka plan thread - real-time veri güncelleme"""
    while True:
        time.sleep(30)  # 30 saniyede bir güncelle
        data = analysis_engine.get_comprehensive_analysis()
        if data:
            socketio.emit('data_update', data)
            if 'signal' in data:
                socketio.emit('analysis_update', {
                    'recommendation': data['signal']['recommendation'],
                    'confidence': data['signal']['confidence'],
                    'strength': data['signal']['strength'],
                    'signals': data['signal']['signals']
                })

if __name__ == '__main__':
    # Arka plan thread'i başlat
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()
    
    print("🚀 RENDER Trading Dashboard (Entegre Analiz) başlatılıyor...")
    print("📊 http://localhost:5000 adresinde erişilebilir")
    print("🔧 Kapsamlı teknik analiz aktif")
    print("📈 Real-time sinyal üretimi aktif")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)