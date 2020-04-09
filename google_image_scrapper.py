import os
import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

executable_path = 'D://GDrive//selenium_driver//geckodriver.exe'
buffer_size = 1024


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images_from_link(url):
    """
    Function to find image links in a given website
    :param url: the URL of the desired website
    :return: a list of image links (URLs)
    """

    try:
        soup = bs(requests.get(url).content, "html.parser")
    except:
        return []

    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        alt = img.attrs.get("alt")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)

        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass

            # finally, if the url is valid
            if is_valid(img_url):
                urls.append(img_url)
    return urls


def download_image_from_url(url, pathname):
    """
    Download an image online from a URL and save it locally
    :param url: the image URL
    :param pathname: where to save the image
    :return: non
    """

    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    try:
        response = requests.get(url, stream=True)
    except:
        return 0
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    if file_size < 30 * 1024:
        return 0

    try:
        img_name = url.split("/")[-1]
        img_name = img_name[:150]
        img_name = re.sub(r'[\\:/*"<>]', '_', img_name)

        # get the file name
        filename = os.path.join(pathname, img_name)

        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        progress = tqdm(response.iter_content(buffer_size), f"Downloading {filename}", total=file_size, unit="B",
                        unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            for data in progress:
                # write data read to the file
                f.write(data)
                # update the progress bar manually
                progress.update(len(data))
    except:
        return 0


def download_images_from_website(url, path):
    """
    Download all the images from a given URL
    :param url: the website URL
    :param path: where to save these images
    :return: none
    """
    imgs = get_all_images_from_link(url)
    imgs = list(set(imgs))
    for img in imgs:
        # for each image, download it
        if img.split('.')[-1] in ['jpg', 'png', 'jpeg', 'jfif']:
            download_image_from_url(img, path)


def search_google_images(url, query):
    """
    Search a query keywork in Google images
    :param url: the URL of google images
    :param query: the keyword to search for
    :return: the HTML code of the Google Image result page
    """

    browser = webdriver.Firefox(executable_path=executable_path)
    browser.set_window_size(1024, 768)
    browser.minimize_window()
    print("\n===============================================\n")
    print("[%] Successfully launched ChromeDriver")

    # Open the link
    browser.get(url)
    time.sleep(1)
    print("[%] Successfully opened link.")

    element = browser.find_element_by_tag_name("body")

    print("[%] Scrolling down.")
    # Scroll down
    for i in range(30):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)  # bot id protection

    try:
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)  # bot id protection
    except Exception:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)  # bot id protection

    print("[%] Reached end of Page.")

    time.sleep(1)
    # Get page source and close the browser
    source = browser.page_source
    with open("{}/dataset/soups/{}.html".format(os.getcwd(), query), 'w', encoding='utf-8',
              errors='replace') as f:
        f.write(source)
    browser.close()
    print("[%] Closed ChromeDriver.")

    return source


if __name__ == "__main__":

    # List of queries to search in Google images
    queries = ['cats', 'dogs']
    google_url_base = "https://www.google.com/search?q={}&source=lnms&tbm=isch"

    cwd = os.getcwd()
    if not os.path.isdir("{}/dataset/".format(cwd)):
        os.makedirs("{}/dataset/".format(cwd))
    if not os.path.isdir("{}/dataset/soups/".format(cwd)):
        os.makedirs("{}/dataset/soups/".format(cwd))

    for query in queries:
        url = google_url_base.format(query)

        # Return the HTML page of Google Image search of the query
        source_html = search_google_images(url, query.replace(' ', '_'))

        # Parse the HTML using BS4
        soup = bs(source_html, "html.parser")

        # Find all images href
        all_href = soup.find_all('a', href=True)

        # Return the original Web pages of these images
        pages = []
        for a in all_href:
            link = a.attrs.get('href')
            if link.startswith('http'):
                pages.append(link)
        pages = list(set(pages))

        # download the images from their official website
        for p in pages:
            download_images_from_website(p, './dataset/images/{}/'.format(query))
