# Use the official Python image with OpenCV installed
FROM python:3.10-slim

# Upgrade pip
RUN pip install --upgrade pip

RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    lsb-release \
    && add-apt-repository universe \
    && apt-get update && \
    apt-get install -y \
    python3-opencv \
    libopencv-dev \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY /app ./app

# Ensure image file is copied if necessary
COPY pictures/pct-dichiu-t.58-1117.10.jpeg .

# Run the Python script
CMD ["python", "app/main.py"]
