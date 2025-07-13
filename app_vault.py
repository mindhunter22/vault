import pyotp
import uuid
import hvac
import mysql.connector

# Génération d’un nonce (protection anti-rejeu)
used_nonces = set()
def generate_nonce():
    nonce = str(uuid.uuid4())
    used_nonces.add(nonce)
    return nonce

def validate_nonce(nonce):
    if nonce in used_nonces:
        used_nonces.remove(nonce)
        return True
    return False

# TOTP fixe pour test (à enregistrer dans FreeOTP)
totp = pyotp.TOTP("JBSWY3DPEHPK3PXP")
code = input("Entrez le code TOTP (FreeOTP) : ")
if not totp.verify(code):
    print("Code TOTP invalide.")
    exit()

# Génération et validation du nonce
nonce = generate_nonce()
if not validate_nonce(nonce):
    print("Requête rejetée (nonce invalide).")
    exit()

# Connexion à Vault
client = hvac.Client(url='http://127.0.0.1:8300', token='root')
secrets = client.secrets.kv.read_secret_version(path='secret/dbcreds')
username = secrets['data']['data']['username']
password = secrets['data']['data']['password']

# Connexion à MariaDB
conn = mysql.connector.connect(
    host='localhost',
    port=3307,
    user=username,
    password=password,
    database='testvault'
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM livre")
for (id, titre) in cursor.fetchall():
    print(f"{id}: {titre}")

cursor.close()
conn.close()