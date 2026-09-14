# Animal World — Django edition

Your original static site (`index.html` / `style.css` / `style.js`) rebuilt on
a Django backend. The animal data now lives in a database instead of being
hard-coded in JavaScript, and the search box and "Learn More" button now call
real Django API endpoints instead of filtering the DOM / calling `alert()`.

## Project layout

```
animal_world_django/
├── manage.py
├── requirements.txt
├── db.sqlite3                  (created after you run migrate)
├── animal_world/                # project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── animals/                     # the app
    ├── models.py                 # Animal model
    ├── admin.py                  # registers Animal in /admin/
    ├── views.py                  # index page + JSON API views
    ├── urls.py
    ├── migrations/0001_initial.py
    ├── fixtures/animals.json     # seeds the original 6 animals
    ├── templates/animals/index.html
    └── static/animals/style.css, script.js
```

## 1. Install dependencies

It's best to use a virtual environment:

```bash
cd animal_world_django
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Set up the database

```bash
python manage.py migrate
python manage.py loaddata animals   # seeds Lion, Tiger, Elephant, Giraffe, Panda, Dog
```

## 3. (Optional) Create an admin user

So you can add/edit/remove animals from a UI instead of editing the fixture:

```bash
python manage.py createsuperuser
```

Then visit `http://127.0.0.1:8000/admin/` after starting the server.

## 4. Run it

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** — you should see the same site as before,
now backed by Django.

## What changed vs. the original static site

- **Animal data → database.** The `animalInfo` object in `style.js` is gone;
  animals are now an `Animal` model (`animals/models.py`) with `name`,
  `emoji`, `image_url`, `short_description`, `full_description`, and `order`
  fields. The homepage loops over `Animal.objects.all()` in the template.
- **Search → server-side.** Typing in the search box now calls
  `GET /api/search/?q=...`, which filters animals in the database and
  returns JSON. The page re-renders only the matching cards.
- **"Learn More" → server-side + modal.** Clicking the button calls
  `GET /api/animals/<id>/` and shows the result in a small modal instead of
  a browser `alert()`.
- **Admin panel.** `/admin/` lets you add, edit, reorder, or delete animals
  without touching code — the site updates automatically since it reads
  from the database.
- **Static files.** `style.css` and `script.js` moved into
  `animals/static/animals/` (Django's convention) and are referenced with
  `{% static %}` tags rather than plain `<link>`/`<script src>` paths.

## Adding a new animal

Two options:

1. **Admin panel (recommended):** go to `/admin/animals/animal/add/` and
   fill in the fields.
2. **Shell:**
   ```bash
   python manage.py shell
   ```
   ```python
   from animals.models import Animal
   Animal.objects.create(
       name="Zebra",
       emoji="🦓",
       image_url="https://.../zebra.jpg",
       short_description="Zebras are known for their black-and-white stripes.",
       full_description="Every zebra has a unique stripe pattern, like a fingerprint.",
       order=7,
   )
   ```

No template or JavaScript changes are needed — new animals just appear.

## Notes for production

Before deploying, at minimum:
- Set `DEBUG = False` in `animal_world/settings.py`.
- Set a real, secret `SECRET_KEY` (ideally from an environment variable).
- Set `ALLOWED_HOSTS` to your real domain(s).
- Run `python manage.py collectstatic` and serve `staticfiles/` via your
  web server / CDN (or a tool like WhiteNoise).
- Switch from SQLite to Postgres/MySQL if you expect concurrent writes.
