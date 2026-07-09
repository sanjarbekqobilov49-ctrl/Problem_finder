# Problem Finder

Odamlar muammolarini o'rganish platformasi.

## Loyiha haqida

**Problem Finder** — bu Django asosida ishlab chiqilgan anonim so'rovnoma platformasi. Platforma orqali foydalanuvchilardan kundalik hayotda uchraydigan muammolar haqida anonim ma'lumot yig'iladi va administratorga ushbu javoblarni tahlil qilish imkoniyati yaratiladi.

## Texnologiyalar

- **Backend:** Python + Django
- **Frontend:** Bootstrap 5, JavaScript + Chart.js
- **Ma'lumotlar bazasi:** SQLite (Development) / PostgreSQL (Production)
- **Eksport:** openpyxl (Excel), csv

## O'rnatish

```bash
git clone <repository-url>
cd problem_finder
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Sozlamalar (.env)

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*
# PostgreSQL uchun (ixtiyoriy):
DB_ENGINE=django.db.backends.postgresql
DB_NAME=problemfinder
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

## Imkoniyatlar

- Anonim so'rovnoma
- Progress Bar
- Session orqali boshqarish
- Django Admin (maxsus URL orqali)
- Dashboard va analytics (Chart.js)
- CSV va Excel eksport
- Responsive dizayn
- IP limit (24 soatda 1 marta)
- O'zbek tili

## Loyiha tuzilishi

```
problem_finder/
├── core/          # Asosiy sahifalar (consent, thank-you)
├── survey/        # So'rovnoma logikasi (models, forms, views)
├── analytics/     # Statistikalar, dashboard, admin, eksport
├── templates/     # HTML sahifalar
├── static/        # Frontend fayllar (CSS, JS, SVG)
├── media/         # Yuklangan fayllar
├── staticfiles/   # collectstatic chiqishi (production)
├── .env           # Muhit o'zgaruvchilari
└── manage.py
```

## Productionga chiqish

```bash
# Static fayllarni yig'ish
python manage.py collectstatic

# .env faylida DEBUG=False qiling
# PostgreSQL ulanishini sozlang
# Nginx + Gunicorn + SSL (Certbot) bilan ishga tushiring
```
