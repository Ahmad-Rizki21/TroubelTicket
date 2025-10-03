# Sistem Trouble Ticket (Trouble Ticket System)

Sistem Trouble Ticket adalah aplikasi web modern yang dirancang untuk mengelola dan melacak tiket permasalahan (trouble tickets) dalam lingkungan organisasi. Sistem ini dibangun dengan pendekatan full-stack menggunakan FastAPI sebagai backend dan Vue.js sebagai frontend.

## Fitur Utama

### Backend (FastAPI)
- **API RESTful** - menyediakan endpoint untuk semua operasi sistem
- **Otentikasi & Otorisasi** - login/logout, pengelolaan sesi pengguna
- **Manajemen Pengguna** - CRUD pengguna, peran dan izin
- **Manajemen Tiket** - pembuatan, pengelolaan, dan pelacakan tiket dengan sequential ID generation
- **Manajemen Tindakan Tiket** - mencatat tindakan yang diambil terhadap tiket
- **Sistem Peran & Izin** - kontrol akses berdasarkan peran (RBAC)
- **Reset Password** - fitur pemulihan kata sandi
- **Upload File** - dukungan untuk mengunggah gambar terkait tiket
- **Advanced Business Logic** - validasi bisnis untuk deletion prevention dan workflow management
- **Remote Sites Integration** - integrasi dengan tabel Remotes untuk Site Name selection
- **Dashboard Analytics** - ringkasan statistik real-time tiket, status distribusi, dan performa sistem
- **Remote Management** - manajemen lokasi remote dan BTS (Base Transceiver Station) dengan integrasi peta
- **Laporan & Analitik** - fitur pelaporan komprehensif dengan visualisasi data dan metrik performa
- **Export Functionality** - export PDF dan Excel untuk tiket dan laporan

### Frontend (Vue.js)
- **Antarmuka Responsif** - tampilan yang menyesuaikan dengan berbagai perangkat
- **Dashboard** - ringkasan status tiket dan statistik real-time dengan berbagai grafik
- **Advanced Ticket Creation** - form pembuatan tiket dengan Site Name dropdown dan fixed High priority
- **Manajemen Tiket** - membuat, melihat, dan memperbarui tiket dengan business logic validation
- **Manajemen Pengguna** - pengaturan akun dan informasi pengguna dengan interface berbahasa Inggris
- **Manajemen Peran & Izin** - konfigurasi kontrol akses dengan interface berbahasa Inggris
- **Laporan** - analisis dan ringkasan tiket dengan filter berdasarkan kategori dan tanggal
- **Pengaturan Sistem** - konfigurasi aplikasi dengan interface berbahasa Inggris
- **Tampilan Peta untuk Lokasi Remote** - visualisasi lokasi BTS menggunakan peta interaktif
- **Grafik Analitik** - berbagai jenis grafik untuk analisis data tiket
- **Filter dan Sorting Laporan** - kemampuan untuk filter berdasarkan kategori, status, dan rentang tanggal
- **Visual Priority System** - badge priority dengan animasi untuk menunjukkan urgency
- **Enhanced Modal System** - modal untuk konfirmasi dan peringatan business logic

## Teknologi yang Digunakan

### Backend
- **Python 3.x**
- **FastAPI** - framework web modern untuk API
- **SQLAlchemy** - ORM untuk database
- **PyMySQL** - driver database MySQL
- **JWT** - token otentikasi
- **Passlib** - hashing password
- **Uvicorn** - ASGI server
- **Chart.js** - visualisasi data untuk laporan
- **Leaflet** - integrasi peta untuk manajemen remote

### Frontend
- **Vue.js 3** - framework JavaScript progresif
- **Typescript** - pengecekan tipe statis
- **Vue Router** - routing halaman
- **Pinia** - manajemen state
- **Axios** - komunikasi HTTP
- **Bootstrap** - framework CSS
- **Chart.js** - visualisasi data
- **Leaflet** - peta interaktif untuk lokasi remote

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

### Remote Management
- `GET /remotes/` - Dapatkan semua lokasi remote
- `POST /remotes/` - Buat remote baru
- `GET /remotes/{id}` - Dapatkan remote berdasarkan ID
- `PUT /remotes/{id}` - Perbarui remote
- `DELETE /remotes/{id}` - Hapus remote

