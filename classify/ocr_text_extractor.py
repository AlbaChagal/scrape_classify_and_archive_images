# External Imports
import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

class OCRTextExtractor:
    """
    An OCR extractor class to extract text from an image.
    All methods are static/class methods
    """
    def __init__(self, langauge='heb', image_to_string_config='--psm 6'):
        """
        Initialize the OCRTextExtractor class
        :param langauge: The language of the OCR text - default: Hebrew
        :param image_to_string_config: The config mode to use for text extraction -
                                       default: '--psm 6'  (Assuming single uniform block of text)
        """
        self.langauge = langauge
        self.image_to_string_config = image_to_string_config

    @staticmethod
    def preprocess_image(image_path: str) -> Image.Image:
        """
        Preprocess the image before passing it to the OCR extractor
        :param image_path: The path of the image to preprocess
        :return: A PIL Image object after preprocessing
        """
        img: Image.ImageFile = Image.open(image_path)
        gray_img: Image.Image = img.convert('L')
        gray_img_np: np.ndarray = np.array(gray_img)

        # Use Otsu's thresholding to convert to black and white
        binary_img: np.ndarray
        _, binary_img = cv2.threshold(gray_img_np,
                                      thresh=0,
                                      maxval=255,
                                      type=cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Convert back to PIL for consistency
        binary_img_pil: Image.Image = Image.fromarray(binary_img)

        return binary_img_pil

    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from an image
        :param image_path: The path of the image to preprocess
        :return: A string of text extracted from the image
        """
        # Preprocess the image to improve OCR results
        processed_img: Image.Image = self.preprocess_image(image_path)

        # Use pytesseract to do OCR
        text: str = pytesseract.image_to_string(
            processed_img,
            lang=self.langauge,
            config=self.image_to_string_config
        )

        return text

    def save_text_files_in_folder(self, folder_path: str):
        """
        Save text files in folder
        :param folder_path: The path of the folder to save the text files
        :return: None
        """
        # Declare all loop-variable types once in advance (for Cythonization)
        image_path: str
        text: str
        text_file_path: str

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
                image_path = os.path.join(folder_path, filename)

                # Extract the text from the image
                text = self.extract_text_from_image(image_path)

                # Save the extracted text to the file
                text_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.txt")
                with open(text_file_path, "w", encoding="utf-8") as text_file:
                    text_file.write(text)
                print(f"Saved text for {filename} to {text_file_path}")


if __name__ == '__main__':
    folder_path_main = "~/PycharmProjects/scrape_classify_and_archive_images/data/archive_images"
    OCRTextExtractor().save_text_files_in_folder(folder_path_main)
