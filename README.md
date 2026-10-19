# DevFolio — Portfolio & Blog API

A Django REST Framework backend for a personal developer portfolio and blog, including JWT owner authentication, project listings, publishing, comments, likes, contact messages, and dashboard statistics.

## Tech stack

- Python, Django 5.2, Django REST Framework
- Simple JWT, django-filter, django-cors-headers
- SQLite (local development), Pillow (image handling)

## Features

- Profile, skills, experience, education and projects
- Blog posts, categories, tags, search, filtering, ordering and pagination
- Draft and published posts; public visitors see published posts only
- Owner-only content management
- Comment moderation, contact inbox, post likes and dashboard statistics
- JWT login, refresh, logout, current user and password change

## Installation — Windows PowerShell

```powershell
git clone https://github.com/julfe-julfeker/devfolio-backend.git
cd devfolio-backend
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DJANGO_SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API base URL: `http://127.0.0.1:8000/api/`

### Environment variables

| Variable | Required | Description |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Yes | Secret signing key. Set securely; never commit it. |

The PowerShell example generates a temporary key for the current terminal. For persistent deployments, configure a stable secret securely. Review production settings before deployment: do not use development `DEBUG=True` in production.

## API endpoints

All paths below are relative to `/api/`.

| Method | Path | Access |
| --- | --- | --- |
| POST | `auth/login/` | Public (active superuser credentials) |
| POST | `auth/refresh/` | Refresh token required |
| POST | `auth/logout/` | Owner |
| GET | `auth/me/` | Owner |
| POST | `auth/change-password/` | Owner |
| GET | `profile/` | Public |
| GET | `skills/` | Public |
| GET | `experiences/` | Public |
| GET | `education/` | Public |
| GET | `projects/` | Public |
| GET | `categories/` | Public |
| GET | `tags/` | Public |
| GET | `posts/` | Public; visitors see published posts |
| GET | `posts/{slug}/` | Public for published posts |
| POST | `posts/` | Owner |
| PATCH, PUT, DELETE | `posts/{slug}/` | Owner |
| POST | `categories/`, `tags/` | Owner |
| GET, POST | `comments/` | Public-facing comments endpoint |
| GET | `comments/inbox/` | Owner |
| PATCH, DELETE | `comments/{id}/` | Owner moderation (confirm supported methods in views) |
| POST | `contact/` | Public |
| GET | `messages/` | Owner |
| `GET/PATCH/DELETE` | `messages/{id}/` | Owner (confirm supported methods in views) |
| POST | `posts/{slug}/like/` | Like toggle (confirm method in views) |
| GET | `dashboard/stats/` | Owner |

Other router-backed CRUD routes are registered for skills, experiences, education, projects, categories and tags. Their write permissions and detail lookup types are defined in the respective viewsets.

### Search, filter, and pagination

```text
GET /api/posts/?search=django
GET /api/posts/?category=python
GET /api/posts/?tag=django
GET /api/posts/?is_featured=true
GET /api/posts/?ordering=-views_count
GET /api/posts/?page=1&page_size=6
GET /api/posts/?status=DRAFT    (owner only)
```

The blog uses page-number pagination with six posts per page by default, and a maximum requested page size of 100. Published posts require a category and at least 100 characters of content. Post titles require at least five characters.

## Authentication and permissions

`POST /api/auth/login/` accepts `username` and `password` and returns `access`, `refresh`, and owner details. Protected requests send `Authorization: Bearer <access_token>`. The blog viewsets use `IsOwnerOrReadOnly`; anonymous visitors cannot access draft posts. Owner account endpoints use `IsOwner`.

## Data model overview

Portfolio resources include Profile, Skill, Experience, Education and Project. Blog resources include Post, Category and Tag. Interactions include comments, likes and contact messages. Consult the model definitions in `portfolio/`, `projects/`, `blog/` and `interactions/` for exact fields and relationships.

## View counts and throttling

Posts expose a read-only `views_count` field. The exact view-count deduplication logic and throttle rates should be documented after verifying their implementations in the backend source; no unverified rate or deduplication claim is made here.

## Postman collection

[DevFolio API Postman Collection](./DevFolio%20API.postman_collection.json)

Import the JSON into Postman, configure the local `base_url` and demo credentials, run Login to obtain tokens, and test protected endpoints. Verify example request bodies before use. **Do not commit real credentials or JWTs.**

## Frontend repository

[DevFolio React frontend](https://github.com/julfe-julfeker/devfolio-frontend)

## Demo video

Add the public-viewable 4–6 minute demonstration link here before submission.
