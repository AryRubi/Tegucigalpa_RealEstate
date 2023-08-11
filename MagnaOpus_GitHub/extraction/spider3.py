import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import datetime


def scrape_page_with_button(url, origin):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # To load more content, this web page make us click a button
        button_css_selector = "#loadMore > a"

        while True:
            try:
                # We click on the button to load everything before scraping
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_css_selector)))
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)

            except KeyboardInterrupt:
                print("Process interrupted by the user.")
                break

            except Exception as e:
                print(f"No more clicks {e}")
                break

        # Scrape the content after loading all data
        all_data = []

        element_number = 1
        while True:
            content_css_selector = f"#searchListing > div:nth-of-type({element_number}) > div"
            elements = driver.find_elements(By.CSS_SELECTOR, content_css_selector)

            if not elements:
                break  # If no elements found with the current selector, exit the loop

            for element in elements:
                element_html = element.get_attribute('outerHTML')
                element_soup = BeautifulSoup(element_html, 'html.parser')

                href_element = element_soup.select_one('div > div:first-of-type > a:nth-of-type(2)')
                if href_element:
                    href_value = href_element.get('href')
                    link = origin + href_value
                else:
                    continue  # Skip to the next iteration if no link is found

                try:
                    response = requests.get(link)
                    response.raise_for_status()
                    soup2 = BeautifulSoup(response.content, 'html.parser')

                    details = soup2.select('#description > div > div:first-of-type > div:nth-of-type(3) > div > div:first-of-type')

                    for detail in details:
                        titulo = detail.select_one('div:nth-of-type(2) > h2').get_text()
                        colonia = detail.select_one('div:nth-of-type(2) > small').get_text()
                        precio = detail.select_one('div:nth-of-type(3) > span').get_text()
                        id = detail.select_one("div:nth-of-type(4) > span:nth-of-type(2)").get_text()
                        specs = detail.select('div:first-of-type > div:nth-of-type(6) > ul > li')
                        detalles = [i.get_text() for i in specs]
                        specs = soup2.select('#additional > ul > li ')
                        especificaciones = [i.get_text() for i in specs]

                        all_data.append((id, titulo, colonia, precio, detalles, especificaciones))
                        print(f'Currently there are {len(all_data)} in "all_data"')

                except requests.RequestException as e:
                    return f"Error: Unable to access the URL. Exception: {e}"
                except Exception as ex:
                    return f"Error: An error occurred. Exception: {ex}"

            element_number += 1

        df = pd.DataFrame(all_data, columns=['ID', 'title', 'location', 'price', 'details', 'specifications'])
        return df

    except Exception as e:
        return f"Error: {e}"
    finally:
        driver.quit()


website_url = "https://www.website.com"
origin = "https://www.website.com"
timestamp = datetime.datetime.now().strftime('%Y-%m-%d')

df = scrape_page_with_button(website_url, origin)
if isinstance(df, pd.DataFrame):
    df.to_csv(f'MagnaOpus_GitHub/transform/housing3/housing3_{timestamp}.csv', index=False)
else:
    print(df)
