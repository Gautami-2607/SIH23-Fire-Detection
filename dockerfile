# Get the required Image
FROM python:3.11

# install the rwquirements
RUN pip install -r requirements.txt

# Specify Working Directory
WORKDIR /code
# Copy everything in current directory to /code
COPY . /code

# The last line is always a CMD in docker
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]