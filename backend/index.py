import uvicorn
from app import app
from routes.service import *

if __name__ == '__main__':
  uvicorn.run('app:app', port=8000, reload=True)