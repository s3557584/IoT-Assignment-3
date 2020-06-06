from requestsUtil import requestsUtil
import simplejson as json
import re
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import requests

objRec = requestsUtil()
data = objRec.get_users()

def generate_key():
    password = b"password"
    salt = b'Oy\nK5o\x15\xa8ex2U\x94A\xb9\x8c'
    kdf = PBKDF2HMAC(

            algorithm=hashes.SHA256(),

            length=32,

            salt=salt,

            iterations=100000,

            backend=default_backend()

        )

    key = base64.urlsafe_b64encode(kdf.derive(password))

    return key

def encryptPassword(password):
        """
        Task A
        
        Written by: Ching Loo(s3557584)
        
        Function to encrypt password
        
        Parameters:
                password(str): Plaintext password from user input
            
        Returns:
                encrypted(byte): Encrypted password
        """
        f = Fernet(generate_key())
        encrypted = f.encrypt(password.encode('utf-8'))
        return encrypted

def decryptPassword(encrypted_password):
        """
        Task A
        
        Written by: Ching Loo(s3557584)
        
        Function to decrypt encrypted password
        
        Parameters:
                encrypted_password(byte): ciphertext password from database
            
        Returns:
                password(str): plaintext password
        """
        f = Fernet(generate_key())
        toDecrypt = encrypted_password.encode('utf-8')
        decrypted = f.decrypt(toDecrypt)
        password = decrypted.decode('utf-8')
        
        return password

encrypted = ""


updateobj = requestsUtil("10")
updateobj.update_user("CY","Ching","Loo","Testing@123","croppedImage")