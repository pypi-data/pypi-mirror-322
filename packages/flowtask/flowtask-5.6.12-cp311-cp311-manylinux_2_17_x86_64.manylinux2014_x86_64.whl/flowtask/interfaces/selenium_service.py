from abc import ABC
from typing import Optional
from collections.abc import Callable
import random
import time
# BeautifulSoup:
from bs4 import BeautifulSoup
from lxml import html, etree
# Selenium Support:
from webdriver_manager.chrome import ChromeDriverManager
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from navconfig.logging import logging
from ..conf import (
    ### Oxylabs Proxy Support for Selenium
    OXYLABS_USERNAME,
    OXYLABS_PASSWORD,
    OXYLABS_ENDPOINT
)
from ..exceptions import (
    NotSupported,
    TimeOutError,
    ComponentError
)
from .http import ua, mobile_ua


logging.getLogger(name='selenium.webdriver').setLevel(logging.INFO)
logging.getLogger(name='WDM').setLevel(logging.WARNING)
logging.getLogger(name='hpack').setLevel(logging.WARNING)
logging.getLogger(name='seleniumwire').setLevel(logging.INFO)


mobile_devices = [
    'iPhone X',
    'Google Nexus 7',
    'Pixel 2',
    'Samsung Galaxy Tab',
    'Nexus 5',
]


