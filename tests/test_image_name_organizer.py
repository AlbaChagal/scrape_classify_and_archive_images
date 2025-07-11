# External Imports
import os
import unittest
import tempfile
from unittest.mock import patch

# Internal Imports
from archive.image_name_organizer import ImageNameOrganizer


class TestImageNameOrganizer(unittest.TestCase):

    @patch("classify.ocr_number_extractor.OCRNumberExtractor.extract_number_from_image")
    def test_rename_images_in_folder(self, mock_extract):
        # Simulate OCR results
        mock_extract.side_effect = ["123", None, "456"]

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create fake image files
            filenames = ["a.jpg", "b.png", "c.jpeg"]
            for fname in filenames:
                with open(os.path.join(tmpdir, fname), "w") as f:
                    f.write("fake image data")

            # Run rename logic
            ImageNameOrganizer.rename_images_in_folder(tmpdir)

            # Expected final file paths
            expected_files = ["123.jpg", "456.jpg"]
            actual_files = os.listdir(tmpdir)

            # Check renamed and retained files
            for name in expected_files:
                self.assertIn(name, actual_files)

            # The one with None should not be renamed (should still exist with original name)
            self.assertIn("b.png", actual_files or "b.jpeg" in actual_files)

            # Verify the number of OCR calls
            self.assertEqual(mock_extract.call_count, 3)

    def test_invalid_file_type_skipped(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "document.txt"), "w") as f:
                f.write("not an image")

            # Patch the OCR extractor to make sure it's never called
            with patch("classify.ocr_number_extractor.OCRNumberExtractor.extract_number_from_image") as mock_extract:
                ImageNameOrganizer.rename_images_in_folder(tmpdir)
                mock_extract.assert_not_called()


if __name__ == "__main__":
    unittest.main()
