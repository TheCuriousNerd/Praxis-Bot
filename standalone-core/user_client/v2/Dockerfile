FROM python:3.9

COPY . .
COPY /core/settings_docker.py /core/settings.py

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install psycopg2-binary

# running migrations
#RUN python manage.py makemigrations
# If you use this, option you will currently not be able to connect to the database for some reason.
#RUN python manage.py migrate

# gunicorn
#CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"] # If you use this, option you will currently not be able to connect to the database for some reason.
CMD ["python", "manage.py", "runserver 0.0.0.0:85"]
