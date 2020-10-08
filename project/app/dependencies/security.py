from fastapi import Header, HTTPException
import os
async def verify_token(token : str = Header(None)):
    if token != os.environ['TOKEN']:
        raise HTTPException(status_code=403, detail="Device token invalid")
    return True
