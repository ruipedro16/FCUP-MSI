# Python image to use.
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Set the GOOGLE_CLOUD_PROJECT environment variable
ENV GOOGLE_CLOUD_PROJECT=big-data-project1-347618

# Define network ports for the container to listen on at runtime
EXPOSE 8080

# Run main.py when the container launches
ENTRYPOINT ["python", "main.py"]
