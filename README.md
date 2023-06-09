# Gemu Shoppu
Gemu Shoppu adalah aplikasi web untuk membeli gaming gear dan produk-produk terkait komputer. Aplikasi ini dikembangkan menggunakan kerangka kerja Django untuk proyek akhir Rekayasa Perangkat Lunak (RPL).

## Deskripsi
Gemu Shoppu merupakan platform e-commerce yang menyediakan berbagai macam produk gaming gear seperti mouse, keyboard, headset, dan banyak lagi. Pengguna dapat menjelajahi katalog produk, menambahkan produk ke keranjang belanja, dan menyelesaikan pembelian.

Fitur utama yang ada pada Gemu Shoppu meliputi:

- Menambahkan produk ke wishlist untuk menyimpan produk yang diminati
- Menambahkan produk ke keranjang belanja
- Proses checkout untuk menyelesaikan pembelian
- Daftar akun pengguna dengan autentikasi
- Halaman profil pengguna untuk melihat riwayat pesanan dan mengelola informasi akun

### Berikut adalah langkah-langkah untuk menginstal aplikasi Gemu Shoppu di lingkungan lokal Anda:

Clone repositori ini ke dalam direktori lokal Anda:
```bash
git clone https://github.com/khalidziarabbani/projek-akhir-RPL.git
```

Buka terminal dan masuk ke direktori proyek:
```bash
cd projek-akhir-RPL
```

Buat virtual environment dan aktifkan:
```bash
python -m venv env
source env/bin/activate
```

Instal semua dependensi yang diperlukan:
 ```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi
Untuk menjalankan aplikasi, Anda perlu melakukan langkah-langkah berikut:

Migrasikan basis data:
```bash
python manage.py migrate
```

Jalankan server pengembangan:
```bash
python manage.py runserver
```

Buka browser dan akses aplikasi melalui URL ``http://localhost:8000.``

Dengan begitu, Anda dapat menjalankan aplikasi Gemu Shoppu di lingkungan lokal Anda. Selamat berbelanja!
