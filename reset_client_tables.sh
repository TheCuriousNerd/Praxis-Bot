#!/bin/bash
echo 'User Client Table Deletion'
echo "Are you sure you want to delete all user client tables? y/n: "
read variable
if [ "$variable" == "y" ]; then
    echo "Deleting user client tables..."
    curl http://localhost:42002/api/v1/user_client/drop_tables_all?drop_tables_pin=DROP_DJANGO_TABLES_PIN23344
    echo "User client tables deleted."
    echo "Recreating user client tables..."
    bash settings_for_setup.sh
    bash migrate_django_tables.sh
    bash settings_for_setup_postsetup.sh
    echo "User client tables recreated."

else
    echo "Aborting..."
fi