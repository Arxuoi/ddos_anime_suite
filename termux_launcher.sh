#!/data/data/com.termux/files/usr/bin/bash

echo "======================================"
echo "    EL CIENCO - 7 SINS DDoS SUITE    "
echo "         Termux Edition v1.0         "
echo "======================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 tidak ditemukan. Install dengan:"
    echo "    pkg install python"
    exit 1
fi

# Install dependencies
echo "[*] Menginstall dependencies..."
pip install flask flask-cors requests scapy --quiet

# Check if backend exists
if [ ! -f "backend/api.py" ]; then
    echo "[!] File backend tidak ditemukan!"
    echo "[*] Pastikan struktur folder sesuai:"
    echo "    ddos_anime_suite/"
    echo "    ├── backend/"
    echo "    ├── frontend/"
    echo "    └── termux_launcher.sh"
    exit 1
fi

# Get local IP
LOCAL_IP=$(ifconfig wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}')
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP="127.0.0.1"
fi

echo ""
echo "[✓] Dependencies terinstall"
echo "[✓] Backend siap dijalankan"
echo ""
echo "======================================"
echo "  AKSES WEB INTERFACE"
echo "======================================"
echo "  Local:  http://127.0.0.1:5000"
echo "  Network: http://$LOCAL_IP:5000"
echo "======================================"
echo ""
echo "[*] Menjalankan El Cienco Server..."
echo "[*] Tekan CTRL+C untuk berhenti"
echo ""

# Run backend
cd backend
python3 api.py
