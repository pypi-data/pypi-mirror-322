from multiprocessing import Pool
import logging
import requests
import pickle
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import *
from . import helper

RETRIES = 3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = helper.os.path.abspath(helper.os.path.dirname(__file__))
CACHE_FILE = helper.os.path.join(BASE_DIR, 'cachefiles/cache.pkl')
LAST_UPDATED_FILE = helper.os.path.join(BASE_DIR, 'cachefiles/last_updated.txt')
CHROMEDRIVER = helper.os.path.join(BASE_DIR, '../chromedriver/chromedriver')

# Load cache from disk
if helper.os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'rb') as f:
        cache = pickle.load(f)
else:
    cache = {}

if helper.os.path.exists(LAST_UPDATED_FILE):
    with open(LAST_UPDATED_FILE, 'r') as f:
        last_updated = json.loads(f.read())
else:
    last_updated = {}

chrome_options = Options()
chrome_options.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
service = Service(CHROMEDRIVER)
driver = webdriver.Chrome(service=service, options=chrome_options)


def main():
    if not validate():
        logger.error("Validation failed. Exiting...")
        helper.sys.exit(1)

    home_page, url = get_home_page()
    if not home_page:
        logger.error(f"Failed to retrieve the page. Exiting...")
        del cache[url]
        del last_updated[url]
        save_cache()
        save_last_updated()
        return

    count_of_universities_on_homepage = helper.get_count_of_universities_on_page(home_page)
    count_of_university_elements_in_list = helper.get_universities_count(home_page)

    if count_of_universities_on_homepage != count_of_university_elements_in_list:
        logger.info(f"Count of universities on homepage: {count_of_universities_on_homepage} "
                     f"does not match with the count of universities in the list: {count_of_university_elements_in_list}.")
        logger.info("Retrieving the list of universities from the homepage.")

    # Anchor tags containing the university's url and nested name
    university_list = helper.get_university_list(home_page)
    university_data = []
    c = len(university_list)
    for count, university in enumerate(university_list):
        university_name, university_url = helper.get_university_name_and_url(university)
        if not university_url or not university_name:
            logger.error(f"\nFailed to retrieve the URL or name of the university. Skipping...\n")
            continue

        university_home_page, university_url = get_university_home_page(university_url)
        if not university_home_page:
            logger.error(f"\nFailed to retrieve the page. Skipping...\n")
            continue
        else:
            logger.info(f"\nSuccessfully retrieved the page: {university_url}")
            logger.info(f"{count + 1} of {c} universities processed.\n")

        university_data.append(process_university(university_home_page, university_name, url, university_url))



    with open('usnews.json', 'w') as f:
        json.dump(university_data, f, indent=4)
    save_cache()
    save_last_updated()
    return


def process_university(university_home_page, university_name, url, university_url):
    about_us_paragraph = get_about_us_paragraph(university_home_page)

    institution_data = get_institution_data(university_home_page, university_name, about_us_paragraph)
    student_data = get_student_data(university_home_page, about_us_paragraph)
    admission_data = get_admission_data(university_home_page)
    academics_data = get_available_programs_data(university_home_page)
    rankings_data = get_ranking_data(university_home_page)
    financial_data = get_financial_data(university_home_page)
    after_graduation_data = get_after_graduation_data(university_home_page)
    features_data = get_notable_features(university_home_page, about_us_paragraph)
    meta_data = get_metadata(university_home_page, last_updated.get(university_url, 'N/A'))

    # with Pool() as pool:
    #     tasks = [
    #         pool.apply_async(get_institution_data, (university_home_page, university_name, about_us_paragraph)),
    #         pool.apply_async(get_student_data, (university_home_page, about_us_paragraph)),
    #         pool.apply_async(get_admission_data, (university_home_page,)),
    #         pool.apply_async(get_available_programs_data, (university_home_page,)),
    #         pool.apply_async(get_ranking_data, (university_home_page,)),
    #         pool.apply_async(get_financial_data, (university_home_page,)),
    #         pool.apply_async(get_after_graduation_data, (university_home_page,)),
    #         pool.apply_async(get_notable_features, (university_home_page, about_us_paragraph)),
    #         pool.apply_async(get_metadata, (university_home_page, last_updated.get(university_url, 'N/A'))),
    #     ]

    #     results = [task.get() for task in tasks]

    # institution_data, student_data, admission_data, academics_data, rankings_data, financial_data,  \
    #     after_graduation_data, features_data, meta_data = results

    return {
        "basic_info": institution_data,
        "rankings": rankings_data,
        "admissions": admission_data,
        "costs_and_aid": financial_data,
        "academics": academics_data,
        "student_life": student_data,
        "after_graduation": after_graduation_data,
        "notable_features": features_data,
        "metadata": meta_data,
        "url": university_url
    }

