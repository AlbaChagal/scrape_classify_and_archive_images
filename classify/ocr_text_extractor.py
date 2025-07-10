import pytesseract
from PIL import Image, ImageOps
import cv2
import numpy as np
import os


def preprocess_image(image_path):
    # Open the image using PIL
    img = Image.open(image_path)

    # Convert image to grayscale (this is a common first step for OCR)
    gray_img = img.convert('L')

    # Apply a threshold to binarize the image (helps to separate text from background)
    # Convert the image to a NumPy array
    open_cv_image = np.array(gray_img)

    # Use Otsu's thresholding to convert to black and white
    _, binary_img = cv2.threshold(open_cv_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert back to PIL for consistency
    binary_img_pil = Image.fromarray(binary_img)

    return binary_img_pil


def extract_text_from_image(image_path):
    # Preprocess the image to improve OCR results
    processed_img = preprocess_image(image_path)

    # Use pytesseract to do OCR (only in Hebrew)
    text = pytesseract.image_to_string(processed_img, lang='heb',
                                       config='--psm 6')  # Use page segmentation mode 6 (Assume single uniform block of text)

    return text


def save_text_files_in_folder(folder_path):
    # Iterate over all images in the folder
    for filename in os.listdir(folder_path):
        # Only process image files (with jpg, jpeg, png, etc.)
        if filename.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
            # Get the full path to the image
            image_path = os.path.join(folder_path, filename)

            # Extract the text from the bottom half of the image
            text = extract_text_from_image(image_path)

            # Define the output text file path (same name as the image, but with .txt extension)
            text_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.txt")

            # Save the extracted text to the file
            with open(text_file_path, "w", encoding="utf-8") as text_file:
                text_file.write(text)
            print(f"Saved text for {filename} to {text_file_path}")


if __name__ == '__main__':
    folder_path = "../data/archive_images"  # Replace with the folder path containing your images
    save_text_files_in_folder(folder_path)
