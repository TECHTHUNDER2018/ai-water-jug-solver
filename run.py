import uvicorn
import sys
import os

if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__))
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)