class SeleniumService(ABC):
    """SeleniumService.

        Interface for making HTTP connections using Selenium.
    """
    chrome_options = [
        "--headless=new",
        "--enable-automation",
        "--lang=en",
        "--disable-extensions",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-features=NetworkService",
        "--disable-dev-shm-usage",
        "--disable-features=VizDisplayCompositor",
        "--disable-features=IsolateOrigins",
        "--ignore-certificate-errors-spki-list",
        "--ignore-ssl-errors"
    ]
    accept: str = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"  # noqa

    def __init__(self, *args, **kwargs):
        self._driver: Callable = None
        self._wait: WebDriverWait = None
        # Accept Cookies is a tuple with button for accepting cookies.
        self.accept_cookies: tuple = kwargs.pop('accept_cookies', None)
        self.as_mobile: bool = kwargs.pop('as_mobile', False)
        # Device type, defaulting to:
        # TODO: create a dictionary matching userAgent and Mobile Device.
        self.mobile_device: str = kwargs.pop(
            'mobile_device',
            random.choice(mobile_devices)
        )
        self.default_tag: str = kwargs.pop('default_tag', 'body')
        self.accept_is_clickable: bool = kwargs.pop('accept_is_clickable', False)
        self.timeout: int = kwargs.pop('timeout', 60)
        self.wait_until: tuple = kwargs.pop('wait_until', None)
        self.inner_tag: tuple = kwargs.pop('inner_tag', None)
        # Selenium Options:
        self._options = Options()
        super().__init__(*args, **kwargs)
        headers = kwargs.get('headers', {})
        self.headers: dict = {
            "Accept": self.accept,
            "TE": "trailers",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(ua),
            **headers
        }
        # Configure Cookies:
        self.cookies: dict = kwargs.get('cookies', {})
        if isinstance(self.cookies, str):
            self.cookies = self.parse_cookies(self.cookies)

    def parse_cookies(self, cookie_pair: str) -> dict:
        """Parse the Cookies."""
        cookies = {}
        cookie_pairs = [c.strip() for c in cookie_pair.strip().split(';') if c.strip()]
        for pair in cookie_pairs:
            if '=' in pair:
                name, value = pair.split('=', 1)
                name = name.strip()
                value = value.strip().strip('"')  # remove quotes if any
                cookies[name] = value
        return cookies

    def check_by_attribute(self, attribute: tuple):
        if not attribute:
            return None
        el = attribute[0]
        value = attribute[1]
        new_attr = None
        if el == 'id':
            new_attr = (By.ID, value)
        elif el in ('class', 'class name'):
            new_attr = (By.CLASS_NAME, value)
        elif el == 'name':
            new_attr = (By.NAME, value)
        elif el == 'xpath':
            new_attr = (By.XPATH, value)
        elif el == 'css':
            new_attr = (By.CSS_SELECTOR, value)
        elif el in ('tag', 'tag name', 'tagname', 'tag_name'):
            new_attr = (By.TAG_NAME, value)
        else:
            raise NotSupported(
                f"Selenium: Attribute {el} is not supported."
            )
        return new_attr

    def driver(self):
        return self._driver

    def close_driver(self):
        if self._driver:
            self._driver.quit()

    async def start(self, **kwargs) -> bool:
        await super(SeleniumService, self).start(**kwargs)
        # Check the Accept Cookies:
        if self.accept_cookies:
            if not isinstance(self.accept_cookies, tuple):
                raise NotSupported(
                    "Accept Cookies must be a Tuple with the Button to Accept Cookies."
                )
            self.accept_cookies = self.check_by_attribute(self.accept_cookies)
        if self.inner_tag:
            self.inner_tag = self.check_by_attribute(self.inner_tag)
        if hasattr(self, 'screenshot'):
            try:
                self.screenshot['portion'] = self.check_by_attribute(
                    self.screenshot['portion']
                )
            except (KeyError, ValueError):
                pass
        return True

    def proxy_selenium(self, user: str, password: str, endpoint: str, only_http: bool = True) -> dict:
        if only_http is True:
            wire_options = {
                "proxy": {
                    "http": f"http://{user}:{password}@{endpoint}",
                    "https": f"http://{user}:{password}@{endpoint}",
                }
            }
        else:
            wire_options = {
                "proxy": {
                    "http": f"http://{user}:{password}@{endpoint}",
                    "https": f"https://{user}:{password}@{endpoint}",
                    # "socks5": f"https://{user}:{password}@{endpoint}",
                }
            }
        print(':: Proxy :', wire_options)
        return wire_options

    async def get_driver(self):
        if self.as_mobile is True:
            # Use Chrome mobile emulation options
            mobile_emulation_options = {
                "deviceName": self.mobile_device,
                "userAgent": random.choice(mobile_ua)
            }
            self._options.add_experimental_option(
                "mobileEmulation",
                mobile_emulation_options
            )
            self._logger.debug(
                f"Running in mobile emulation mode as {self.mobile_device}"
            )
        else:
            # Add UA to Headers:
            _ua = random.choice(ua)
            self._options.add_argument(f"user-agent={_ua}")
        proxies = None
        if self.use_proxy is True:
            if self._free_proxy is False:
                if hasattr(self, 'us_proxy'):
                    endpoint = "us-pr.oxylabs.io:10000"
                else:
                    endpoint = OXYLABS_ENDPOINT
                customer = f"customer-{OXYLABS_USERNAME}-sesstime-1"
                proxies = self.proxy_selenium(
                    customer, OXYLABS_PASSWORD, endpoint
                )
            else:
                proxy = await self.get_proxies()
                self._options.add_argument(f"--proxy-server={proxy}")
        for option in self.chrome_options:
            self._options.add_argument(option)
        self._driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self._options,
            seleniumwire_options=proxies
        )
        self._wait = WebDriverWait(self._driver, self.timeout)
        return self._driver

    def _execute_scroll(self):
        """
        Execute JavaScript to scroll to the bottom of the page.
        """
        # Scroll to the bottom and back to the top
        WebDriverWait(self._driver, 20).until(
            lambda driver: driver.execute_script("return document.body.scrollHeight") > 0
        )
        # self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Give some time for content to load
        self._driver.execute_script("window.scrollTo(0, 0);")

    def save_screenshot(self, filename: str) -> None:
        """Saving and Screenshot of entire Page."""
        original_size = self._driver.get_window_size()
        width = self._driver.execute_script(
            'return document.body.parentNode.scrollWidth'
        ) or 1920
        height = self._driver.execute_script(
            'return document.body.parentNode.scrollHeight'
        ) or 1080
        if not width:
            width = 1920
        if not height:
            height = 1080
        self._driver.set_window_size(width, height)
        self._execute_scroll()

        # Ensure the page is fully loaded after resizing
        self._wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        # Wait for specific elements to load
        if self.wait_until:
            WebDriverWait(self._driver, 20).until(
                EC.presence_of_all_elements_located(
                    self.wait_until
                )
            )
        if 'portion' in self.screenshot:
            element = self._driver.find_element(*self.screenshot['portion'])
            # Check if the element has a size
            size = element.size
            if size['height'] == 0 or size['width'] == 0:
                # Try scrolling or waiting until element is visible
                self.logger.warning(
                    "Element to screenshot has zero dimension, waiting for it to render..."
                )
                WebDriverWait(self._driver, 20).until(
                    lambda driver: element.size['height'] > 0 and element.size['width'] > 0
                )
            element.screenshot(filename)
        else:
            # Take a full-page screenshot
            self._driver.save_screenshot(filename)
        # resize to the Original Size:
        self._driver.set_window_size(
            original_size['width'],
            original_size['height']
        )

    def get_soup(self, content: str, parser: str = 'html.parser'):
        """Get a BeautifulSoup Object."""
        return BeautifulSoup(content, parser)

    def get_etree(self, content: str) -> tuple:
        try:
            x = etree.fromstring(content)
        except etree.XMLSyntaxError:
            x = None
        try:
            h = html.fromstring(content)
        except etree.XMLSyntaxError:
            h = None
        return x, h

    async def get_page(
        self,
        url: str,
        cookies: Optional[dict] = None,
        retries: int = 3,
        backoff_delay: int = 2
    ):
        """get_page with selenium.

        Get one page using Selenium.
        """
        if not self._driver:
            await self.get_driver()
        attempt = 0
        # Debug for using Proxy:
        # self._driver.get('https://api.ipify.org?format=json')
        # page_source = self._driver.page_source
        # print(page_source)
        while attempt < retries:
            try:
                self._driver.get(url)
                if cookies:
                    # Add the cookies
                    for cookie_name, cookie_value in cookies.items():
                        if cookie_value:
                            self._driver.add_cookie({'name': cookie_name, 'value': cookie_value})
                        # Refresh the page to apply the cookies
                        self._driver.refresh()

                # Ensure the page is fully loaded before attempting to click
                self._wait.until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )

                # Wait for specific elements to load (replace with your actual elements)
                if self.wait_until:
                    WebDriverWait(self._driver, 20).until(
                        EC.presence_of_all_elements_located(
                            self.wait_until
                        )
                    )
                else:
                    # Wait for the tag to appear in the page.
                    self._wait.until(
                        EC.presence_of_element_located(
                            (By.TAG_NAME, self.default_tag)
                        )
                    )
                # Accept Cookies if enabled.
                if self.accept_cookies:
                    # Wait for the button to appear and click it.
                    try:
                        # Wait for the "Ok" button to be clickable and then click it
                        if self.accept_is_clickable is True:
                            accept_button = self._wait.until(
                                EC.element_to_be_clickable(self.accept_cookies)
                            )
                            accept_button.click()
                        else:
                            accept_button = self._wait.until(
                                EC.presence_of_element_located(
                                    self.accept_cookies
                                )
                            )
                        self._driver.execute_script("arguments[0].click();", accept_button)
                    except TimeoutException:
                        self._logger.warning(
                            'Accept Cookies Button not found'
                        )
                # Execute an scroll of the page:
                self._execute_scroll()
                return
            except TimeoutException:
                # The page never reached complete.
                print("Page did not reach a complete readyState.")
                print("Current Page Source:")
                print('===========================')
                print(self._driver.page_source)
                print('===========================')
                # Challenge Button:
                # Try to detect the challenge element. For example, if the button has text "Pulsar y mantener pulsado"

                wait = WebDriverWait(self._driver, 20)
                base = wait.until(EC.presence_of_element_located((By.ID, "px-captcha")))
                iframe = base.find_element(By.TAG_NAME, "iframe")
                print('IFRAME > ', iframe)
                self._driver.switch_to.frame(iframe)
                challenge_button = self._driver.find_element(By.XPATH, "//p[contains(text(), 'Pulsar y mantener pulsado')]")
                print('BUTTON HERE > ', challenge_button)

                try:
                    challenge_button = WebDriverWait(self._driver, 5).until(
                        EC.presence_of_element_located(challenge_button)
                    )
                    print('BUTTON HERE > ', challenge_button)
                    # If we found the button, simulate the click and hold action
                    actions = ActionChains(self._driver)
                    # Hold the button for, say, 5 seconds
                    actions.click_and_hold(challenge_button).pause(5).release().perform()
                    self._driver.switch_to.default_content()
                    # Optionally wait again for the page to load after the challenge
                    self._wait.until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )
                    # Execute an scroll of the page:
                    self._execute_scroll()
                    return
                except TimeoutException:
                    # If the challenge button isn't present, continue as normal
                    pass
                attempt += 1
                if attempt < retries:
                    self._logger.warning(
                        f"TimeoutException occurred. Retrying ({attempt}/{retries}) in {backoff_delay}s..."
                    )
                    time.sleep(backoff_delay)
                else:
                    raise TimeOutError(f"Timeout Error on URL {self.url} after {retries} attempts")
            except Exception as exc:
                raise ComponentError(
                    f"Error running Scrapping Tool: {exc}"
                )
