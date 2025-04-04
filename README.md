# MaThPot

This repository is an open-source :honey_pot: honeypot for the Matter over Thread IoT network.

## Deployment

The first step to deploy the honeypot is to have a running VM with SSH enabled and set to host-only mode. Once that is done, you can run the `scripts/db.sh`. This script will create a MySQL database with all the required tables.

Before installing Cowrie, you need to modify the `config/cowrie/cowrie.cfg` file. In this file, you need to modify the following:

- `backend_ssh_host`: The IP address of the VM.
- MySQL password.
- `url`: Discord Web Hook (if you don't want to use it, set `enabled` to `false`).

After making these changes, you can run `scripts/init.sh`. This script will install all the required dependencies and configure Cowrie.  
To start Cowrie, run the following:
```
sudo su - cowrie 
make start
```


Before starting the monitoring app, you need to modify the `monitoring/config.py` file with some information. Then, you can start the monitoring by running the `scripts/startMonitoring.sh` script.

## Config Folder

### Cowrie

#### cowrie.cfg

In this file, you need to modify the following:

- `backend_ssh_host`: The IP address of the VM.
- MySQL password.
- `url`: Discord Web Hook URL.

#### userdb.txt

This file is used to configure which SSH credentials are allowed by Cowrie.

## Scripts

### db.sh

This script will install and configure the MySQL database.

### init.sh

This script will install Cowrie and configure it correctly. It will create a new host on the server without `sudo` privileges.

### startMonitoring.sh

This script starts the network monitoring process.

### stopMonitoring.sh

This script stops the network monitoring process.
