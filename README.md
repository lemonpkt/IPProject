# IPProject

FreeAgent system using Python 3 and Django. Written for ELEC3609 Semester 2, 2017 at The University of Sydney.

## Installation

### 1. Clone this repo

Download the files with:

```
git clone https://github.com/lemonpkt/IPProject
```

### 2. Install dependencies

Navigate to the cloned folder and install the requirements:

```
cd IPProject
pip3 install -r requirements.txt
```

### 3. Setup the database

Migrate the database:

```
python manage.py makemigrations
python manage.py migrate
```

### 4. Run

Launch the website locally at `http://127.0.0.1:8000`:

```
python manage.py runserver 0:8000
```

Navigate to `http://127.0.0.1:8000/freeAgentApp` in your browser to test it.

## Project layout

* `freeAgent` contains the Django project
* `freeAgentApp` contains the primary app used by the freeAgent project, including all views and models
* `media` contains sample code uploads to the site

## Overview of views

A brief overview of the views in `views.py` and what they do:

* `IndexView` - The main page. Displays a list of projects and allows an "Free Agent" to accept them.
* `UserFormView` - New user registration.
* `Login` - Login page.
* `DetailView` - Displays detailed information about a project.
* `ProjectCreate`, `ProjectUpdate`, `ProjectDelete` - Views for manipulating a project.
* `add_worker` - Assigns a "Free Agent" to a given project, among other things.
* `UserSerializer` - RESTful GET endpoint for retreiving a list of usernames.
* `ProjectCreateAPI`, `ProjectListAPI` - RESTful endpoints for manipulating projects.

## AJAX

There is a Javascript function based on JQuery to checking whether username had been taken. This function contains an AJAX to get existing username from Restful API which ‘url’ is /freeAgentApp/serializerUsername. The AJAX use get method and JSON datatype. After matching with the typed username, a remind message will be shown through JQuery. 

## RESTful API

In this project, there are four rest api built.

* Username, without authentication, support GET method, `freeAgentApp/serializerUsername`, can get all the username and their identification.

* Create project, must be authenticated, support POST method, `/freeAgentApp/SerializeProject/create`, users can create project through this webpage.

* List project, must be authenticated, support GET method, `/freeAgentApp/SerializeProject/list`,
User can check their relevant projects through this page, get the id for indicated project.

* Manage project, must be authenticated and given the id, support GET, PUT, DELETE method, `/freeAgentApp/SerializeProject/manage/<id>`, user can modify the project (Update, Delete) through this site.
