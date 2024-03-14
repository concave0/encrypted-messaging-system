from fastapi import FastAPI, Form
from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from starlette.datastructures import MutableHeaders
from fastapi.security import OAuth2PasswordBearer
from src.accounting.user import UserHanlder, JWTHanlder, remove_whitespaces, remove_quotes 
from starlette.applications import Starlette
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from src.log import log_ip
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import datetime 
import jwt 
import uvicorn
import json


class RequestListofUsers: 
    def __init__(self):
        self.stack_public_keys = {}
        self.stack_users = {}
        self.stack_passwords = {}
        self.stack_is_authoirized = {}
        self.message_queue = {}
        self.headers_for_auth = {}

# Setting up FastAPI 
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#  Creating objects
user_handler = UserHanlder()
jwt_handler = JWTHanlder()
user_list = RequestListofUsers()


""" Website Routes """
@app.get("/sign-up", response_class=HTMLResponse)
@limiter.limit("1/second")
async def login(request: Request):
    log_ip("/login",status.HTTP_200_OK,get_remote_address(request))
    return templates.TemplateResponse(request=request, name="sign-up.html")

""" API's Endpoints """
@app.post("/create-account")
@limiter.limit("1/second")
async def add_user(request: Request, username: str = Form(), password: str = Form()):

    if user_handler.search_for_username("data/nosql/users.json",username) == True: 
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="user already exists")
    
    # Storing private and public key with user in order to decode the JTW since every time the server restarts the key rotate.
    now = datetime.datetime.now() 
    hashed_password = user_handler.hash_single_item(password)
    keys = jwt_handler.generate_key_string()
    private_key = keys[0]
    public_key = keys[1]
    user_to_create = {f"{username}": f"Account created on: {str(now)}"}
    token = jwt_handler.encode_payload_with_str_certs(private_key, public_key, user_to_create)

    with open(f'data/user_certs/private/{username}_private_key.pem', 'wb') as private_key_file:
        private_key_file.write(private_key)
        private_key_file.close()

    with open(f'data/user_certs/public/{username}_public_key.pem', 'wb') as public_key_file:
        public_key_file.write(public_key)
        public_key_file.close()

    user_info  = {}
    user_info["hashed_password"]  = hashed_password
    user_info["token"] = token
    
    storing = {}
    storing[username] = user_info

    with open("data/nosql/users.json",'r+') as file:
        file_data = json.load(file)
        file_data.update(storing)
        file.seek(0)
        new_data = json.dump(file_data, file, indent = 4)

    mailbox = user_handler.create_mailbox("data/indox", username)

    if mailbox == True: 
        pass 
    elif mailbox == False: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="could create mailbox.")

    log_ip("/add_user", status.HTTP_201_CREATED, get_remote_address(request))
    response_success = RedirectResponse(f"http://127.0.0.1:8000/sign-up-success/{username}/success")
    return response_success

@app.post("/sign-up-success/{username}/success")
async def sign_up_success(request: Request, username):
    headers = request.headers
 
    with open("data/nosql/users.json",'r+') as file:
        file_data = json.load(file)
        token = file_data.get(username).get("token")
    file.close()
    return templates.TemplateResponse("sign-up-success.html", {"request": request, "token": token})

@app.get("/fetch-mailbox/{username}")
async def get_mailbox(request: Request, username): 

    headers = request.headers

    for_auth = {
        "User" : headers.get("User"), 
        "Password" : headers.get("Password"),
        "Authorization": headers.get("Token"), 
    }

    auth = authorizing(request, for_auth)

    if auth == False:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Your details did not match")
    
    with open(f"data/indox/{username}.json",'r') as mailbox:
        mailbox_content = json.load(mailbox)
    mailbox.close()

    return mailbox_content 


