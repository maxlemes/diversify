import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# from selenium.webdriver.edge.service import Service
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from selenium.webdriver.edge.options import Options

# Logging configuration for development
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Scraper:
    def __init__(self, headless=True):
        """Initializes the browser and sets the URL and XPath of the financial statement to be scraped."""

        # self.url = url
        # self.xpath = xpath
        self.headless = headless
        self.driver = self._start_browser()

    def _start_edge(self):
        """Configures and starts the Microsoft Edge browser."""
        options = Options()
        if self.headless:
            options.add_argument(
                "--headless"
            )  # Run without a graphical interface if True

        service = Service(
            EdgeChromiumDriverManager().install()
        )  # Use EdgeDriverManager to manage EdgeDriver
        driver = webdriver.Edge(service=service, options=options)
        return driver

    def _start_browser(self):
        profile_path = "/home/max/.mozilla/firefox/diwmikes.selenium"

        """Configures and starts the Firefox browser."""
        options = Options()

        # Load your custom Firefox profile
        # options.set_preference("profile", profile_path)
        options.add_argument("-profile")
        options.add_argument(profile_path)

        if self.headless:
            options.add_argument(
                "--headless"
            )  # Run without a graphical interface if True

        service = Service(
            GeckoDriverManager().install()
        )  # Use WebDriverManager to manage GeckoDriver
        driver = webdriver.Firefox(service=service, options=options)

        return driver

    def access_site(self, url):
        self.url = url
        """Accesses the specified URL and waits for the page to load."""
        self.driver.get(self.url)
        time.sleep(5)  # Waits 5 seconds for the site to load completely

    def collect_table_div(self, xpath):
        self.xpath = xpath
        """Collects a table where rows are of type /div."""
        try:
            # Access the site
            # self.access_site()

            # Locate the table
            table = self.driver.find_element(By.XPATH, self.xpath)

            # Locate the table rows
            rows = table.find_elements(By.XPATH, "./div")

            # Extract the table rows
            data_list = [
                [cell.text for cell in row.find_elements(By.XPATH, "./div")]
                for row in rows
            ]

            return data_list

        except Exception as e:
            # (TimeoutException, NoSuchElementException):
            logging.error(f"Error collecting table. {e}")
            print(f"Error collecting table. {e}")
            return None

    def collect_table__tr(self):
        """Collects a table within a /table element."""
        try:
            # Access the site
            self.access_site()

            # Locate the table
            table = self.driver.find_element(By.XPATH, self.xpath)

            data_list = []

            # Extract headers
            header = [th.text for th in table.find_elements(By.XPATH, ".//thead/tr/th")]
            data_list.append(header)

            # Locate table rows
            for tr in table.find_elements(By.XPATH, ".//tbody/tr"):
                row = [td.text for td in tr.find_elements(By.XPATH, ".//td")]
                data_list.append(row)

            return data_list

        except (TimeoutException, NoSuchElementException):
            print("Error collecting table.")
            return None

    def collect_element(self):
        """Collects a financial statement (Income Statement, Balance Sheet, Cash Flow) from the TradingView website."""
        try:
            # Access the site
            self.access_site()

            # Locate and extract the element
            element = self.driver.find_element(By.XPATH, self.xpath).text

            return element

        except (TimeoutException, NoSuchElementException):
            print("Error collecting element.")
            return None

    def close_browser(self):
        """Closes the browser."""
        self.driver.quit()
