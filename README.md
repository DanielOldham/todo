# To-do List Application

This is a simple to-do list web application written in Python Django, with CSS Bootstrap for the frontend styling and PostgreSQL for the backend database. It was designed, developed, and deployed in one week as a quick showcase project. 

![image](https://github.com/user-attachments/assets/b9b841f6-45ca-4bff-bb7e-e24240b85161)


### Features

- User accounts
- User signup/login/logout functionality
- To-do list page
- To-do completion
- Edit to-do functionality
- Delete to-do functionality
- To-do list filter functionality
  - Filter by to-do status (All, Completed, Pending)
  - Filter by keyword
 

# Developer Setup

Since these directions are mainly for my own reference, they will be MacOS centric.
`$ROOT` refers to the project root directory.

#### 1. Clone the repo and checkout the `dev` branch
#### 2. Set up python and install dependencies
The Python versioning and dependencies are managed by [mise-en-place](https://mise.jdx.dev/) and [uv](https://www.google.com/search?client=safari&rls=en&q=uv&ie=UTF-8&oe=UTF-8). It is recommended to install and configure both, but not necessary. It is possible to locate the dependencies from the `uv.lock` and install with `pip`, since there aren't very many.
<br>When you have mise and uv set up, install Python and the dependencies with
```bash
uv python install 3.13.2 # Uses uv to install a prebuilt Python
mise sync python --uv    # Tells mise to use the uv-provided Python
mise install             # Installs tools specified in $ROOT/.mise.toml
cd ..                    # Leave the directory
cd $ROOT                 # and re-enter to invoke mise's auto venv activation
uv sync                  # Use uv to create the venv and install the Python dependencies specified in
                         #   pyproject.toml and uv.lock
```

#### 3. Create `.env` dev file
This project manages environment variables with `.env` files, which are not tracked by git.
<br>Add a new file titled `.env.dev` in `$ROOT` with the following contents:
```
SECRET_KEY = '<insecure development key>'
DEBUG = 'True'
DJANGO_ALLOWED_HOSTS="*"
DJANGO_CSRF_TRUSTED_ORIGINS='http://localhost:8000'

DATABASE_NAME = 'todo'
DATABASE_USER = 'todo'
DATABASE_PASSWORD = '<password>'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'
```

#### 4. Install Postgres and configure database
You can install Postgres by installing the application [here](https://postgresapp.com/).
<br>Make sure the developer tools are added to your path, they are usually located in `/Applications/Postgres.app/Contents/Versions/16/bin`.
<br>Create the developer db user and instance with
```
createuser --superuser todo --pwprompt <password>
createdb --owner todo todo
```
`cd` into the directory with `manage.py` and run database migrations with
```
python manage.py migrate
```

#### 4. Download Bootstrap and Bootstrap Icons
Download the compiled Boostrap files located [here](https://getbootstrap.com/docs/5.3/getting-started/download/), and the Bootstrap Icons [here](https://icons.getbootstrap.com/#install).
Make new directories for the Bootstrap files with
```
mkdir $ROOT/todo/static/boostrap
mkdir $ROOT/todo/static/bootstrap/icons
```
Move the `css` and `js` directories from the Bootstrap dist folder into `$ROOT/todo/static/boostrap`.
<br>Unzip the Bootstrap Icons folder and move its contents to `$ROOT/todo/static/bootstrap/icons`.
<br><br>In lieu of downloading Bootstrap, it is also acceptable to use [CDN](https://getbootstrap.com/docs/5.3/getting-started/introduction/). Replace the `stylesheet` links in the `base_header.html` template with references links to CDN instead of local static paths.

#### 5. Try it out!
Run
```
python manage.py runserver
```
Navigate to http://127.0.0.1:8000 to view the application!

#### 6. Testing
Unit tests are located in the `$ROOT/todo/tests` directory. You can run all tests with
```
python manage.py test
```

#### 6. Deployment
This application was hosted with [Fly](https://fly.io).
<br>To deploy, checkout the `main` branch. You can then follow the [directions](https://fly.io/docs/django/getting-started/existing/) for deploying existing Django apps.
You will need to create a file titled `.env.prod` in `$ROOT` with the following contents:
```
SECRET_KEY = "<secure key>"
DEBUG = 'False'
DJANGO_ALLOWED_HOSTS="<app name>.fly.dev"
DJANGO_CSRF_TRUSTED_ORIGINS="https://<app name>.fly.dev"

DATABASE_URL = "postgresql://<fly database name>.flycast"
```
