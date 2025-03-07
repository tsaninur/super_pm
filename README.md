```md
# Super PM - Password Manager

Super PM adalah password manager yang dirancang untuk menyimpan, mengelola, dan melindungi password dengan aman.

## 📌 Fitur Utama
- 🔑 **add** : Menambahkan entri password baru  
- 🔍 **extract** : Mengambil password berdasarkan filter  
- 🔢 **generate** : Menghasilkan password acak  
- 🔎 **check** : Mengecek kebocoran password  
- 🚪 **exit** : Keluar dari program  

## 🚀 Instalasi dan Persiapan

### 1️⃣ Instal Python  
Pastikan Python sudah terinstal di sistem. Jika belum, unduh dan instal dari [Python.org](https://www.python.org/downloads/).  

### 2️⃣ Instal MariaDB dan Buat User
```bash
sudo apt update
sudo apt install mariadb-server -y
```
Masuk ke MariaDB dan buat user:
```sql
CREATE DATABASE pm;
CREATE USER 'pm'@'localhost' IDENTIFIED BY 'password_kuat';
GRANT ALL PRIVILEGES ON pm.* TO 'pm'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3️⃣ Instal Dependensi Python
Buat virtual environment dan instal dependensi:
```bash
python3 -m venv venv
source venv/bin/activate  # Untuk Linux/macOS
venv\Scripts\activate  # Untuk Windows
pip install -r requirements.txt
```

## 🔧 Konfigurasi Super PM

### ➖ Menghapus Konfigurasi Lama
```bash
python3 config.py delete
```
Konfirmasi dengan `y` untuk menghapus semua data.  

### ➕ Membuat Konfigurasi Baru
```bash
python3 config.py make
```
Ikuti instruksi untuk memasukkan **MASTER PASSWORD**.

## ▶️ Menjalankan Super PM
```bash
python3 super_pm.py
```
Tampilan awal akan muncul dengan opsi fitur utama.

## ❌ Keluar dari Program
Gunakan perintah berikut untuk keluar:  
```bash
Super PM > exit
```

## 📜 Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).  

---
💡 Dibuat oleh **Sani, Zho & Riel**  
```
