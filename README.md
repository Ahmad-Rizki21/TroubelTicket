# Sistem Trouble Ticket (Trouble Ticket System)

Sistem Trouble Ticket adalah aplikasi web modern yang dirancang untuk mengelola dan melacak tiket permasalahan (trouble tickets) dalam lingkungan organisasi. Sistem ini dibangun dengan pendekatan full-stack menggunakan FastAPI sebagai backend dan Vue.js sebagai frontend.

## Fitur Utama

### Backend (FastAPI)
- **API RESTful** - menyediakan endpoint untuk semua operasi sistem
- **Otentikasi & Otorisasi** - login/logout, pengelolaan sesi pengguna
- **Manajemen Pengguna** - CRUD pengguna, peran dan izin
- **Manajemen Tiket** - pembuatan, pengelolaan, dan pelacakan tiket
- **Manajemen Tindakan Tiket** - mencatat tindakan yang diambil terhadap tiket
- **Sistem Peran & Izin** - kontrol akses berbasis peran (RBAC)
- **Reset Password** - fitur pemulihan kata sandi
- **Upload File** - dukungan untuk mengunggah gambar terkait tiket

### Frontend (Vue.js)
- **Antarmuka Responsif** - tampilan yang menyesuaikan dengan berbagai perangkat
- **Dashboard** - ringkasan status tiket dan statistik
- **Manajemen Tiket** - membuat, melihat, dan memperbarui tiket
- **Manajemen Pengguna** - pengaturan akun dan informasi pengguna
- **Manajemen Peran & Izin** - konfigurasi kontrol akses
- **Laporan** - analisis dan ringkasan tiket
- **Pengaturan Sistem** - konfigurasi aplikasi

## Teknologi yang Digunakan

### Backend
- **Python 3.x**
- **FastAPI** - framework web modern untuk API
- **SQLAlchemy** - ORM untuk database
- **PyMySQL** - driver database MySQL
- **JWT** - token otentikasi
- **Passlib** - hashing password
- **Uvicorn** - ASGI server

### Frontend
- **Vue.js 3** - framework JavaScript progresif
- **Typescript** - pengecekan tipe statis
- **Vue Router** - routing halaman
- **Pinia** - manajemen state
- **Axios** - komunikasi HTTP
- **Bootstrap** - framework CSS
- **Chart.js** - visualisasi data

## Prasyarat

Sebelum memulai, pastikan sistem Anda memiliki:
- Python 3.8+
- Node.js 16+
- MySQL 8.0+ (atau database kompatibel)

## Instalasi

### Backend (Server Side)

1. Clone repository ini:
```bash
git clone <url-repository>
cd sistem-tiket-backend
```

2. Buat dan aktifkan environment virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. Install dependensi:
```bash
pip install -r requirements.txt
```

4. Buat file konfigurasi `.env` berdasarkan `.env.example`:
```bash
cp .env.example .env
# Edit file .env sesuai konfigurasi Anda
```

5. Jalankan migrasi database:
```bash
alembic upgrade head
```

6. Jalankan aplikasi:
```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend (Client Side)

1. Pindah ke direktori frontend:
```bash
cd frontend
```

2. Install dependensi:
```bash
npm install
```

3. Buat file `.env` berdasarkan `.env.example`:
```bash
cp .env.example .env
# Edit file .env sesuai konfigurasi API Anda
```

4. Jalankan aplikasi:
```bash
npm run dev
```

## Konfigurasi

### File .env Backend
- `DATABASE_URL` - URL koneksi database (misalnya: mysql+pymysql://user:password@localhost/dbname)
- `SECRET_KEY` - kunci enkripsi JWT
- `ALGORITHM` - algoritma enkripsi token
- `ACCESS_TOKEN_EXPIRE_MINUTES` - durasi token akses dalam menit

### File .env Frontend
- `VITE_API_URL` - URL API backend (misalnya: http://localhost:8000)

## Struktur Proyek

```
sistem-tiket-backend/
├── app/
│   ├── core/           # Konfigurasi dan utilitas inti
│   ├── models/         # Model database
│   ├── routers/        # Endpoint API
│   ├── schemas/        # Schema Pydantic
│   ├── crud.py         # Operasi database
│   ├── database.py     # Konfigurasi dan koneksi database
│   ├── main.py         # Aplikasi utama FastAPI
│   └── security.py     # Fungsi otentikasi dan keamanan
├── alembic/            # Migrasi database
├── frontend/           # Kode sumber frontend
├── static/             # File statis (upload, dll)
├── requirements.txt    # Dependensi Python
└── README.md
```

## API Endpoint

### Otentikasi
- `POST /auth/login` - Login pengguna
- `POST /auth/logout` - Logout pengguna
- `POST /auth/change-password` - Ganti kata sandi
- `POST /auth/reset-password-request` - Permintaan reset kata sandi
- `POST /auth/reset-password` - Reset kata sandi

### Tiket
- `GET /tickets/` - Dapatkan semua tiket
- `POST /tickets/` - Buat tiket baru
- `GET /tickets/{id}` - Dapatkan tiket berdasarkan ID
- `PUT /tickets/{id}` - Perbarui tiket
- `DELETE /tickets/{id}` - Hapus tiket

### Pengguna
- `GET /users/` - Dapatkan semua pengguna
- `POST /users/` - Buat pengguna baru
- `GET /users/{id}` - Dapatkan pengguna berdasarkan ID
- `PUT /users/{id}` - Perbarui pengguna
- `DELETE /users/{id}` - Hapus pengguna

### Peran & Izin
- `GET /roles/` - Dapatkan semua peran
- `POST /roles/` - Buat peran baru
- `PUT /roles/{id}` - Perbarui peran
- `DELETE /roles/{id}` - Hapus peran
- `GET /permissions/` - Dapatkan semua izin
- `PUT /permissions/` - Perbarui izin

## Database

Sistem menggunakan database MySQL dengan skema berikut:
- **tickets** - menyimpan informasi tiket
- **users** - menyimpan informasi pengguna
- **roles** - menyimpan peran pengguna
- **permissions** - menyimpan izin sistem
- **ticket_actions** - menyimpan tindakan yang diambil terhadap tiket
- **password_reset_tokens** - menyimpan token reset password

## Kontribusi

Kami menyambut kontribusi dari komunitas. Silakan ikuti langkah-langkah berikut:
1. Fork repository
2. Buat branch fitur baru (`git checkout -b fitur/AwesomeFeature`)
3. Commit perubahan Anda (`git commit -m 'Add some AwesomeFeature'`)
4. Push ke branch (`git push origin fitur/AwesomeFeature`)
5. Buka Pull Request

## Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail selengkapnya.

## Dukungan

Jika Anda mengalami masalah dengan aplikasi, silakan buka isu di halaman GitHub repository.

## Penutup

Sistem Trouble Ticket ini menyediakan solusi komprehensif untuk mengelola tiket permasalahan dalam organisasi, dengan fitur manajemen pengguna, tiket, dan otorisasi yang lengkap. Sistem ini dirancang dengan pendekatan yang modern dan skalabel, memungkinkan integrasi mudah dengan sistem lainnya.