# Get the required Image
FROM python:3.11

# Specify Working Directory
WORKDIR /code

# Copy only the requirements file
COPY requirements.txt .

# install the requirements
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# The last line is always a CMD in docker
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
