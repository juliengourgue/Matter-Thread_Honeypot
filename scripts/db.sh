#!/bin/bash

DB_NAME='cowrie'
DB_USER='cowrie'
MYSQL_HOST='localhost'



echo "Installing MySQL..."
sudo apt install mysql-server
sudo service mysql restart

read -p "Do you want to create the database in MySQL ? [Y|N] " dbcreate
if [[ "$dbcreate" == "Y" || "$dbcreate" == "y" ]]; then
    read -s -p "Enter a password for the db :" DB_PASSWORD
    echo "Creating the DB in MySQL and the User: $DB_USER"

    # Create the database if it doesn't exist
    sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"

    # Create the user and set a password
    sudo mysql -u root -e "CREATE USER IF NOT EXISTS '$DB_USER'@'$MYSQL_HOST' IDENTIFIED BY '$DB_PASSWORD';"

    # Grant privileges (this should not include IDENTIFIED BY)
    sudo mysql -u root -e "GRANT ALL ON $DB_NAME.* TO '$DB_USER'@'$MYSQL_HOST';"
    sudo mysql -u root -e "GRANT INSERT, SELECT, UPDATE ON $DB_NAME.* TO '$DB_USER'@'$MYSQL_HOST';"

    # Flush privileges to apply changes
    sudo mysql -u root -e "FLUSH PRIVILEGES;"

    echo "WARNING: You need to add the db password in 'config/Cowrie/cowrie.cfg'"

fi
