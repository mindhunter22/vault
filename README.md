# 🔐 Projet Vault – Sécurité by Design

## 👤 Auteur
**Akram Kalami**  
[GitHub : https://github.com/akramkalami]

---

## 🎯 Objectifs du projet

- Utiliser **HashiCorp Vault** pour sécuriser les identifiants
- Se connecter à une base **MariaDB**
- Lire dynamiquement les identifiants sans les stocker en dur
- Ajouter une **double authentification (TOTP)**
- Protéger contre les attaques de type **rejeu**
- Ajouter un **captcha** pour sécuriser le formulaire de connexion
- Proposer une stratégie de **détection des comptes inactifs**

---

## ⚙️ Configuration système (testé sous Ubuntu 24.04)

### 🧱 Prérequis à installer

```bash
sudo apt update
sudo apt install mariadb-server
pip install pyotp mysql-connector-python hvac
```

Assurez-vous aussi que **Vault** est lancé à :
```
http://127.0.0.1:8300
```

---

## 🗄️ Configuration MariaDB

```sql
CREATE DATABASE testvault;
USE testvault;

CREATE TABLE livre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255)
);

INSERT INTO livre (titre) VALUES ('1984'), ('Le Petit Prince'), ('Sapiens');
```

Utilisateur :
```sql
CREATE USER 'testvault'@'localhost' IDENTIFIED BY 'azerty';
GRANT ALL PRIVILEGES ON testvault.* TO 'testvault'@'localhost';
```

---

## 🔑 Configuration Vault (en local)

Dans Vault :
```
Path : secret/dbcreds
Clé : username = testvault
Clé : password = azerty
```

Token Vault par défaut :
```
root
```

---

## 🧪 Identifiants de test

- **Nom d'utilisateur DB :** `testvault`
- **Mot de passe DB :** `azerty`
- **Token Vault :** `root`

---

## 🔐 Authentification TOTP

Clé OTP à entrer dans FreeOTP (ou Google Authenticator) :
```
JBSWY3DPEHPK3PXP
```

---

## 🛠️ Étapes réalisées

### 1. Base de données MariaDB
- Port utilisé : `3307`
- Base : `testvault`
- Table : `livre(id, titre)`

### 2. Connexion sécurisée via Vault
- Credentials lus dynamiquement via Vault (aucun stockage en dur)

### 3. Double Authentification (TOTP)
- Implémentée avec `pyotp`
- Clé fixe pour test dans FreeOTP

### 4. Captcha côté serveur
- Captcha Google (non inclus dans la version CLI)

### 5. Détection de comptes obsolètes
```sql
SELECT username FROM users WHERE last_login < NOW() - INTERVAL 6 MONTH;
```

### 6. Protection contre les attaques par rejeu
- Jetons `nonce` à usage unique générés via `uuid`

---

## 🚀 Lancer le projet

```bash
python3 app_vault.py
```

---