### Laporan & Dashboard
- `GET /reports/` - Dapatkan laporan dan analitik
- `GET /dashboard/` - Dapatkan data ringkasan dashboard
- `GET /reports/{ticket_id}/export/pdf` - Export tiket ke PDF
- `GET /reports/{ticket_id}/export/excel` - Export tiket ke Excel
- `GET /reports/export/excel` - Export semua tiket ke Excel

## Database

Sistem menggunakan database MySQL dengan skema berikut:
- **tickets** - menyimpan informasi tiket
- **users** - menyimpan informasi pengguna
- **roles** - menyimpan peran pengguna
- **permissions** - menyimpan izin sistem
- **ticket_actions** - menyimpan tindakan yang diambil terhadap tiket
- **password_reset_tokens** - menyimpan token reset password
- **remotes** - menyimpan informasi lokasi remote dan BTS

## M: Kontribusi

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

## Changelog / Rilis Terbaru

### Version 2.2.0 (Latest) - Advanced Ticket Management & Business Logic Enhancement
- **✨ Major New Features:**
  - **Site Name Integration**: Dropdown Site Name yang terintegrasi dengan tabel Remotes untuk form pembuatan ticket
  - **Sequential Ticket ID**: Format ticket ID berurutan AG-00000001, AG-00000002, dst. sesuai standar perusahaan
  - **Fixed High Priority**: Semua ticket otomatis High priority dengan badge visual yang menarik
  - **Advanced Deletion Logic**: Business logic untuk mencegah penghapusan ticket dengan status "Open"
  - **Enhanced Category System**: Perbaikan sistem kategori ticket dengan field yang lengkap
  - **Remote Sites API**: API lengkap untuk manajemen lokasi remote sites dengan integrasi database

- **🎨 UI/UX Improvements:**
  - **Modern Create Ticket Form**: Redesign form pembuatan ticket dengan Site Name dropdown
  - **Priority Badge**: Visual badge dengan animasi api untuk High priority tickets
  - **Enhanced Modal System**: Modal peringatan untuk business logic validation
  - **Improved Loading States**: Loading indicators untuk API calls dan data fetching
  - **Responsive Site Dropdown**: Dropdown yang menampilkan site_name dan site_id_poi

- **🔧 Technical Enhancements:**
  - **Backend-Generated Ticket Codes**: Sistem generate ID otomatis di backend untuk konsistensi
  - **Business Logic Validation**: Validasi bisnis di backend dan frontend untuk deletion prevention
  - **API Schema Updates**: Update schemas untuk mendukung field kategori dan sequential generation
  - **Enhanced CRUD Operations**: Improvements pada database operations untuk ticket creation
  - **Database Migration**: Migration untuk menambahkan category column ke tickets table

- **🛡️ Security & Validation:**
  - **Status-Based Deletion Control**: Mencegah penghapusan ticket yang masih "Open"
  - **Form Validation**: Enhanced validation untuk required fields dan business rules
  - **User Guidance**: Clear error messages dan guidance untuk user workflows

- **🐛 Bug Fixes:**
  - Fixed category display issues (from "Uncategorized" to proper categories)
  - Resolved ticket code generation consistency
  - Fixed API responses untuk Remotes integration
  - Corrected form submission validation

