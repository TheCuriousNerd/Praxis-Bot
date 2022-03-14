cd "standalone-core\user_client\v2"
.\env\Scripts\activate.bat & python manage.py makemigrations & python manage.py migrate --database=localhost & deactivate & exit