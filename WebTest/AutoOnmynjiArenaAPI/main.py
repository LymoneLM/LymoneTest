from fastapi import FastAPI, Depends

app = FastAPI()
"""
uvicorn main:app --reload
"""
readyList = 0
clientWait = 0


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ready")
async def ready():
    global readyList, clientWait
    if readyList == 0:
        readyList += 1
        return {"id": "server"}
    elif readyList < 3:
        readyList += 1
        clientWait += 1
        return {"id": "client"}


@app.get("/server/wait")
async def server_wait():
    global clientWait
    if clientWait > 0:
        clientWait -= 1
        return {"ans": 1}
    else:
        return {"ans": 0}


