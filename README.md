# IPProject

FreeAgent system using Python 3 and Django. Written for ELEC3609 Semester 2, 2017 at The University of Sydney.

# Installation

## 1. Clone this repo

Download the files with:

```
git clone https://github.com/lemonpkt/IPProject
```

## 2. Install dependencies

Navigate to the cloned folder and install the requirements:

```
cd IPProject
pip3 install -r requirements.txt
```

## 3. Setup the database

Migrate the database:

```
python manage.py makemigrations
python manage.py migrate
```

## 4. Run

Launch the website locally at `http://127.0.0.1:8000`:

```
python manage.py runserver 0:8000
```

Navigate to `http://127.0.0.1:8000/freeAgentApp` in your browser to test it.

# Project layout

* `freeAgent` contains the Django project
* `freeAgentApp` contains the primary app used by the freeAgent project, including all views and models
* `media` contains sample code uploads to the site
