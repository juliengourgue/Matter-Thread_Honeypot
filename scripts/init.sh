#! /bin/bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
GIT_ROOT="$(git rev-parse --show-toplevel)"
USERNAME="cowrie"
SOURCE_FOLDER="$GIT_ROOT/config/Cowrie"
cd $GIT_ROOT


read -p "Have you already run db.sh ? [Y|N] " dbcreate
if [[ "$dbcreate" == "N" || "$dbcreate" == "n" ]]; then
    echo "Need to firstly run the db.sh script and modify the cwrie.cfg file"
    exit 1
fi

echo "Installing system dependencies for Cowrie..."
sudo apt-get install git python3-venv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind > /dev/null

# Create the COWRIE non-root account
if id "$USERNAME" &>/dev/null; then
    echo "User $USERNAME exists."
else
    echo "User $USERNAME does not exist."
    echo "WARNING :"
    echo "For security purpose, Cowrie should run on a non-root user"
    echo "Creating a Cowrie non-root user..."
    sudo adduser --disabled-password --gecos "" "$USERNAME"
fi

COWRIE_HOME=$(eval echo ~"$USERNAME")

# Check if the user's home directory exists
if [ ! -d "$COWRIE_HOME" ]; then
    echo "ERROR: User $USERNAME has no home directory"
    exit 1
fi


cd $SOURCE_FOLDER
if [ ! -d "cowrie" ]; then
    echo "Cloning Cowrie repository..."
    git clone  https://github.com/cowrie/cowrie.git
fi

cp "userdb.txt" "cowrie.cfg" "cowrie/etc/"

cd $GIT_ROOT

# Function to move files and set ownership
move_files_and_set_permissions() {
    # Ensure the target directory exists
    mkdir -p "$COWRIE_HOME"

    # Move the files (recursively for the 'cowrie' directory)
    echo "Moving $SOURCE_FOLDER/cowrie to $COWRIE_HOME..."
    sudo cp -r "$SOURCE_FOLDER/cowrie" "$COWRIE_HOME/"
    echo "Moving $SOURCE_FOLDER/Makefile to $COWRIE_HOME..."
    sudo cp "$SOURCE_FOLDER/Makefile" "$COWRIE_HOME/"

    # Change the ownership of the copied files and directories
    sudo chown -R "$USERNAME":"$USERNAME" "$COWRIE_HOME/cowrie/"
    sudo chown "$USERNAME":"$USERNAME" "$COWRIE_HOME/Makefile"

    echo "Files have been successfully moved and ownership updated."

}

if sudo [ -d "$COWRIE_HOME/cowrie/" ]; then
    echo "WARNING: $COWRIE_HOME/cowrie/ already exists!"
    read -p "Do you want to recreate it? [Y|N] " recreate
    if [[ "$recreate" == "Y" || "$recreate" == "y" ]]; then
        echo "Recreating $COWRIE_HOME/cowrie/..."

        # Remove the existing cowrie directory
        sudo rm -rf "$COWRIE_HOME/cowrie"

        # Move the files and set the ownership
        move_files_and_set_permissions
    else
        echo "Skipping recreation of $COWRIE_HOME/cowrie/"
    fi
else
    # If the directory doesn't exist, move the files and set ownership directly
    move_files_and_set_permissions
fi


# Create the PYTHON VENV
VENV_DIR="$COWRIE_HOME/cowrie/cowrie-env"
# Check if the virtual environment already exists
if sudo [ ! -d "$VENV_DIR" ]; then
    echo "Creating a Python virtual environment in $VENV_DIR..."

    # Switch to the 'cowrie' user and create a Python virtual environment
    sudo -u "$USERNAME" python3 -m venv "$VENV_DIR"

    # Give 'cowrie' ownership of the virtual environment
    sudo chown -R "$USERNAME":"$USERNAME" "$VENV_DIR"
else
    echo "Virtual environment already exists in $VENV_DIR"
fi

echo "Upgrading pip and installing required Python packages..."
sudo -u "$USERNAME" bash -c "
    source $VENV_DIR/bin/activate
    python -m pip install --upgrade pip > /dev/null
    python -m pip install --upgrade -r $COWRIE_HOME/cowrie/requirements.txt > /dev/null
    python -m pip install mysql-connector-python > /dev/null
"

echo "Virtual environment setup complete and dependencies installed."


# Path to the SQL file
SQL_FILE_PATH="$SOURCE_FOLDER/mysql.sql"
DB_USER='cowrie'
DB_NAME='cowrie'
# Execute MySQL commands as the newly created user
echo "Importing database schema from mysql.sql..."
read -s -p "Enter the password of the Cowrie db :" DB_PASSWORD
# Using `mysql -u cowrie -p` to import the schema
echo "$DB_PASSWORD" | mysql -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "$SQL_FILE_PATH"

# run the source command inside MySQL
mysql -u "$DB_USER" -p"$DB_PASSWORD" -e "USE $DB_NAME; source $SQL_FILE_PATH;" > /dev/null
echo "Database schema imported successfully!"


cd $GIT_ROOT/monitoring
echo Creating the monitoring venv...
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd $GIT_ROOT

echo "By default cowrie listen on PORT 2222 to redirect traffic from port 22 to port 2222 run the following command:"
echo "sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222"