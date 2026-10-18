# Lost & Found

A Django web application for reporting, searching and claiming lost or found items on a university campus.

Someone who finds an item registers it on the site. The owner can search the list, submit a claim with proof of ownership, and the finder reviews that claim until the item is delivered.

> **Status:** backend is functional; front-end styling is still in progress.

## Features

- **Authentication:** sign up, log in and log out.
- **Item management:** create, view, edit and delete items (title, description, category, location, event date, image).
- **Search and filters:** free-text search (title, location, description), filter by status and category, filter by registration date range, sort by newest or oldest, and a result counter.
- **Image upload:** one image per item, up to 2 MB.
- **Status workflow:** `open → reviewing → delivered → closed` (a `reviewing` item can go back to `open`). Invalid transitions are rejected.
- **Ownership claims:** a user can claim an item by writing proof of ownership. Only one claim per user per item, and you cannot claim your own item. The finder approves or rejects claims from a review list.
- **Personal report page:** a summary of the items you registered.
- **Input validation:** future dates, too-short titles or descriptions, profanity and vague titles are rejected.

## Tech Stack

| Layer     | Technology                                 |
| --------- | ------------------------------------------ |
| Language  | Python 3.12+                               |
| Framework | Django 6.1                                 |
| Database  | SQLite (default)                           |
| Media     | Pillow (image uploads)                     |
| Frontend  | Django templates + plain CSS               |
| Code style | [Black](https://black.readthedocs.io/)    |

## Requirements

- Git
- Python 3.12 or newer (Django 6.x does not support older versions)

## Installation

```bash
git clone https://github.com/YeganehKhayyat/LostandFound.git
cd LostandFound

# create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

## Database Setup

```bash
python manage.py migrate
```

This creates a local `db.sqlite3` file. It is git-ignored, so each developer gets their own database.

## Create Superuser

```bash
python manage.py createsuperuser
```

The admin panel is available at `/admin/`. Item categories are managed there, so add at least one category before registering items.

## Run the Project

```bash
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

| URL                          | Description                        |
| ---------------------------- | ---------------------------------- |
| `/`                          | Home page                          |
| `/signup/`, `/login/`, `/logout/` | Authentication                |
| `/item/list/`                | Browse and search items            |
| `/item/create/`              | Register an item (login required)  |
| `/item/<id>/`                | Item details                       |
| `/item/<id>/edit/`           | Edit an item                       |
| `/item/<id>/claim/`          | Submit an ownership claim          |
| `/item/claim_list/`          | Review claims                      |
| `/report/`                   | Your personal report               |
| `/admin/`                    | Django admin                       |

## Environment Variables

The project does not read environment variables yet. `SECRET_KEY` and `DEBUG` are hard-coded in `config/settings.py` for development. **Before deploying**, move them to environment variables and set `DEBUG = False`.

## Data Model

```
Category 1 ───── N Item
User     1 ───── N Item
Item     1 ───── N Claim
User     1 ───── N Claim
```

## Project Structure

```
config/          project settings and root URLs
authentication/  sign up / log in / log out
home/            landing page
core/            items, claims, status workflow, business rules
  ├── models.py      Category, Item, Claim
  ├── views.py       item and claim views
  ├── workflows.py   allowed status transitions and claim rules
  ├── services.py    validation rules (keywords, bad words, locations)
  └── data/          JSON word lists used by validation
```

## Code Style

The code is formatted with [Black](https://black.readthedocs.io/) (PEP 8 compatible). Its configuration lives in `pyproject.toml`; migrations are excluded.

```bash
pip install -r requirements-dev.txt
black .             # format everything
black --check .     # verify only (useful in CI)
```

## Documentation

- [`ERD.md`](ERD.md): entity relationships
- [`TEST_PLAN.md`](TEST_PLAN.md): test cases
- [`BUG_REPORT.md`](BUG_REPORT.md): known and fixed bugs
- [`models_review.md`](models_review.md): model design notes

<details>
<summary>Product analysis (Persian) / تحلیل محصول</summary>

<div dir="rtl">

### ۱. افراد درگیر

- **صاحب وسیله:** فردی که وسیله‌اش را گم کرده است.
- **یابنده:** فردی که وسیله‌ای را پیدا کرده و آن را در سامانه ثبت می‌کند.
- **مسئول حراست:** فردی که بر روند نگهداری و تحویل وسیله نظارت می‌کند.
- **ادمین سایت (سیستم):** مسئول مدیریت و پشتیبانی سامانه.

> **نکته:** یابنده و مسئول حراست دو نقش متفاوت هستند و نباید در یک دسته‌بندی قرار بگیرند.

### ۲. پیدا کردن وسیله در سامانه

- جستجو و فیلتر
- دسته‌بندی
- جستجو بر اساس محل پیدا شدن
- جستجو بر اساس تاریخ
- مشاهده عکس
- بررسی اطلاعات هویتی، در صورت وجود

### ۳. حداقل محصول پذیرفتنی (MVP)

- ثبت وسیله گمشده
- ثبت وسیله پیدا‌شده
- مشاهده فهرست وسایل
- مشاهده جزئیات وسیله
- جستجوی وسایل
- اعلام مالکیت وسیله
- تعیین وضعیت وسیله: در انتظار صاحب، در حال بررسی، تحویل داده‌شده

### ۴. داستان‌های کاربر

**داستان اول: ثبت وسیله پیدا‌شده**

> من کاربر الف هستم. می‌خواهم وسیله‌ای را که پیدا کرده‌ام ثبت کنم. بنابراین باید بتوانم وارد سایت شوم و اطلاعات وسیله را ثبت کنم.

**داستان دوم: پیدا کردن وسیله گمشده**

> من کاربر ب هستم. می‌خواهم وسیله‌ای را که گم کرده‌ام پیدا کنم یا آن را ثبت کنم. بنابراین باید بتوانم وارد سایت شوم و وسیله را جستجو یا اطلاعات آن را ثبت کنم.

### ۵. اطلاعات لازم برای ثبت وسیله

عنوان، توضیحات، دسته‌بندی، محل پیدا شدن، تاریخ پیدا شدن، عکس، وضعیت، تاریخ ثبت، مشخصات ثبت‌کننده

</div>

</details>
