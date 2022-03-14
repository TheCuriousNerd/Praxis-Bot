echo "WARNING: This will not work if the settings are not configured correctly."
cd "standalone-core\user_client\v2"
.\env\Scripts\activate.bat & python manage.py makemigrations & python manage.py migrate & deactivate & exit