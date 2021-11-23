import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from abc import ABC, abstractmethod
import click
from plays.utils import Charts


class Extractor(ABC):
    def __init__(self):
        self._init_driver()
        super(Extractor, self).__init__()

    @abstractmethod
    def extract(self):
        raise NotImplementedError()

    def _init_driver(self):
        try:
            options = ChromeOptions()
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options)

        except Exception as e:
            raise Exception(
                f"Webdriver not found. Install either Chrome or Firefox webdriver! - {e}"
            )


class YTChartsExtractor(Extractor):
    """
    Extracts TOP Something charts from youtube
    """

    def __init__(self, chart=Charts["TOPSONGS_GLOBAL"]):
        self.url = None
        self.chart = chart
        self.base_url = "https://charts.youtube.com/charts/"
        super().__init__()

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


class YTRelatedExtractor(Extractor):
    """Extracts the first related video from this video and sets that as new url for the video
    Can recursively call extract
    """

    def __init__(self, url=None):
        self.url = url
        super().__init__()

    def add_url(self, url):
        self.url = url

    def extract(self):
        try:
            click.echo("Extracting Related song...")
            self.driver.get(self.url)
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".yt-simple-endpoint.style-scope.ytd-compact-video-renderer",
                    )
                )
            )
            self.url = element.get_attribute("href")
            return self.url
        except Exception as e:
            click.echo(e)
