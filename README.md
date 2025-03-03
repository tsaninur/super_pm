# Python Password Manager

A simple local password manager written in Python and MariaDB. Uses [pbkdf2](https://en.wikipedia.org/wiki/PBKDF2) to derive a 256 bit key from a MASTER PASSWORD and DEVICE SECRET to use with AES-256 for encrypting/decrypting.


# Installation
You need to have python3 to run this on Windows, Linux or MacOS
## Linux
### Install Python Requirements
```
sudo apt install python3-pip
pip install -r requirements.txt
```

### MariaDB
#### Install MariaDB on linux with apt
```
sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
sudo add-apt-repository 'deb http://ftp.osuosl.org/pub/mariadb/repo/5.5/ubuntuprecise main'
sudo apt-get update
sudo apt-get install mariadb-server
```
#### Create user 'pm' and grant permissions
**Login to mysql as root**

```
sudo mysql -u root
```
**Create User**
```
CREATE USER 'pm'@localhost IDENTIFIED BY 'password';
```
**Grant privileges**
```
GRANT ALL PRIVILEGES ON *.* TO 'pm'@localhost IDENTIFIED BY 'password';
```

### Pyperclip
[Pyperclip](https://pypi.org/project/pyperclip/) is a python module used to copy data to the clipboard. If you get a "not implemented error", follow this simple fix: https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error

## Windows
### Install Python Requirements
```pip install -r requirements.txt```

### MariaDB
#### Install
Follow [these instructions](https://www.mariadbtutorial.com/getting-started/install-mariadb/) to install MariaDB on Windows
#### Create user and grant privileges
- Navigate to MariaDB bin directory
```
C:\Program Files\MariaDB\bin
```
- Login as root with the password you chose while installation
```
mysql.exe -u root -p
```
- Create user
```
CREATE USER 'pm'@localhost IDENTIFIED BY 'password';
```
- Grant privileges
```
GRANT ALL PRIVILEGES ON *.* TO 'pm'@localhost IDENTIFIED BY 'password';
```


## Run
### Configure

You need to first configure the password manager by choosing a MASTER PASSWORD. This config step is only required to be executed once.
```
python config.py make
```
The above command will make a new configuration by asking you to choose a MASTER PASSWORD.
This will generate the DEVICE SECRET, create db and required tables.

```
python config.py delete
```
The above command will delete the existing configuration. Doing this will completely delete your device secret and all your entries and you will loose all your passwords. So be aware!

```
python config.py remake
```
The above command will first delete the existing configuration and create a fresh new configuration by asking you to choose a MASTER PASSWORD, generate the DEVICE SECRET, create the db and required tables.
SSS
