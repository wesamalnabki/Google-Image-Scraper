
# Google Image Scraper
Image scraper for Google Image to collect images from their official websites (Python3 and Selenim)

This code is used to scrap images from Google Image. Typical image scrapers query a keyword in Google Image and download the result images. However, this technique returns a small image size without their original names. 

## Scraper Logic
This crawler collects images from their original websites. Basically, it follows the next logic:
1. Query Google Image for a particular query, e.g. "cat"
2. Using Selenium library, it opens a web page and collects and scroll down the Google Image page to obtain as many images as possible
3. Then, the result HTML code of the Google Image is saved locally
4. Using the Beautiful Soup library, the crawler parses the original websites of each image and visits them website individually
5- For each website, the crawler collects all the images and save them locally in a new folder, named as the query.

## Parameters
For this version, I hardcoded the following parameters, but they need to be changed when you use the script:
1. Selenium driver path ( you can download it online, just google it)
2. The query keywords
3. The output folder name

## Requirements
The requirements for this project are:
1. BeautifulSoup
2. Selenium
3. Python3, of course :)
4. tqdm
5. requests

Just download everything with pip, and you are ready to go!
