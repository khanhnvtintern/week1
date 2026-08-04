from fastapi import FastAPI

app = FastAPI(title="booksAPI")

@app.get("/")
def read_root():
    return {"message": "Hello World"}
