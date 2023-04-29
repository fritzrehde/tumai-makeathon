FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container and install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the source code into the container
COPY . .

# Start the application
CMD ["python", "database.py"]
