import bcrypt
import jwt 
import json
import os 
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa 
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel


""" Meant to authorize and authicate incoming traffic being sent to apis """
class JWTHanlder: 
 
    def encode_payload_with_str_certs(self,private_cert, public_cert, payload:dict): 
        private_key = private_cert
        public_key = public_cert
        encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256")
        return encoded_jwt
    
    def generate_key_string(self):
        # Generate private key
        private_key = rsa.generate_private_key(  
            public_exponent=65537,  
            key_size=4096,  
            backend=default_backend()  
        )  
        pem_private_key  = private_key.private_bytes(  
            encoding=serialization.Encoding.PEM,  
            format=serialization.PrivateFormat.PKCS8,  
            encryption_algorithm=serialization.NoEncryption()  
        ) 

        # generate public key  
        public_key = private_key.public_key()  
        pem_public_key = public_key.public_bytes(  
            encoding=serialization.Encoding.PEM,  
            format=serialization.PublicFormat.SubjectPublicKeyInfo  
        )  
        return pem_private_key, pem_public_key
        

class UserHanlder: 
    def hash_user_info(self,username:str, email:str, password: str) -> set:
        user_info = set()
        user_info.add(self.hash_single_item(email))
        user_info.add(self.hash_single_item(password))
        return user_info 

    def hash_single_item(self,item:str): 
         # Encode the password into a readable utf-8 byte code
        password_bytes = item.encode('utf-8')
        # Generate a salt
        salt = bcrypt.gensalt()
        # Hash the encoded password
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode('utf-8')  # Convert bytes to string

    def search_for_username(self,path_to_json:str,username_to_check:str) -> bool: 

        with open("data/nosql/users.json","r") as info: 
            data = json.load(info)
    
        for username, password in data.items(): 
            if username_to_check == username: 
                return True  
        info.close()
        return False 
    
    def search_for_password(self,path_to_json:str,password_to_check:str): 
        with open(path_to_json,"r") as info: 
            information = info.read()
        info.close()
        data = dict(eval(information))
        for username, nested_details in data.items(): 
            for key, password in nested_details.items(): 
                if key == "hashed_password": 
                    if bcrypt.checkpw(password_to_check.encode('utf-8'), password.encode('utf-8')): 
                            return True   
        return False 
    
    def check_password(self,path_to_json:str,username:str, password_to_check:str): 
        password_to_check_copy  = password_to_check
        with open(path_to_json,"r") as info: 
            data = json.load(info)
        info.close()
 
        password = data.get(username).get("hashed_password").encode('utf-8')
        if bcrypt.checkpw(password_to_check.encode('utf-8'), password): 
            return True 
        else: 
            return False 

    def get_all_user_info(self, username_to_check:str): 
        with open("data/nosql/users.json","r") as info: 
            data = json.load(info)
    
        for username, nested_details in data.items(): 
            if username_to_check == username: 
                return username, nested_details 
        info.close()
        return False 

    def search_for_email(self,path_to_json:str, email_to_check:str): 
        with open(path_to_json,"r") as info: 
            information = info.read()
        info.close()
        data = dict(eval(information))
        for username, password in data.items(): 
            if email_to_check == username: 
                        return True   
        return False 

    def create_mailbox(self,path_to_json:str,username:str): 
        filler_json = {
                "test": "test"
            }
        try: 
            if os.path.isfile(f"{path_to_json}/{username}.json"):
                return True 
            else: 
                with open(f"{path_to_json}/{username}.json", "x+") as new_mail_box:
                    new_mail_box.close()

                with open(f"{path_to_json}/{username}.json", "w") as mailbox: 
                    json.dump(filler_json, mailbox, indent=4) 
                mailbox.close()
                
                return True 
        except:
            return False 
     
    
def remove_whitespaces(input_string:str):
    return input_string.replace(" ", "").replace("\t", "").replace("\n", "").replace('"','')

def remove_quotes(input_string:str): 
    return input_string.replace('"','')



