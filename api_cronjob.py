from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app_1 = FastAPI()
JSON_FILE = "edgex_users.json"

class UserRequest(BaseModel):
    username: str

@app_1.post("/get-token")
def get_token(request: UserRequest):
    """Return token for a given username from JSON file."""

    if not os.path.exists(JSON_FILE):
        raise HTTPException(status_code=500, detail="Token store not found.")

    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)

        for entry in data:
            if entry.get("username") == request.username:
                return {"username": request.username, "token": entry.get("token", "")}

        raise HTTPException(status_code=404, detail="User not found.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading token store: {e}")
