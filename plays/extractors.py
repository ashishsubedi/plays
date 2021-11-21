import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from abc import ABC
import click
from plays.utils import Charts


class Extractor(ABC):
    def extract(self):
        raise NotImplementedError()


class YTChartsExtractor(Extractor):
    def __init__(self, chart=Charts["TOPSONGS_GLOBAL"]):
        self._init_driver()
        self.url = None
        self.chart = chart
        self.base_url = "https://charts.youtube.com/charts/"

    def _init_driver(self):
        try:
            options = ChromeOptions()
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options)

        except Exception as e:
            raise Exception(
                f"Webdriver not found. Install either Chrome or Firefox webdriver! - {e}"
            )

    def extract(self):
        try:
            self.driver.get(f"{self.base_url}{self.chart}")
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='playlist-button']"))
            )
            endpoint = element.get_attribute("endpoint")
            endpoint = json.loads(endpoint)
            print("Endpoint", endpoint)
            self.url = endpoint["urlEndpoint"]["url"]
            return self.url
        except Exception as e:
            click.echo(e)
