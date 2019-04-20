# SportsCatalogAppAWS
## Description
Configuring an Amazon Lightsail Instance to run this Flask Application with a PostgreSQL Database. This includes securing it against a number of attack vectors, installing and configuring a database server and deploying a handmade web application as specified in project details section from Udacity.

## Setup steps in Amazon Lightsail Instance
### Step 1 - Create Linux Instance
Created Amazon Lightsail Ubuntu 16.04 LTS instance:

IP Address: 35.166.162.17

PORT: 2200

SSH Key: Private key provided in "Notes to Reviewer" section upon project submission.

### Step 2 - Updated Instance
Used following Linux commands to update currently installed packages:

```linux
$ sudo apt-get update
```

And upgraded packages:

```linux
$ sudo apt-get upgrade
```
### Step 3 - Changed Port Number
Edited ssh configuration file to change port number from 22 to 2200 using:

```linux 
$ sudo nano /etc/ssh/sshd_config
```
### Step 4 - Configure Firewall

Configure using ufw (Uncomplicated Firewall) to change firewall rules:

First Check firewall status

```linux
$ sudo ufw status
```
Then initial set up to deny all incoming traffic but allow outgoing traffic:

```linux
$ sudo ufw deny incoming
$ sudo ufw allow outgoing
```

Then allow for SSH on port 2200, HTTP on port 80, and NTP on port 123:

```linux
$ sudo ufw allow ssh
$ sudo ufw allow 2200/tcp
$ sudo ufw allow http
$ sudo ufw allow https
```
Finally, check rules and enable firewall:
```linux
$ sudo ufw show added
$ sudo ufw enable
$ sudo ufw status
```
## References
* [Amazon Lightsail Documentation](https://aws.amazon.com/documentation/lightsail/)
* [UFW Essentials: Common Firewall Rules and Commands](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands)
