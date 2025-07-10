import os
import unittest
import tempfile
from unittest.mock import patch, MagicMock

from scrape.image_downloader import ImageDownloader


class TestImageDownloader(unittest.TestCase):

    @patch("scrape.image_downloader.requests.get")
    def test_download_images_success(self, mock_get):
        # Mock response content
        mock_response = MagicMock()
        mock_response.content = b"fake_image_data"
        mock_get.return_value = mock_response

        urls = ["http://example.com/image1.jpg", "http://example.com/image2.jpg"]

        with tempfile.TemporaryDirectory() as tmpdir:
            downloader = ImageDownloader()
            downloader.download_image(urls, output_dir=tmpdir)

            # Check that files were created
            expected_files = [
                os.path.join(tmpdir, "image_001.jpg"),
                os.path.join(tmpdir, "image_002.jpg")
            ]
            for file in expected_files:
                self.assertTrue(os.path.exists(file))
                with open(file, "rb") as f:
                    self.assertEqual(f.read(), b"fake_image_data")

            # Check correct number of downloads
            self.assertEqual(mock_get.call_count, 2)

    @patch("scrape.image_downloader.requests.get")
    def test_download_image_failure(self, mock_get):
        # Simulate request failure
        mock_get.side_effect = Exception("Download failed")

        urls = ["http://example.com/broken.jpg"]

        with tempfile.TemporaryDirectory() as tmpdir:
            downloader = ImageDownloader()
            downloader.download_image(urls, output_dir=tmpdir)

            # File should not exist
            file_path = os.path.join(tmpdir, "image_001.jpg")
            self.assertFalse(os.path.exists(file_path))


if __name__ == "__main__":
    unittest.main()
