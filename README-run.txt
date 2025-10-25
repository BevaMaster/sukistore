1. Jalankan backend
   cd sukistore/backend
   python -m venv venv
   venv\Scripts\activate   (Windows)  atau  source venv/bin/activate (Mac/Linux)
   pip install -r requirements.txt
   python db_init.py
   python app.py

2. Buat akun lewat terminal
   python create_user.py nama password
   atau pakai curl:
   curl -X POST http://localhost:5000/api/register -H "Content-Type: application/json" -d "{\"username\":\"u\",\"password\":\"p\"}"

3. Jalankan frontend
   cd ../frontend
   npm install
   npm start


-----

1. Jalankan backend Flask

Buka terminal baru, lalu jalankan langkah berikut satu per satu:

cd D:\Folder XTKJ2\sukistore\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python db_init.py
python app.py


Kalau berhasil, terminal akan menampilkan seperti:

 * Running on http://127.0.0.1:5000


Biarkan terminal ini tetap terbuka.

2. Coba lagi perintah register

Buka terminal baru (biar Flask tetap jalan), lalu jalankan:

cd D:\Folder XTKJ2\sukistore
curl -X POST http://localhost:5000/api/register -H "Content-Type: application/json" -d "{\"username\":\"u\",\"password\":\"p\"}"


Kalau berhasil, akan muncul output seperti:

{"token":"...","username":"u"}

3. Tes di browser

Buka browser, masuk ke:

http://localhost:5000