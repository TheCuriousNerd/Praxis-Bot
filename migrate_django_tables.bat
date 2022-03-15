echo "WARNING: This will not work if the settings are not configured correctly."
cd "standalone-core\user_client\v2"
python -m venv ./env
.\env\Scripts\activate.bat & python -m pip install --upgrade pip & pip install -r requirements.txt & python manage.py makemigrations & python manage.py migrate & deactivate & exit