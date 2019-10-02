# Use an official Python runtime as a parent image
FROM python:3.7-slim

COPY src/ /usr/src/initialisation-service/

COPY requirements.txt /usr/src/initialisation-service/

# Set the working directory to /usr/src/knowledge-base-service/
WORKDIR /usr/src/initialisation-service/

# Install any needed packages specified in requirements.txt
RUN pip3 install --upgrade pip 
RUN rm requirements.txt

# Run app.py when the container launches
CMD ["python3", "init_service.py"]