from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dynamic_file(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    # Do something with the uploaded file
    contents = await file.read()
    
    # You can now process the contents of the CSV file, for example, parse it using a CSV library
    # For demonstration purposes, let's print the first 100 characters of the contents
    print(contents[:100])

    # You can return a response or perform further processing here
    return {"filename": file.filename}

@app.get("/example")
async def example(request: Request):
    return templates.TemplateResponse("example.html", {"request": request}) 

@app.get("/image_example", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("img_example.html", {"request": request})

@app.post("/upload_image/")
async def upload_image(request: Request, image: UploadFile = File(...)):
    # You can save or process the image here
    # For now, just return the filename as a response
    return templates.TemplateResponse("image_result.html", {"request": request, "filename": image.filename})

@app.get("/sensor_form", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("sensor_form.html", {"request": request})

@app.post("/process_sensor_values/")
async def process_sensor_values(
    request: Request,
    sensor1: float = Form(...),
    sensor2: float = Form(...),
    sensor3: float = Form(...),
):
    # Calculate average value
    average_value = (sensor1 + sensor2 + sensor3) / 3

    # Set the threshold
    threshold = 5.0  # You can adjust this threshold value

    # Display message based on the average value
    if average_value > threshold:
        alert_message = "ALERT: Average value is above the threshold!"
    else:
        alert_message = "Everything is good."

    return templates.TemplateResponse(
        "result.html",
        {"request": request, "average_value": average_value, "alert_message": alert_message},
    )