
# 📚 School Management System

یک سیستم مدیریت مدرسه کامل با **بک‌اند اختصاصی** و **فرانت‌اند ساخته‌شده توسط Claude (Anthropic AI)**.

> 🎯 **بک‌اند**: طراحی و پیاده‌سازی شده توسط من  
> 🎨 **فرانت‌اند**: تولید شده با کمک Claude (مدل هوش مصنوعی Anthropic)

[![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![JWT](https://img.shields.io/badge/JWT-Auth-blue?style=flat-square&logo=jsonwebtokens)](https://jwt.io/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=flat-square)](https://www.sqlalchemy.org/)
[![Claude](https://img.shields.io/badge/Frontend-Claude-8A2BE2?style=flat-square&logo=anthropic)](https://anthropic.com/claude)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## 📖 فهرست مطالب

- [توسعه‌دهنده](#-توسعه‌دهنده)
- [ویژگی‌ها](#-ویژگی‌ها)
- [تکنولوژی‌ها](#-تکنولوژی‌ها)
- [ساختار پروژه](#-ساختار-پروژه)
- [نصب و راه‌اندازی](#-نصب-و-راه‌اندازی)
- [مستندات API](#-مستندات-api)
- [متغیرهای محیطی](#-متغیرهای-محیطی)
- [تست با cURL](#-تست-با-curl)
- [قوانین اعتبارسنجی](#-قوانین-اعتبارسنجی)
- [Deployment](#-deployment-production)
- [مشارکت](#-مشارکت)
- [تماس](#-تماس)
- [مجوز](#-مجوز)
- [قدردانی](#-قدردانی)

---

## 👨‍💻 توسعه‌دهنده

| بخش | توضیحات |
|-----|---------|
| **Backend** | طراحی و پیاده‌سازی کامل توسط خودم (Flask, JWT, SQLAlchemy) |
| **Frontend** | تولید شده توسط Claude (Anthropic AI) شامل صفحات HTML, CSS, JavaScript |

---

## ✨ ویژگی‌ها

### 👑 مدیر (Manager)
- مشاهده و ویرایش پروفایل شخصی
- مدیریت معلمان (ویرایش اطلاعات)
- مدیریت دانش‌آموزان (ویرایش اطلاعات، نمره، پایه تحصیلی)
- انتصاب دانش‌آموز به معلم
- مشاهده لیست همه دانش‌آموزان و معلمان

### 👩‍🏫 معلم (Teacher)
- مشاهده و ویرایش پروفایل شخصی
- مشاهده لیست دانش‌آموزان خود
- ثبت نمره برای دانش‌آموزان (۰ تا ۲۰)
- ویرایش و حذف نمره

### 👨‍🎓 دانش‌آموز (Student)
- مشاهده پروفایل شخصی
- ویرایش اطلاعات (شماره تماس، آدرس، تاریخ تولد)
- مشاهده نمره خود

### 🔐 امنیت (پیاده‌سازی شده توسط من)
- احراز هویت با JWT
- سیاه‌نامه توکن‌ها (Logout)
- رمزنگاری پسورد با Werkzeug
- اعتبارسنجی نقش‌ها با دکوراتور سفارشی

---

## 🛠️ تکنولوژی‌ها

### بک‌اند (توسعه شخصی)

| ابزار | کاربرد |
|-------|--------|
| Flask | فریمورک اصلی وب |
| Flask-JWT-Extended | احراز هویت توکن |
| Flask-SQLAlchemy | ORM و دیتابیس |
| Flask-CORS | مدیریت درخواست‌های cross-origin |
| SQLite / PostgreSQL | دیتابیس (قابل تعویض) |
| python-dotenv | مدیریت متغیرهای محیطی |
| Waitress | سرور تولید (Production) |

### فرانت‌اند (تولید شده توسط Claude)

| ابزار | کاربرد |
|-------|--------|
| HTML5 | ساختار صفحات |
| CSS3 | استایل‌بندی و ریسپانسیو |
| JavaScript | تعاملات و ارتباط با API |
| Bootstrap-Flask | المان‌های آماده |

---

## 📁 ساختار پروژه

📂 school-management/
│
├── 📄 main.py              # ورودی اصلی برنامه (نوشته شده توسط من)
├── 📄 wsgi.py              # برای deployment (نوشته شده توسط من)
├── 📄 database.py          # مدل‌های دیتابیس (نوشته شده توسط من)
├── 📄 decorators.py        # دکوراتور role_required (نوشته شده توسط من)
│
├── 📂 api/                 # (نوشته شده توسط من)
│   ├── auth.py             # ثبت‌نام، ورود، خروج
│   ├── manager.py          # APIهای مدیر
│   ├── teacher.py          # APIهای معلم
│   └── student.py          # APIهای دانش‌آموز
│
├── 📂 templates/           # HTML صفحات (تولید شده توسط Claude)
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── student.html
│   ├── teacher.html
│   └── manager.html
│
├── 📂 instance/            # دیتابیس SQLite (ایجاد خودکار)
│
├── 📄 requirements.txt
├── 📄 .env.example
└── 📄 README.md
```

> 📌 **تذکر**: فایل‌های `templates/` شامل HTML، CSS و JavaScript توسط Claude ساخته شده‌اند.

---

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.9+
- pip

### مراحل نصب

```bash
# 1. کلون کردن پروژه
git clone https://github.com/Armin-Sehatzadeh/school-management.git
cd school-management

# 2. ایجاد محیط مجازی
python -m venv venv

# فعال‌سازی در ویندوز
venv\Scripts\activate

# فعال‌سازی در Mac/Linux
source venv/bin/activate

# 3. نصب وابستگی‌ها
pip install -r requirements.txt

# 4. تنظیم متغیرهای محیطی
cp .env.example .env

# 5. اجرای برنامه
python main.py
```

برنامه روی `http://localhost:5000` اجرا می‌شود.

---

## 📡 مستندات API

### احراز هویت

| متد | مسیر | توضیح |
|-----|------|-------|
| POST | `/api/auth/sign-in` | ثبت‌نام کاربر جدید |
| POST | `/api/auth/login` | ورود و دریافت توکن |
| POST | `/api/auth/logout` | خروج (باطل کردن توکن) |

### ثبت‌نام (`/sign-in`)

```json
// دانش‌آموز
{
  "first_name": "علی",
  "last_name": "رضایی",
  "role": "student",
  "email": "ali@example.com",
  "password": "StrongPass123!",
  "phone_number": "09123456789",
  "grade_level": 10
}

// معلم (manager_id اجباری)
{
  "first_name": "مریم",
  "last_name": "کریمی",
  "role": "teacher",
  "email": "maryam@example.com",
  "password": "StrongPass123!",
  "manager_id": 1
}

// مدیر
{
  "first_name": "رضا",
  "last_name": "احمدی",
  "role": "manager",
  "email": "reza@example.com",
  "password": "StrongPass123!"
}
```

### مدیریت (نیاز به توکن مدیر)

| متد | مسیر | توضیح |
|-----|------|-------|
| GET | `/api/manager/profile` | پروفایل مدیر |
| PATCH | `/api/manager/profile` | ویرایش پروفایل |
| GET | `/api/manager/students` | لیست دانش‌آموزان |
| GET | `/api/manager/teachers` | لیست معلمان |
| POST | `/api/manager/assign-student` | انتصاب دانش‌آموز به معلم |
| PATCH | `/api/manager/student/<id>` | ویرایش دانش‌آموز |
| PATCH | `/api/manager/teacher/<id>` | ویرایش معلم |

### معلم (نیاز به توکن معلم)

| متد | مسیر | توضیح |
|-----|------|-------|
| GET | `/api/teacher/profile` | پروفایل معلم |
| PATCH | `/api/teacher/profile` | ویرایش پروفایل |
| GET | `/api/teacher/students` | دانش‌آموزان این معلم |
| POST | `/api/teacher/score/<student_id>` | ثبت نمره |
| PATCH | `/api/teacher/score/<student_id>` | ویرایش نمره |
| DELETE | `/api/teacher/score/<student_id>` | حذف نمره |

### دانش‌آموز (نیاز به توکن دانش‌آموز)

| متد | مسیر | توضیح |
|-----|------|-------|
| GET | `/api/student/profile` | پروفایل |
| PATCH | `/api/student/profile` | ویرایش پروفایل |
| GET | `/api/student/score` | مشاهده نمره |

---

## 🔧 متغیرهای محیطی

در فایل `.env` تنظیم کنید:

```env
DATABASE_URL=sqlite:///instance/site.db
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this
SECRET_KEY=your-secret-key-change-this
FLASK_DEBUG=True
PORT=5000
```

> ⚠️ **هشدار**: برای محیط تولید، حتماً `JWT_SECRET_KEY` را به یک مقدار تصادفی و امن تغییر دهید.

---

## 🧪 تست با cURL

```bash
# 1. ورود
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"ali@example.com","password":"StrongPass123!"}'

# 2. دریافت نمره دانش‌آموز
curl -X GET http://localhost:5000/api/student/score \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 3. ثبت نمره توسط معلم
curl -X POST http://localhost:5000/api/teacher/score/1 \
  -H "Authorization: Bearer TEACHER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"score": 18.5}'

# 4. خروج از سیستم
curl -X POST http://localhost:5000/api/auth/logout \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📝 قوانین اعتبارسنجی

| فیلد | قانون |
|------|-------|
| **رمز عبور** | حداقل ۸ کاراکتر + حروف بزرگ + حروف کوچک + عدد + کاراکتر ویژه |
| **ایمیل** | فرمت استاندارد (`user@example.com`) |
| **نمره** | بین ۰ تا ۲۰ |
| **تاریخ تولد** | فرمت `YYYY-MM-DD` |

---

## 🚀 Deployment (Production)

```bash
# استفاده از Waitress (توصیه شده برای ویندوز)
python wsgi.py

# یا با Gunicorn (لینوکس / Mac)
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
``` 


---

## 🤝 مشارکت

1. Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/amazing`)
3. Commit کنید (`git commit -m 'Add amazing feature'`)
4. Push کنید (`git push origin feature/amazing`)
5. Pull Request باز کنید

---

## 📞 تماس

- **ایمیل**: arminsehatzadeh@gmail.com
- **گزارش باگ**: [Issues](https://github.com/Armin-Sehatzadeh/school-management/issues)

---

## 📜 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است.

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
...

---

## 🙏 قدردانی

- **Claude (Anthropic)** - برای تولید فرانت‌اند پروژه
- **Flask Community** - برای فریمورک فوق‌العاده بک‌اند
- **JWT Extended Team** - برای مدیریت احراز هویت

---

## ⭐️ حمایت

اگر این پروژه برایتان مفید بود، لطفاً یک ستاره ⭐️ به آن بدهید تا دیگران هم آن را پیدا کنند.

---

**ساخته شده با ❤️ توسط من | فرانت‌اند با 🤖 Claude**
```
