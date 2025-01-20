# University Rankings Scraper

This project is a web scraper designed to fetch data about universities from the [Top Universities website](https://www.topuniversities.com). It utilizes Selenium and Requests to retrieve data and extract specific details such as institution information, student body details, and faculty data.

## Features

- Scrapes university data from Top Universities.
- Extracts information such as institution details, student demographics, and faculty information.
- Caches HTML content locally to avoid redundant requests.
- Configurable to scrape up to 500 universities.

## Prerequisites

- Python 3.x
- Google Chrome browser

### Python Dependencies

Install the required Python packages using pip:

```bash
git clone https://github.com/sortstring/topuniv.git
cd topuniv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install -e .
topuniversities 500 1 1 1
```

## Usage

### Setup

1. Download and install [ChromeDriver](https://sites.google.com/chromium.org/driver/). Ensure it is accessible at `/usr/local/bin/chromedriver` or update the `Service` path in the script (univer/univer.py).
2. Ensure all required dependencies are installed.

### Running the Script

To execute the scraper, run:


```topuniversities <number_of_universities> <start_page_number> <use_cache> <use_NLP>```

For example, ```topuniversities 10 1 1 1``` will scrape details of 10 universities starting from page 1. Since the third argument is set to 1, the scraper will use cached data and avoid accessing the live website. If this argument is set to 0, the scraper will fetch data directly from the live website.

The fourth argument is optional. If set to 1, the scraper will use a machine learning (ML) model to extract and process unstructured data. Any other value for this argument will be ignored.

---

## License

This project is proprietary to Sort String Solutions LLP. All rights are reserved. Unauthorized use, reproduction, or distribution of this software is prohibited. Please contact Sort String Solutions LLP for any licensing inquiries.

---

Happy scraping!

