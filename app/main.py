import cv2
import numpy as np
import os
import csv
import pytesseract

# If Tesseract is installed in a standard location, this line is not needed.
# Otherwise, specify the path explicitly (adjust if necessary):
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


# Function to preprocess the image
def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    # Check if the image was loaded successfully
    if image is None:
        raise FileNotFoundError(f"Image not found or unable to load: {image_path}")
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

# Function to recognize numbers from the preprocessed image
def recognize_numbers(preprocessed_image):
    # Configure tesseract to recognize digits only
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    # Perform OCR on the preprocessed image
    text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
    return text
# Save data to csv
def save_to_csv(data, output_path):
    # Write the recognized data to a CSV file
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Extracted Text'])  # Column header
        for row in data:
            writer.writerow([row])  # Each row of data
# Main function
def main():
    # Prompt the user for the image path
    image_path = input("Enter the path to the image file: ").strip()

    # Ensure the image path is valid
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Invalid path: {image_path}")
    
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    # Recognize numbers
    extracted_text = recognize_numbers(preprocessed_image)

    # Process extracted text into lines (or individual numbers, as needed)
    lines = extracted_text.splitlines()
    
    # Define output CSV path
    output_csv_path = 'extracted_numbers.csv'
    
    # Save to CSV
    save_to_csv(lines, output_csv_path)
    print("Recognized Numbers:", extracted_text)

# Run the main function with the path to your image
if __name__ == "__main__":
    main()