# Copyright 2024 by BAFDIL Mehdi.
# All rights reserved.
# file that should have been included as part of this package.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import random
import requests

class AutoVisitor:
    def __init__(self, country, cities, referrers, user_agents, timezone, proxies=None, use_proxy=False):
        self.con_total = 0
        self.con_success = 0
        self.con_failed = 0
        
        # Store the country data
        self.cities = cities
        self.referrers = referrers
        self.user_agents = user_agents
        self.timezone = timezone
        self.proxies = proxies  # List of proxies
        self.use_proxy = use_proxy  # Option to use proxy
        
        # Set up Chrome options
        self.chrome_options = Options()
        
        # Basic Chrome settings
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Country-specific settings
        self.chrome_options.add_argument(f'--lang={country.lower()}')
        self.chrome_options.add_argument(f'--accept-lang={country.lower()}')
        self.chrome_options.add_argument(f'--timezone="{self.timezone}"')
        
        # Set geolocation preferences
        self.chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_settings.geolocation": 1,
            "profile.content_settings.exceptions.geolocation.*,*.": {
                'setting': 1
            }
        })
        
        # Randomly choose a User-Agent from the provided list
        self.chrome_options.add_argument(f'user-agent={random.choice(self.user_agents)}')
        
        # Initialize the Chrome driver
        self.service = Service('C:/Windows/chromedriver.exe')
        self.driver = None

    def is_proxy_working(self, proxy):
        """Check if the given proxy is working."""
        try:
            response = requests.get('http://httpbin.org/ip', proxies={"http": proxy, "https": proxy}, timeout=5)
            return response.status_code == 200
        except:
            return False

    def init_driver(self):
        """Initialize or refresh the Chrome driver"""
        if self.driver:
            self.driver.quit()
        
        # Select a random proxy from the list if using proxy
        if self.use_proxy and self.proxies:
            selected_proxy = random.choice(self.proxies)
            if self.is_proxy_working(selected_proxy):
                self.chrome_options.add_argument(f'--proxy-server={selected_proxy}')
                print(f"Using proxy: {selected_proxy}")
            else:
                print(f"Proxy {selected_proxy} is not working. Skipping proxy usage.")
        
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)

        # Set random referrer
        self.driver.execute_script(f"Object.defineProperty(document, 'referrer', {{get : function(){{ return '{random.choice(self.referrers)}'}}}})")

    def simulate_human_behavior(self):
        """Simulate human-like browsing behavior"""
        try:
            scroll_points = [random.randint(100, 1000) for _ in range(random.randint(3, 7))]
            for scroll_point in scroll_points:
                self.driver.execute_script(f"window.scrollTo(0, {scroll_point});")
                time.sleep(random.uniform(1.5, 4))  # Simulate reading
            
            time.sleep(random.uniform(20, 45))  # Longer reading time
            
            # Simulate random mouse movements
            for _ in range(random.randint(2, 5)):
                x = random.randint(0, 800)
                y = random.randint(0, 600)
                webdriver.ActionChains(self.driver).move_by_offset(x, y).perform()
                time.sleep(random.uniform(0.8, 2))
                
            # Simulate clicks on random elements
            elements = self.driver.find_elements(By.TAG_NAME, "a")
            if elements:
                random_elements = random.sample(elements, min(3, len(elements)))
                for element in random_elements:
                    try:
                        webdriver.ActionChains(self.driver).move_to_element(element).perform()
                        time.sleep(random.uniform(0.5, 1.5))
                    except:
                        continue

        except Exception as e:
            print(f"Error in human behavior simulation: {str(e)}")

    def connect(self, url):
        """Attempt to connect to the specified URL using Selenium"""
        self.con_total += 1
        try:
            self.init_driver()
            self.driver.get(url)
            time.sleep(random.uniform(3, 7))  # Initial page load wait
            
            # Simulate human behavior
            self.simulate_human_behavior()
            
            self.con_success += 1
            print(f"Connection successful! Total: {self.con_total}, Success: {self.con_success}, Failed: {self.con_failed}")
            
        except Exception as e:
            self.con_failed += 1
            print(f"Connection failed! Total: {self.con_total}, Success: {self.con_success}, Failed: {self.con_failed}. Error: {str(e)}")
        
        finally:
            if self.driver:
                self.driver.quit()

    def summary(self):
        """Print a summary of connection attempts"""
        print(f"\nSummary:")
        print(f"Total connections: {self.con_total}")
        print(f"Successful connections: {self.con_success}")
        print(f"Failed connections: {self.con_failed}")
        if self.con_total > 0:
            print(f"Success rate: {(self.con_success/self.con_total)*100:.2f}%")

    def run(self, url, attempts):
        """Run the connection attempts for a specified URL a number of times"""
        print(f"Starting {attempts} visits to {url}")
        for i in range(attempts):
            print(f"\nAttempt {i+1}/{attempts}")
            self.connect(url)
            time.sleep(random.uniform(30, 60))  # Longer wait between attempts to appear more natural
        self.summary()

if __name__ == "__main__":
    # Configuration for Poland
    country = "pl"  # Country code
    cities = ['Warsaw', 'Krakow', 'Gdansk', 'Wroclaw', 'Poznan', 'Lodz', 'Szczecin']
    referrers = [
        'https://www.wp.pl',
        'https://www.onet.pl',
        'https://www.interia.pl',
        'https://www.gazeta.pl',
        'https://www.o2.pl'
    ]
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15'
    ]
    timezone = "Europe/Warsaw"
    
    # List of Polish proxies (5 proxies)
    proxies = [
        "http://83.1.176.118:80",
        "http://212.127.93.44:8081",
        "http://79.110.201.235:8081",
        "http://79.110.202.131:8081",
        "http://78.133.163.190:4145"
    ]

    # Set whether to use proxy (True/False)
    use_proxy = True  # Change to False to disable proxy usage

    # Create an instance of AutoVisitor
    visitor = AutoVisitor(country, cities, referrers, user_agents, timezone, proxies if use_proxy else None, use_proxy)
    
    # URL to visit
    url_to_visit = "https://www.google.com/"
    number_of_attempts = 10
    
    visitor.run(url_to_visit, number_of_attempts)