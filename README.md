# Coordinate Extraction from Images

Extracts geographic coordinates from images using OCR (Optical Character Recognition) with OpenCV and Tesseract.

## Features

- ✅ Image preprocessing for better OCR accuracy
- ✅ Coordinate pattern recognition using regex
- ✅ CSV output for easy data processing
- 🐋 Docker support for easy deployment

## Prerequisites

- Docker (recommended) or:
- Python 3.9+
- Tesseract OCR (v4.00+)
- OpenCV

## Installation

### Using Docker (recommended)

1. Build the Docker image:
   ```bash
   docker build -t coordinate-extractor .
2. Run the container
    ```bash
    docker run -v $(pwd)/images:/app/images coordinate-extractor python main.py images/your_image.jpg
## Project structure
text_recognition/
│
├── images/ # Folder for input images
│ └── example.jpg # Sample image file
│
├── outputs/ # Generated output files
│ └── coordinates.csv # Output CSV with extracted coordinates
│
├── app/
│ ├── init.py # Python package marker
│ ├── main.py # Main application script
│ ├── image_processor.py # Image processing functions
│ └── coordinate_utils.py # Coordinate extraction utilities
│
├── Dockerfile # Docker configuration
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── .dockerignore # Files to exclude from Docker builds
## Expected output
Raw OCR Output: Sample text with coordinates (12.345, -67.890)
Found Coordinates: [('12.345', '-67.890')]
Saved to coordinates.csv