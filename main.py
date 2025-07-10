import os

from archive.image_name_organizer import ImageNameOrganizer
from archive.csv_writer import CSVWriter
from scrape.html_parser import HTMLParser
from scrape.image_downloader import ImageDownloader


def main():
    # Step 1: Extract image URLs from the given webpage
    url = "https://www.ilitazoulay.com/no-thing-dies/#"
    print(f"Extracting image URLs from: {url}")
    image_urls = HTMLParser.get_all_image_urls_from_site(url)
    print(f"Found {len(image_urls)} image URLs.")

    # Step 2: Download the images into a local folder
    output_dir = "data/archive_images"
    print(f"Downloading images to: {output_dir}")
    ImageDownloader().download_image(image_urls, output_dir=output_dir)

    # Step 3: Run OCR to extract numbers and rename the images accordingly
    print("Extracting numbers and renaming images...")
    ImageNameOrganizer.rename_images_in_folder(output_dir)

    # Step 4: Create an Excel sheet containing all the renamed images
    excel_output_path = "outputs/image_index_sheet.xlsx"
    print(f"Generating Excel sheet: {excel_output_path}")
    os.makedirs(os.path.dirname(excel_output_path), exist_ok=True)
    writer = CSVWriter(excel_output_path)
    writer.create_sheet_from_images(output_dir, title="Image Indexes")

    print("Processing complete.")


if __name__ == "__main__":
    main()
