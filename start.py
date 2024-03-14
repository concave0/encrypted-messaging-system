import threading
import uvicorn 
from main import app
from cache_server import flask_app, scheduler

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
def caching_flask_server():
   scheduler.start()
   flask_app.run("0.0.0.0",port=5000)

if __name__=='__main__':
    threading.Thread(target=run_fastapi).start()
    caching_flask_server()
