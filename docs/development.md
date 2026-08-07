# Development


## Setup

Create environment:

python -m venv .venv


Activate:

Windows:

.venv\Scripts\activate


Install:

pip install -r requirements.txt


Create:

.env

from:

.env.example


Run:

uvicorn app.main:app --reload


Swagger:

http://localhost:8000/docs