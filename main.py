from fastapi import FastAPI, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dynamic_file(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Do something with the uploaded file
    contents = await file.read()
    
    # You can now process the contents of the CSV file, for example, parse it using a CSV library
    # For demonstration purposes, let's print the first 100 characters of the contents
    print(contents[:100])

    # You can return a response or perform further processing here
    return {"filename": file.filename}