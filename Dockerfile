# Use an official Python runtime as a parent image
FROM python:3.7-slim

COPY dummy_credentials/ /usr/src/dummy_credentials/
COPY src/ /usr/src/initialisation-service/

COPY requirements.txt /usr/src/initialisation-service/

# Set the working directory to /usr/src/initialisation-service/
WORKDIR /usr/src/initialisation-service/

# Install any needed packages specified in requirements.txt
RUN pip3 install --upgrade pip 
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
RUN rm requirements.txt

# Run app.py when the container launches
CMD ["python3", "init_service.py"]