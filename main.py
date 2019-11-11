import uvicorn
from fastapi import FastAPI

from glasspool_logging import glassflow, glassflow_log

app = FastAPI()

@app.get("/")
async def root():
    glassflow_log.debug("test")
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)