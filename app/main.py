import cv2
import numpy as np
import os
import csv
import re
import pytesseract

# If Tesseract is installed in a standard location, this line is not needed.
# Otherwise, specify the path explicitly (adjust if necessary):
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.,-()'

def extract_coordinates(image_path):
    """Extract coordinates from the image using OCR."""
    pattern = r'\(([-+]?\d+\.?\d*),\s*([-+]?\d+\.?\d*)\)' # Regex pattern to match coordinates
    return re.findall(pattern, image_path)

def save_to_csv(data, output_path):
    """Save the extracted coordinates to a CSV file."""
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['X', 'Y'])  # Header
        for (x, y) in data:
            writer.writerow([x, y])
# Function to preprocess the image
def preprocess_image(image_path, invert=True):
    # Load the image
    image = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if image is None:
        raise FileNotFoundError(f"Image not found or unable to load: {image_path}")
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reduce noise (optional, adjust kernel size)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Apply thresholding
    thresh = cv2.adaptiveThreshold(
        blurred, 
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY,
        11, 2
        )
    # Invert the image if needed
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return cleaned

# Main function
def main():
    # Check if the script is run directly
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', help='Path to the image file')
    args = parser.parse_args()
    image_path = args.image_path

    # Prompt the user for the image path in a simple way
    # image_path = input("Enter the path to the image file: ").strip()

    # Ensure the image path is valid
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Invalid path: {image_path}")
    
    try:
        # Step 1: Preprocess image
        processed_image = preprocess_image(image_path)
        
        # Step 2: Perform OCR
        extracted_text = pytesseract.image_to_string(processed_image, config=custom_config)
        print("Raw OCR Output:", extracted_text)
        
        # Step 3: Extract coordinates
        coordinates = extract_coordinates(extracted_text)
        print("Found Coordinates:", coordinates)
        
        # Step 4: Save to CSV
        if coordinates:
            save_to_csv(coordinates, 'coordinates.csv')
            print("Saved to coordinates.csv")
        else:
            print("No coordinates found in image")
            
    except Exception as e:
        print(f"Error: {e}") # Print the error message 
    finally:
        cv2.destroyAllWindows() # Cleanup OpenCV windows

# Run the main function with the path to your image
if __name__ == "__main__":
    main()