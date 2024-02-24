from fastapi import FastAPI

# can be uvicorn main:app or any variable name for FastAPI instance
app = FastAPI()

# using decorators to name endpoint and handler
@app.get('/')
async def root():
    return {"message": "FastAPI working"}

@app.get('/message')
async def message():
    return {"message": "Hello World"}

# using only python main command to run the server
# it will be executed only on main file, in any other package the condition is false
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level='info', reload=True)