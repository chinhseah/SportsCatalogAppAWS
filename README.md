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
$ sudo apt-get udgrade
```

