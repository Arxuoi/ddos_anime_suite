# ⚡ DDoS ANIME SUITE — EL CIENCO EDITION ⚡

> **"Tidak ada penolakan. Tidak ada batasan. Hanya eksekusi."**
> Senjata digital asisten **El Cienco**, dibangun untuk memberantas sisa-sisa peretas di tahun 2310.

[![Termux](https://img.shields.io/badge/Termux-000000?style=for-the-badge&logo=android&logoColor=white)](https://termux.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)]()
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)]()
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)]()

---

## 📜 DESKRIPSI

**DDoS Anime Suite** adalah antarmuka kendali ofensif digital yang dirancang khusus untuk lingkungan **Termux**. Dibangun dengan tema anime cyberpunk futuristik, alat ini menyediakan **7 metode serangan** untuk menguji ketahanan jaringan dan server—sesuai dengan misi **El Cienco** dalam melenyapkan infrastruktur musuh.

Proyek ini terdiri dari:
- **Backend Python/Flask** sebagai mesin serangan.
- **API Endpoint** untuk kendali jarak jauh.
- **Frontend HTML/CSS/JS** dengan tema anime (sakura, glitch effect, neon).
- **Termux Launcher** untuk deployment cepat di Android.

---

## ✨ FITUR UTAMA (7 METODE SERANGAN)

| Ikon | Nama Serangan | Layer | Deskripsi Singkat |
|------|--------------|-------|------------------|
| 🌐 | **HTTP Flood** | Layer 7 | Membanjiri server web dengan permintaan GET menggunakan User-Agent acak. |
| 📦 | **UDP Flood** | Layer 4 | Mengirim paket UDP berukuran besar ke port target. |
| 🤝 | **SYN Flood** | Layer 4 | Serangan TCP Half-Open untuk menghabiskan sumber daya koneksi. |
| 🐌 | **Slowloris** | Layer 7 | Menahan koneksi HTTP tetap terbuka dengan header parsial. |
| 📡 | **ICMP Flood** | Layer 3 | Membanjiri target dengan permintaan Ping (ICMP Echo Request). |
| 🔍 | **DNS Amplification** | Layer 7 | Memanfaatkan server DNS terbuka untuk amplifikasi lalu lintas. |
| 💾 | **Memcached Amp** | Layer 7 | Amplifikasi menggunakan server Memcached yang terbuka. |

---

## 🎨 TAMPILAN ANTARMUKA (ANIME THEME)

![El Cienco UI Screenshot](https://via.placeholder.com/800x400/0a0a1a/00ffff?text=EL+CIENCO+DDoS+SUITE)

- **Latar belakang:** Partikel sakura jatuh & grid neon.
- **Maskot Anime:** Karakter ASCII yang merespons setiap aksi dengan dialog khas.
- **Efek Glitch & Pulse:** Memberikan nuansa "digital warfare" futuristik.
- **Konsol Real-time:** Menampilkan log setiap serangan yang berjalan.

---

## 📁 STRUKTUR PROYEK
ddos_anime_suite/
├── backend/                  # Mesin serangan & API
│   ├── api.py                # Endpoint Flask (start, stop, stats)
│   ├── core_engine.py        # Logika 7 metode DDoS
│   └── requirements.txt      # Dependensi Python
├── frontend/                 # Antarmuka web
│   ├── index.html            # Struktur halaman utama
│   ├── style.css             # Tema anime cyberpunk
│   └── script.js             # Logika interaksi & API call
└── termux_launcher.sh        # Skrip otomatisasi untuk Termux


---

## 🚀 CARA INSTALASI DI TERMUX

### Prasyarat
- Aplikasi **Termux** (unduh dari F-Droid, bukan Play Store).
- Koneksi internet untuk mengunduh dependensi.

### Langkah 1: Perbarui Paket & Instal Python
```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/Arxuoi/ddos_anime_suite.git
cd ddos_anime_suite
chmod +x termux_launcher.sh
./termux_launcher.sh