### Version 2.1.0 - UI/UX Enhancement & Theme Standardization
- **✨ New Features:**
  - Separate Create Ticket page dengan layout 2-kolom yang responsive
  - Card-style header design untuk seluruh halaman dengan tema maroon konsisten
  - Live indicator dengan animasi pulse pada header
  - Gradient title effect menggunakan tema maroon (#800000 ke #5c0000)

- **🎨 UI/UX Improvements:**
  - Header standardization di semua halaman (Dashboard, Tickets, Users, Roles, Settings, Remotes)
  - Responsive design untuk tablet, mobile, dan desktop zoom compatibility
  - Form layout optimization untuk viewport single-page tanpa scroll
  - Enhanced button styling dengan gradien maroon dan hover effects
  - Improved focus states dengan maroon theme colors

- **🔧 Technical Updates:**
  - Fixed Vue runtime compilation warnings
  - Optimized Chart.js rendering dengan setTimeout delay
  - Enhanced form validation dan error handling
  - Improved performance dengan 60-second refresh interval
  - Fixed zoom compatibility issues dengan flexible height layouts

- **🐛 Bug Fixes:**
  - Fixed continuous refreshing issue pada Dashboard
  - Resolved TypeScript warnings untuk unused functions
  - Fixed modal display issues pada CreateTicket page
  - Corrected color inconsistencies pada action buttons

### Version 2.0.0 - Major Feature Release
- **Dashboard Analytics** - Real-time statistics dengan Chart.js
- **Remote Management** - BTS location management dengan Leaflet maps
- **Laporan & Analitik** - Comprehensive reporting dengan visualisasi data
- **Enhanced Security** - Improved authentication dan authorization

## CI/CD Pipeline & Security Configuration

### GitHub Actions Workflow
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  backend-tests:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: testpassword
          MYSQL_DATABASE: test_tickets
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install pytest pytest-cov bandit safety

    - name: Run security tests
      run: |
        cd backend
        bandit -r app/ -f json -o bandit-report.json
        safety check --json --output safety-report.json
        pytest --cov=app tests/

    - name: Upload security reports
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          backend/bandit-report.json
          backend/safety-report.json

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json

    - name: Install dependencies
      run: |
        cd frontend
        npm ci

    - name: Run security audit
      run: |
        cd frontend
        npm audit --audit-level=high

    - name: Run tests
      run: |
        cd frontend
        npm run test:unit

    - name: Build application
      run: |
        cd frontend
        npm run build

  code-quality:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Run ESLint
      uses: eslint-action@v1
      with:
        files: frontend/src/
        extensions: js,ts,vue

    - name: Run Prettier
      uses: creyD/prettier_action@v4.3
      with:
        prettier_options: --write frontend/src/**/*.{js,ts,vue}

  deploy-staging:
    needs: [security-scan, backend-tests, frontend-tests, code-quality]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'

    steps:
    - uses: actions/checkout@v4

    - name: Deploy to staging
      run: |
        echo "Deploy to staging environment"
        # Add your staging deployment commands here

  deploy-production:
    needs: [security-scan, backend-tests, frontend-tests, code-quality]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v4

    - name: Deploy to production
      run: |
        echo "Deploy to production environment"
        # Add your production deployment commands here
```

### Docker Configuration dengan Security Best Practices
```dockerfile
# Dockerfile (Backend)
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Install security updates
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Security
```bash
# .env.example - Update dengan best practices
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/tickets_db
SECRET_KEY=your-super-secret-key-here-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Security Headers
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
ALLOWED_HOSTS=["localhost", "127.0.0.1", "yourdomain.com"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=15

# File Upload Security
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=["jpg", "jpeg", "png", "pdf", "doc", "docx"]
UPLOAD_DIR="static/uploads"

# Logging
LOG_LEVEL=INFO
SECURITY_LOG_FILE="logs/security.log"
```

### Additional Security Measures

1. **HTTPS & SSL Configuration**
2. **JWT Token Management**
3. **Input Validation & Sanitization**
4. **SQL Injection Prevention**
5. **XSS Protection Headers**
6. **Rate Limiting Implementation**
7. **Security Headers Configuration**

## Penutup

Sistem Trouble Ticket ini menyediakan solusi komprehensif untuk mengelola tiket permasalahan dalam organisasi, dengan fitur manajemen pengguna, tiket, dan otorisasi yang lengkap. Sistem ini dirancang dengan pendekatan yang modern dan skalabel, memungkinkan integrasi mudah dengan sistem lainnya.

U: Fitur-fitur terbaru termasuk dashboard real-time, manajemen lokasi remote, dan laporan analitik komprehensif meningkatkan kemampuan sistem untuk memberikan wawasan dan kontrol yang lebih baik terhadap operasional trouble ticket.

**Security Focus:** Versi terbaru dilengkapi dengan CI/CD pipeline, security scanning, dan best practices untuk memastikan aplikasi aman dan terpercaya.