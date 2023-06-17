# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory to the container
COPY . .

# Install dotenv package
RUN pip install python-dotenv

# Expose the port on which Django runs
EXPOSE 8000

# Load environment variables from .env file and export them
CMD ["bash", "-c", "source .env && python3 manage.py runserver 0.0.0.0:8000"]
