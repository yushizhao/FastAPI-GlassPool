from fastapi import FastAPI

from glasspool_logging import glassflow, glassflow_log

app = FastAPI()

@app.get("/")
async def root():
    glassflow_log.debug("test")
    return {"message": "Hello World"}