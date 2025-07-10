# External Imports
import unittest
from unittest.mock import patch, MagicMock
from scrape.html_parser import HTMLParser


class TestHTMLParser(unittest.TestCase):

    def test_extract_img_urls(self):
        html = """
        <html><body>
        <img src="image1.jpg" />
        <img src="image2.png" />
        <img />
        </body></html>
        """
        expected = ["image1.jpg", "image2.png"]
        result = HTMLParser.extract_img_urls(html)
        self.assertEqual(result, expected)

    @patch("parse_html.requests.get")
    def test_get_html_content_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        url = "http://example.com"
        result = HTMLParser.get_html_content(url)
        self.assertEqual(result, "<html></html>")
        mock_get.assert_called_once_with(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    @patch("parse_html.HTMLParser.get_html_content")
    def test_get_all_image_urls_from_site(self, mock_get_html_content):
        sample_html = """
        <html><body>
        <img src="img1.jpg"/>
        <img src="img2.jpg"/>
        </body></html>
        """
        mock_get_html_content.return_value = sample_html
        url = "http://test.com"
        expected = ["img1.jpg", "img2.jpg"]

        result = HTMLParser.get_all_image_urls_from_site(url)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
