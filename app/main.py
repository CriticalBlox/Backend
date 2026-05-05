from fastapi import FastAPI

app = FastAPI(title="My Products API", version="1.0")


@app.get("/")
def read_root():
    return {"Hello": "World"}
