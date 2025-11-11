# 🚂 Railway Deployment - Panduan Lengkap

## ✅ Masalah yang Sudah Diperbaiki

1. ✅ **"ModuleNotFoundError: No module named 'main'"** - Fixed
2. ✅ **"ImportError: cannot import name 'create_app'"** - Fixed dengan rename `app.py` → `application.py`
3. ✅ Konfigurasi gunicorn optimal untuk production
4. ✅ File deployment lengkap (railway.json, Procfile, gunicorn_config.py)

---

## 📋 Environment Variables untuk Railway

Copy paste nilai-nilai ini ke **Railway Dashboard → Variables**:

### ✅ Variables yang BENAR:

```bash
# Flask Configuration
FLASK_DEBUG=false
FLASK_HOST=0.0.0.0

# CORS (ganti dengan domain Railway Anda setelah deploy)
ALLOWED_ORIGINS=https://your-app-name.up.railway.app

# Firebase Configuration
FIREBASE_PROJECT_ID=chatbot-cbf07
FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n[ISI DENGAN PRIVATE KEY LENGKAP DARI FIREBASE]\n-----END PRIVATE KEY-----
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@chatbot-cbf07.iam.gserviceaccount.com

# API Keys (WAJIB!)
GEMINI_API_KEY=[ISI DENGAN API KEY GEMINI ANDA]
SESSION_SECRET=[GENERATE RANDOM STRING MINIMAL 32 KARAKTER]
```

---

## 🔑 Cara Mendapatkan Credentials

### 1. GEMINI_API_KEY
1. Buka: https://aistudio.google.com/apikey
2. Login dengan Google account
3. Klik "Create API Key"
4. Copy key tersebut

### 2. SESSION_SECRET
Generate random string dengan command ini:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Firebase Credentials
1. Buka: https://console.firebase.google.com
2. Pilih project: **chatbot-cbf07**
3. Klik Settings (⚙️) → Project Settings
4. Tab "Service accounts"
5. Klik "Generate new private key"
6. Download file JSON
7. Ambil nilai:
   - `project_id` → FIREBASE_PROJECT_ID
   - `private_key` → FIREBASE_PRIVATE_KEY (pastikan ada `\n` untuk newlines)
   - `client_email` → FIREBASE_CLIENT_EMAIL

---

## 🚀 Langkah Deploy ke Railway

### Step 1: Push Code ke GitHub
```bash
git add .
git commit -m "Fix Railway deployment configuration"
git push origin main
```

### Step 2: Deploy di Railway
1. Login ke https://railway.app
2. Klik "New Project"
3. Pilih "Deploy from GitHub repo"
4. Pilih repository Anda
5. Railway akan auto-detect configuration dari `railway.json`

### Step 3: Tambahkan Environment Variables
1. Di Railway dashboard, klik project Anda
2. Klik tab "Variables"
3. Tambahkan semua environment variables di atas
4. **Penting:** Untuk `FIREBASE_PRIVATE_KEY`, pastikan ada `\n` untuk newlines!

### Step 4: Verifikasi Deployment
1. Tunggu build selesai (lihat di tab "Deployments")
2. Cek logs untuk error
3. Railway akan memberikan URL: `https://your-app-name.up.railway.app`
4. Update variable `ALLOWED_ORIGINS` dengan URL tersebut
5. Redeploy (Railway auto-deploy saat variable berubah)

---

## 🔍 Troubleshooting

### Error: "Worker failed to boot"
✅ **Sudah diperbaiki!** Pastikan Anda sudah push code terbaru dengan `application.py`

### Error: "GEMINI_API_KEY not found"
❌ Tambahkan variable `GEMINI_API_KEY` di Railway dashboard

### Error: "SESSION_SECRET is required"
❌ Tambahkan variable `SESSION_SECRET` di Railway dashboard

### Error: Firebase initialization failed
⚠️ **Opsional** - App bisa jalan tanpa Firebase (pakai mock database)
- Jika mau pakai Firebase, pastikan semua 3 credentials Firebase sudah benar
- `FIREBASE_PRIVATE_KEY` harus include `-----BEGIN PRIVATE KEY-----` dan `-----END PRIVATE KEY-----`
- Newlines di private key harus di-encode sebagai `\n`

### Port Already in Use
Railway otomatis handle `$PORT` variable, tidak perlu setting manual

---

## ⚙️ Konfigurasi Production (Sudah Optimal)

Railway menggunakan konfigurasi dari `railway.json`:

```json
{
  "deploy": {
    "startCommand": "gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 4 --threads 2 --timeout 120"
  }
}
```

**Specs:**
- Workers: 4 (optimal untuk most use cases)
- Threads: 2 per worker
- Timeout: 120 seconds (untuk request yang lama)
- Port: Auto dari Railway ($PORT variable)

---

## 📊 Monitoring

### Check Logs
```
Railway Dashboard → Deployments → View Logs
```

### Check Status
```
Railway Dashboard → Service → Status
```

### Health Check (Optional - bisa ditambahkan nanti)
Tambahkan endpoint health check di `application.py`:
```python
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

---

## 🎯 Checklist Deployment

- [ ] Push code terbaru ke GitHub
- [ ] Set `GEMINI_API_KEY` di Railway
- [ ] Set `SESSION_SECRET` di Railway
- [ ] Set `FIREBASE_PROJECT_ID` di Railway
- [ ] Set `FIREBASE_PRIVATE_KEY` di Railway
- [ ] Set `FIREBASE_CLIENT_EMAIL` di Railway
- [ ] Set `FLASK_DEBUG=false` di Railway
- [ ] Set `FLASK_HOST=0.0.0.0` di Railway
- [ ] Deploy di Railway
- [ ] Dapatkan Railway URL
- [ ] Update `ALLOWED_ORIGINS` dengan Railway URL
- [ ] Test aplikasi di Railway URL

---

## ✨ Quick Copy-Paste Format

Untuk Railway Variables (format key=value):

```
FLASK_DEBUG=false
FLASK_HOST=0.0.0.0
ALLOWED_ORIGINS=https://your-railway-url.up.railway.app
FIREBASE_PROJECT_ID=chatbot-cbf07
FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nYOUR_ACTUAL_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----
FIREBASE_CLIENT_EMAIL=your-firebase-email@chatbot-cbf07.iam.gserviceaccount.com
GEMINI_API_KEY=your_gemini_api_key_here
SESSION_SECRET=your_random_32_char_secret_here
```

**Ganti:**
- `your-railway-url.up.railway.app` dengan URL Railway actual Anda
- `YOUR_ACTUAL_PRIVATE_KEY_HERE` dengan private key dari Firebase
- `your-firebase-email` dengan client email dari Firebase
- `your_gemini_api_key_here` dengan API key Gemini Anda
- `your_random_32_char_secret_here` dengan random string

---

## 🎉 Selesai!

Aplikasi Anda sekarang siap di-deploy ke Railway dan production-ready!

**Need Help?**
- Cek logs di Railway dashboard
- Baca `DEPLOYMENT.md` untuk info lebih lengkap
- Error? Cek troubleshooting section di atas