def validate():
    """
    Validate the command line arguments
    """
    if len(helper.sys.argv) not in [2, 3]:
        logger.error("Please provide the two command line arguments. Exiting...")
        return False

    try:
        use_cache = int(helper.sys.argv[1])
    except Exception as e:
        logger.error(f"Please provide a valid number of Cache choice: {e}")
        return False

    return True


def get_home_page(retries=0):
    url = f"https://www.usnews.com/best-colleges/rankings/national-universities"
    home_page = get_html_content(url)
    if not home_page and retries < RETRIES:
        logger.error(f"Failed to retrieve the page: {url}. Retrying...")
        return get_home_page(retries + 1)
    logger.info(f"Successfully retrieved the home page: {url}")
    return home_page, url


def get_university_home_page(university_href, retries=0):
    university_home_page = None
    try:
        url = 'https://www.usnews.com' + university_href
        university_home_page = get_html_content(url, university_home=True)
    except Exception as e:
        if retries < RETRIES:
            logger.error(f"Failed to retrieve the page: {url}. Retrying...")
            return get_university_home_page(university_href, retries + 1)

    if not university_home_page and retries < RETRIES:
        logger.error(f"Failed to retrieve the page: {url}. Retrying...")
        return get_university_home_page(university_href, retries + 1)
    return university_home_page, url

def scroll_to_load_content(driver, scroll_top=0):
    scroll_pause_time = 1
    while True:
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        scroll_increment = int((scroll_height - scroll_top) / 4) or 10
        logger.info("Scrolling to the bottom of the page")

        for i in range(scroll_top, scroll_height, scroll_increment):
            driver.execute_script(f"window.scrollTo({i}, {i + scroll_increment});")
            helper.time.sleep(scroll_pause_time)

        try:
            # anchor tags containing the university's url and nested name
            university_elements = driver.find_elements(By.CSS_SELECTOR, '.Card__StyledAnchor-sc-1ra20i5-10')
        except Exception as e:
            logger.error(f"Failed to retrieve the list of universities: {e}")
        else:
            logger.info(f"Found {len(university_elements)} universities.")

        offsetHeight = driver.execute_script("return document.body.offsetHeight")
        if offsetHeight == scroll_height:
            break
        scroll_top = scroll_height


    try:
        button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pager__ButtonStyled-sc-1i8e93j-1'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", button)  # Scroll the button into view
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'pager__ButtonStyled-sc-1i8e93j-1')))
        button.click()
        helper.time.sleep(1)
    except Exception as e:
        logger.error(f"Failed to click the button: {e}. Stopping the scroll.")
        return driver.page_source
    return scroll_to_load_content(driver, scroll_top=scroll_top)


def get_html_content(url, university_home=False):
    if int(helper.sys.argv[1]) and url in cache:
        logger.info(f"Using cached content for URL: {url}")
        return cache[url]

    last_modified = None

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code != 200:
            logger.error(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None

    last_modified = response.headers.get('Date', None)

    if last_modified and last_updated.get(url) == last_modified:
        logger.info(f"No update found. Using cached content for URL: {url}")
        return cache[url]

    logger.info(f"Fetching live content for URL: {url}")
    if university_home:

        try:
            driver.get(url)
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.pr-snippet-review-count, .ContentSection__Header-sc-699pa9-0'))
            )
            html_content = driver.page_source
        except Exception as e:
            logger.error(f"Failed to retrieve university home page: {url}. Error: {e}")
            return None
    else:
        try:
            driver.get(url)
            html_content = scroll_to_load_content(driver)
        except Exception as e:
            logger.error(f"Failed to retrieve the list of universities: {e}")
            return None

    cache[url] = html_content
    last_updated[url] = last_modified
    return html_content


def save_cache():
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache, f)
    return

def save_last_updated():
    with open(LAST_UPDATED_FILE, 'w') as f:
        f.write(json.dumps(last_updated))
    return


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred {e}. Exiting...")
    finally:
        driver.quit()
        helper.sys.exit(0)



