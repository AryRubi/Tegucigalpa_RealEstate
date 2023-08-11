import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# To minimize the number of requests, we collect all the URLs first and then make requests in batches.


def get_house_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        try:
            precio = soup.select_one(
                    '#header_ficha > div:nth-of-type(2) > div:first-of-type > div:nth-of-type(2) > div > div:nth-of-type(2) > div > span')
            price = precio.get_text() if precio else "N.A"
        except Exception as e:
            print("An error occurred:", e)
            price = "N.A"

        detalle_cuerpo = soup.select('#ficha_detalle_cuerpo > div')
        details = [div.get_text() for div in detalle_cuerpo]

        lista_informacion_basica = soup.select('#lista_informacion_basica > li')
        basic_information = [element.get_text() for element in lista_informacion_basica]

        return price, details, basic_information

    else:
        print(f"Error: Failed to retrieve data from {url}. Status code: {response.status_code}")
        return "N.A", [], []


origin = "https://www.website.com"
u = "https://www.website.com"
url = origin + u

timestamp = datetime.datetime.now().strftime('%Y-%m-%d')

# This web page is an "Infinite Scroll" type of web page so we need Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# The path for the information part of the web page (CSS)
path = "#propiedades > li "

try:
    driver.get(url)

    # Capturing the entire page source at once and parsing with BeautifulSoup reduces the number of interactions with Selenium.
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, path)))

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, "html.parser")
    html = soup.select(path)
    urls = [origin + line.find('a')['href'] for line in html]

    # Fetch data in batches
    batch_size = 10
    price, details, basic_information = [], [], []
    for i in range(0, len(urls), batch_size):
        batch_urls = urls[i:i + batch_size]
        batch_results = [get_house_data(url) for url in batch_urls]
        price_batch, details_batch, basic_info_batch = zip(*batch_results)
        price.extend(price_batch)
        details.extend(details_batch)
        basic_information.extend(basic_info_batch)
        print(f"Processed {min(i + batch_size, len(urls))} out of {len(urls)}")

    data = {
        "Precio": price,
        "URLs": urls
    }

    max_length_cuerpo = max(len(d) for d in details)
    max_length_basic = max(len(i) for i in basic_information)

    details = [d + [None] * (max_length_cuerpo - len(d)) for d in details]
    basic_information = [i + [None] * (max_length_basic - len(i)) for i in basic_information]

    for i in range(max_length_cuerpo):
        data[f"Detalle{i+1}"] = [d[i] for d in details]

    for i in range(max_length_basic):
        data[f"Info_basica{i+1}"] = [d[i] for d in basic_information]

    # We create a dictionary of lists and then convert it to a DataFrame to optimize the DataFrame creation process.
    df = pd.DataFrame(data)

    df.to_csv(f'MagnaOpus_GitHub/transform/housing1/housing1_{timestamp}.csv', index=False)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
print("FINISHED!!")
