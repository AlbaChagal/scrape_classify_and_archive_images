# External Imports
import os
import unittest
import tempfile
import numpy as np
from unittest.mock import patch
import cv2

# Internal Imports
from classify.ocr_number_extractor import OCRNumberExtractor


class TestOCRNumberExtractor(unittest.TestCase):

    def create_test_image(self, tmpdir: str, filename: str = "test.jpg") -> str:
        """Creates a simple blue rectangle image for testing."""
        img = np.zeros((100, 200, 3), dtype=np.uint8)
        img[:] = (255, 0, 0)  # Blue in BGR
        path = os.path.join(tmpdir, filename)
        cv2.imwrite(path, img)
        return path

    @patch("classify.ocr_number_extractor.pytesseract.image_to_string")
    def test_extract_number_full_image_success(self, mock_ocr):
        mock_ocr.return_value = "index 123"

        with tempfile.TemporaryDirectory() as tmpdir:
            img_path = self.create_test_image(tmpdir)
            number = OCRNumberExtractor.extract_number_from_image(img_path)
            self.assertEqual(number, "123")

    @patch("classify.ocr_number_extractor.pytesseract.image_to_string")
    def test_extract_number_with_crop_success(self, mock_ocr):
        mock_ocr.return_value = "id: 456"

        with tempfile.TemporaryDirectory() as tmpdir:
            img_path = self.create_test_image(tmpdir)
            crop_rect = [(10, 10, 90, 190)]  # Crop region
            number = OCRNumberExtractor.extract_number_from_image(img_path, crop_rects=crop_rect)
            self.assertEqual(number, "456")

    @patch("classify.ocr_number_extractor.pytesseract.image_to_string")
    def test_no_number_found(self, mock_ocr):
        mock_ocr.return_value = "no digits here"

        with tempfile.TemporaryDirectory() as tmpdir:
            img_path = self.create_test_image(tmpdir)
            result = OCRNumberExtractor.extract_number_from_image(img_path)
            self.assertIsNone(result)

    def test_invalid_file_path(self):
        with self.assertRaises(AssertionError):
            OCRNumberExtractor.extract_number_from_image("nonexistent.jpg")

    def test_invalid_params(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            img_path = self.create_test_image(tmpdir)

            # invalid crop_rects
            with self.assertRaises(AssertionError):
                OCRNumberExtractor.extract_number_from_image(img_path, crop_rects="not_a_list")

            # invalid lower_blue_search_range
            with self.assertRaises(AssertionError):
                OCRNumberExtractor.extract_number_from_image(img_path, lower_blue_search_range="not_a_list")

            # invalid upper_blue_search_range
            with self.assertRaises(AssertionError):
                OCRNumberExtractor.extract_number_from_image(img_path, upper_blue_search_range="not_a_list")


if __name__ == "__main__":
    unittest.main()
