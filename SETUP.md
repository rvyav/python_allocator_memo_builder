# SETUP

This application requires to run `REACT` as frontend and `DJANGO REST FRAMEWORK` in the backend to work.

## FRONTEND

Make sure to be in the following folder `frontend/src/` then do:
- `npm install` to install all the dependencies
- `npm run dev` to start the application.

Now open the browser and then application should be available on: `http://localhost:5173/`

## BACKEND

Make sure to be in the root folder of the project, the one that includes `frontend` and `backend` folders then:
- create a virtual environment first: `python3 -m venv venv` then type `source venv/bin/activate`
- go to `backend` folder, the one that include `manage.py` file and do `pip install -r requirements.txt` to install all the dependencies.
- in the same folder, create a `.env` by typing `touch .env` and in the file, we need the following content:
```
DJANGO_SECRET_KEY="django-insecure-mg%%am6*tbreo)(mty2y@ol&nup(7^g@!=urwq(4mk!pj-pngz"
POSTGRESQL_NAME=[your-postgresql-db-name]
POSTGRESQL_USER=[your-postgresql-db-name]
POSTGRESQL_PASSWORD=[your-postgresql-db-name]
POSTGRESQL_HOST=localhost
POSTGRESQL_PORT=5432
OPENAI_API_KEY=[your-openai-developer-ai-key]
OPENAI_MODEL="gpt-5.6-luna"
```
- to create the postgresql db, please refer to the POSTGRESQL section below
- for OPENAPI developer API key, there are videos on Youtube on how to generate one

After all these steps are completed.

From `backend` folder, the one that include `manage.py` file, type `python manage.py runserver` to start the backend application.

Once its running, open the browser to access the health check page: `http://127.0.0.1:8000/health/` that return the message `connected!!!` if you are well connected to the database.

[WE ARE NOT REALLY USING ANY DATABASE IN THIS PROJECT BECAUSE ITS NOT A PRODUCTION READY APPLICATION]

### POSTGRESQL

Assuming that you are postgresql running in your terminal in the background:
- `psql -U postgres`: access postgresql
- `CREATE USER myapp_user WITH PASSWORD 'your_secure_password';` create a new user
- `CREATE DATABASE myapp_db OWNER myapp_user;` create a database
- `GRANT ALL PRIVILEGES ON DATABASE myapp_db TO myapp_user;` give all privileges to the database created to the user above

Now you can use those values in the `POSTGRESQL` of in `BACKEND` section above.
