from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel
import numpy as np


app = FastAPI()

data_storage = {"temperature": 40, "humidity": 50}
class SensorData(BaseModel):
    temperature: float
    humidity: float

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dynamic_file(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/Analysis")
async def Patient_form(request: Request):
    return templates.TemplateResponse("Analysis.html", {"request": request})  

@app.get("/Dashboard")
async def Patient_form(request: Request):
    return templates.TemplateResponse("Dashboard.html", {"request": request})    

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

# @app.post("/process_sensor_values/")
# async def process_sensor_values(
#     request: Request,
#     sensor1: float = Form(...),
#     sensor2: float = Form(...),
#     sensor3: float = Form(...),
# ):
#     # Calculate average value
#     average_value = (sensor1 + sensor2 + sensor3) / 3

#     # Set the threshold
#     threshold = 5.0  # You can adjust this threshold value

#     # Display message based on the average value
#     if average_value > threshold:
#         alert_message = "ALERT: Average value is above the threshold!"
#     else:
#         alert_message = "Everything is good."

#     return templates.TemplateResponse(
#         "result.html",
#         {"request": request, "average_value": average_value, "alert_message": alert_message},
#     )

@app.post("/upload")
async def report_file(request: Request,
                        UTC: float = Form(...),
                        Temperature: float = Form(...),
                        Humidity: float = Form(...),
                        TVOC: float = Form(...),
                        eCO2: float = Form(...),
                        RawH2: float = Form(...),
                        RawEthanol: float = Form(...),
                        Pressure: float = Form(...),
                        PM1: float = Form(...),
                        PM2: float = Form(...),
                        NC0: float = Form(...),
                        NC1: float = Form(...),
                        NC2: float = Form(...),
                        CNT: float = Form(...)
                       ):
    import joblib

    # Load the model
    model = joblib.load("smoke_detect_model.joblib")                   

    user_input_array = np.array([[UTC, Temperature, Humidity, TVOC, eCO2, RawH2, RawEthanol, Pressure, PM1, PM2, NC0, NC1, NC2, CNT]])

    # Make prediction
    prediction = model.predict(user_input_array)[0]

    # Print the prediction
    print(f"The model predicts: {'Smoke Detected' if prediction == 1 else 'No Smoke Detected'}")
    # if prediction == 1:
    #   from twilio.rest import Client

    #   account_sid = 'ACaee2f7670275fb8bcd7c1aa143995fb4'
    #   auth_token = 'b2beeb85065aad18d2e116b2e90e862f'
    #   client = Client(account_sid, auth_token)

    #   message = client.messages.create(
    #     from_='whatsapp:+14155238886',
    #     body='There is going to be a fire accident in the industry near your location.',
    #     to='whatsapp:+918688425204'
    #   )
    #   prediction_message = "Fire Accident Will occur!"

    # else:
    #   from twilio.rest import Client

    #   account_sid = 'ACaee2f7670275fb8bcd7c1aa143995fb4'
    #   auth_token = 'b2beeb85065aad18d2e116b2e90e862f'
    #   client = Client(account_sid, auth_token)

    #   message = client.messages.create(
    #     from_='whatsapp:+14155238886',
    #     body='No smoke detected.',
    #     to='whatsapp:+918688425204'
    #   )
    #   prediction_message = "Everything is good"

    if prediction == 1:
      prediction_message = "Fire Accident Will occur!"
    else:
      prediction_message = "Everything is good"

    # Need to modify -------------->
    return templates.TemplateResponse("Analysis.html", 
        {"request": request, 
        "prediction_message": prediction_message}
        )

# @app.post("/upload_sensor_data")
# async def upload_sensor_data(request: Request):
#     data = await request.json()
#     temperature = data.get("temperature")
#     humidity = data.get("humidity")
#     print(type(temperature), type(humidity))
#     print(f"Received data - Temperature: {temperature}, Humidity: {humidity}")
#     return {"message": f"Data received successfully {temperature}, {humidity}"} 
#     return templates.TemplateResponse("Analysis.html", 
#         {"request": request, 
#         "temperature": str(temperature), "humidity":str(humidity)}
#         ) 
    # print(type(temperature), type(humidity))
    # print(f"Received data - Temperature: {temperature}, Humidity: {humidity}")
    
    # return templates.TemplateResponse("Analysis.html", 
    #     {"request": request, "temperature": temperature, "humidity": humidity}
    # )

@app.post("/update_sensor_data")
async def update_sensor_data(sensor_data: SensorData):
    data_storage["temperature"] = sensor_data.temperature
    data_storage["humidity"] = sensor_data.humidity
    return {"message": "Data updated successfully"}

@app.get("/get_sensor_data")
async def get_sensor_data():
    if data_storage["temperature"] is None or data_storage["humidity"] is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return data_storage    