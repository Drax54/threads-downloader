import requests, bs4
from bs4 import BeautifulSoup
from lxml import etree
from parsel import Selector
from urllib.parse import urljoin
from urllib.parse import urlencode
import json
import re
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template, request, send_file
from selenium import webdriver
import os

# SCRAPEOPS_API_KEY = '4ae9ffca-da04-4da8-a898-c9c40b9fc67f'


# def scrapeops_url(url):
#     payload = {'api_key': SCRAPEOPS_API_KEY, 'url': url, 'country': 'us'}
#     proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
#     return proxy_url

# URL = "https://en.wikipedia.org/wiki/Nike,_Inc."

# HEADERS = ({'User-Agent':
# 			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
# 			(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
# 			'Accept-Language': 'en-US, en;q=0.5'})

# webpage = requests.get(scrapeops_url(URL))
# soup = BeautifulSoup(webpage.content, "html.parser")
# dom = etree.HTML(str(soup))
# print(dom.xpath('//*[@id="firstHeading"]/span')[0].text)


# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)

# driver = webdriver.Chrome(options=chrome_options)
# URL = "https://www.threads.net/t/Cugn8DUNJOQ/"

# driver.get(URL)

# # Wait for the "Allow cookies" button to be clickable
# allow_cookies_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Allow all cookies")]')))

# # Click on the "Allow cookies" button
# allow_cookies_button.click()

# html = driver.page_source
# soup = bs4.BeautifulSoup(html, "html.parser")
# video_data = soup.find_all('video')[0]
# video_src = video_data['src']

# print(video_src)

# response = requests.get(video_src)

# file_name = "downloads.mp4"

# if response.status_code == 200:
#     with open(file_name, 'wb') as file:
#         file.write(response.content)
#     print("Video downloaded successfully.")
# else:
#     print("Failed to download the video.")




app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')

        # Set up Selenium driver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # Wait for the "Allow cookies" button to be clickable
        allow_cookies_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Allow all cookies")]')))

        # Click on the "Allow cookies" button
        allow_cookies_button.click()

        html = driver.page_source
        driver.quit()

        soup = bs4.BeautifulSoup(html, "html.parser")
        video_data = soup.find_all('video')[0]
        video_src = video_data['src']

        # Download the video
        response = requests.get(video_src)

        file_name = "downloads.mp4"

        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print("Video downloaded successfully.")
        else:
            print("Failed to download the video.")

        download_link = request.host_url + 'download'

        return render_template('result.html', download_link=download_link)

    return render_template('index.html')

@app.route('/download')
def download():
    file_path = 'downloads.mp4'
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