""" Protected Endpoints # checks with JWT, password, username"""   
# checking for the rest of the Protected Endpoints
def authorizing(request: Request, user_to_auth:dict) -> bool:
    log_ip("/authorizing",status.HTTP_200_OK, get_remote_address(request))

    """
    users_to_auth should be formated like this.
    users_to_auth =  {
        "User" : username, 
        "Password : password, 
        "Authorization" : token, 
    }
    """

    try:
        user = user_to_auth.get("User")
        password = user_to_auth.get("Password")
        token = user_to_auth.get("Authorization")
        finding_user_details = user_handler.get_all_user_info(user)
        user_details = finding_user_details[1]
        
        with open(f"data/user_certs/public/{user}_public_key.pem", "rb") as key: 
            public_key = key.read()
        key.close()

        # Check Password
        checking_password = user_handler.check_password("data/nosql/users.json", user, password)
        if checking_password == True: 
            decoded = dict(jwt.decode(token, public_key, algorithms=["RS256"]))
            return True 
        else: 
            return False 
        
    except Exception as e: 
        print(f"{e} is the error") 

@app.get("/rerouting-message-to-designation")
@limiter.limit("1/second")
async def routing_middleware(request: Request):

    """
    Incoming headers should be: 
    {
    "User": username, 
    "Pasword": password, 
    "Token": token, 
    "TO": designation_user, 
    "FROM": who_it_is_coming_from_username, 
    "MESSAGE": message, 
    }
    """

    headers = request.headers

    password =  headers.get("Password")

    for_auth = {
        "User" : headers.get("User"), 
        "Password" : headers.get("Password"),
        "Authorization": headers.get("Token"), 
    }

    designation_user = headers.get("TO")
    from_user = headers.get("FROM")
    message = headers.get("MESSAGE")
    new_message = {"MESSAGE": message}

    keys = jwt_handler.generate_key_string()
    private_key = keys[0]
    public_key = keys[1]
    
    encapsulate_message = jwt_handler.encode_payload_with_str_certs(private_key, public_key,new_message) 
    routing_message = {
        "TO": designation_user, 
        "FROM": from_user,
        "MESSAGE_ENCAPSULATE": encapsulate_message, 
        "KEY_TO_DECRYPT": public_key,   
    }

    auth = authorizing(request, for_auth)

    if auth == False:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Your details did not match")

    # Key is public key and 
    timestamp = datetime.datetime.now() 
    username = headers.get("User")
    adding_message_to_queue = user_list.message_queue[f"{username}&{timestamp}"] = routing_message
    new_url = f"http://127.0.0.1:8000/messaging-service/indox/{username}/{timestamp}"
    rerouting_message = RedirectResponse(new_url,status_code=307)
    return rerouting_message

@app.get("/messaging-service/indox/{username}/{timestamp}")
@limiter.limit("1/second")
async def mailbox_store(request: Request, username, timestamp):

    # No need for auth already done by routing_middleware
    try: 
        message = user_list.message_queue.get(f"{username}&{timestamp}")
        to_user = message.get("TO")
        from_user = message.get("FROM")
        token_message = message.get("MESSAGE_ENCAPSULATE")
        public_key = message.get("KEY_TO_DECRYPT")
        message = jwt.decode(token_message, public_key, algorithms=["RS256"])

        remove_user_message = user_list.message_queue.pop(f"{username}&{timestamp}")
     
        # Using timestamp as forgien key
        forgien_key_time = datetime.datetime.now() 

        recored_message = {
            "TO": to_user, 
            "FROM": from_user, 
            "MESSAGE":  message
        }
    
        record = {str(forgien_key_time): recored_message}
        mailbox_data = json.load(open(f"data/indox/{to_user}.json"))
        mailbox_data.update(record)
        with open(f"data/indox/{to_user}.json", "w") as mailbox: 
            json.dump(mailbox_data, mailbox, indent=4) 

        return {"add": True}
    
    except Exception as e: 
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Was not able to add to mailbox! {e} was the error")

