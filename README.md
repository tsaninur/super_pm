# Super PM - Password Manager

Super PM is a password manager designed to securely store, manage, and protect passwords.

## 📌 Key Features
- 🔑 **add** : Add a new password entry  
- 🔍 **extract** : Retrieve passwords based on filters  
- 🔢 **generate** : Generate a random password  
- 🔎 **check** : Check for password breaches  
- 🚪 **exit** : Exit the program  

## 🚀 Installation and Setup

### 1️⃣ Install Python  
Ensure Python is installed on your system. If not, download and install it from [Python.org](https://www.python.org/downloads/).  

### 2️⃣ Install MariaDB and Create a User
```bash
sudo apt update
sudo apt install mariadb-server -y
```
Access MariaDB and create a user:
```bash
CREATE DATABASE pm;
CREATE USER 'pm'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON pm.* TO 'pm'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3️⃣ Install Python Dependencies
Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows
pip install -r requirements.txt
```

## 🔧 Super PM Configuration

### ➖ Remove Existing Configuration
```bash
python3 config.py delete
```
Confirm with `y` to delete all data.  

### ➕ Create a New Configuration
```bash
python3 config.py make
```
Follow the instructions to set up your **MASTER PASSWORD**.

## ▶️ Running Super PM
```bash
python3 super_pm.py
```
The main interface will appear with the key feature options.

## ❌ Exiting the Program
Use the following command to exit:  
```bash
Super PM > exit
```
💡 Created by **Sani, Zho & Riel**  
