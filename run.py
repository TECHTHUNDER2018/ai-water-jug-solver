import uvicorn
import sys
import os

if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__))
    # Dynamically pull Render's assigned port, default to 8000 locally
    port = int(os.environ.get("PORT", 8000))
    # Must bind to 0.0.0.0 for Render to route traffic!
    uvicorn.run("backend.app:app", host="0.0.0.0", port=port, reload=False)
