import os
import unittest
import tempfile
from unittest.mock import patch
from PIL import Image

from classify.ocr_text_extractor import save_text_files_in_folder


class TestOCRPipeline(unittest.TestCase):

    @patch("classify.ocr_text_extractor.pytesseract.image_to_string")
    def test_save_text_files_in_folder(self, mock_ocr):
        mock_ocr.return_value = "שלום עולם"  # Fake Hebrew OCR result

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create dummy image files
            image_filenames = ["image1.jpg", "image2.png", "not_image.txt"]
            for fname in image_filenames:
                if fname.endswith(('.jpg', '.png')):
                    img = Image.new("RGB", (100, 100), color='white')
                    img.save(os.path.join(tmpdir, fname))
                else:
                    with open(os.path.join(tmpdir, fname), 'w') as f:
                        f.write("some text")

            # Call the function
            save_text_files_in_folder(tmpdir)

            # Check that .txt files were created for the images
            for name in ["image1", "image2"]:
                txt_path = os.path.join(tmpdir, f"{name}.txt")
                self.assertTrue(os.path.exists(txt_path))
                with open(txt_path, "r", encoding="utf-8") as f:
                    self.assertEqual(f.read(), "שלום עולם")

            # Ensure OCR was called exactly twice
            self.assertEqual(mock_ocr.call_count, 2)

            # Check that no text file was created for the .txt input
            self.assertFalse(os.path.exists(os.path.join(tmpdir, "not_image.txt.txt")))

            # Clean archive_images from


if __name__ == "__main__":
    unittest.main()
