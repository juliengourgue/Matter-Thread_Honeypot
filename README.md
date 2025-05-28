@author  Julien Gourgue

# MaThPot

This repository is an open-source :honey_pot: honeypot for the Matter over Thread IoT network.

## Deployment

The first step to deploy the honeypot is to have a running VM with SSH enabled and set to host-only mode. Once that is done, you can run the `scripts/db.sh`. This script will create a MySQL database with all the required tables.

Before installing Cowrie, you need to modify the `config/cowrie/cowrie.cfg` file. In this file, you need to modify the following:

- `backend_ssh_host`: The IP address of the VM.
- MySQL password.
- `url`: Discord Web Hook (if you don't want to use it, set `enabled` to `false`).

After making these changes, you can run `scripts/init.sh`. This script will install all the required dependencies and configure Cowrie and the monitoring app.  

Before starting the monitoring app, you need to modify the `monitoring/config.py` file with :

- `ha_ip` : the IP of the Home Assistant VM
- `ha_port` : the port of the Home Assistant WEB GUI ("8123" by default)
- `db_pswd` : the password you define during the creation of the DB
  



### To start :
#### Cowrie
```
sudo su - cowrie 
make start
```

#### Monitoring app
You can start the monitoring by running the `scripts/startMonitoring.sh` script.

### To stop :
#### Cowrie
```
sudo su - cowrie 
make stop
```

#### Monitoring app
To stop the monitoring you just have to run the `scripts/stopMonitoring.sh` script.
