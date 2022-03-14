echo 'User Client Table Deletion'
set /p variable="Are you sure you want to delete all user client tables? y/n: "
echo '%variable%'
if '%variable%' == 'y' echo "Deleting user client tables..."
if '%variable%' == 'y' curl http://localhost:42002/api/v1/user_client/drop_tables_all?drop_tables_pin=DROP_DJANGO_TABLES_PIN23344
if '%variable%' == 'y' echo "User client tables deleted."
if '%variable%' == 'y' echo "Recreating tables..."
if '%variable%' == 'y' start /wait call settings_for_setup.bat
if '%variable%' == 'y' start /wait call migrate_django_tables.bat
if '%variable%' == 'y' start /wait call settings_for_setup_postsetup.bat
if '%variable%' == 'y' echo "Recreated tables."