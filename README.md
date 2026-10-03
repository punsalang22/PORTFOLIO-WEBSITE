# Karl Adrian Punsalang — Personal Portfolio (Django)

A personal portfolio website built with Django. Visitors see my personal information and projects. I (the site owner) can sign in to a private dashboard, which only superusers can access, to manage **projects** and **tech stacks**. Anything added there appears on the public portfolio straight away.

- **Live site:** https://punsalang22.pythonanywhere.com
- **Repository:** https://github.com/punsalang22/PORTFOLIO-WEBSITE

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Requirements](#requirements)
4. [Run It Locally (Step by Step)](#run-it-locally-step-by-step)
5. [Environment Variables (.env)](#environment-variables-env)
6. [Pages and URLs](#pages-and-urls)
7. [How to Use the Dashboard](#how-to-use-the-dashboard)
8. [Running the Tests](#running-the-tests)
9. [Deploying to PythonAnywhere](#deploying-to-pythonanywhere)
10. [Project Structure](#project-structure)
11. [Data Model](#data-model)
12. [Git Workflow](#git-workflow)
13. [Troubleshooting](#troubleshooting)

---

## Features

**Public portfolio**
- Home page with my personal information (name, summary, contact details).
- Project list and project detail pages, read directly from the database.

**Admin-only area**
- **Dedicated sign-in page** (`/login/`) that **only superusers** can use. Regular users (and staff users who are not superusers) cannot sign in, even with a correct password. They get the same "incorrect username or password" message, so the page does not reveal which accounts exist.
- After signing in you are redirected to **`/dashboard/`**.
- **Projects table**: Project Name, Description (truncated to 50 characters), Tech Stack (comma separated), and Link (a clickable `<a>` tag).
- **Tech Stacks table**: Tech Stack Name, Project It Was Used, and Date Added.
- **Create Project** form: Project Name, Project Description (textarea), Tech Stacks (one checkbox per tech stack in the database), and Link. Every field is required and the form shows an error for each field that is missing or invalid.
- **Create Tech Stack** form: Tech Stack Name (required; duplicates such as `python` vs `Python` are rejected).
- A tech stack is a single record that can be linked to **many projects** (many-to-many), so nothing is duplicated.
- Every dashboard page redirects anyone who is not a superuser to the sign-in page.

---

## Tech Stack

| Layer      | Technology                         |
|------------|------------------------------------|
| Language   | Python 3.12+ (developed on 3.14)   |
| Framework  | Django 6.0.7                       |
| Database   | SQLite (file is created by `migrate`) |
| Config     | python-dotenv (`.env` file)        |
| Hosting    | PythonAnywhere                     |

---

## Requirements

Install these before you start:

- **Python 3.12 or newer** (Django 6 does not support older versions). Check with:
  ```bash
  python --version        # Windows
  python3 --version       # macOS / Linux
  ```
- **Git**: https://git-scm.com/downloads

---

## Run It Locally (Step by Step)

> The Django project lives in the **`portfolio_django/`** folder (the one that contains `manage.py`). Run every command below from that folder unless stated otherwise.
>
> The repository does **not** include a database, a virtual environment, or a `.env` file. You create all three in the steps below.

### 1. Clone the repository

```bash
git clone https://github.com/punsalang22/PORTFOLIO-WEBSITE.git
cd PORTFOLIO-WEBSITE/portfolio_django
```

### 2. Create and activate a virtual environment

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
> If PowerShell says running scripts is disabled, run
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then activate again.
> In **Command Prompt (cmd)**, use `.venv\Scripts\activate.bat` instead.

**Windows (Git Bash)**
```bash
python -m venv .venv
source .venv/Scripts/activate
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

When it is active, your prompt starts with `(.venv)`.

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

Copy the example file:

```bash
# Windows (PowerShell / cmd)
copy .env.example .env

# macOS / Linux / Git Bash
cp .env.example .env
```

Then generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Open `.env` and replace the value of `SECRET_KEY` with the key you just generated. The other default values already work for local development. See [Environment Variables](#environment-variables-env) for details.

### 5. Apply the database migrations

```bash
python manage.py migrate
```

This creates a new `db.sqlite3` with all the tables. You do **not** need to run `makemigrations`; the migration files are already in the repository.

### 6. Create a superuser (admin account)

```bash
python manage.py createsuperuser
```

Enter a username, an email (optional) and a password. This is the **only kind of account** that can sign in at `/login/`.

### 7. Start the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

### 8. Try it out

1. Go to **http://127.0.0.1:8000/login/** and sign in with the superuser from step 6. You land on `/dashboard/`.
2. Open **Tech Stacks → + Create Tech Stack** and add a few (e.g. `Python`, `Django`, `HTML`).
3. Open **Projects → + Create Project**, fill in every field, tick one or more tech stacks, and save.
4. Click **View Portfolio** (or open http://127.0.0.1:8000/projects/). The new project and its tech stacks are listed there.
5. *(Optional)* Add your personal information (name, summary, contact) at **http://127.0.0.1:8000/admin/** → *Personal informations* → *Add*. It appears on the home page.

**To check that regular users are blocked:** create a normal user in `/admin/` → *Users* → *Add user* (leave "Superuser status" unticked). Sign out, then try to sign in at `/login/` with that user. It is rejected.

Stop the server with `Ctrl + C`. Next time, you only need to activate the virtual environment (step 2) and run `python manage.py runserver`.

---

## Environment Variables (.env)

Settings are read from `portfolio_django/.env` (loaded by `python-dotenv`). The repository only contains **`.env.example`**, which has placeholder values. The real `.env` is listed in `.gitignore` and must never be committed.

| Variable               | Required | Example (local)                                   | Example (PythonAnywhere)                          | Description |
|------------------------|----------|---------------------------------------------------|---------------------------------------------------|-------------|
| `SECRET_KEY`           | **Yes**  | *(generated key)*                                 | *(a different generated key)*                     | Django cryptographic signing key. The app refuses to start without it. |
| `DEBUG`                | No       | `True`                                            | `False`                                           | Shows detailed error pages. Defaults to `False`. |
| `ALLOWED_HOSTS`        | No       | `127.0.0.1,localhost`                             | `punsalang22.pythonanywhere.com`                  | Comma-separated hostnames the site may be served from. |
| `CSRF_TRUSTED_ORIGINS` | No       | `http://127.0.0.1:8000,http://localhost:8000`     | `https://punsalang22.pythonanywhere.com`          | Comma-separated origins (with `http://` / `https://`) trusted for form submissions. |

---

## Pages and URLs

| URL                               | Who can open it | Description |
|-----------------------------------|-----------------|-------------|
| `/`                               | Everyone        | Home: personal information |
| `/personal/`                      | Everyone        | Same as home |
| `/projects/`                      | Everyone        | All projects with their tech stacks |
| `/projects/<id>/`                 | Everyone        | Project detail |
| `/login/`                         | Everyone (only superusers can sign in) | Admin-only sign-in page |
| `/logout/`                        | Signed-in user (POST) | Sign out ("Sign out" button in the dashboard) |
| `/dashboard/`                     | Superuser only  | Overview with counts and shortcuts |
| `/dashboard/projects/`            | Superuser only  | Projects table + "Create Project" button |
| `/dashboard/projects/create/`     | Superuser only  | Create Project form |
| `/dashboard/tech-stacks/`         | Superuser only  | Tech Stacks table + "Create Tech Stack" button |
| `/dashboard/tech-stacks/create/`  | Superuser only  | Create Tech Stack form |
| `/admin/`                         | Staff/superuser | Built-in Django admin |

---

## How to Use the Dashboard

- **Create tech stacks first.** The Create Project form lists every tech stack in the database, so add them before creating a project. If none exist yet, the form shows a link to create one.
- **Validation:** submitting a form with an empty field, a whitespace-only name, an invalid URL, or no tech stack selected shows an error under that field. Nothing is saved until the form is valid.
- **No duplicate tech stacks:** a tech stack is a single shared record. Selecting `Python` on several projects links them all to the same `Python` record, and the Tech Stacks table lists every project that uses it.

---

## Running the Tests

From `portfolio_django/` with the virtual environment active:

```bash
python manage.py test punsalang_q2
```

The 20 tests cover the superuser-only sign-in, dashboard access rules, both tables, both create forms (including failure cases), and the new projects showing on the public pages.

---

## Deploying to PythonAnywhere

These steps assume a free account named `punsalang22`. Replace it with your own username everywhere.

### 1. Clone the project and set it up (in a **Bash console**)

Open **Dashboard → Consoles → Bash** and run:

```bash
git clone https://github.com/punsalang22/PORTFOLIO-WEBSITE.git
cd PORTFOLIO-WEBSITE/portfolio_django

python3.13 -m venv .venv          # any installed Python 3.12+ works
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
nano .env                          # paste the key, then set the production values below
```

Production `.env`:

```env
SECRET_KEY=<the key you just generated>
DEBUG=False
ALLOWED_HOSTS=punsalang22.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://punsalang22.pythonanywhere.com
```

(Save in nano with `Ctrl + O`, `Enter`, then exit with `Ctrl + X`.)

Then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 2. Create the web app

1. Go to the **Web** tab → **Add a new web app** → *Next*.
2. Choose **Manual configuration** (not "Django"), and pick the **same Python version** you used for the virtualenv.
3. In the **Virtualenv** section, enter:
   `/home/punsalang22/PORTFOLIO-WEBSITE/portfolio_django/.venv`
4. In the **Code** section, set **Source code** and **Working directory** to:
   `/home/punsalang22/PORTFOLIO-WEBSITE/portfolio_django`

### 3. Edit the WSGI file

On the Web tab, click the **WSGI configuration file** link (`/var/www/punsalang22_pythonanywhere_com_wsgi.py`), delete everything in it, and paste:

```python
import os
import sys

path = '/home/punsalang22/PORTFOLIO-WEBSITE/portfolio_django'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Save it. (`settings.py` loads `.env` from the project folder on its own.)

### 4. Static files

In **Web → Static files**, add:

| URL        | Directory                                                    |
|------------|--------------------------------------------------------------|
| `/static/` | `/home/punsalang22/PORTFOLIO-WEBSITE/portfolio_django/staticfiles` |

This is needed for the `/admin/` styling when `DEBUG=False`.

### 5. Reload and test

Click the green **Reload** button and open https://punsalang22.pythonanywhere.com. Test:
home → projects → `/login/` (superuser works, regular user is blocked) → dashboard tables → create a tech stack → create a project → check that it appears on `/projects/`.

### Updating the deployed site later

```bash
cd ~/PORTFOLIO-WEBSITE && git pull
cd portfolio_django && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then click **Reload** on the Web tab.

---

## Project Structure

```
PORTFOLIO-WEBSITE/
├── .gitignore
├── README.md
├── index.html, style.css, script.js   # Quiz 1 static portfolio (not used by Django)
└── portfolio_django/                  # Django project root (run manage.py here)
    ├── manage.py
    ├── requirements.txt
    ├── .env.example                   # template for your .env
    ├── config/                        # project settings, root urls, wsgi/asgi
    │   ├── settings.py
    │   └── urls.py
    └── punsalang_q2/                  # main app
        ├── models.py                  # PersonalInformation, TechStack, Project
        ├── forms.py                   # superuser login form, ProjectForm, TechStackForm
        ├── views.py                   # public pages, login, dashboard, create views
        ├── urls.py
        ├── admin.py
        ├── tests.py
        ├── migrations/
        └── templates/
            ├── personal_info.html, project_list.html, project_detail.html
            └── dashboard/             # base, login, home, tables, forms
```

---

## Data Model

```
TechStack                       Project
---------                       -------
id                              id
name        (unique)   <──M2M──> tech_stack
created_at  (auto)              project_name
                                description
                                link (URL)

PersonalInformation: first_name, middle_name, last_name, summary,
                     contact_number, email, address
```

`Project.tech_stack` is a `ManyToManyField` to `TechStack` (`related_name='projects'`). One tech stack can belong to many projects, and one project can have many tech stacks.

---

## Git Workflow

Nothing is pushed straight to `main`. Each quiz is built on its own branch and merged through a pull request:

| Branch     | Work                                                      | Merged via |
|------------|-----------------------------------------------------------|------------|
| `quiz2`    | Django models, project list/detail and personal info pages | PR #1 |
| `quiz5-6`  | Superuser-only sign-in, dashboard, TechStack model, create views, `.env`, deployment | Pull request into `main` |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ImproperlyConfigured: SECRET_KEY is not set` | You have no `.env`, or it is in the wrong folder. It must be next to `manage.py` (step 4). |
| `ModuleNotFoundError: No module named 'django'` / `'dotenv'` | The virtual environment is not active, or you skipped `pip install -r requirements.txt`. |
| `no such table: ...` | Run `python manage.py migrate`. |
| Sign-in says "Please enter a correct username and password" | Only **superusers** can sign in. Create one with `python manage.py createsuperuser`. |
| `CSRF verification failed` on the live site | Add your `https://...` domain to `CSRF_TRUSTED_ORIGINS` in `.env` and reload the web app. |
| `DisallowedHost` / "Bad Request (400)" | Add the domain to `ALLOWED_HOSTS` in `.env`. |
| PowerShell won't activate the venv | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again. |
