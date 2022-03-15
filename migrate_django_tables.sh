#!/bin/bash
echo "WARNING: This will not work if the settings are not configured correctly."
cd "standalone-core/user_client/v2/"
python3 -m venv ./env
source ./env/bin/activate && python3 -m pip install --upgrade pip && pip3 install -r requirements.txt && python3 manage.py makemigrations && python3 manage.py migrate && deactivate
exit