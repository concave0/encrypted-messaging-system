import requests as r
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


class UsersToBatchUpdate: 
    def __init__(self) -> None:
        self.users = {}

# Configs and Objects 
batch_update_users = UsersToBatchUpdate()
flask_app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=flask_app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Caches
messages_cache = {} # username, message
user_to_cache = {}

def fetch_mail(token, password, user):
    url_fetch_mail = f"http://127.0.0.1:8000/fetch-mailbox/{user}" 
    headers = {
    "User" : user, 
    "Password": password, 
    "Token": token,
    } 
    response = r.get(url=url_fetch_mail, headers=headers).text
    messages_cache[user] = response
    
def proccess_incoming_requests(): 
    user = batch_update_users.users.get("User")
    password = batch_update_users.users.get("Password")
    token = batch_update_users.users.get("Token")
    user_to_cache[user] = token, password  # key username, tuple(token, password)

def proccess_batch_users(): 
    for user, user_info in user_to_cache.items():
        token = user_info[0]
        password = user_info[1]
        fetch_mail(user=user,token=token, password=password) 

# Scheduler tasks 
scheduler = BackgroundScheduler()
scheduler.add_job(proccess_batch_users, 'interval', seconds = 2)


# Routes
@flask_app.get("/users-to-cache")
@limiter.limit("1/second", override_defaults=False)
def cache_user_setup():
    batch_update_users.users = request.headers
    proccess_incoming_requests()
    return {}

@flask_app.get("/clear-cache")
@limiter.limit("1/second", override_defaults=False)
def clear_cache_route(): 
    user_to_cache.clear()

@flask_app.get("/sync-mail")
@limiter.limit("1/second", override_defaults=False)
def sync_mail():
    return messages_cache

@flask_app.get("/hello_world") 
def hello_world(): 
    return {"hello":"world"}
