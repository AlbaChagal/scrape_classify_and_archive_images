# External Imports
import os
import requests
from typing import List

# Internal Imports
from data.urls import img_urls as urls


class ImageDownloader:
    """
    A Class for downloading images from URLs
    """
    def __init__(self):
        pass

    @staticmethod
    def download_image(img_urls: List[str], output_dir: str) -> None:
        """
        Downloads all images from all given URLs
        :param img_urls: The URLs to download the images from
        :param output_dir: The path to the desired output directory for saving the images
        :return: None
        """
        os.makedirs(output_dir, exist_ok=True)

        # Declare all loop-variable types once in advance (for Cythonization)
        img_data: bytes
        filename: str

        for idx, url in enumerate(img_urls):
            try:
                # Get image from url
                img_data = requests.get(url).content
                # The filename for the image
                filename = os.path.join(output_dir, f"image_{idx+1:03d}.jpg")
                # Save the image to disk
                with open(filename, "wb") as f:
                    f.write(img_data)
                print(f"✓ Downloaded image_{idx+1:03d}.jpg")
            except Exception as e:
                print(f"Failed to download {url}: {e}")


if __name__ == "__main__":

    output_dir_main = "~/PycharmProjects/scrape_classify_and_archive_images/data/archive_images"

    ImageDownloader().download_image(urls, output_dir=output_dir_main)