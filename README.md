# Dokumentasi API Gacha Impact

## Pendahuluan
API ini adalah layanan backend untuk simulasi sistem gacha dalam permainan Genshin Impact. API ini memungkinkan pengguna untuk melakukan pull gacha, melihat riwayat gacha, serta mengelola data pengguna.

---

## Instalasi dan Konfigurasi
1. **Persyaratan**
   - Python 3.x
   - Flask
   - Flask-SQLAlchemy
   - Flask-Marshmallow
   - MySQL Server
   
2. **Instalasi Dependensi dari requirements.txt**
```sh
pip install -r requirements.txt
```

3. **Konfigurasi Database**
   - Pastikan MySQL berjalan dan buat database `gacha_impact`.
   - Pastikan koneksi database dikonfigurasi dengan benar di `app.py`:
   ```python
   app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@localhost/gacha_impact"
   ```

4. **Menjalankan Server**
```sh
python app.py
```
---

## Model Database
### 1. User
| Field            | Type      | Description              |
|-----------------|----------|--------------------------|
| uid             | String   | ID unik pengguna        |
| username        | String   | Nama pengguna           |
| email           | String   | Email pengguna          |
| primogems       | Integer  | Jumlah primogems        |
| pity            | Integer  | Hitungan pity gacha     |
| four_star_pity  | Integer  | Hitungan pity 4-star    |
| is_rate_on      | Boolean  | Apakah rate up aktif    |
| four_star_rate_on | Boolean | Apakah rate up 4-star aktif |

### 2. Item
| Field       | Type    | Description               |
|------------|--------|---------------------------|
| id         | Integer | ID item                   |
| name       | String  | Nama item                 |
| item_type  | String  | Jenis item                |
| type       | String  | Kategori item             |
| rarity     | Enum    | Rarity (3-star, 4-star, 5-star) |
| image_url  | String  | URL gambar item           |
| is_rate_up | Boolean | Status rate up            |

### 3. History
| Field      | Type      | Description               |
|-----------|----------|---------------------------|
| id_result | Integer  | ID hasil gacha            |
| uid       | String   | ID pengguna               |
| item_name | String   | Nama item yang diperoleh  |
| rarity    | Enum     | Rarity item (3-star, 4-star, 5-star) |
| date      | DateTime | Waktu gacha dilakukan     |

---

## Endpoint API
### 1. **GET /user**
Mengambil daftar pengguna.
#### Request:
```sh
GET /user
```
#### Response:
```json
[
  {
    "uid": "your uid",
    "username": "your username",
    "email": "your email",
    "primogems": 1600,
    "pity": 50,
    "four_star_pity": 5,
    "is_rate_on": false,
    "four_star_rate_on": false
  }
]
```

### 2. **GET /history**
Mengambil riwayat gacha pengguna tertentu.
#### Request:
```sh
GET /history
Content-Type: application/json
{
  "uid": "your uid"
}
```
#### Response:
```json
[
  {
    "id_result": 1,
    "uid": "your uid",
    "item_name": "Skyward Harp",
    "rarity": "5-star",
    "date": "2024-03-23T12:00:00"
  }
]
```

### 3. **GET /pull**
Melakukan gacha pull.
#### Request one pull:
```sh
GET /pull
Content-Type: application/json
{
  "uid": "your uid",
  "type": "one_pull"
}
```
#### Request ten pull:
```sh
GET /pull
Content-Type: application/json
{
  "uid": "your uid",
  "type": "ten_pull"
}
```
#### Response one pull:
```json
{
  "current_4star_pity": 9,
  "current_pity": 35,
  "five_star_rateon": false,
  "four_star_rateon": true,
  "gacha_color": "biru",
  "gacha_result": [
    {
      "date": "Sun, 23 Mar 2025 18:48:12 GMT",
      "image_url": "https://gensh.honeyhunterworld.com/img/i_n14302_gacha_icon_w145.webp",
      "item_name": "Thrilling Tales of Dragon Slayer",
      "rarity": "3-star",
      "user_4star_pity": 9,
      "user_pity": 35
    }
  ],
  "uid": "4FxCWzMMQDbRU45jBbXer5Hk7Sk1"
}
```

#### Response ten pull:
```json
{
  "current_4star_pity": 9,
  "current_pity": 45,
  "five_star_rateon": false,
  "four_star_rateon": false,
  "gacha_color": "ungu",
  "gacha_result": [
    {
      "date": "Sun, 23 Mar 2025 18:48:43 GMT",
      "image_url": "https://gensh.honeyhunterworld.com/img/bennett_032_gacha_card_w145.webp",
      "item_name": "Bennet",
      "rarity": "4-star",
      "user_4star_pity": 0,
      "user_pity": 36
    },
    {
      "date": "Sun, 23 Mar 2025 18:48:43 GMT",
      "image_url": "https://gensh.honeyhunterworld.com/img/i_n15304_gacha_icon_w145.webp",
      "item_name": "Slingshot",
      "rarity": "3-star",
      "user_4star_pity": 1,
      "user_pity": 37
    },
    {
      "date": "Sun, 23 Mar 2025 18:48:43 GMT",
      "image_url": "https://gensh.honeyhunterworld.com/img/i_n11302_gacha_icon_w145.webp",
      "item_name": "Harbinger of Dawn",
      "rarity": "3-star",
      "user_4star_pity": 2,
      "user_pity": 38
    },
    ...,
    {
      "date": "Sun, 23 Mar 2025 18:48:43 GMT",
      "image_url": "https://gensh.honeyhunterworld.com/img/i_n15304_gacha_icon_w145.webp",
      "item_name": "Slingshot",
      "rarity": "3-star",
      "user_4star_pity": 9,
      "user_pity": 45
    }
  ],
  "uid": "4FxCWzMMQDbRU45jBbXer5Hk7Sk1"
}
```

### 4. **PATCH /user/<uid>**
Memperbarui informasi pengguna.
#### Request:
```sh
PATCH /user/{your uid}
Content-Type: application/json
{
  "username": "NewTraveler",
  "primogems": 1600
}
```
#### Response:
```json
{
  "message": "User update success"
}
```

---

## Mekanisme Gacha
- **Probabilitas Gacha:**
  - 5-star: 1%
  - 4-star: 5%
  - 3-star: 94%
- **Pity System:**
  - 5-star dijamin setiap 90 pull
  - 4-star dijamin setiap 10 pull
  - Probabilitas 4-star naik menjadi 15% ketika mencapai pity 5 dan naik menjadi 35% ketika mencapai pity 8.
  - Probabilitas 5-star naik menjadi 2% ketika mencapai pity 50 dan naik menjadi 14% ketika mencapai pity 70.
  - Pity akan reset ketika mendapatkan rarity tertentu.
  - Mendapatkan karakter rate-up akan mengubah status rate-on user menjadi `false`.
  - Ketika dalam status false pada rate-on, probabilitas mendapatkan rate-on karakter adalah 50%. Jika mendapatkan rate-on karakter, user tetap dalam status `false` dalam rate-on. Jika mendapatkan karater yang bukan rate-up, maka status akan menjadi `true` pada rate-on
  - Rate-up meningkatkan peluang karakter banner.

---

## Kesimpulan
API ini menyediakan fitur lengkap untuk sistem gacha, termasuk manajemen pengguna, history gacha, dan mekanisme gacha yang mengikuti sistem pity.

