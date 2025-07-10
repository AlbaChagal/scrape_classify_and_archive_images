# External Imports
import os
from typing import List, Optional

# Internal Imports
from classify.ocr_number_extractor import OCRNumberExtractor


class ImageNameOrganizer(object):
    """
    An image organizer class to extract numbers from an image using OCRNumberExtractor
    and change the names of all images in a given folder to the numbers found in them
    """
    def __init__(self):
        pass

    @staticmethod
    def rename_images_in_folder(folder_path: str) -> None:
        """
        Rename all images in a given folder to the numbers found in them
        :param folder_path: The folder path containing the images
        :return: None
        """
        # Declare all loop-variable types once in advance (for Cythonization)
        new_filename: str
        new_file_path: str

        # Get all files in the folder
        numbers_identified: int = 0
        unidentified_images: List[str] = []
        for filename in os.listdir(folder_path):
            file_path: str = os.path.join(folder_path, filename)

            # If it's a file and ends with an image extension
            if os.path.isfile(file_path) and filename.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
                # Extract the number from the image
                new_name: Optional[str] = OCRNumberExtractor.extract_number_from_image(file_path)

                # If a number is found, rename the image
                if new_name:
                    numbers_identified += 1
                    new_filename = f"{new_name}.jpg"  # You can change the extension if needed
                    new_file_path = os.path.join(folder_path, new_filename)
                    os.rename(file_path, new_file_path)
                    print(f"Renamed '{filename}' to '{new_filename}'")
                else:
                    unidentified_images.append(file_path)


        print(f"Number of images identified is {numbers_identified}")
        print(f'Number of unidentified images is {len(unidentified_images)}')
        print(f'Unidentified images are {len(unidentified_images)}')

if __name__ == "__main__":
    # Example usage:
    folder_path = "../data/archive_images"  # Replace with the folder path containing your images
    ImageNameOrganizer.rename_images_in_folder(folder_path)