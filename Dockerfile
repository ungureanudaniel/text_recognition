# Use the official Python image with OpenCV installed
FROM python:3.12-slim

# Upgrade pip
RUN pip install --upgrade pip

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && rm -rf /var/lib/apt/lists/*

# Set Tesseract path (Linux container)
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
ENV pytesseract.pytesseract.tesseract_cmd=/usr/bin/tesseract

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run the Python script
CMD ["python", "app/main.py"]
