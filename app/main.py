from fastapi import FastAPI

app = FastAPI()  # This should be the FastAPI instance

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}