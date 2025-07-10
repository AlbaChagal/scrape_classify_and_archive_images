# Scrape, Archive & Classify Images

This project automates the following workflow:

1. Extract image URLs from a web page.
2. Download the images.
3. Extract numeric identifiers from the top-left corner of each image using OCR.
4. Rename the images based on the extracted numbers.
5. Generate an Excel sheet containing all renamed images in a structured format.

---

## Purpose

This script was originally created to help my partner with a repetitive task she needed to do at work. She was manually downloading images, extracting numbers from them, renaming the files and creating an annotated spreadsheet. This project fully automates that process, turning a time-consuming task into a one-command solution.

---

## Installation

### Requirements

- **Python** 3.8 or newer
- **Tesseract OCR** installed and available on your system’s PATH

You can install Tesseract here:  
- macOS: `brew install tesseract`  
- Ubuntu: `sudo apt install tesseract-ocr`  
- Windows: [Download Tesseract](https://github.com/tesseract-ocr/tesseract/wiki)

### Python Dependencies

Install dependencies using:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with:
```bash
python main.py
```
This will:

Scrape image URLs from: https://www.ilitazoulay.com/no-thing-dies/#
Download images into: data/archive_images
Rename images based on the numbers found in them
Generate an Excel file at: outputs/image_index_sheet.xlsx

***NOTICE! The OCR extractor is optimized for the URL in the example expecting certain attributes for this specific project, changing this will require some thought!***

## Folder Structure

```
scrape_classify_and_archive_images/
├──archive/
│   ├── cs_writer.py
│   └── image_name_organizer.py
├── classify/
│   ├── ocr_number_extractor.py
│   └── ocr_text_extractor.py
├── data/
│   ├── images_archive/
│   └── urls.py
├── scrape/
│   ├── html_parser.py
│   └── image_downloader.py
├── main.py
├── README.md
└── requirements.txt
```

## Customization

You can change:

The source URL: edit the url value in main.py.
The image download or output directories: update the output_dir and excel_output_path paths in main.py.
The color filtering or crop logic: tweak parameters in ocr_number_extractor.py, especially lower_blue_search_range, upper_blue_search_range, and crop_rects.
The expected language of the ocr text extractor: change ocr text extractor params for text in English or any other language

## License

You are free to use, modify, and share it for personal or educational purposes.
Scraping and using data from websites is according to the websites' Licensing.

## Acknowledgments

Thanks to my partner for inspiring this project with a real-world problem. This script was written to save her time and reduce repetitive manual work.