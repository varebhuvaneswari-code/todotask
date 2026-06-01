# TodoFlow Django Todo Management System

TodoFlow is a professional Django todo application with authentication, task CRUD, dashboard statistics, search/filter/sort, priority/category support, password reset, responsive Bootstrap UI, animations, dark mode, and secure form handling.

## Project Structure

```text
TO_DO_TASK/
|-- manage.py
|-- requirements.txt
|-- db.sqlite3
|-- TO_DO_TASK/          # project settings, urls, wsgi/asgi
|-- accounts/           # signup, login, profile, password flows
|-- todo/               # task, category, priority, activity models and views
|-- core/               # home and error pages
|-- templates/          # reusable and page templates
|-- static/             # CSS and JavaScript
|-- media/              # uploaded user files
```

## Setup

```powershell
cd C:\Users\LENOVO\Desktop\to-do_task\TO_DO_TASK
..\env\Scripts\python.exe -m pip install -r requirements.txt
..\env\Scripts\python.exe manage.py migrate
..\env\Scripts\python.exe manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Useful Commands

```powershell
..\env\Scripts\python.exe manage.py createsuperuser
..\env\Scripts\python.exe manage.py check
..\env\Scripts\python.exe manage.py test accounts todo core
..\env\Scripts\python.exe manage.py collectstatic
```

## Notes

- Password reset sends a secure reset link. If `.env` has SMTP credentials, it sends to the inbox. Without SMTP credentials, Django prints the reset email in the terminal.
- To enable Gmail delivery, copy `.env.example` to `.env`, add your Gmail address and a Gmail App Password, then restart `runserver`.
- Default priorities are seeded by `todo/migrations/0002_seed_priorities.py`.
- Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and `DJANGO_ALLOWED_HOSTS` before deployment.
- Uploaded avatars are validated by extension and stored under `media/avatars/`.
