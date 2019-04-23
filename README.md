# SportsCatalogAppAWS
## Description
Configuring an Amazon Lightsail Instance to run Sports Catalog Flask Application with a PostgreSQL Database. Instructions includes securing it against a number of attack vectors, installing and configuring a Postgres database server and deploying a handmade web application as specified in project details section from Udacity.
## Setup steps in Amazon Lightsail Instance
### Step 1 - Create Linux Instance
Created Amazon Lightsail Ubuntu 16.04 LTS instance:

IP Address: 35.166.162.17

PORT: 2200

SSH Key: Private key provided in "Notes to Reviewer" section upon project submission.

### Step 2 - Update Instance
Used following Linux commands to update currently installed packages:
```linux
$ sudo apt-get update
```
And upgraded packages:
```linux
$ sudo apt-get upgrade
```
### Step 3 - Change ssh Port Number
Edited ssh configuration file to change port number from 22 to 2200 using:
```linux 
$ sudo nano /etc/ssh/sshd_config
```
___resource___: [Amazon Lightsail Documentation](https://aws.amazon.com/documentation/lightsail/)
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
___resource___: [UFW Essentials: Common Firewall Rules and Commands](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands)
### Step 5 - Add 'grader' user
Logging into my Amazon Lightsail account, add user 'grader' and switch to grader user.
```linux
$ ssh -i LightsailDefaultKey-us-west-2.pem ubuntu@35.166.162.17 -p 2200
$ sudo adduser grader
$ sudo su - grader
```
Edit the sudoers file in order to grant grader access to the sudo command. 
Add the line grader ALL=(ALL:ALL) ALL to the file /etc/sudoers.d/grader file.
```linux
$ sudo nano /etc/sudoers.d/grader
```
Using Amazon AWS Management Console to create key-pair as described in below resource.
To use an SSH client on a Mac or Linux computer to connect to my Linux instance, I used following command to set the permissions of my private key file so that only I can read it. If I did not set these permissions, then I cannot connect to my instance using my key pair. 
On my local machine:
```linux
$ chmod 400 grader-keypair.pem
```
Back to my Amazon Lightsail prompt, logged into grader account:
```linux
$ mkdir .ssh
$ chmod 700 .ssh
$ cd .ssh
$ touch authorized_keys
$ chmod 600 authorized_keys
```
On my local machine:
```linux
$ ssh-keygen -y
```
Provided "grader-keypair.pem" filename for file I downloaded from Amazon AWS Management Console during key-pair creation.
Back to my Amazon Lightsail prompt, I logged into grader account, copy and paste output from ssh-keygen into authorized_keys file:
```linux
$ nano authorized_keys
```
On my local machine, I checked login to Amazon Lightsail using:
```linux
ssh -i grader-keypair.pem grader@35.166.162.17 -p 2200
```
___resource___: [How do I add new user accounts with SSH access to my Amazon EC2 Linux instance?](https://aws.amazon.com/premiumsupport/knowledge-center/new-user-accounts-linux-instance/)
### Step 6 - Set up Environment
Set up necessary packages to run my web application like Apache server, Python, Flask, WSGI (Web Server Gateway Interface)
```linux
$ sudo apt-get update
$ sudo apt-get install python-pip
$ sudo apt-get install python-flask 
$ sudo apt-get install python-alchemy
$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-wsgi
```
After running all these, I went to my public IP listed above in a browser and check that I get “Apache2 Ubuntu Default Page”.
Next check timezone is already set to UTC:
```linux
$ sudo dpkg-reconfigure tzdata
```
___resource___: [Deploying a Flask App Using Lightsail on Amazon Web Services](https://alonavarshal.com/blog/flask-on-lightsail-aws/)