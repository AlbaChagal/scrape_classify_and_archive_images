# External Imports
import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
from typing import Tuple, List, Optional

class OCRNumberExtractor(object):
    """
    An OCR extractor class to extract numbers from an image.
    All methods are static/class methods
    """
    def __init__(self):
        pass

    @staticmethod
    def preprocess(img: np.ndarray, contour: Optional[np.ndarray]) -> Image.Image:
        """
        Preprocess an image
        :param img: The image to preprocess
        :param contour: The contour to create a bbox from (Optional)
        :return: Preprocessed image
        """
        img: np.ndarray
        if contour is not None:
            x: int
            y: int
            w: int
            h: int
            x, y, w, h = cv2.boundingRect(contour)
            img = img[y: y + h, x: x + w]

        pil_img = Image.fromarray(img)
        bw_pil_img = pil_img.convert('L')
        return bw_pil_img


    @staticmethod
    def get_contours(
            img: np.ndarray,
            lower_blue_search_range: List[int],
            upper_blue_search_range: List[int]
    ) -> Tuple[np.ndarray, ...]:
        """
        Get contours from an image
        :param img: The image to extract contours from
        :param lower_blue_search_range: The lower boundary of the contour
        :param upper_blue_search_range: The upper boundary of the contour
        :return: Contours
        """

        # Convert the image to HSV (Hue, Saturation, Value) color space
        hsv: np.ndarray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define the range of light blue color in HSV
        lower_blue: np.ndarray = np.array(lower_blue_search_range)
        upper_blue: np.ndarray = np.array(upper_blue_search_range)

        # Threshold the image to extract blue areas
        mask: np.ndarray = cv2.inRange(hsv, lower_blue, upper_blue)

        # Find contours in the mask
        contours: Tuple[np.ndarray, ...]
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    @classmethod
    def extract_number_from_image(
            cls,
            image_path: str,
            crop_rects: Optional[List[Optional[Tuple[int, int, int, int]]]] = None,
            lower_blue_search_range: Optional[List[int]] = None,
            upper_blue_search_range: Optional[List[int]] = None,
    ) -> Optional[str]:

        """
        Extracts the number from an image, if crop rects are passed,
        it will try to extract the number from the crop rects and stop
        once it finds the first number.
        :param image_path: The path to the image
        :param crop_rects: The crop rectangles to search in, the algorithm will return the first number it finds.
                           If None, the entire image will be checked for numbers
        :param lower_blue_search_range: The lower bounds (in HSV) for the shade of blue we expect
                                        the index numbers to appear in
        :param upper_blue_search_range: The upper bounds (in HSV) for the shade of blue we expect
                                        the index numbers to appear in
        :return: A string containing the number from the image
        """

        # Replace Nones with defaults
        if lower_blue_search_range is None:
            lower_blue_search_range: List[int] = [90, 50, 50]
        if upper_blue_search_range is None:
            upper_blue_search_range: List[int] = [130, 255, 255]
        if crop_rects is None:
            crop_rects: Optional[List[Optional[Tuple[int, int, int, int]]]] = [None]

        # Assert all inputs are valid
        assert os.path.isfile(image_path), f"File '{image_path}' does not exist"
        assert type(lower_blue_search_range) is list, "lower_blue_search_range is not a list"
        assert type(upper_blue_search_range) is list, "upper_blue_search_range is not a list"
        assert type(crop_rects) is list, "crop_rects is not a list"
        for i in lower_blue_search_range:
            assert type(i) is int, "lower_blue_search_range is not an int"
        for i in upper_blue_search_range:
            assert type(i) is int, "upper_blue_search_range is not an int"
        for crop_rect in crop_rects:
            if crop_rect is not None:
                assert type(crop_rect) is tuple, "crop_rects is not a tuple"
                for i in crop_rect:
                    assert type(i) is int, "crop_rects is not a int"

        # Declare all loop-variable types once in advance (for Cythonization)
        first_cropped_img: np.ndarray
        contours: Tuple[np.ndarray, ...]
        cropped_img: np.ndarray
        bw_pil_img: Image.Image
        text: str
        number: str

        # Load the image from disk
        img: np.ndarray = cv2.imread(image_path)
        for crop_rect in crop_rects:
            # Crop the image if needed
            first_cropped_img = img[crop_rect[0]: crop_rect[2], crop_rect[1]: crop_rect[3]] \
                if crop_rect is not None else img

            contours = cls.get_contours(img=first_cropped_img,
                                        lower_blue_search_range=lower_blue_search_range,
                                        upper_blue_search_range=upper_blue_search_range)

            # Find the bounding box for the largest contour (which should be the blue rectangle)
            for contour in contours:
                bw_pil_img = cls.preprocess(img=first_cropped_img, contour=contour)

                # Perform OCR on the cropped image
                text = pytesseract.image_to_string(bw_pil_img)
                number = ''.join([c for c in text if c.isdigit()])

                if number:
                    print(f'found a number, with crop rect: {crop_rect}')
                    return number

        print(f'No number found in {image_path}')
        return None
