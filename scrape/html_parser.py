from typing import Dict, List
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import requests

class HTMLParser(object):
    """
    An HTML parser class to parse HTML pages, for image URL extraction.
    All methods are static/class methods
    """
    def __init__(self, url: str, ):
        pass

    @staticmethod
    def extract_img_urls(html_content: str) -> List[str]:
        # Initialize BeautifulSoup with the provided HTML content
        soup: BeautifulSoup = BeautifulSoup(html_content, 'html.parser')

        # Find all <img> tags in the HTML
        img_tags: ResultSet = soup.find_all('img')

        # Extract the 'src' attribute of each image tag
        img_urls: List[str] = [img['src'] for img in img_tags if img.get('src')]

        return img_urls

    @staticmethod
    def get_html_content(url: str, is_debug: bool = False) -> str:
        # Add headers to avoid being blocked
        headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # Send request
        response: requests.models.Response = requests.get(url, headers=headers)

        # Raise an error if the request failed
        response.raise_for_status()

        # Get HTML as string
        html_content: str = response.text

        if is_debug:
            print('===========================DEBUGGING HTML PREVIEW================================')
            print(html_content[:1000])  # Print first 1000 characters for preview
            print('=================================================================================')
        return html_content

    @classmethod
    def get_all_image_urls_from_site(cls, url: str, is_debug: bool = False) -> List[str]:
        """
        Reads the html file of the given URL and return a list of all image urls in that HTML
        :param url: The URL of the page in the site were we want to get all images from
        :param is_debug: Indicates if the parser should print out debug prints
        :return: A list of all image URLs from the given URL
        """
        html_content: str = cls.get_html_content(url, is_debug=is_debug)
        image_urls: List[str] = cls.extract_img_urls(html_content)
        return image_urls

if __name__ == "__main__":
    url_main = "https://www.ilitazoulay.com/no-thing-dies/#"
    is_debug = False

    image_urls_main = HTMLParser.get_all_image_urls_from_site(url_main, is_debug=is_debug)

    # Print the extracted image URLs
    for image_url in image_urls_main:
        print(f"'{image_url}',")